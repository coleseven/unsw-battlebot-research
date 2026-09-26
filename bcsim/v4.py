"""Isolated v4 teammate-head safety ablations against frozen v3."""

import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import arena, guarded, population
from .paths import ROOT, RESULTS, bot_hash, file_hash, foreign_imports, map_signature

BASE = ROOT / "versions/v3"
HYBRID = RESULTS / "20260923-231438-hybrid-b0801d"
MODES = {"guard_all": False, "guard_later": True}


def make_candidate(destination, later_only):
    population.snapshot(BASE, destination)
    (destination / "brain.py").rename(destination / "v3_brain.py")
    shutil.copy2(ROOT / "experiments/v4/brain.py", destination / "brain.py")
    shutil.copy2(ROOT / "framework/v4_safety.py", destination / "v4_safety.py")
    (destination / "v4_config.py").write_text(f"LATER_ONLY = {later_only!r}\n", encoding="utf8")
    assert not foreign_imports(destination)
    return destination


def prepare():
    assert bot_hash(BASE) == "69382825b699723d"
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-v4-" + uuid.uuid4().hex[:6])
    out.mkdir()
    for name in ("control_v3", "reference_v3"):
        population.snapshot(BASE, out / "bots" / name)
    for name, later_only in MODES.items():
        make_candidate(out / "bots" / name, later_only)
    for name in ("splitter", "hunter"):
        population.snapshot(HYBRID / "bots" / name, out / "bots" / name)
    source = json.loads((HYBRID / "plan.json").read_text())
    (out / "maps").mkdir()
    maps = []
    for name in source["maps"]:
        path = Path(name)
        dest = out / "maps" / path.name
        shutil.copy2(path, dest)
        maps.append(str(dest))
    assert len(maps) == len({map_signature(Path(p)) for p in maps}) == 11
    plan = {
        "question": "Does a hard visible teammate-head guard improve frozen v3 movement?",
        "baseline_hash": bot_hash(BASE),
        "live_hash": bot_hash(ROOT / "mybot"),
        "candidate_hashes": {n: bot_hash(out / "bots" / n) for n in MODES},
        "opponent_hashes": {n: bot_hash(out / "bots" / n) for n in ("splitter", "hunter")},
        "maps": maps,
        "map_hashes": {p: file_hash(Path(p)) for p in maps},
        "modes": MODES,
        "screen_seeds": [41000, 41001],
        "direct_seed": 41000,
        "screen_games": 3 * 2 * len(maps) * 2 * 2,
        "direct_games": 2 * len(maps) * 2,
        "selection": "Among modes with positive paired pool score versus control and direct score "
                     "at least 50% versus v3, choose larger paired gain. Screen is exploratory. "
                     "Direct v3 games use one seed because both bots are deterministic.",
        "future_gate": "Fresh opponents and layouts, map-cluster 95% paired-gain lower bound > 0, "
                       "plus exact replay and judge-sandbox budget checks before any v4 freeze.",
        "limits": "The 11 maps are familiar. Split logic and linear weights are unchanged. "
                  "All-threatened move states fall back to the original v3 candidates. "
                  "No competitor source is copied into a candidate.",
        "source_hashes": {str(p.relative_to(ROOT)): file_hash(p) for p in
                          (ROOT / "experiments/v4/brain.py", ROOT / "framework/v4_safety.py",
                           ROOT / "bcsim/v4.py")},
    }
    population.write_json(out / "plan.json", plan)
    print(out, flush=True)


def screen(out, workers):
    plan = json.loads((out / "plan.json").read_text())
    assert bot_hash(BASE) == plan["baseline_hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    for name, expected in plan["candidate_hashes"].items():
        assert bot_hash(out / "bots" / name) == expected
    for path, expected in plan["map_hashes"].items():
        assert file_hash(Path(path)) == expected
    maps = [Path(p) for p in plan["maps"]]
    bots = out / "bots"
    candidates = [bots / n for n in ("control_v3", *MODES)]
    opponents = [bots / n for n in ("splitter", "hunter")]
    pooled = guarded.stage(out, "screen-pool", candidates, opponents, maps,
                           plan["screen_seeds"], workers, True)
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
