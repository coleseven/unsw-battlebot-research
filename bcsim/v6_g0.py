"""Freeze and evaluate hand-default v6 on G0's five hardest maps.

This is a diagnostic architecture gate, not a full bot-change promotion test.
Only a passing architecture proceeds to all eleven maps and tuning.
"""

import argparse
import json
import shutil
import statistics
import uuid
from datetime import datetime
from pathlib import Path

from . import analyze, guarded, margin, official_suite, population, replay, v6_initial
from .paths import ROOT, RESULTS, bot_hash, file_hash

BASELINE = RESULTS / "20260924-233609-full-change-bb86e5"
NICKED = ROOT / "sparring/nicked"
NAMES = {"default_small", "Devil", "queen_of_spades", "trophy", "big_empty"}


def prepare(workers=6):
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") +
                     "-v6-g0-" + uuid.uuid4().hex[:6])
    out.mkdir()
    v6_initial.variant(out / "bots/v6")
    population.snapshot(NICKED, out / "bots/nicked")
    (out / "maps").mkdir()
    maps = []
    for source in official_suite.official_maps():
        if source.stem in NAMES:
            dest = out / "maps" / source.name
            shutil.copy2(source, dest)
            maps.append(str(dest))
    if len(maps) != 5:
        raise ValueError("missing G0 map")
    sources = [ROOT / path for path in (
        "framework/core_params.py", "framework/core_memory.py",
        "framework/core_search.py", "framework/core_split.py",
        "framework/core_king.py", "experiments/v6/brain.py",
        "bcsim/v6_initial.py", "bcsim/v6_g0.py")]
    population.write_json(out / "plan.json", {
        "question": "Does the hand-default v6 core improve G0 trajectory margin by 0.15?",
        "scope": "Diagnostic G0 only; full eleven-map suite required before promotion.",
        "seed": 61001, "workers": workers,
        "v6_hash": bot_hash(out / "bots/v6"),
        "nicked_hash": bot_hash(out / "bots/nicked"),
        "baseline_hash": bot_hash(BASELINE / "bots/candidate"),
        "live_hash": bot_hash(ROOT / "mybot"),
        "maps": maps, "map_hashes": {path: file_hash(Path(path)) for path in maps},
        "source_hashes": {str(path.relative_to(ROOT)): file_hash(path)
                          for path in sources},
    })
    print(out, flush=True)


def screen(out):
    plan = json.loads((out / "plan.json").read_text())
    assert bot_hash(out / "bots/v6") == plan["v6_hash"]
    assert bot_hash(out / "bots/nicked") == plan["nicked_hash"]
    assert bot_hash(BASELINE / "bots/candidate") == plan["baseline_hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    for path, expected in plan["map_hashes"].items():
        assert file_hash(Path(path)) == expected
    for path, expected in plan["source_hashes"].items():
        assert file_hash(ROOT / path) == expected
    games = guarded.stage(out, "g0", [out / "bots/v6"],
                          [out / "bots/nicked"], [Path(p) for p in plan["maps"]],
                          [plan["seed"]], plan["workers"], True)
    rows = []
    crashes = fallback = turns = 0
    for game in games:
        side_a = game["bot_a"] == "v6"
        side = "A" if side_a else "B"
        old = BASELINE / "full/replays" / (
            ("candidate-vs-nicked" if side_a else "nicked-vs-candidate") +
            f"-{game['map']}-s53001.replay")
        stats = analyze.load_stats(("file", str(ROOT / game["replay"]), None))
        old_stats = analyze.load_stats(("file", str(old), None))
        raw = replay.load(ROOT / game["replay"])
        crashes += sum(ev[0] == replay.DRAGON_LOG and "crash " in ev[2]
                       for ev in raw.events)
        fallback += sum(ev[0] == replay.DRAGON_LOG and "V6_HARD_FALLBACK" in ev[2]
                        for ev in raw.events)
        turns += sum(ev[0] == replay.DRAGON_ACTION for ev in raw.events)
        rows.append({"map": game["map"], "side": side,
                     "v6": margin.game_margin(stats, side),
                     "v5": margin.game_margin(old_stats, side),
                     "winner": game["winner"], "error": game["error"]})
    new_mean = statistics.fmean(row["v6"]["margin"] for row in rows)
    old_mean = statistics.fmean(row["v5"]["margin"] for row in rows)
    result = {"games": len(rows), "v6_mean": new_mean, "v5_mean": old_mean,
              "delta": new_mean - old_mean,
              "g0_pass": new_mean - old_mean >= 0.15 and not crashes and
                         not any(row["error"] for row in rows),
              "wins": sum(row["winner"] == row["side"] for row in rows),
              "crash_logs": crashes, "hard_fallback_logs": fallback,
              "observed_action_events": turns, "detail": rows}
    population.write_json(out / "comparison.json", result)
    print(json.dumps({k: v for k, v in result.items() if k != "detail"}, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", nargs="?", type=Path)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--screen", action="store_true")
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    if args.prepare:
        prepare(args.workers)
    elif args.screen and args.result:
        screen(args.result)
    else:
        parser.error("choose --prepare or RESULT_DIR --screen")
