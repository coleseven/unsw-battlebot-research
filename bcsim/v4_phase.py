"""Predeclared early-growth phase screen against frozen v3 and pinned sparring bots."""

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
MODES = ("global_300", "reserve_300")
MAP_NAMES = ("default_small", "default", "queen_of_spades", "Trauma", "Colosseum", "schooltime")
OPPONENTS = ("ctmes", "nicked")


def make_candidate(dest, mode):
    if mode not in MODES:
        raise ValueError(mode)
    population.snapshot(BASE, dest)
    (dest / "brain.py").rename(dest / "v3_brain.py")
    shutil.copy2(ROOT / "experiments/v4/phase_brain.py", dest / "brain.py")
    (dest / "phase_config.py").write_text(f"MODE = {mode!r}\n", encoding="utf8")
    assert not foreign_imports(dest)
    return dest


def prepare():
    assert bot_hash(BASE) == "69382825b699723d"
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-v4-phase-" + uuid.uuid4().hex[:6])
    out.mkdir()
    for name in ("control_v3", "reference_v3"):
        population.snapshot(BASE, out / "bots" / name)
    for mode in MODES:
        make_candidate(out / "bots" / mode, mode)
    for name in OPPONENTS:
        population.snapshot(ROOT / "sparring" / name, out / "bots" / name)
    source = json.loads(SOURCE_MAP_PLAN.read_text())
    (out / "maps").mkdir()
    maps = []
    for name in source["maps"]:
        p = Path(name)
        if not any(p.name.startswith(m + "_") for m in MAP_NAMES):
            continue
        dest = out / "maps" / p.name
        shutil.copy2(p, dest)
        maps.append(str(dest))
    assert len(maps) == len({map_signature(Path(p)) for p in maps}) == len(MAP_NAMES)
    sources = (ROOT / "experiments/v4/phase_brain.py", ROOT / "bcsim/v4_phase.py",
               ROOT / "bcsim/match.py", ROOT / "bcsim/guarded.py", ROOT / "bcsim/bounded.py")
    plan = {
        "question": "Does stopping all splitting at round 300, or reserving one in seven dragons then, "
                    "improve v3 against stronger pinned opponents?",
        "baseline_hash": bot_hash(BASE), "live_hash": bot_hash(ROOT / "mybot"),
        "candidate_hashes": {n: bot_hash(out / "bots" / n) for n in MODES},
        "opponent_hashes": {n: bot_hash(out / "bots" / n) for n in OPPONENTS},
        "maps": maps, "map_hashes": {p: file_hash(Path(p)) for p in maps},
        "screen_seed": 43000, "direct_seed": 43000,
        "screen_games": 3 * len(OPPONENTS) * len(maps) * 2,
        "direct_games": len(MODES) * len(maps) * 2,
        "selection": "Exploratory: positive paired pool score over v3 and at least 50% direct "
                     "v3 score. Choose highest paired gain; exact tie prefers reserve_300 "
                     "as the smaller change. No winner means no finalist.",
        "future_gate": "Fresh layouts and opponent versions, positive map-cluster lower bound, "
                       "exact replay audit and sandbox budget before a v4 freeze.",
        "limits": "Six familiar maps and one bot seed; process opponents may have unseeded "
                  "internal randomness, so matching block labels are not matched opponent RNG. "
                  "IDs are globally allocated; id modulo seven is a coarse, possibly side-biased "
                  "reserve assignment. No competitor code is copied into candidates.",
        "source_hashes": {str(p.relative_to(ROOT)): file_hash(p) for p in sources},
    }
    population.write_json(out / "plan.json", plan)
    print(out, flush=True)


def screen(out, workers):
    plan = json.loads((out / "plan.json").read_text())
    assert bot_hash(BASE) == plan["baseline_hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    for name, expected in {**plan["candidate_hashes"], **plan["opponent_hashes"]}.items():
        assert bot_hash(out / "bots" / name) == expected
    for path, expected in plan["map_hashes"].items():
        assert file_hash(Path(path)) == expected
    for path, expected in plan["source_hashes"].items():
        assert file_hash(ROOT / path) == expected
    bots = out / "bots"
    maps = [Path(p) for p in plan["maps"]]
    pooled = guarded.stage(out, "screen-pool", [bots / n for n in ("control_v3", *MODES)],
                           [bots / n for n in OPPONENTS], maps, [plan["screen_seed"]], workers, True)
    direct = guarded.stage(out, "screen-direct", [bots / n for n in MODES],
                           [bots / "reference_v3"], maps, [plan["direct_seed"]], workers, True)
    assert len(pooled) == plan["screen_games"] and len(direct) == plan["direct_games"]
    comparison = {}
    for name in MODES:
        delta = population.paired_delta(pooled, name, "control_v3")
        tally = population.tally(direct, name)
        comparison[name] = {"paired_pool": delta, "direct": {
            "wins": tally.w, "draws": tally.d, "losses": tally.l, "score": tally.score}}
    eligible = [n for n in MODES if comparison[n]["paired_pool"]["difference"] > 0 and
                comparison[n]["direct"]["score"] >= .5]
    selected = max(eligible, key=lambda n: (comparison[n]["paired_pool"]["difference"],
                                      n == "reserve_300")) if eligible else None
    population.write_json(out / "screen-comparison.json", {"comparison": comparison,
                          "selected_for_fresh_followup": selected, "selection_is_promotion": False})
    print(json.dumps({"comparison": comparison, "selected_for_fresh_followup": selected}, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", nargs="?", type=Path)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--screen", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if args.prepare:
        prepare()
    elif args.screen and args.experiment:
        screen(args.experiment, args.workers)
    else:
        parser.error("choose --prepare or an experiment path with --screen")
