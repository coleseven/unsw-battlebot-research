"""Isolate earlier local feeding and rendezvous atop the early-king bot."""

import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import guarded, population, v5_initial
from .paths import ROOT, RESULTS, bot_hash, file_hash, map_signature

KING = RESULTS / "20260924-194928-v5-early-king-47a8ab/bots/early_king"
MAPS = (ROOT / "maps/big_empty.map", ROOT / "maps/default.map",
        ROOT / "maps/schooltime.map", ROOT / "maps/server/stronghold.map",
        ROOT / "maps/server/Trauma.map", ROOT / "maps/trophy.map")


def prepare():
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") +
                     "-v5-feed-" + uuid.uuid4().hex[:6])
    out.mkdir()
    population.snapshot(KING, out / "bots/early_king")
    population.snapshot(v5_initial.BASE, out / "bots/additive")
    v5_initial.variant(out / "bots/feed_king", False, True, True)
    (out / "maps").mkdir()
    maps = []
    for source in MAPS:
        dest = out / "maps" / source.name
        shutil.copy2(source, dest)
        maps.append(str(dest))
    assert len({map_signature(Path(p)) for p in maps}) == len(maps)
    sources = [ROOT / p for p in (
        "experiments/v5/brain.py", "framework/v5_feeding.py",
        "framework/v5_king.py", "framework/v5_hotspot.py",
        "bcsim/v5_initial.py", "bcsim/v5_feed_trial.py")]
    plan = {
        "question": "Does earlier local rendezvous/feeding grow a protected king more reliably?",
        "mechanism": "Feed length-2..4 dragons from round 440 only beside a collectible, unthreatened long ally; nudge visible short dragons toward it from 430.",
        "limits": "One deterministic local game per map and side, six maps, one worker. Bot seeds do not independently reseed the engine.",
        "seed": 47001, "workers": 1,
        "king_hash": bot_hash(KING),
        "baseline_hash": bot_hash(v5_initial.BASE),
        "live_hash": bot_hash(ROOT / "mybot"),
        "bot_hashes": {name: bot_hash(out / "bots" / name)
                       for name in ("early_king", "additive", "feed_king")},
        "maps": maps, "map_hashes": {p: file_hash(Path(p)) for p in maps},
        "source_hashes": {str(p.relative_to(ROOT)): file_hash(p) for p in sources},
    }
    population.write_json(out / "plan.json", plan)
    print(out, flush=True)


def screen(out):
    plan = json.loads((out / "plan.json").read_text())
    assert bot_hash(KING) == plan["king_hash"]
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
    games = guarded.stage(out, "vs-king", [bots / "feed_king"],
                          [bots / "early_king"], maps, [plan["seed"]], 1, True)
    tally = population.tally(games, "feed_king")
    against_king = {"wins": tally.w, "draws": tally.d,
                    "losses": tally.l, "score": tally.score}
    games2 = guarded.stage(out, "vs-additive", [bots / "feed_king"],
                           [bots / "additive"], maps, [plan["seed"]], 1, True)
    tally2 = population.tally(games2, "feed_king")
    result = {"vs_early_king": against_king,
              "vs_additive": {"wins": tally2.w, "draws": tally2.d,
                              "losses": tally2.l, "score": tally2.score}}
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
