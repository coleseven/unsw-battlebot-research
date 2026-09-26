"""One-worker matched screen of clean v3+feed+sonar against v3 and old route."""

import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import guarded, population
from .paths import ROOT, RESULTS, bot_hash, file_hash, foreign_imports, map_signature

BASE = ROOT / "versions/v3"
OLD_ROUTE = RESULTS / "20260924-133212-v4-sonar-e451f4/bots/route"
MAP_PLAN = RESULTS / "20260924-131752-v4-feed-48a467/plan.json"


def make_candidate(dest):
    population.snapshot(BASE, dest)
    (dest / "brain.py").rename(dest / "v3_brain.py")
    shutil.copy2(ROOT / "experiments/v4/additive_brain.py", dest / "brain.py")
    shutil.copy2(ROOT / "framework/v4_feeding.py", dest / "v4_feeding.py")
    shutil.copy2(ROOT / "framework/v4_sonar.py", dest / "v4_sonar.py")
    assert not foreign_imports(dest)
    return dest


def prepare():
    assert bot_hash(BASE) == "69382825b699723d"
    assert bot_hash(OLD_ROUTE) == "a3bd27841857e668"
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-v4-additive-" + uuid.uuid4().hex[:6])
    out.mkdir()
    population.snapshot(BASE, out / "bots/reference_v3")
    population.snapshot(OLD_ROUTE, out / "bots/old_route")
    make_candidate(out / "bots/additive")
    (out / "maps").mkdir()
    maps = []
    for name in json.loads(MAP_PLAN.read_text())["maps"]:
        source = Path(name)
        dest = out / "maps" / source.name
        shutil.copy2(source, dest)
        maps.append(str(dest))
    assert len(maps) == len({map_signature(Path(p)) for p in maps}) == 4
    sources = (ROOT / "experiments/v4/additive_brain.py", ROOT / "framework/v4_feeding.py",
               ROOT / "framework/v4_sonar.py", ROOT / "bcsim/v4_additive.py",
               ROOT / "bcsim/match.py", ROOT / "bcsim/guarded.py", ROOT / "bcsim/bounded.py")
    plan = {
        "question": "Does adding only feeding and sonar routing to frozen v3 beat v3 or the old grower+feed+sonar route?",
        "baseline_hash": bot_hash(BASE), "old_route_hash": bot_hash(OLD_ROUTE),
        "live_hash": bot_hash(ROOT / "mybot"),
        "bot_hashes": {n: bot_hash(out / "bots" / n) for n in
                       ("reference_v3", "old_route", "additive")},
        "maps": maps, "map_hashes": {p: file_hash(Path(p)) for p in maps},
        "seed": 44001, "workers": 1, "pool_games": 16, "direct_games": 8,
        "pairings": "additive and old_route each vs v3, then additive directly vs old_route; both sides per map",
        "selection": "Exploratory. No promotion from one seed/four familiar maps. Compare paired scores and replay mechanism.",
        "limits": "In-process one-worker games after host crash; judge CPU and fresh-opponent validation remain required.",
        "source_hashes": {str(p.relative_to(ROOT)): file_hash(p) for p in sources},
    }
    population.write_json(out / "plan.json", plan)
    print(out, flush=True)


def screen(out):
    plan = json.loads((out / "plan.json").read_text())
    assert plan["workers"] == 1 and bot_hash(BASE) == plan["baseline_hash"]
    assert bot_hash(OLD_ROUTE) == plan["old_route_hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    for name, expected in plan["bot_hashes"].items():
        bot = out / "bots" / name
        assert bot_hash(bot) == expected and (bot / "bc.py").is_file()
    for path, expected in plan["map_hashes"].items():
        assert file_hash(Path(path)) == expected
    for path, expected in plan["source_hashes"].items():
        assert file_hash(ROOT / path) == expected
    bots = out / "bots"
    maps = [Path(p) for p in plan["maps"]]
    pool = guarded.stage(out, "vs-v3", [bots / "additive", bots / "old_route"],
                         [bots / "reference_v3"], maps, [plan["seed"]], 1, True)
    direct = guarded.stage(out, "vs-old-route", [bots / "additive"],
                           [bots / "old_route"], maps, [plan["seed"]], 1, True)
    assert len(pool) == plan["pool_games"] and len(direct) == plan["direct_games"]
    results = {}
    for name in ("additive", "old_route"):
        tally = population.tally(pool, name)
        results[name + "_vs_v3"] = {"wins": tally.w, "draws": tally.d,
                                   "losses": tally.l, "score": tally.score}
    tally = population.tally(direct, "additive")
    results["additive_vs_old_route"] = {"wins": tally.w, "draws": tally.d,
                                         "losses": tally.l, "score": tally.score}
    paired = population.paired_delta(pool, "additive", "old_route")
    population.write_json(out / "screen-comparison.json", {
        "results": results, "paired_vs_v3_delta": paired, "is_promotion": False})
    print(json.dumps({"results": results, "paired_vs_v3_delta": paired}, indent=2), flush=True)


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
