"""Small one-worker upload-readiness check on maps unused by additive screening."""

import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import guarded, population
from .paths import ROOT, RESULTS, bot_hash, file_hash, map_signature

SOURCE = RESULTS / "20260924-172250-v4-additive-9c22dc/bots/additive"
V3 = ROOT / "versions/v3"
V2 = ROOT / "versions/v2"
MAPS = (ROOT / "maps/server/Devil.map", ROOT / "maps/server/Trauma.map",
        ROOT / "maps/queen_of_spades.map", ROOT / "maps/Colosseum.map")


def prepare():
    assert bot_hash(SOURCE) == "bf33497158a49a7b"
    assert bot_hash(V3) == "69382825b699723d"
    assert bot_hash(V2) == "9f29ab4138b51d26"
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-v4-additive-validation-" + uuid.uuid4().hex[:6])
    out.mkdir()
    for name, source in (("additive", SOURCE), ("reference_v3", V3), ("reference_v2", V2)):
        population.snapshot(source, out / "bots" / name)
    (out / "maps").mkdir()
    maps = []
    for source in MAPS:
        dest = out / "maps" / source.name
        shutil.copy2(source, dest)
        maps.append(str(dest))
    assert len(set(map_signature(Path(p)) for p in maps)) == len(maps) == 4
    sources = (ROOT / "bcsim/v4_additive_validate.py", ROOT / "bcsim/match.py",
               ROOT / "bcsim/guarded.py", ROOT / "bcsim/bounded.py")
    plan = {"question": "Does clean v3+feed+sonar remain promising on four new maps, and beat uploaded v2?",
            "candidate_hash": bot_hash(SOURCE), "v3_hash": bot_hash(V3), "v2_hash": bot_hash(V2),
            "live_hash": bot_hash(ROOT / "mybot"),
            "bot_hashes": {n: bot_hash(out / "bots" / n) for n in
                           ("additive", "reference_v3", "reference_v2")},
            "maps": maps, "map_hashes": {p: file_hash(Path(p)) for p in maps},
            "v3_seeds": [44002, 44003], "v2_seeds": [44002], "workers": 1,
            "v3_games": 16, "v2_games": 8,
            "decision": "A small upload-readiness screen, not a ladder-strength claim. Prefer at least "
                        "a winning v3 score, a clear v2 edge, no errors, and a passing separate "
                        "judge-sandbox runtime test. Do not submit automatically.",
            "source_hashes": {str(p.relative_to(ROOT)): file_hash(p) for p in sources}}
    population.write_json(out / "plan.json", plan)
    print(out, flush=True)


def screen(out):
    plan = json.loads((out / "plan.json").read_text())
    assert plan["workers"] == 1 and bot_hash(SOURCE) == plan["candidate_hash"]
    assert bot_hash(V3) == plan["v3_hash"] and bot_hash(V2) == plan["v2_hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    for name, expected in plan["bot_hashes"].items():
        assert bot_hash(out / "bots" / name) == expected
    for path, expected in plan["map_hashes"].items():
        assert file_hash(Path(path)) == expected
    for path, expected in plan["source_hashes"].items():
        assert file_hash(ROOT / path) == expected
    bots = out / "bots"
    maps = [Path(p) for p in plan["maps"]]
    v3 = guarded.stage(out, "vs-v3", [bots / "additive"], [bots / "reference_v3"],
                       maps, plan["v3_seeds"], 1, True)
    v2 = guarded.stage(out, "vs-v2", [bots / "additive"], [bots / "reference_v2"],
                       maps, plan["v2_seeds"], 1, True)
    assert len(v3) == plan["v3_games"] and len(v2) == plan["v2_games"]
    results = {}
    for name, games in (("v3", v3), ("v2", v2)):
        tally = population.tally(games, "additive")
        results[name] = {"wins": tally.w, "draws": tally.d, "losses": tally.l,
                         "score": tally.score, "pair_ci95": tally.ci()}
    population.write_json(out / "screen-comparison.json", {"results": results,
                           "sandbox_required": True, "is_submission": False})
    print(json.dumps(results, indent=2), flush=True)


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
