"""Round-200 mechanism probe for the exploration mover against nicked v34."""

import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import analyze, guarded, population, replay, v5_initial
from .paths import ROOT, RESULTS, bot_hash, file_hash

NICKED = ROOT / "sparring/nicked"
CONTROL = RESULTS / "20260924-233609-full-change-bb86e5/bots/candidate"
OLD = RESULTS / "20260924-233609-full-change-bb86e5/full/replays"
MAPS = (ROOT / "maps/server/Default.map", ROOT / "maps/queen_of_spades.map")


def prepare():
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") +
                     "-v5-explore-probe-" + uuid.uuid4().hex[:6])
    out.mkdir()
    v5_initial.variant(out / "bots/exploration", True, True, exploration=True)
    population.snapshot(NICKED, out / "bots/nicked")
    (out / "maps").mkdir()
    maps = []
    for source in MAPS:
        dest = out / "maps" / source.name
        shutil.copy2(source, dest)
        maps.append(str(dest))
    sources = [ROOT / p for p in (
        "experiments/v5/brain.py", "framework/v5_exploration.py",
        "framework/navigation.py", "bcsim/v5_initial.py",
        "bcsim/v5_explore_probe.py")]
    population.write_json(out / "plan.json", {
        "question": "Does exploration change decisions and r200 growth against nicked?",
        "scope": "Diagnostic only: Default and Queen, both sides.",
        "seed": 59001, "workers": 1,
        "control_hash": bot_hash(CONTROL), "nicked_hash": bot_hash(NICKED),
        "live_hash": bot_hash(ROOT / "mybot"),
        "bot_hashes": {name: bot_hash(out / "bots" / name)
                       for name in ("exploration", "nicked")},
        "maps": maps, "map_hashes": {p: file_hash(Path(p)) for p in maps},
        "source_hashes": {str(p.relative_to(ROOT)): file_hash(p) for p in sources},
    })
    print(out, flush=True)


def actions(path):
    return [(ev[1], ev[2]) for ev in replay.load(path).events
            if ev[0] == replay.DRAGON_ACTION]


def at_200(path, side):
    stats = analyze.game_stats(path.read_bytes())
    row = min(stats["timeline"], key=lambda x: abs(x["round"] - 200))
    return row[side]


def screen(out):
    plan = json.loads((out / "plan.json").read_text())
    assert bot_hash(CONTROL) == plan["control_hash"]
    assert bot_hash(NICKED) == plan["nicked_hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    for name, expected in plan["bot_hashes"].items():
        assert bot_hash(out / "bots" / name) == expected
    for path, expected in plan["map_hashes"].items():
        assert file_hash(Path(path)) == expected
    for path, expected in plan["source_hashes"].items():
        assert file_hash(ROOT / path) == expected
    games = guarded.stage(out, "diagnostic", [out / "bots/exploration"],
                          [out / "bots/nicked"], [Path(p) for p in plan["maps"]],
                          [plan["seed"]], 1, True)
    rows = []
    for game in games:
        side_a = game["bot_a"] == "exploration"
        side = "A" if side_a else "B"
        old = OLD / (("candidate-vs-nicked" if side_a else "nicked-vs-candidate") +
                     f"-{game['map']}-s53001.replay")
        new = ROOT / game["replay"]
        rows.append({"map": game["map"], "side": side,
                     "changed_actions": actions(old) != actions(new),
                     "r200_control": at_200(old, side),
                     "r200_exploration": at_200(new, side),
                     "winner": game["winner"], "error": game["error"]})
    result = {"games": rows}
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
        parser.error("choose --prepare or RESULT_DIR --screen")
