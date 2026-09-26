"""Matched, one-worker screen for isolated v5 territory and king-safety ideas."""

import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import guarded, population
from .paths import ROOT, RESULTS, bot_hash, file_hash, map_signature

BASE = RESULTS / "20260924-172250-v4-additive-9c22dc/bots/additive"
MAPS = (ROOT / "maps/server/stronghold.map", ROOT / "maps/server/Trauma.map",
        ROOT / "maps/default.map", ROOT / "maps/trophy.map")
MODES = {"territory": (True, False), "king_guard": (False, True),
         "combined": (True, True)}


def variant(dest, territory, king, feed=False, sonar=True, king_start=400,
            portal_push=False, trap_guard=False, economy=False,
            queen_opening=False, head_guard=False, exploration=False,
            population_control=False):
    population.snapshot(ROOT / "versions/v3", dest)
    (dest / "brain.py").rename(dest / "v3_brain.py")
    for source, target in (
        ("experiments/v5/brain.py", "brain.py"),
        ("framework/v4_feeding.py", "v4_feeding.py"),
        ("framework/v4_sonar.py", "v4_sonar.py"),
        ("framework/v5_hotspot.py", "v5_hotspot.py"),
        ("framework/v5_king.py", "v5_king.py"),
        ("framework/v5_feeding.py", "v5_feeding.py"),
        ("framework/v5_portal_push.py", "v5_portal_push.py"),
        ("framework/v5_economy.py", "v5_economy.py"),
        ("framework/v5_queen_opening.py", "v5_queen_opening.py"),
        ("framework/v5_head_guard.py", "v5_head_guard.py"),
        ("framework/v5_exploration.py", "v5_exploration.py"),
        ("framework/v5_population.py", "v5_population.py"),
        ("framework/v4_safety.py", "v4_safety.py"),
        ("framework/navigation.py", "navigation.py"),
        ("framework/portal_escape.py", "portal_escape.py"),
        ("framework/local_safety.py", "local_safety.py"),
    ):
        shutil.copy2(ROOT / source, dest / target)
    (dest / "v5_config.py").write_text(
        f"TERRITORY = {territory!r}\nKING = {king!r}\nFEED = {feed!r}\n"
        f"SONAR = {sonar!r}\nKING_START = {king_start!r}\n"
        f"PORTAL_PUSH = {portal_push!r}\nTRAP_GUARD = {trap_guard!r}\n"
        f"ECONOMY = {economy!r}\nQUEEN_OPENING = {queen_opening!r}\n"
        f"HEAD_GUARD = {head_guard!r}\nEXPLORATION = {exploration!r}\n"
        f"POPULATION_CONTROL = {population_control!r}\n",
        encoding="utf8")
    return dest


def prepare():
    assert bot_hash(BASE) == "bf33497158a49a7b"
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") +
                     "-v5-initial-" + uuid.uuid4().hex[:6])
    out.mkdir()
    population.snapshot(BASE, out / "bots/additive")
    for name, (territory, king) in MODES.items():
        variant(out / "bots" / name, territory, king)
    (out / "maps").mkdir()
    maps = []
    for source in MAPS:
        dest = out / "maps" / source.name
        shutil.copy2(source, dest)
        maps.append(str(dest))
    assert len({map_signature(Path(path)) for path in maps}) == len(maps)
    sources = [ROOT / p for p in (
        "experiments/v5/brain.py", "framework/v5_hotspot.py",
        "framework/v5_king.py", "bcsim/v5_initial.py")]
    plan = {
        "question": "Do hotspot-directed scouts or protected growers improve frozen additive v4?",
        "limits": "Four known maps, one seed, both sides; 48x24 territory prior is map-specific. "
                  "Exploratory only; no promotion or upload from this screen.",
        "modes": MODES, "seed": 45000, "workers": 1,
        "baseline_hash": bot_hash(BASE),
        "live_hash": bot_hash(ROOT / "mybot"),
        "bot_hashes": {name: bot_hash(out / "bots" / name)
                       for name in ("additive", *MODES)},
        "maps": maps, "map_hashes": {p: file_hash(Path(p)) for p in maps},
        "source_hashes": {str(p.relative_to(ROOT)): file_hash(p) for p in sources},
    }
    population.write_json(out / "plan.json", plan)
    print(out, flush=True)


def screen(out):
    plan = json.loads((out / "plan.json").read_text())
    assert bot_hash(BASE) == plan["baseline_hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    for name, expected in plan["bot_hashes"].items():
        assert bot_hash(out / "bots" / name) == expected
    for path, expected in plan["map_hashes"].items():
        assert file_hash(Path(path)) == expected
    for path, expected in plan["source_hashes"].items():
        assert file_hash(ROOT / path) == expected
    games = guarded.stage(out, "vs-additive",
                          [out / "bots" / name for name in MODES],
                          [out / "bots/additive"],
                          [Path(p) for p in plan["maps"]],
                          [plan["seed"]], 1, True)
    result = {}
    for name in MODES:
        tally = population.tally(games, name)
        result[name] = {"wins": tally.w, "draws": tally.d,
                        "losses": tally.l, "score": tally.score,
                        "pair_ci95": tally.ci()}
    population.write_json(out / "screen-comparison.json", result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", nargs="?", type=Path)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--screen", action="store_true")
    args = parser.parse_args()
    if args.prepare:
        prepare()
    elif args.screen and args.experiment:
        screen(args.experiment)
    else:
        parser.error("choose --prepare or an experiment path with --screen")
