"""Screen sparse round-400 protected king candidates versus additive v4."""

import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import guarded, population, v5_initial
from .paths import ROOT, RESULTS, bot_hash, file_hash, map_signature

MAPS = (ROOT / "maps/big_empty.map", ROOT / "maps/default.map",
        ROOT / "maps/schooltime.map", ROOT / "maps/server/stronghold.map",
        ROOT / "maps/server/Trauma.map", ROOT / "maps/trophy.map")


def prepare():
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") +
                     "-v5-early-king-" + uuid.uuid4().hex[:6])
    out.mkdir()
    population.snapshot(v5_initial.BASE, out / "bots/additive")
    v5_initial.variant(out / "bots/early_king", False, True)
    (out / "maps").mkdir()
    maps = []
    for source in MAPS:
        dest = out / "maps" / source.name
        shutil.copy2(source, dest)
        maps.append(str(dest))
    assert len({map_signature(Path(p)) for p in maps}) == len(maps)
    sources = [ROOT / p for p in (
        "experiments/v5/brain.py", "framework/v5_king.py",
        "framework/v5_hotspot.py", "bcsim/v5_initial.py",
        "bcsim/v5_king_early.py")]
    plan = {
        "question": "Can sparse, safety-screened preexisting dragons stop splitting at round 400 and survive as kings?",
        "hypothesis": "Earlier protection creates a larger final dragon without the overpopulation cost of a one-quarter cutoff.",
        "limits": "Six known maps, two seeds, both sides, one worker; mechanism screen, not ladder validation.",
        "seeds": [46001, 46002], "workers": 1,
        "baseline_hash": bot_hash(v5_initial.BASE),
        "live_hash": bot_hash(ROOT / "mybot"),
        "bot_hashes": {name: bot_hash(out / "bots" / name)
                       for name in ("additive", "early_king")},
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
    games = guarded.stage(out, "vs-additive", [out / "bots/early_king"],
                          [out / "bots/additive"], [Path(p) for p in plan["maps"]],
                          plan["seeds"], 1, True)
    tally = population.tally(games, "early_king")
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
