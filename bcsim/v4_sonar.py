"""One-worker sonar delivery and routing feasibility screen."""

import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import guarded, population, reconstruct, replay
from .paths import ROOT, RESULTS, bot_hash, file_hash, foreign_imports, map_signature

BASE = ROOT / "versions/v3"
FEED = RESULTS / "20260924-131752-v4-feed-48a467/bots/feed"
SOURCE_MAP_PLAN = RESULTS / "20260924-131752-v4-feed-48a467/plan.json"
MAP_NAMES = ("schooltime", "stronghold")
MODES = ("beacon", "route")


def make_candidate(dest, mode):
    if mode not in MODES:
        raise ValueError(mode)
    population.snapshot(BASE, dest)
    (dest / "brain.py").rename(dest / "v3_brain.py")
    shutil.copy2(ROOT / "experiments/v4/sonar_brain.py", dest / "brain.py")
    shutil.copy2(ROOT / "framework/v4_feeding.py", dest / "v4_feeding.py")
    shutil.copy2(ROOT / "framework/v4_sonar.py", dest / "v4_sonar.py")
    (dest / "sonar_config.py").write_text(f"MODE = {mode!r}\n", encoding="utf8")
    assert not foreign_imports(dest)
    return dest


def sonar_counts(game, candidate):
    r = replay.load(game["replay"])
    board = reconstruct.Board(r.map_text)
    teams = {i: team for i, (team, _) in enumerate(board.dragons)}
    side = "A" if game["bot_a"] == candidate else "B"
    counts = {"pings": 0, "friendly_hits": 0, "enemy_hits": 0, "misses": 0,
              "candidate_received": 0}
    for ev in r.events:
        if ev[0] == replay.DRAGON_SPLIT:
            teams[ev[2]] = ev[3]
        elif ev[0] == replay.SONAR_PING:
            if teams.get(ev[1]) == side:
                counts["pings"] += 1
                hit = ev[6]
                if hit is None:
                    counts["misses"] += 1
                elif teams.get(hit) == side:
                    counts["friendly_hits"] += 1
                    counts["candidate_received"] += 1
                else:
                    counts["enemy_hits"] += 1
            elif ev[6] is not None and teams.get(ev[6]) == side:
                counts["candidate_received"] += 1
    return counts


def prepare():
    assert bot_hash(BASE) == "69382825b699723d"
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-v4-sonar-" + uuid.uuid4().hex[:6])
    out.mkdir()
    population.snapshot(FEED, out / "bots" / "feed_base")
    population.snapshot(BASE, out / "bots" / "reference_v3")
    for mode in MODES:
        make_candidate(out / "bots" / mode, mode)
    source = json.loads(SOURCE_MAP_PLAN.read_text())
    (out / "maps").mkdir()
    maps = []
    for name in source["maps"]:
        p = Path(name)
        if p.stem.rsplit("_", 1)[0] not in MAP_NAMES:
            continue
        dest = out / "maps" / p.name
        shutil.copy2(p, dest)
        maps.append(str(dest))
    assert len(maps) == len({map_signature(Path(p)) for p in maps}) == len(MAP_NAMES)
    sources = (ROOT / "experiments/v4/sonar_brain.py", ROOT / "framework/v4_sonar.py",
               ROOT / "framework/v4_feeding.py", ROOT / "bcsim/v4_sonar.py",
               ROOT / "bcsim/match.py", ROOT / "bcsim/guarded.py", ROOT / "bcsim/bounded.py")
    plan = {"question": "Can a public sonar king-beacon reach teammates, and does routing alter outcomes?",
            "baseline_hash": bot_hash(BASE), "feed_baseline_hash": bot_hash(FEED),
            "live_hash": bot_hash(ROOT / "mybot"),
            "bot_hashes": {n: bot_hash(out / "bots" / n) for n in
                           ("feed_base", "reference_v3", *MODES)},
            "maps": maps, "map_hashes": {p: file_hash(Path(p)) for p in maps},
            "seed": 44000, "workers": 1,
            "screen_games": 3 * len(maps) * 2,
            "direct_games": len(maps) * 2,
            "selection": "Feasibility only. Beacon must preserve base action outcomes and yield "
                         "a friendly sonar hit. Route is exploratory, with no promotion gate here.",
            "limits": "Two familiar maps, deterministic in-process opponents, one seed and "
                      "one worker. Sonar rays can hit enemies; packets reveal only public position "
                      "and approximate length. No claim about ladder strength.",
            "source_hashes": {str(p.relative_to(ROOT)): file_hash(p) for p in sources}}
    population.write_json(out / "plan.json", plan)
    print(out, flush=True)


def screen(out):
    plan = json.loads((out / "plan.json").read_text())
    assert plan["workers"] == 1 and bot_hash(BASE) == plan["baseline_hash"]
    assert bot_hash(FEED) == plan["feed_baseline_hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    for name, expected in plan["bot_hashes"].items():
        path = out / "bots" / name
        assert bot_hash(path) == expected and (path / "bc.py").is_file()
    for path, expected in plan["map_hashes"].items():
        assert file_hash(Path(path)) == expected
    for path, expected in plan["source_hashes"].items():
        assert file_hash(ROOT / path) == expected
    bots = out / "bots"
    maps = [Path(p) for p in plan["maps"]]
    pool = guarded.stage(out, "screen-v3", [bots / n for n in ("feed_base", *MODES)],
                         [bots / "reference_v3"], maps, [plan["seed"]], 1, True)
    direct = guarded.stage(out, "route-vs-beacon", [bots / "route"],
                           [bots / "beacon"], maps, [plan["seed"]], 1, True)
    assert len(pool) == plan["screen_games"] and len(direct) == plan["direct_games"]
    results = {}
    for name in ("feed_base", *MODES):
        tally = population.tally(pool, name)
        results[name] = {"wins": tally.w, "draws": tally.d, "losses": tally.l,
                         "score": tally.score}
    tally = population.tally(direct, "route")
    results["route_vs_beacon"] = {"wins": tally.w, "draws": tally.d,
                                   "losses": tally.l, "score": tally.score}
    delivery = {}
    for name in MODES:
        rows = [sonar_counts(g, name) for g in pool if name in (g["bot_a"], g["bot_b"])]
        delivery[name] = {key: sum(row[key] for row in rows) for key in
                          ("pings", "friendly_hits", "enemy_hits", "misses", "candidate_received")}
    control = [g for g in pool if "feed_base" in (g["bot_a"], g["bot_b"])]
    beacon_games = [g for g in pool if "beacon" in (g["bot_a"], g["bot_b"])]
    def signature(g, name):
        return (g["map"], "A" if g["bot_a"] == name else "B", g["winner"], g["reason"],
                g["rounds"], g["a_length"], g["b_length"], g["a_longest"], g["b_longest"], g["deaths"])
    equivalent = sorted(map(str, (signature(g, "feed_base") for g in control))) == \
                 sorted(map(str, (signature(g, "beacon") for g in beacon_games)))
    population.write_json(out / "screen-comparison.json", {
        "results": results, "delivery": delivery, "beacon_base_outcomes_identical": equivalent,
        "feasibility_pass": equivalent and delivery["beacon"]["friendly_hits"] > 0,
        "is_promotion": False})
    print(json.dumps({"results": results, "delivery": delivery,
                      "beacon_base_outcomes_identical": equivalent}, indent=2), flush=True)


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
