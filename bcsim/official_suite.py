"""The eleven distinct competition maps; required coverage for bot changes."""

import os
from pathlib import Path

from .paths import ROOT, map_signature


# User-specified full suite. Duplicate server/bundled exports are intentionally
# excluded; these are eleven distinct playable layouts, in the requested order.
SPECS = (
    ("default_small", "maps/default_small.map", 16, 16),
    ("trophy", "maps/trophy.map", 25, 25),
    ("queen_of_spades", "maps/queen_of_spades.map", 25, 35),
    ("default", "maps/default.map", 32, 32),
    ("Devil", "maps/server/Devil.map", 32, 16),
    ("stronghold", "maps/server/stronghold.map", 48, 24),
    ("Trauma", "maps/server/Trauma.map", 48, 24),
    ("schooltime", "maps/schooltime.map", 60, 40),
    ("big_empty", "maps/big_empty.map", 64, 64),
    ("arena", "maps/arena.map", 11, 11),
    ("Colosseum", "maps/Colosseum.map", 16, 16),
)

# Sixteen simultaneous matches exhausted available RAM with process-based
# nicked; eight is the highest previously completed full-suite setting here.
# The bounded runner can still use more on a machine with measured headroom.
DEFAULT_WORKERS = min(8, os.cpu_count() or 8)


def dimensions(path: Path) -> tuple[int, int]:
    for line in path.read_text(encoding="utf8").splitlines():
        words = line.split()
        if words and words[0] == "MAP":
            return int(words[1]), int(words[2])
    raise ValueError(f"missing MAP header: {path}")


def official_maps() -> list[Path]:
    paths = []
    for name, relative, width, height in SPECS:
        path = ROOT / relative
        if not path.is_file() or path.stem != name:
            raise ValueError(f"missing official map {name}: {path}")
        if dimensions(path) != (width, height):
            raise ValueError(f"wrong dimensions for {name}: {dimensions(path)}")
        paths.append(path)
    if len({map_signature(path) for path in paths}) != len(SPECS):
        raise ValueError("official suite contains duplicate playable layouts")
    return paths


def require_coverage(paths: list[Path]) -> None:
    expected = {map_signature(path) for path in official_maps()}
    present = {map_signature(path) for path in paths}
    if present != expected or len(paths) != len(SPECS):
        raise ValueError(f"bot-change test must cover all {len(SPECS)} distinct official maps")
