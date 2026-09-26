"""Validate a Trauma-gated scout that splits to export hotspot length."""

import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import guarded, population, v5_initial
from .paths import ROOT, RESULTS, bot_hash, file_hash, map_signature

MAPS = (ROOT / "maps/server/stronghold.map", ROOT / "maps/server/Trauma.map")


def prepare():
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") +
                     "-v5-export-" + uuid.uuid4().hex[:6])
    out.mkdir()
    population.snapshot(v5_initial.BASE, out / "bots/additive")
    v5_initial.variant(out / "bots/export_scout", True, False)
    (out / "maps").mkdir()
    maps = []
    for source in MAPS:
        dest = out / "maps" / source.name
        shutil.copy2(source, dest)
        maps.append(str(dest))
    assert len({map_signature(Path(p)) for p in maps}) == 2
    sources = [ROOT / p for p in (
        "experiments/v5/brain.py", "framework/v5_hotspot.py",
        "framework/v5_king.py", "bcsim/v5_initial.py", "bcsim/v5_export.py")]
    plan = {
        "question": "Does observation-gated Trauma scouting retain its advantage on fresh seeds while leaving stronghold unchanged?",
        "hypothesis": "Fission exports length from the dead end; visible opening tiles gate the route to Trauma.",
        "limits": "Known 48x24 maps, four fresh seeds, both sides, one worker; exploratory only.",
        "seeds": [45003, 45004, 45005, 45006], "workers": 1,
        "baseline_hash": bot_hash(v5_initial.BASE),
        "live_hash": bot_hash(ROOT / "mybot"),
        "bot_hashes": {name: bot_hash(out / "bots" / name)
                       for name in ("additive", "export_scout")},
        "maps": maps, "map_hashes": {p: file_hash(Path(p)) for p in maps},
        "source_hashes": {str(p.relative_to(ROOT)): file_hash(p) for p in sources},
    }
    population.write_json(out / "plan.json", plan)
    print(out, flush=True)


def screen(out):
    plan = json.loads((out / "plan.json").read_text())
    assert bot_hash(v5_initial.BASE) == plan["baseline_hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    for name, expected in plan["bot_hashes"].items():
        assert bot_hash(out / "bots" / name) == expected
    for path, expected in plan["map_hashes"].items():
        assert file_hash(Path(path)) == expected
    for path, expected in plan["source_hashes"].items():
        assert file_hash(ROOT / path) == expected
    games = guarded.stage(out, "vs-additive", [out / "bots/export_scout"],
                          [out / "bots/additive"], [Path(p) for p in plan["maps"]],
                          plan["seeds"], 1, True)
    tally = population.tally(games, "export_scout")
    result = {"wins": tally.w, "draws": tally.d, "losses": tally.l,
              "score": tally.score, "pair_ci95": tally.ci()}
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
