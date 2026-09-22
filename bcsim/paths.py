from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FRAMEWORK = ROOT / "framework"
MAPS = ROOT / "maps"
DATA = ROOT / "data"
RESULTS = ROOT / "results"


def bot_dirs() -> list[pathlib.Path]:
    out = [ROOT / "mybot"] if (ROOT / "mybot").is_dir() else []
    for parent in (ROOT / "opponents", ROOT / "versions"):
        if parent.is_dir():
            out += sorted(p for p in parent.iterdir() if (p / "bot.toml").is_file())
    return out


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
    seen, uniq = set(), []
    for p in out:
        if p.resolve() not in seen:
            seen.add(p.resolve())
            uniq.append(p)
    return uniq
