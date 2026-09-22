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

import hashlib
import importlib.abc
import importlib.util
import pathlib
import sys
import time
from dataclasses import asdict, dataclass, field

from unswbc.engine import EngineModule

from . import replay as rp
from .paths import bot_files, bot_hash

_ENGINE: EngineModule | None = None


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
        self.finder = _CodeFinder(self.codes)

    def new_brain(self, init_text: str, seed: int):
        saved = {n: sys.modules.pop(n) for n in list(self.codes) if n in sys.modules}
        sys.meta_path.insert(0, self.finder)
        try:
            brain_mod = importlib.import_module("brain")
            bc_mod = sys.modules["bc"]
            return brain_mod.Brain(bc_mod.Init(init_text), seed=seed)
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
        return self.brain.step(block.decode()).encode()

    def stop(self) -> None:
        pass


# -- subprocess bots (anything unswbc run can play) -----------------------------


class ProcessBot:
    kind = "process"

    def __init__(self, path: pathlib.Path, team: str) -> None:
        from unswbc import run as ubc_run
        from unswbc.bot import Pool

        self.hash = bot_hash(path)
        argv, botdir, _ = ubc_run._resolve(str(path))
        self.pool = Pool(argv, cwd=str(botdir), team=team.lower())

    def new_dragon(self, init: bytes, name: str):
        from unswbc.bot import Bot

        return Bot(self.pool, init=init, name=name)

    def close(self) -> None:
        self.pool.close()


def load_bot(path: pathlib.Path, team: str):
    if (path / "brain.py").is_file():
        return InProcessBot(path)
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

    def to_dict(self) -> dict:
        return asdict(self)


def _seed_for(seed: int, team: str, dragon_id: int) -> int:
    h = hashlib.blake2b(f"{seed}:{team}:{dragon_id}".encode(), digest_size=8).digest()
    return int.from_bytes(h, "little")


def play(map_path: pathlib.Path, bot_a: pathlib.Path, bot_b: pathlib.Path,
         seed: int = 0, replay_to: pathlib.Path | None = None,
         debug: int = 0) -> Result:
    """Play bot_a (team A) against bot_b (team B) on map_path.
    `debug` = 0 drops bot logs/indicators/drawings from the replay (faster);
    pass unswbc.engine.DEBUG_ALL to keep them."""
    start = time.perf_counter()
    loaders = {"A": load_bot(bot_a, "A"), "B": load_bot(bot_b, "B")}
    hashes = {t: loaders[t].hash for t in "AB"}
    live: dict[int, object] = {}
    teams: dict[int, str] = {}
    deaths: dict[str, int] = {}

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
        return bot.ask(block)

    def death(dragon_id: int, round_num: int, reason: str) -> None:
        key = f"{teams.get(dragon_id, '?')}:{reason}"
        deaths[key] = deaths.get(key, 0) + 1
        bot = live.pop(dragon_id, None)
        if bot is not None:
            bot.stop()

    eng = engine()
    error = None
    try:
        res = eng.run(map_path.read_bytes(), reply, death, spawn, lambda line: None, debug)
    except Exception as exc:  # engine refused the map, or a bot blew up badly
        res, error = None, f"{type(exc).__name__}: {exc}"
    finally:
        for bot in live.values():
            bot.stop()
        for loader in loaders.values():
            loader.close()

    common = dict(map=map_path.stem, bot_a=bot_a.name, bot_b=bot_b.name, seed=seed,
                  deaths=deaths, hash_a=hashes["A"], hash_b=hashes["B"])
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
        seconds=time.perf_counter() - start,
    )
