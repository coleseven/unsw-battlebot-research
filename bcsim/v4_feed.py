"""Sequential, in-process protected-grower and conditional-feeding ablation."""

import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import guarded, population
from .paths import ROOT, RESULTS, bot_hash, file_hash, foreign_imports, map_signature

BASE = ROOT / "versions/v3"
SOURCE_MAP_PLAN = RESULTS / "20260924-113203-v4-abbee0/plan.json"
MAP_NAMES = ("default", "schooltime", "stronghold", "big_empty")


def make_candidate(dest, feed):
    population.snapshot(BASE, dest)
    (dest / "brain.py").rename(dest / "v3_brain.py")
    shutil.copy2(ROOT / "experiments/v4/feed_brain.py", dest / "brain.py")
    shutil.copy2(ROOT / "framework/v4_feeding.py", dest / "v4_feeding.py")
    (dest / "feed_config.py").write_text(f"FEED = {feed!r}\n", encoding="utf8")
    assert not foreign_imports(dest)
    return dest


def prepare():
    assert bot_hash(BASE) == "69382825b699723d"
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-v4-feed-" + uuid.uuid4().hex[:6])
    out.mkdir()
    population.snapshot(BASE, out / "bots" / "reference_v3")
    make_candidate(out / "bots" / "grower", False)
    make_candidate(out / "bots" / "feed", True)
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
    sources = (ROOT / "experiments/v4/feed_brain.py", ROOT / "framework/v4_feeding.py",
               ROOT / "bcsim/v4_feed.py", ROOT / "bcsim/match.py", ROOT / "bcsim/guarded.py",
               ROOT / "bcsim/bounded.py")
    plan = {
        "question": "Does protected growth help v3, and does conditional local feeding add benefit?",
        "baseline_hash": bot_hash(BASE), "live_hash": bot_hash(ROOT / "mybot"),
        "bot_hashes": {n: bot_hash(out / "bots" / n) for n in
                       ("reference_v3", "grower", "feed")},
        "maps": maps, "map_hashes": {p: file_hash(Path(p)) for p in maps},
        "seed": 44000, "workers": 1, "games_per_stage": len(maps) * 2,
        "pairings": (("grower", "reference_v3"), ("feed", "grower"),
                     ("feed", "reference_v3")),
        "screen_rule": "Exploratory only. A worthwhile combined finalist must score >50% "
                       "in all three direct pairings, with no errors; no v4 freeze from this screen.",
        "future_gate": "Fresh maps and mixed opponents, positive map-cluster lower bound, "
                       "replay action audit and judge CPU check before any v4 freeze.",
        "limits": "Four familiar round-limit-prone maps. Deterministic local bots, one seed "
                  "and both sides. All games use the in-process protocol and one worker after "
                  "the host crash during four concurrent process-bot games. The feed predicate "
                  "requires a visible long teammate; it may rarely activate.",
        "source_hashes": {str(p.relative_to(ROOT)): file_hash(p) for p in sources},
    }
    population.write_json(out / "plan.json", plan)
    print(out, flush=True)


def screen(out):
    plan = json.loads((out / "plan.json").read_text())
    assert plan["workers"] == 1 and bot_hash(BASE) == plan["baseline_hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    for name, expected in plan["bot_hashes"].items():
        path = out / "bots" / name
        assert bot_hash(path) == expected and (path / "bc.py").is_file()
    for path, expected in plan["map_hashes"].items():
        assert file_hash(Path(path)) == expected
    for path, expected in plan["source_hashes"].items():
        assert file_hash(ROOT / path) == expected
    maps = [Path(p) for p in plan["maps"]]
    results = {}
    for candidate, opponent in plan["pairings"]:
        name = f"{candidate}-vs-{opponent}"
        games = guarded.stage(out, name, [out / "bots" / candidate],
                              [out / "bots" / opponent], maps, [plan["seed"]], 1, True)
        assert len(games) == plan["games_per_stage"]
        tally = population.tally(games, candidate)
        results[name] = {"wins": tally.w, "draws": tally.d, "losses": tally.l,
                         "score": tally.score, "pair_ci95": tally.ci()}
    promising = all(row["score"] > .5 for row in results.values())
    population.write_json(out / "screen-comparison.json", {
        "results": results, "worth_fresh_followup": promising, "is_promotion": False})
    print(json.dumps({"results": results, "worth_fresh_followup": promising}, indent=2), flush=True)


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
