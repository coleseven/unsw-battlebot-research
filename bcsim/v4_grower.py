"""Independent growth-role screen; v3 movement, no safety guard."""

import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import guarded, population
from .paths import ROOT, RESULTS, bot_hash, file_hash, foreign_imports, map_signature

BASE = ROOT / "versions/v3"
MODES = ("mature", "opportunity")
MAPS = ("default_small", "default", "queen_of_spades", "Trauma")
OPPONENTS = ("ctmes", "nicked")


def make_candidate(dest, mode):
    population.snapshot(BASE, dest)
    (dest / "brain.py").rename(dest / "v3_brain.py")
    shutil.copy2(ROOT / "experiments/v4/grower_brain.py", dest / "brain.py")
    (dest / "grower_config.py").write_text(f"MODE = {mode!r}\n", encoding="utf8")
    assert not foreign_imports(dest)
    return dest


def prepare():
    assert bot_hash(BASE) == "69382825b699723d"
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-v4-grower-" + uuid.uuid4().hex[:6])
    out.mkdir()
    for name in ("control_v3", "reference_v3"):
        population.snapshot(BASE, out / "bots" / name)
    for mode in MODES:
        make_candidate(out / "bots" / mode, mode)
    for name in OPPONENTS:
        population.snapshot(ROOT / "sparring" / name, out / "bots" / name)
    source = json.loads((RESULTS / "20260924-113203-v4-abbee0/plan.json").read_text())
    (out / "maps").mkdir()
    maps = []
    for name in source["maps"]:
        p = Path(name)
        if p.stem.split("_")[0] not in MAPS and not any(p.name.startswith(x + "_") for x in MAPS):
            continue
        dest = out / "maps" / p.name
        shutil.copy2(p, dest)
        maps.append(str(dest))
    assert len(maps) == len({map_signature(Path(p)) for p in maps}) == 4
    plan = {
        "question": "Can v2's hysteretic grower roles help when v3 movement is kept intact?",
        "baseline_hash": bot_hash(BASE), "live_hash": bot_hash(ROOT / "mybot"),
        "candidate_hashes": {n: bot_hash(out / "bots" / n) for n in MODES},
        "opponent_hashes": {n: bot_hash(out / "bots" / n) for n in OPPONENTS},
        "maps": maps, "map_hashes": {p: file_hash(Path(p)) for p in maps},
        "screen_seed": 42000, "direct_seed": 42000,
        "screen_games": 3 * 2 * len(maps) * 2,
        "direct_games": 2 * len(maps) * 2,
        "selection": "Exploratory: positive paired gain over v3 against both stronger opponents "
                     "and at least 50% direct v3 score; choose larger paired gain.",
        "future_gate": "Fresh layouts and opponent versions with positive map-cluster lower bound, "
                       "exact replay audit and sandbox budget before v4 freeze.",
        "limits": "Only four familiar maps and one seed; competitors are pinned local source "
                  "snapshots, not the live ladder. The grower-role thresholds were imported unchanged "
                  "from the earlier v2 ablation. No opponent code is copied into candidates.",
        "source_hashes": {str(p.relative_to(ROOT)): file_hash(p) for p in
                          (ROOT / "experiments/v4/grower_brain.py", ROOT / "bcsim/v4_grower.py")},
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
    maps = [Path(p) for p in plan["maps"]]
    bots = out / "bots"
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
    selected = max(eligible, key=lambda n: comparison[n]["paired_pool"]["difference"]) if eligible else None
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
