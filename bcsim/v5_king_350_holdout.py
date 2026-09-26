"""Untuned holdout: frozen round-350 versus round-400 kings on five other maps."""

import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import guarded, population
from .paths import ROOT, RESULTS, bot_hash, file_hash, map_signature

SOURCE = RESULTS / "20260924-222647-v5-king-350-937025/bots"
MAPS = (ROOT / "maps/arena.map", ROOT / "maps/Colosseum.map",
        ROOT / "maps/default_small.map", ROOT / "maps/queen_of_spades.map",
        ROOT / "maps/server/Devil.map")


def prepare():
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") +
                     "-v5-king-350-holdout-" + uuid.uuid4().hex[:6])
    out.mkdir()
    for name in ("king_350", "king_400"):
        population.snapshot(SOURCE / name, out / "bots" / name)
    (out / "maps").mkdir()
    maps = []
    for source in MAPS:
        dest = out / "maps" / source.name
        shutil.copy2(source, dest)
        maps.append(str(dest))
    assert len({map_signature(Path(p)) for p in maps}) == 5
    population.write_json(out / "plan.json", {
        "question": "Does the unchanged round-350 king generalize beyond its six screen maps?",
        "limits": "Five distinct held-out official maps, both sides, deterministic engine, one worker.",
        "seed": 51001, "workers": 1,
        "live_hash": bot_hash(ROOT / "mybot"),
        "source_hashes": {name: bot_hash(SOURCE / name)
                          for name in ("king_350", "king_400")},
        "bot_hashes": {name: bot_hash(out / "bots" / name)
                       for name in ("king_350", "king_400")},
        "maps": maps, "map_hashes": {p: file_hash(Path(p)) for p in maps},
        "script_hash": file_hash(Path(__file__)),
    })
    print(out, flush=True)


def screen(out):
    plan = json.loads((out / "plan.json").read_text())
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    assert file_hash(Path(__file__)) == plan["script_hash"]
    for name, expected in plan["source_hashes"].items():
        assert bot_hash(SOURCE / name) == expected
    for name, expected in plan["bot_hashes"].items():
        assert bot_hash(out / "bots" / name) == expected
    for path, expected in plan["map_hashes"].items():
        assert file_hash(Path(path)) == expected
    bots = out / "bots"
    games = guarded.stage(out, "vs-king_400", [bots / "king_350"],
                          [bots / "king_400"], [Path(p) for p in plan["maps"]],
                          [plan["seed"]], 1, True)
    tally = population.tally(games, "king_350")
    result = {"wins": tally.w, "draws": tally.d,
              "losses": tally.l, "score": tally.score}
    population.write_json(out / "comparison.json", result)
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
