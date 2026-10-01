"""The eleven distinct competition maps (required coverage for bot changes)
plus the four ladder-only maps: fifteen layouts, the whole ranked pool."""

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

# Ladder-only maps: in the ranked pool since about 25 Sep but not in the
# eleven above. Every ranked map seen in our downloaded replays (23 names) is
# one of these fifteen layouts, so SPECS + LADDER_SPECS is the whole pool.
LADDER_SPECS = (
    ("Autarky", "maps/server/Autarky.map", 54, 18),
    ("Prisoners_Dilemma", "maps/server/Prisoners_Dilemma.map", 32, 16),
    ("Slithery_Fight", "maps/server/Slithery_Fight.map", 63, 27),
    ("Portals", "maps/server/Portals.map", 32, 16),
)

# Maps the ranked server is drawing right now (sampled from public ranked
# battles, 27 Sep 02:00 UTC): since about 26 Sep 14:00-16:00 UTC ten maps;
# Default Small, Stronghold and Big Empty left then, Arena and Colosseum have
# not appeared since at least 25 Sep 12:00. Elo counts games won, so this pool
# is the primary target; the other five stay as a regression guard because the
# pool has changed twice in two days. Re-sample before relying on it.
CURRENT_POOL = ("trophy", "queen_of_spades", "default", "Devil", "Trauma", "schooltime",
                "Autarky", "Prisoners_Dilemma", "Slithery_Fight", "Portals")

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
    """Every official layout present, no layout twice (extra ladder maps allowed)."""
    expected = {map_signature(path) for path in official_maps()}
    signatures = [map_signature(path) for path in paths]
    if not expected <= set(signatures) or len(set(signatures)) != len(signatures):
        raise ValueError(f"bot-change test must cover all {len(SPECS)} distinct official maps")


def _load(specs) -> list[Path]:
    paths = []
    for name, relative, width, height in specs:
        path = ROOT / relative
        if not path.is_file() or path.stem != name:
            raise ValueError(f"missing map {name}: {path}")
        if dimensions(path) != (width, height):
            raise ValueError(f"wrong dimensions for {name}: {dimensions(path)}")
        paths.append(path)
    return paths


def ladder_extra_maps() -> list[Path]:
    """The four ladder-only maps."""
    return _load(LADDER_SPECS)


# The Sprint tournament (1 Oct 2026) played only unseen maps (best of 7). The
# ladder still drew the ten CURRENT_POOL maps afterwards (sampled 1 Oct 14:51
# UTC), so these are a separate generalisation panel: no map book applies to
# them, as in later tournaments that may use unseen maps too.
SPRINT_SPECS = (
    ("Australia", "maps/server/Australia.map", 64, 64),
    ("Islands", "maps/server/Islands.map", 56, 40),
    ("Maze", "maps/server/Maze.map", 48, 24),
    ("Stripes", "maps/server/Stripes.map", 24, 12),
    ("Tower_Defense", "maps/server/Tower_Defense.map", 32, 16),
    ("Around_UNSW", "maps/server/Around_UNSW.map", 64, 64),
    ("weakhold", "maps/server/weakhold.map", 40, 15),
)


def sprint_maps() -> list[Path]:
    """The seven Sprint (unseen-map) layouts: a generalisation panel, not ladder maps."""
    return _load(SPRINT_SPECS)


def current_pool_maps() -> list[Path]:
    """The maps in the current ranked rotation (CURRENT_POOL), in suite order."""
    return [p for p in ranked_maps() if p.stem in CURRENT_POOL]


def ranked_maps() -> list[Path]:
    """All fifteen distinct ranked layouts: the official eleven, then the ladder four."""
    paths = official_maps() + ladder_extra_maps()
    if len({map_signature(p) for p in paths}) != len(paths):
        raise ValueError("ranked pool contains duplicate playable layouts")
    return paths
