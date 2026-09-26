"""Paired test of round-350 versus round-400 protected king election."""

import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import guarded, population, v5_initial
from .paths import ROOT, RESULTS, bot_hash, file_hash, map_signature

KING_400 = RESULTS / "20260924-194928-v5-early-king-47a8ab/bots/early_king"
MAPS = (ROOT / "maps/big_empty.map", ROOT / "maps/default.map",
        ROOT / "maps/schooltime.map", ROOT / "maps/server/stronghold.map",
        ROOT / "maps/server/Trauma.map", ROOT / "maps/trophy.map")


def prepare():
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") +
                     "-v5-king-350-" + uuid.uuid4().hex[:6])
    out.mkdir()
    population.snapshot(KING_400, out / "bots/king_400")
    population.snapshot(v5_initial.BASE, out / "bots/additive")
    v5_initial.variant(out / "bots/king_350", False, True, king_start=350)
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
        "bcsim/v5_initial.py", "bcsim/v5_king_350.py")]
    population.write_json(out / "plan.json", {
        "question": "Can protection from round 350 build a longer king without losing survival?",
        "limits": "Six maps, both sides, deterministic engine, one worker; no promotion.",
        "seed": 50001, "workers": 1,
        "king_400_hash": bot_hash(KING_400),
        "baseline_hash": bot_hash(v5_initial.BASE),
        "live_hash": bot_hash(ROOT / "mybot"),
        "bot_hashes": {name: bot_hash(out / "bots" / name)
                       for name in ("king_350", "king_400", "additive")},
        "maps": maps, "map_hashes": {p: file_hash(Path(p)) for p in maps},
        "source_hashes": {str(p.relative_to(ROOT)): file_hash(p) for p in sources},
    })
    print(out, flush=True)


def screen(out):
    plan = json.loads((out / "plan.json").read_text())
    assert bot_hash(KING_400) == plan["king_400_hash"]
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
    for opponent in ("king_400", "additive"):
        games = guarded.stage(out, "vs-" + opponent, [bots / "king_350"],
                              [bots / opponent], maps, [plan["seed"]], 1, True)
        tally = population.tally(games, "king_350")
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
