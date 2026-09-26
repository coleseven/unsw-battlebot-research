"""One-worker mechanism probe for a v5 local trap guard vs nicked."""

import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import guarded, population, replay, v5_initial
from .paths import ROOT, RESULTS, bot_hash, file_hash, map_signature

NICKED = ROOT / "sparring/nicked"
CONTROL = RESULTS / "20260924-223816-v5-combo-809e43/bots/scout_king"
OLD = RESULTS / "20260924-233609-full-change-bb86e5/full/replays"
MAPS = (ROOT / "maps/default_small.map", ROOT / "maps/server/Trauma.map")


def prepare():
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") +
                     "-v5-trap-probe-" + uuid.uuid4().hex[:6])
    out.mkdir()
    v5_initial.variant(out / "bots/trap_guard", True, True, trap_guard=True)
    population.snapshot(NICKED, out / "bots/nicked")
    (out / "maps").mkdir()
    maps = []
    for source in MAPS:
        dest = out / "maps" / source.name
        shutil.copy2(source, dest)
        maps.append(str(dest))
    assert len({map_signature(Path(p)) for p in maps}) == 2
    sources = [ROOT / p for p in (
        "experiments/v5/brain.py", "framework/local_safety.py",
        "bcsim/v5_initial.py", "bcsim/v5_trap_probe.py")]
    population.write_json(out / "plan.json", {
        "question": "Does the trap guard change actual decisions against nicked?",
        "scope": "Diagnostic only; full eleven-map screen follows any activation.",
        "seed": 55001, "workers": 1,
        "control_hash": bot_hash(CONTROL), "nicked_hash": bot_hash(NICKED),
        "live_hash": bot_hash(ROOT / "mybot"),
        "bot_hashes": {name: bot_hash(out / "bots" / name)
                       for name in ("trap_guard", "nicked")},
        "maps": maps, "map_hashes": {p: file_hash(Path(p)) for p in maps},
        "source_hashes": {str(p.relative_to(ROOT)): file_hash(p) for p in sources},
    })
    print(out, flush=True)


def action_stream(path):
    return [(ev[1], ev[2]) for ev in replay.load(path).events
            if ev[0] == replay.DRAGON_ACTION]


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
    games = guarded.stage(out, "diagnostic", [out / "bots/trap_guard"],
                          [out / "bots/nicked"], [Path(p) for p in plan["maps"]],
                          [plan["seed"]], 1, True)
    rows = []
    for game in games:
        side_a = game["bot_a"] == "trap_guard"
        old = OLD / (("candidate-vs-nicked" if side_a else "nicked-vs-candidate") +
                     f"-{game['map']}-s53001.replay")
        new = ROOT / game["replay"]
        prior, current = action_stream(old), action_stream(new)
        rows.append({"map": game["map"], "side": "A" if side_a else "B",
                     "changed_actions": prior != current,
                     "winner": game["winner"]})
    result = {"games": rows, "changed_action_games": sum(x["changed_actions"] for x in rows)}
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
