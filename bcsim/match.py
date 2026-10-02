"""Play one match with the real engine (the judge's wasm build, from the
unswbc package).

Framework bots (a directory with brain.py) run in-process: every dragon gets
a fresh copy of the bot's modules, so no state leaks between dragons, just
like separate processes on the judge. Any other bot (the helper-based starter,
C/C++) runs the way `unswbc run` runs it: one OS process per dragon. That is
much slower but faithful.

Every Result records a content hash of the code that played each side, and
final lengths come from the engine's own end-of-game standings.
"""

from __future__ import annotations

import ctypes
import hashlib
import importlib.abc
import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from functools import lru_cache

from unswbc.engine import EngineModule

from . import replay as rp
from .paths import ROOT, bot_files, bot_hash, foreign_imports

_ENGINE: EngineModule | None = None


@lru_cache(maxsize=1)
def engine_identity() -> dict:
    import unswbc
    from unswbc.engine import WASM_PATH
    return {"engine_version": unswbc.__version__,
            "engine_sha256": hashlib.sha256(WASM_PATH.read_bytes()).hexdigest()}


def engine() -> EngineModule:
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = EngineModule()
    return _ENGINE


# -- in-process bots ------------------------------------------------------------


class _CodeFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    """Serves a bot directory's modules from cached code objects."""

    def __init__(self, codes: dict[str, tuple]) -> None:
        self.codes = codes

    def find_spec(self, name, path=None, target=None):
        if name in self.codes:
            return importlib.util.spec_from_loader(name, self, origin=self.codes[name][1])
        return None

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        code, origin = self.codes[module.__name__]
        module.__file__ = origin
        exec(code, module.__dict__)


class InProcessBot:
    kind = "inproc"

    def __init__(self, path: pathlib.Path) -> None:
        self.path = path
        self.codes = {}
        # Hash exactly the bytes that get compiled (plus bot.toml etc.), so a
        # result names the code that actually ran, even if files change later.
        h = hashlib.sha256()
        for f in bot_files(path):
            data = f.read_bytes()
            h.update(f.relative_to(path).as_posix().encode() + b"\0")
            h.update(data + b"\0")
            if f.suffix == ".py" and f.parent == path and f.stem != "main":
                self.codes[f.stem] = (compile(data, str(f), "exec"), str(f))
        self.hash = h.hexdigest()[:16]
        if "brain" not in self.codes:
            raise ValueError(f"{path}: no brain.py")
        # Everything a bot runs must be inside its directory (and so inside
        # its hash), exactly as on the judge where only /bot is visible.
        foreign = foreign_imports(path)
        if foreign:
            raise ValueError(f"{path.name} imports {sorted(foreign)}, which it does not carry "
                             f"and the judge does not provide (run python -m bcsim.sync?)")
        self.finder = _CodeFinder(self.codes)

    def new_brain(self, init_text: str, seed: int):
        saved = {n: sys.modules.pop(n) for n in list(self.codes) if n in sys.modules}
        sys.meta_path.insert(0, self.finder)
        try:
            brain_mod = importlib.import_module("brain")
            bc_mod = sys.modules["bc"]
            brain = brain_mod.Brain(bc_mod.Init(init_text), seed=seed)
            if os.environ.get("BCSIM_DETERMINISTIC_V6") == "1" and "core_search" in self.codes:
                from .local_v6_clock import install
                install(brain)
            return brain
        finally:
            sys.meta_path.remove(self.finder)
            for n in self.codes:
                sys.modules.pop(n, None)
            sys.modules.update(saved)

    def close(self) -> None:
        pass


class _InProcDragon:
    def __init__(self, brain) -> None:
        self.brain = brain
        self.error = None

    def ask(self, block: bytes) -> bytes:
        clock = getattr(self.brain, "_bcsim_clock", None)
        if clock is not None:
            clock.start_turn()
        return self.brain.step(block.decode()).encode()

    def stop(self) -> None:
        pass


# -- in-process C++ bots (local simulation only) --------------------------------
#
# For fast local tuning we can run the C++ bot in-process instead of one OS
# process per dragon: a small C ABI (cppbot_inproc/inproc.cpp) is built against
# the bot directory's headers/params into a shared library and driven through
# ctypes. Off by default; opt in with BCSIM_CPP_INPROC=1. What gets uploaded is
# unchanged -- inproc.cpp lives outside every bot directory and the .so is
# cached under .unswbc-build (ignored by bot_files, so the bot's hash is the
# same as the process build's).

INPROC_SRC = ROOT / "cppbot_inproc" / "inproc.cpp"
_CPP_LIBS: dict[str, ctypes.CDLL] = {}


def cpp_inproc_enabled() -> bool:
    return os.environ.get("BCSIM_CPP_INPROC") == "1"


def is_cpp_bot(path: pathlib.Path) -> bool:
    """A folder bot built from our cppbot sources (main.cpp + v6_brain.hpp, no
    Python brain). The in-process wrapper only fits our brain; other C++ bots
    (sparring) keep running as processes."""
    return ((path / "main.cpp").is_file() and (path / "v6_brain.hpp").is_file()
            and not (path / "brain.py").is_file())


def _cpp_compiler() -> list[str]:
    # Use the exact compiler unswbc uses for the native process build, so the
    # in-process library computes identical floating point (a different compiler
    # breaks score ties differently and the game diverges over 500 rounds).
    from unswbc import toolchain
    return toolchain.find_compiler(False)


def build_cpp_lib(path: pathlib.Path) -> pathlib.Path:
    """Build (or reuse) the in-process shared library for a C++ bot directory.

    Cached at <bot>/.unswbc-build/inproc.so; that directory is ignored by
    bot_files, so building leaves the bot's content hash untouched. Rebuilt only
    when the wrapper or a bot source is newer than the cached library.
    """
    build_dir = path / ".unswbc-build"
    build_dir.mkdir(exist_ok=True)
    lib = build_dir / "inproc.so"
    sig_file = build_dir / "inproc.sig"
    sources = [INPROC_SRC, *(f for f in path.iterdir()
                             if f.is_file() and f.suffix in (".cpp", ".hpp"))]
    newest = max(f.stat().st_mtime for f in sources)
    # Match unswbc's native flags (-std=c++20 -O2); -fPIC -shared build a
    # library and do not change the arithmetic. The signature leaves out the
    # (per-process) output path: including it made every worker process see a
    # stale cache and recompile every bot at start-up (28 Sep: 8 parallel GCC
    # -O2 builds per batch on top of the games; GCC segfaulted three times and
    # the PC blue-screened twice).
    base_cmd = [*_cpp_compiler(), "-std=c++20", "-O2", "-fPIC", "-shared",
                "-I", str(path), str(INPROC_SRC)]
    sig = " ".join(base_cmd)

    def fresh():
        return (lib.is_file() and lib.stat().st_mtime >= newest
                and sig_file.is_file() and sig_file.read_text() == sig)

    if fresh():
        return lib
    # One builder per library: others wait for it instead of compiling too.
    lock = build_dir / "inproc.lock"
    deadline = time.monotonic() + 600
    while True:
        try:
            os.close(os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
            break
        except FileExistsError:
            try:
                stale = time.time() - lock.stat().st_mtime > 600
            except FileNotFoundError:
                continue                          # released between our checks
            if stale:
                lock.unlink(missing_ok=True)      # left by a killed builder
                continue
            if time.monotonic() > deadline:
                raise RuntimeError(f"timed out waiting for the in-process build of {path.name}")
            time.sleep(0.5)
            if fresh():
                return lib
    try:
        if fresh():
            return lib
        tmp = lib.with_suffix(f".{os.getpid()}.tmp")
        proc = subprocess.run([*base_cmd, "-o", str(tmp)], capture_output=True, text=True)
        if proc.returncode != 0:
            tmp.unlink(missing_ok=True)
            raise RuntimeError(f"in-process build failed for {path.name}:\n{proc.stderr}")
        os.replace(tmp, lib)  # atomic: nobody sees a half-written .so
        sig_file.write_text(sig)
        return lib
    finally:
        lock.unlink(missing_ok=True)


def _load_cpp_lib(path: pathlib.Path) -> ctypes.CDLL:
    lib_path = build_cpp_lib(path)
    key = str(lib_path)
    lib = _CPP_LIBS.get(key)
    if lib is None:
        if os.name == "nt":
            # Windows does not search PATH for a DLL's own dependencies
            # (libstdc++/libgcc from MinGW); add the compiler's directory,
            # where the native bot.exe finds the same runtime.
            import shutil as _shutil
            compiler = _shutil.which(_cpp_compiler()[0])
            if compiler:
                os.add_dll_directory(os.path.dirname(os.path.abspath(compiler)))
        lib = ctypes.CDLL(str(lib_path.resolve()))
        lib.bc_new.restype = ctypes.c_void_p
        lib.bc_new.argtypes = [ctypes.c_char_p, ctypes.c_uint64]
        lib.bc_step.restype = ctypes.c_char_p
        lib.bc_step.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        lib.bc_free.restype = None
        lib.bc_free.argtypes = [ctypes.c_void_p]
        _CPP_LIBS[key] = lib
    return lib


class _CppDragon:
    """One dragon handle in the shared library; the reply matches main.cpp."""

    def __init__(self, lib: ctypes.CDLL, init: bytes) -> None:
        self.lib = lib
        self.handle = lib.bc_new(init, 0)
        self.error = None
        if not self.handle:
            raise RuntimeError("bc_new returned null")

    def ask(self, block: bytes) -> bytes:
        return self.lib.bc_step(self.handle, block)

    def stop(self) -> None:
        if self.handle:
            self.lib.bc_free(self.handle)
            self.handle = None


class InProcessCppBot:
    """A C++ bot driven in-process (like ProcessBot, without the subprocess)."""

    kind = "cpp_inproc"

    def __init__(self, path: pathlib.Path) -> None:
        self.path = path
        self.hash = bot_hash(path)  # same identity as the process build
        self.lib = _load_cpp_lib(path)

    def new_dragon(self, init: bytes, name: str) -> _CppDragon:
        return _CppDragon(self.lib, init)

    def close(self) -> None:
        pass


# -- subprocess bots (anything unswbc run can play) -----------------------------


class ProcessBot:
    kind = "process"

    def __init__(self, path: pathlib.Path, team: str) -> None:
        from unswbc import run as ubc_run
        from unswbc.bot import Pool

        self.hash = bot_hash(path)
        # Python source snapshots already have a runnable main.py. Resolving a
        # project compiles it into a shared .unswbc-build cache on every match;
        # concurrent workers race while replacing the same .pyc files on
        # Windows. Execute the same source entry point directly instead.
        runnable = (ubc_run._inspect(path) if (path / "main.py").is_file() else None)
        argv, botdir, _ = runnable or ubc_run._resolve(str(path))
        # The toolkit may pick the Microsoft Store alias (...\WindowsApps\python3.exe).
        # Every launch through it goes via the AppX Deployment Service, which kept
        # ~75 GB of commit after a long tuning run (WinError 1455). Use the real
        # interpreter instead; same Python, no AppX activation.
        if argv and "windowsapps" in argv[0].lower():
            argv = [getattr(sys, "_base_executable", sys.executable), *argv[1:]]
        self.pool = Pool(argv, cwd=str(botdir), key=team.lower())

    def new_dragon(self, init: bytes, name: str):
        from unswbc.bot import Bot

        return Bot(self.pool, init=init, name=name)

    def close(self) -> None:
        self.pool.close()


def prebuild(paths) -> None:
    """Build every compiled (C/C++) bot once, before workers start.

    The toolkit caches a build in the bot's .unswbc-build, but parallel workers
    that each find no build yet all link the same bot.exe at once, and Windows
    refuses to replace an executable another worker is running. Python and
    in-process bots need no build.
    """
    from unswbc import run as ubc_run

    inproc = cpp_inproc_enabled()
    for path in dict.fromkeys(pathlib.Path(p) for p in paths):
        if (path / "main.py").is_file() or (path / "brain.py").is_file():
            continue
        if inproc and is_cpp_bot(path):
            build_cpp_lib(path)  # in-process shared library, not the wasm build
        else:
            ubc_run._resolve(str(path))


def load_bot(path: pathlib.Path, team: str):
    # Our lightweight in-process protocol requires both modules. Third-party
    # bots may also name a module brain.py while using their own wire format.
    if (path / "brain.py").is_file() and (path / "bc.py").is_file():
        return InProcessBot(path)
    if cpp_inproc_enabled() and is_cpp_bot(path):
        return InProcessCppBot(path)
    return ProcessBot(path, team)


# -- one match -----------------------------------------------------------------


@dataclass
class Result:
    map: str
    bot_a: str
    bot_b: str
    seed: int
    winner: str | None          # "A", "B" or None (draw, or error: check `error`)
    reason: str                 # elimination | length | error
    rounds: int
    a_dragons: int              # living dragons at the end
    b_dragons: int
    a_length: int               # total length of each team's living dragons
    b_length: int
    a_longest: int = 0          # longest living dragon at the end (engine's standings)
    b_longest: int = 0
    deaths: dict = field(default_factory=dict)   # "A:W" -> count
    seconds: float = 0.0
    error: str | None = None
    hash_a: str = ""            # content hash of the code that played each side
    hash_b: str = ""
    engine_version: str = ""
    engine_sha256: str = ""
    map_sha256: str = ""
    a_queen: int | None = None  # None for an engine without queen scoring
    b_queen: int | None = None
    queen_death_round: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


def _seed_for(seed: int, team: str, dragon_id: int) -> int:
    h = hashlib.blake2b(f"{seed}:{team}:{dragon_id}".encode(), digest_size=8).digest()
    return int.from_bytes(h, "little")


def play(map_path: pathlib.Path, bot_a: pathlib.Path, bot_b: pathlib.Path,
         seed: int = 0, replay_to: pathlib.Path | None = None,
         debug: int = 0, hook=None) -> Result:
    """Play bot_a (team A) against bot_b (team B) on map_path.
    `debug` = 0 drops bot logs/indicators/drawings from the replay (faster);
    pass unswbc.engine.DEBUG_ALL to keep them.
    `hook(dragon_id, team, block, reply) -> reply` (optional) sees every bot
    reply after the bot produced it (its private state already updated) and
    may rewrite it: the counterfactual-move teacher (bcsim.mover_teacher)
    forces one move this way. None leaves play unchanged."""
    start = time.perf_counter()
    loaders = {"A": load_bot(bot_a, "A"), "B": load_bot(bot_b, "B")}
    hashes = {t: loaders[t].hash for t in "AB"}
    live: dict[int, object] = {}
    teams: dict[int, str] = {}
    deaths: dict[str, int] = {}
    queen_deaths: dict[str, int] = {}

    def spawn(dragon_id: int, init: bytes) -> None:
        text = init.decode()
        team = "B" if "\nTEAM B" in "\n" + text else "A"
        teams[dragon_id] = team
        loader = loaders[team]
        if loader.kind == "inproc":
            live[dragon_id] = _InProcDragon(loader.new_brain(text, _seed_for(seed, team, dragon_id)))
        else:
            live[dragon_id] = loader.new_dragon(init, str(dragon_id))

    def reply(dragon_id: int, block: bytes) -> bytes:
        bot = live.get(dragon_id)
        if bot is None:
            return b"ENDTURN\n"
        out = bot.ask(block)
        return out if hook is None else hook(dragon_id, teams.get(dragon_id), block, out)

    def death(dragon_id: int, round_num: int, reason: str) -> None:
        if dragon_id in (0, 1):
            queen_deaths[teams.get(dragon_id, "?")] = round_num
        key = f"{teams.get(dragon_id, '?')}:{reason}"
        deaths[key] = deaths.get(key, 0) + 1
        bot = live.pop(dragon_id, None)
        if bot is not None:
            bot.stop()

    eng = engine()
    error = None
    try:
        # unswbc >= 1.1 seeds the engine (pearl spawns) per match, as the judge
        # does; the same seed replays the same pearls
        res = eng.run(map_path.read_bytes(), reply, death, spawn, lambda line: None, debug,
                      seed % (1 << 64))
    except Exception as exc:  # engine refused the map, or a bot blew up badly
        res, error = None, f"{type(exc).__name__}: {exc}"
    finally:
        for bot in live.values():
            bot.stop()
        for loader in loaders.values():
            loader.close()

    common = dict(map=map_path.stem, bot_a=bot_a.name, bot_b=bot_b.name, seed=seed,
                  deaths=deaths, hash_a=hashes["A"], hash_b=hashes["B"],
                  **engine_identity(), map_sha256=hashlib.sha256(map_path.read_bytes()).hexdigest(),
                  queen_death_round=queen_deaths)
    if res is None:
        return Result(**common, winner=None, reason="error", rounds=0, a_dragons=0,
                      b_dragons=0, a_length=0, b_length=0, error=error,
                      seconds=time.perf_counter() - start)

    # Lengths seen in round blocks predate each dragon's last action (and miss
    # later splits and growth); the engine's final standings are exact.
    blob = eng.replay(bot_a.name, bot_b.name)
    if replay_to is not None:
        replay_to.parent.mkdir(parents=True, exist_ok=True)
        replay_to.write_bytes(blob)
    final = rp.read_result(blob)
    return Result(
        **common,
        winner=res.winner, reason="elimination" if res.end_reason == 0 else "length",
        rounds=res.rounds + 1, a_dragons=res.a_dragons, b_dragons=res.b_dragons,
        a_length=res.a_length, b_length=res.b_length,
        a_longest=(final.get("a") or {}).get("longest", 0),
        b_longest=(final.get("b") or {}).get("longest", 0),
        a_queen=getattr(res, "a_queen", None), b_queen=getattr(res, "b_queen", None),
        seconds=time.perf_counter() - start,
    )
