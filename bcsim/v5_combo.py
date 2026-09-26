"""Interaction screen for the Trauma scout plus round-400 protected king."""

import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import guarded, population, v5_initial
from .paths import ROOT, RESULTS, bot_hash, file_hash, map_signature

NICKED = ROOT / "sparring/nicked"
MAPS = (ROOT / "maps/server/Trauma.map", ROOT / "maps/server/stronghold.map")


def prepare():
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") +
                     "-v5-combo-" + uuid.uuid4().hex[:6])
    out.mkdir()
    population.snapshot(v5_initial.BASE, out / "bots/additive")
    population.snapshot(NICKED, out / "bots/nicked")
    v5_initial.variant(out / "bots/scout_king", True, True)
    (out / "maps").mkdir()
    maps = []
    for source in MAPS:
        dest = out / "maps" / source.name
        shutil.copy2(source, dest)
        maps.append(str(dest))
    assert len({map_signature(Path(p)) for p in maps}) == 2
    sources = [ROOT / p for p in (
        "experiments/v5/brain.py", "framework/v5_king.py",
        "framework/v5_hotspot.py", "framework/v5_feeding.py",
        "bcsim/v5_initial.py", "bcsim/v5_combo.py")]
    population.write_json(out / "plan.json", {
        "question": "Can the Trauma scout and round-400 king improve together?",
        "limits": "Two known maps vs additive; Trauma only vs stronger nicked. Both sides, one worker. No release from this screen.",
        "seed": 52001, "workers": 1,
        "live_hash": bot_hash(ROOT / "mybot"),
        "source_bot_hashes": {"additive": bot_hash(v5_initial.BASE),
                              "nicked": bot_hash(NICKED)},
        "bot_hashes": {name: bot_hash(out / "bots" / name)
                       for name in ("scout_king", "additive", "nicked")},
        "maps": maps, "map_hashes": {p: file_hash(Path(p)) for p in maps},
        "source_hashes": {str(p.relative_to(ROOT)): file_hash(p) for p in sources},
    })
    print(out, flush=True)


def screen(out):
    plan = json.loads((out / "plan.json").read_text())
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    for name, source in (("additive", v5_initial.BASE), ("nicked", NICKED)):
        assert bot_hash(source) == plan["source_bot_hashes"][name]
    for name, expected in plan["bot_hashes"].items():
        assert bot_hash(out / "bots" / name) == expected
    for path, expected in plan["map_hashes"].items():
        assert file_hash(Path(path)) == expected
    for path, expected in plan["source_hashes"].items():
        assert file_hash(ROOT / path) == expected
    bots = out / "bots"
    maps = [Path(p) for p in plan["maps"]]
    result = {}
    for opponent, selection in (("additive", maps), ("nicked", maps[:1])):
        games = guarded.stage(out, "vs-" + opponent, [bots / "scout_king"],
                              [bots / opponent], selection, [plan["seed"]], 1, True)
        tally = population.tally(games, "scout_king")
        result[opponent] = {"wins": tally.w, "draws": tally.d,
                            "losses": tally.l, "score": tally.score}
        print(json.dumps({opponent: result[opponent]}, indent=2), flush=True)
    population.write_json(out / "comparison.json", result)


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
