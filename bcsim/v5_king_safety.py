"""Paired safety ablation: stricter election and friendly-head reach guard."""

import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import guarded, population, v5_initial
from .paths import ROOT, RESULTS, bot_hash, file_hash, map_signature

OLD = RESULTS / "20260924-194928-v5-early-king-47a8ab/bots/early_king"
MAPS = (ROOT / "maps/big_empty.map", ROOT / "maps/default.map",
        ROOT / "maps/schooltime.map", ROOT / "maps/server/stronghold.map",
        ROOT / "maps/server/Trauma.map", ROOT / "maps/trophy.map")


def prepare():
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") +
                     "-v5-king-safety-" + uuid.uuid4().hex[:6])
    out.mkdir()
    population.snapshot(OLD, out / "bots/early_king")
    population.snapshot(v5_initial.BASE, out / "bots/additive")
    v5_initial.variant(out / "bots/safe_king", False, True)
    (out / "maps").mkdir()
    maps = []
    for source in MAPS:
        dest = out / "maps" / source.name
        shutil.copy2(source, dest)
        maps.append(str(dest))
    assert len({map_signature(Path(p)) for p in maps}) == len(maps)
    sources = [ROOT / p for p in (
        "experiments/v5/brain.py", "framework/v5_king.py",
        "framework/v5_hotspot.py", "framework/v5_feeding.py",
        "bcsim/v5_initial.py", "bcsim/v5_king_safety.py")]
    population.write_json(out / "plan.json", {
        "question": "Does less crowded king election and friendly-head guarding help?",
        "limits": "Six maps, both sides, deterministic engine, one worker; mechanism screen.",
        "seed": 49001, "workers": 1,
        "old_hash": bot_hash(OLD), "baseline_hash": bot_hash(v5_initial.BASE),
        "live_hash": bot_hash(ROOT / "mybot"),
        "bot_hashes": {name: bot_hash(out / "bots" / name)
                       for name in ("early_king", "additive", "safe_king")},
        "maps": maps, "map_hashes": {p: file_hash(Path(p)) for p in maps},
        "source_hashes": {str(p.relative_to(ROOT)): file_hash(p) for p in sources},
    })
    print(out, flush=True)


def screen(out):
    plan = json.loads((out / "plan.json").read_text())
    assert bot_hash(OLD) == plan["old_hash"]
    assert bot_hash(v5_initial.BASE) == plan["baseline_hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    for name, expected in plan["bot_hashes"].items():
        assert bot_hash(out / "bots" / name) == expected
    for path, expected in plan["map_hashes"].items():
        assert file_hash(Path(path)) == expected
    for path, expected in plan["source_hashes"].items():
        assert file_hash(ROOT / path) == expected
    bots = out / "bots"
    maps = [Path(p) for p in plan["maps"]]
    result = {}
    for opponent in ("early_king", "additive"):
        games = guarded.stage(out, "vs-" + opponent, [bots / "safe_king"],
                              [bots / opponent], maps, [plan["seed"]], 1, True)
        tally = population.tally(games, "safe_king")
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
