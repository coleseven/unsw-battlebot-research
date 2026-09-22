from __future__ import annotations

import ast
import hashlib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FRAMEWORK = ROOT / "framework"
MAPS = ROOT / "maps"
DATA = ROOT / "data"
RESULTS = ROOT / "results"

# Never part of a bot's identity: build output, caches, our own freeze note.
IGNORED_DIRS = {".unswbc-build", "__pycache__", ".git"}
IGNORED_FILES = {"FROZEN.txt"}
IGNORED_SUFFIXES = {".pyc", ".replay"}


def bot_dirs(root: pathlib.Path = ROOT, include_versions: bool = True) -> list[pathlib.Path]:
    out = [root / "mybot"] if (root / "mybot" / "bot.toml").is_file() else []
    parents = [root / "opponents"] + ([root / "versions"] if include_versions else [])
    for parent in parents:
        if parent.is_dir():
            out += sorted(p for p in parent.iterdir() if (p / "bot.toml").is_file())
    return out


def sync_targets(root: pathlib.Path = ROOT) -> list[pathlib.Path]:
    """Live framework bots: mybot and opponents. Frozen versions/ are never
    touched, or a snapshot would silently change under its own name."""
    return [p for p in bot_dirs(root, include_versions=False) if (p / "brain.py").is_file()]


def bot_files(path: pathlib.Path) -> list[pathlib.Path]:
    """Files that make up a bot, in a stable order."""
    out = []
    for f in sorted(path.rglob("*")):
        rel = f.relative_to(path)
        if not f.is_file() or any(part in IGNORED_DIRS for part in rel.parts[:-1]):
            continue
        if f.name in IGNORED_FILES or f.suffix in IGNORED_SUFFIXES:
            continue
        out.append(f)
    return out


def bot_hash(path: pathlib.Path) -> str:
    """Content hash of a bot directory (names + bytes), 16 hex chars."""
    h = hashlib.sha256()
    for f in bot_files(path):
        h.update(f.relative_to(path).as_posix().encode() + b"\0")
        h.update(f.read_bytes() + b"\0")
    return h.hexdigest()[:16]


JUDGE_PACKAGES = {"numpy"}   # the judge's Python has the stdlib plus these


def imports(path: pathlib.Path) -> set[str]:
    """Top-level module names a .py file imports (absolute imports only)."""
    tree = ast.parse(path.read_bytes(), filename=str(path))
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            out |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            out.add(node.module.split(".")[0])
    return out


def foreign_imports(bot: pathlib.Path) -> set[str]:
    """Modules the bot's top-level .py files import that it does not carry
    and the judge does not provide. On the judge these fail; locally they
    could silently resolve to some other copy and escape the bot's hash."""
    local = {f.stem for f in bot.glob("*.py")} | {d.name for d in bot.iterdir() if d.is_dir()}
    out = set()
    for f in bot.glob("*.py"):
        out |= imports(f)
    return {m for m in out - local
            if m not in sys.stdlib_module_names and m not in JUDGE_PACKAGES}


def file_hash(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def resolve_bot(name: str) -> pathlib.Path:
    """`mybot`, `greedy` (an opponent), `v3` (a frozen version) or a path."""
    for cand in (pathlib.Path(name), ROOT / name, ROOT / "opponents" / name, ROOT / "versions" / name):
        if (cand / "bot.toml").is_file() or (cand / "main.py").is_file():
            return cand.resolve()
    raise SystemExit(f"no bot called {name!r} (looked in ., opponents/, versions/)")


def resolve_maps(spec: str) -> list[pathlib.Path]:
    """Comma-separated map names/paths/globs; 'all' = every .map under maps/."""
    out: list[pathlib.Path] = []
    for part in spec.split(","):
        part = part.strip()
        if part == "all":
            out += sorted(MAPS.rglob("*.map"))
        elif part in ("bundled", "local"):
            out += sorted(MAPS.glob("*.map"))
        elif part == "server":
            out += sorted((MAPS / "server").glob("*.map"))
        elif any(ch in part for ch in "*?["):
            out += sorted(MAPS.rglob(part if part.endswith(".map") else part + ".map"))
        else:
            p = pathlib.Path(part)
            for cand in (p, MAPS / part, MAPS / (part + ".map"), MAPS / "server" / (part + ".map")):
                if cand.is_file():
                    out.append(cand)
                    break
            else:
                raise SystemExit(f"no map called {part!r}")
    # Drop repeats, including server copies that differ from a bundled map
    # only in how border edges are written (they play identically). Bundled
    # copies win, then the order given.
    out = sorted(enumerate(out), key=lambda ip: (ip[1].parent.name == "server", ip[0]))
    seen, uniq = set(), []
    for _, p in out:
        sig = map_signature(p)
        if sig not in seen:
            seen.add(sig)
            uniq.append(p)
    return uniq


def map_signature(path: pathlib.Path) -> str:
    """Hash of what a map means to the engine: size, symmetry, spawn tiles,
    non-open edges with wrapped border edges folded onto their twins, and
    dragons. Ignores the name and formatting."""
    w = h = 0
    tiles, edges, dragons, other = [], set(), [], []
    for line in path.read_text(encoding="utf8").splitlines():
        p = line.split()
        if not p or p[0] in ("MAP_NAME",) or p[0].endswith("_COUNT"):
            continue
        if p[0] == "MAP":
            w, h = int(p[1]), int(p[2])
        elif p[0] == "TILE":
            tiles.append(" ".join(p[1:]))
        elif p[0] == "EDGE" and p[2] != "0":
            row, c = divmod(int(p[1]), w + 1)
            r, vertical = divmod(row, 2)
            edges.add(("v" if vertical else "h", c % w, r % h, p[2], p[3]))
        elif p[0] == "DRAGON":
            dragons.append(" ".join(p[1:]))
        else:
            other.append(" ".join(p))
    text = repr((w, h, sorted(tiles), sorted(edges), dragons, sorted(other)))
    return hashlib.sha256(text.encode()).hexdigest()[:16]
