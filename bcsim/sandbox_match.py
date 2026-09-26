"""Meter one candidate for a COMPLETE real-engine game against a frozen bot.

Only the candidate is sandboxed; the opponent uses the existing in-process
harness. This is a runtime integration test, not paired strength evidence.
"""

import argparse
import json
import os
import time
from pathlib import Path

from . import population, replay
from .match import InProcessBot, _InProcDragon, _seed_for, engine
from .paths import bot_hash, file_hash


def intentional_empty(output: bytes) -> bool:
    """The sandbox framer strips ENDTURN but preserves the empty action line."""
    return output.startswith(b"\n")


def run(candidate, opponent, mapfile, out, side="A"):
    if side not in ("A", "B"):
        raise ValueError("side must be A or B")
    if out.exists() or out.with_suffix(".replay").exists():
        raise ValueError("refusing to overwrite sandbox artifacts")
    out.parent.mkdir(parents=True, exist_ok=True)
    os.environ["UNSWBC_WARM"] = "1"
    os.environ["RAYON_NUM_THREADS"] = "1"
    import psutil
    from unswbc.sandbox import SandboxPool, SandboxBot
    psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if os.name == "nt" else 5)
    pool = SandboxPool(["python", "main.py"], cwd=str(candidate.resolve()), team=side.lower())
    loader = InProcessBot(opponent)
    live, teams, rows, errors, deaths, notices = {}, {}, [], [], [], []
    empty_turns = set()
    started = time.monotonic()
    max_rss, next_progress, hard_fallbacks = 0, 0, 0

    def spawn(did, init):
        team = "B" if "\nTEAM B" in "\n" + init.decode() else "A"
        teams[did] = team
        live[did] = (SandboxBot(pool, init=init, name=str(did)) if team == side else
                     _InProcDragon(loader.new_brain(init.decode(), _seed_for(12000, team, did))))

    def reply(did, block):
        nonlocal max_rss, next_progress, hard_fallbacks
        bot = live[did]
        output = bot.ask(block)
        rnd = int(block.splitlines()[0].split()[1])
        if bot.error or b"LOG crash " in output:
            errors.append({"round": rnd, "id": did, "error": bot.error, "output": output.decode()})
        if teams[did] == side:
            hard_fallbacks += b"V6_HARD_FALLBACK" in output
            if not bot.error and intentional_empty(output):
                empty_turns.add((did, rnd))
            points, memory = bot.live
            rows.append({"round": rnd, "id": did, "points": points, "memory_bytes": memory})
        if rnd >= next_progress:
            rss = psutil.Process().memory_info().rss
            max_rss = max(max_rss, rss)
            if psutil.virtual_memory().available < 4 * 2**30 or rss > 4 * 2**30:
                raise RuntimeError("sandbox match resource guard")
            print(f"sandbox round {rnd}, {len(rows)} metered turns, {len(live)} living dragons, "
                  f"{time.monotonic() - started:.0f}s, {rss // 2**20} MiB RSS", flush=True)
            next_progress = rnd + 50
        return output

    def death(did, rnd, why):
        deaths.append({"round": rnd, "id": did, "team": teams[did], "reason": why})
        bot = live.pop(did, None)
        if bot:
            bot.stop()

    exception = None
    try:
        engine().run(mapfile.read_bytes(), reply, death, spawn, notices.append, 1)
        blob = engine().replay(candidate.name, opponent.name)
        out.with_suffix(".replay").write_bytes(blob)
        final = replay.read_result(blob)
    except Exception as exc:
        final = None
        exception = f"{type(exc).__name__}: {exc}"
    finally:
        for bot in live.values():
            bot.stop()
        pool.close()
        loader.close()
    points = sorted(r["points"] for r in rows)
    metrics = {"turns": len(rows), "max_points": max(points, default=0),
               "p50_points": points[len(points) // 2] if points else 0,
               "p99_points": points[min(len(points) - 1, int(len(points) * .99))] if points else 0,
               "max_memory_bytes": max((r["memory_bytes"] for r in rows), default=0),
               "first_turn_max_points": max((r["points"] for r in rows
                                             if r["round"] == 0), default=0),
               "hard_fallback_logs": hard_fallbacks,
               "sampled_host_rss_bytes": max_rss, "seconds": time.monotonic() - started}
    intentional_feed_deaths = [d for d in deaths if d["team"] == side and
                               d["reason"] == "A" and
                               (d["id"], d["round"]) in empty_turns]
    invalid_action_deaths = [d for d in deaths if d["team"] == side and
                             d["reason"] == "A" and
                             (d["id"], d["round"]) not in empty_turns]
    result = {"candidate": str(candidate), "hash": bot_hash(candidate), "side": side,
              "opponent": str(opponent),
              "opponent_hash": bot_hash(opponent), "map": str(mapfile), "map_hash": file_hash(mapfile),
              "metrics": metrics, "errors": errors, "exception": exception, "notices": notices,
              "deaths": deaths, "final": final, "turns": rows,
              "intentional_feed_deaths": intentional_feed_deaths,
              "invalid_action_deaths": invalid_action_deaths,
              "limits": "One full-game runtime test. Only candidate uses judge sandbox; "
                        "opponent is in-process. Not same-seed strength evaluation or a worst-case guarantee."}
    population.write_json(out, result)
    print(json.dumps({"metrics": metrics, "errors": errors, "exception": exception, "final": final}, indent=2), flush=True)
    if exception or errors or invalid_action_deaths:
        raise SystemExit("sandbox game failed; artifacts saved")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("candidate", type=Path)
    p.add_argument("opponent", type=Path)
    p.add_argument("map", type=Path)
    p.add_argument("out", type=Path)
    p.add_argument("--side", choices=("A", "B"), default="A")
    args = p.parse_args()
    run(args.candidate, args.opponent, args.map, args.out, args.side)
