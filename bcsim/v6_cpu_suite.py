"""Resumable 11-map, both-side judge-sandbox release CPU screen.

Prepare: python -m bcsim.v6_cpu_suite --prepare --candidate BOT --opponent BOT
Run:     python -m bcsim.v6_cpu_suite RESULT_DIR --run

Each game uses a fresh sandbox_match process; frozen bot/map hashes are checked
before every run. Completed per-game artifacts are preserved on resume.
"""

import argparse
import importlib.metadata
import json
import subprocess
import sys
import uuid
from datetime import datetime
from pathlib import Path

from . import official_suite, population, replay, sandbox_match
from .paths import RESULTS, ROOT, bot_hash, file_hash, resolve_bot


def prepare(candidate, opponent):
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") +
                     "-v6-cpu-" + uuid.uuid4().hex[:6])
    out.mkdir()
    population.snapshot(candidate, out / "bots/candidate")
    population.snapshot(opponent, out / "bots/opponent")
    maps_dir = out / "maps"
    maps_dir.mkdir()
    maps = []
    for source in official_suite.official_maps():
        dest = maps_dir / source.name
        dest.write_bytes(source.read_bytes())
        maps.append(dest)
    official_suite.require_coverage(maps)
    population.write_json(out / "plan.json", {
        "candidate_source": str(candidate), "opponent_source": str(opponent),
        "candidate_hash": bot_hash(out / "bots/candidate"),
        "opponent_hash": bot_hash(out / "bots/opponent"),
        "maps": {p.stem: file_hash(p) for p in maps},
        "sandbox_match_hash": file_hash(Path(sandbox_match.__file__)),
        "toolkit_version": importlib.metadata.version("unswbc"),
        "sides": ["A", "B"], "games": len(maps) * 2,
        "gate": "zero CPU/invalid-action errors; max<=90M per game; "
                "post-65M work<=25M per game"})
    print(out, flush=True)


def verify(out, plan):
    if bot_hash(out / "bots/candidate") != plan["candidate_hash"]:
        raise ValueError("candidate snapshot changed")
    if bot_hash(out / "bots/opponent") != plan["opponent_hash"]:
        raise ValueError("opponent snapshot changed")
    if file_hash(Path(sandbox_match.__file__)) != plan["sandbox_match_hash"]:
        raise ValueError("sandbox harness changed")
    if importlib.metadata.version("unswbc") != plan["toolkit_version"]:
        raise ValueError("toolkit version changed")
    for name, expected in plan["maps"].items():
        if file_hash(out / "maps" / f"{name}.map") != expected:
            raise ValueError(f"map {name} changed")


def report(out, plan):
    rows = []
    for name in plan["maps"]:
        for side in plan["sides"]:
            path = out / "games" / f"{name}-{side}.json"
            if not path.exists():
                continue
            game = json.loads(path.read_text(encoding="utf8"))
            if game["hash"] != plan["candidate_hash"] or game["side"] != side:
                raise ValueError(f"bad game artifact: {path}")
            logs = None
            replay_path = path.with_suffix(".replay")
            if replay_path.exists():
                raw = replay.load(replay_path)
                logs = sum(ev[0] == replay.DRAGON_LOG and
                           "V6_SOFT_CUTOFF" in ev[2] for ev in raw.events)
            m = game["metrics"]
            rows.append({"map": name, "side": side, "max_points": m["max_points"],
                         "p99_points": m["p99_points"],
                         "first_turn_max_points": m.get("first_turn_max_points"),
                         "soft_guard_logs": logs,
                         "hard_fallback_logs": m.get("hard_fallback_logs"),
                         "cpu_or_bot_errors": len(game["errors"]),
                         "invalid_action_deaths": len(game["invalid_action_deaths"]),
                         "intentional_feed_deaths": len(game["intentional_feed_deaths"]),
                         "exception": game["exception"]})
    result = {"games_done": len(rows), "games_expected": plan["games"],
              "pass": len(rows) == plan["games"] and all(
                  not r["cpu_or_bot_errors"] and not r["invalid_action_deaths"] and
                  not r["exception"] and r["max_points"] <= 90_000_000 and
                  r["max_points"] - 65_000_000 <= 25_000_000 for r in rows),
              "rows": rows}
    # rewritten after every game, so overwrite rather than create-once
    tmp = out / "summary.json.tmp"
    tmp.write_text(json.dumps(result, indent=2) + chr(10), encoding="utf8")
    tmp.replace(out / "summary.json")
    return result


def run(out):
    plan = json.loads((out / "plan.json").read_text(encoding="utf8"))
    verify(out, plan)
    (out / "games").mkdir(exist_ok=True)
    for name in plan["maps"]:
        for side in plan["sides"]:
            path = out / "games" / f"{name}-{side}.json"
            if path.exists():
                print(f"skip {name} {side}", flush=True)
                continue
            print(f"start {name} {side}", flush=True)
            command = [sys.executable, "-m", "bcsim.sandbox_match",
                       str(out / "bots/candidate"), str(out / "bots/opponent"),
                       str(out / "maps" / f"{name}.map"), str(path),
                       "--side", side]
            completed = subprocess.run(command, cwd=ROOT, check=False)
            if not path.exists():
                raise RuntimeError(f"sandbox game failed without artifact: {name} {side} "
                                   f"exit {completed.returncode}")
            result = report(out, plan)
            print(f"done {result['games_done']}/{plan['games']} pass_so_far="
                  f"{all(not r['cpu_or_bot_errors'] and not r['invalid_action_deaths'] and not r['exception'] and r['max_points'] <= 90_000_000 for r in result['rows'])}",
                  flush=True)
    print(json.dumps(report(out, plan), indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", nargs="?", type=Path)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--candidate", type=str)
    parser.add_argument("--opponent", type=str)
    args = parser.parse_args()
    if args.prepare and args.candidate and args.opponent:
        prepare(resolve_bot(args.candidate), resolve_bot(args.opponent))
    elif args.run and args.result:
        run(args.result)
    else:
        parser.error("prepare requires --candidate/--opponent; run requires result")
