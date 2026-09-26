"""Exact stateful action audit and judge probes with real observation history."""

import argparse
import json
import os
from pathlib import Path

from . import arena, audit_jobs, fission_audit, population, reconstruct, replay
from .paths import ROOT, bot_hash


def one_game(args):
    if args[1] is None:
        return fission_audit.one_game(args)
    game, botpath, _ = args
    name, samples, observed = Path(botpath).name, {}, {}

    def observe(brain, obs, actual, turn, counts):
        m = brain.memory
        counts[name + "_turns"] += 1
        counts[name + "_search_turns"] += m.expanded > 0
        counts[name + "_capped_searches"] += m.expanded == 96
        assert m.expanded <= 96
        observed.setdefault(turn.id, set()).update(m.visible)
        metrics = {"mapped_cells": len(observed[turn.id]),
                   "portal_pairs": sum(len(v) == 2 for v in m.ends.values()),
                   "food_entries": len(m.food), "search_nodes": m.expanded}
        for key, score in metrics.items():
            if key not in samples or score > samples[key]["score"]:
                samples[key] = {"score": score, "id": turn.id, "round": turn.round, "block": turn.block,
                                "init": f"ID {turn.id}\nTEAM {turn.team}\nMAP {brain.init.width} {brain.init.height}\nUNIT_LIMIT {brain.init.unit_limit}\n",
                                "source": game["replay"]}

    counts, basic = fission_audit.one_game(args, observer=observe)
    samples.update(basic)
    return counts, {name + "__" + key: {"bot": name, **value} for key, value in samples.items()}


def audit(out, stage, workers):
    os.environ["RAYON_NUM_THREADS"] = "1"
    plan = json.loads((out / "plan.json").read_text())
    for name, value in plan["candidate_hashes"].items():
        assert bot_hash(out / "bots" / name) == value
    assert bot_hash(ROOT / "versions/v2") == plan["baseline_hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    games = [json.loads(l) for l in (out / stage / "games.jsonl").read_text().splitlines()]
    expected = 216 if stage == "screen" else 864
    assert len(games) == expected and not any(arena.is_error(g) for g in games)
    assert len({(g["map"], g["seed"], g["bot_a"], g["bot_b"]) for g in games}) == expected
    assert not arena.check_hashes(games, json.loads((out / stage / "run.json").read_text()))
    maps = {Path(p).stem: p for p in plan["maps"]}
    tasks = []
    for g in games:
        candidate = next((n for n in plan["modes"] if n in (g["bot_a"], g["bot_b"])), None)
        tasks.append((g, str(out / "bots" / candidate) if candidate else None, maps[g["map"]]))
    folder = out / stage / "audit"
    folder.mkdir(exist_ok=True)
    counts, samples = audit_jobs.run(tasks, workers, folder, one_game, "navigation audit")
    assert counts["late_splits"] == 0
    population.write_json(folder / "replay-audit.json", {"counts": dict(counts), "samples": samples})
    print(json.dumps(dict(counts), indent=2), flush=True)


def budget(out, stage):
    """Cold-start each dragon, then replay its own observations up to each probe.

    Memory is observation-driven, so history restores the mapped terrain and
    food state. Judge RNG need not match arena RNG: this measures runtime, not
    paired strength. Single isolated observations would miss accumulated state.
    """
    os.environ["UNSWBC_WARM"] = "1"
    from unswbc.sandbox import SandboxPool, SandboxBot
    folder = out / stage / "audit"
    audit_result = json.loads((folder / "replay-audit.json").read_text())
    plan = json.loads((out / "plan.json").read_text())
    rows = []
    for name in plan["modes"]:
        samples = {k: v for k, v in audit_result["samples"].items() if v["bot"] == name}
        if not samples:
            continue
        path = out / "bots" / name
        assert bot_hash(path) == plan["candidate_hashes"][name]
        pool = SandboxPool(["python", "main.py"], cwd=str(path.resolve()), key="a")
        try:
            for key, sample in samples.items():
                turns = []
                for t in reconstruct.turns(replay.load(sample["source"])):
                    if t.id == sample["id"]:
                        turns.append(t)
                        if t.round == sample["round"]:
                            break
                assert turns and turns[-1].block == sample["block"]
                bot = SandboxBot(pool, init=sample["init"].encode(), name=str(sample["id"]))
                points, memory, errors = [], [], []
                try:
                    for t in turns:
                        output = bot.ask(t.block.encode()).decode()
                        cpu, ram = bot.live
                        points.append(cpu)
                        memory.append(ram)
                        if bot.error or "LOG crash " in output or not output.startswith(("MOVE ", "SPLIT ")):
                            errors.append({"round": t.round, "error": bot.error, "output": output})
                            break
                finally:
                    bot.stop()
                row = {"bot": name, "category": key, "history_turns": len(turns), "measured_turns": len(points),
                       "max_points": max(points), "max_memory_bytes": max(memory), "errors": errors,
                       "source": sample["source"], "id": sample["id"], "through_round": sample["round"]}
                rows.append(row)
                print(f"{key}: {len(points)} history turns, {row['max_points']} points, {len(errors)} errors", flush=True)
        finally:
            pool.close()
    population.write_json(folder / "history-budget.json", {"probes": rows,
                          "limits": "Recorded observation prefixes, not counterfactual full games or worst-case guarantees."})
    assert rows and all(not r["errors"] and r["max_points"] < 100000000 and
                        r["max_memory_bytes"] < 48*2**20 for r in rows)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("experiment", type=Path)
    p.add_argument("--stage", choices=("screen", "validation"), default="screen")
    p.add_argument("--workers", type=int, choices=range(1, 9), default=8)
    p.add_argument("--budget", action="store_true")
    args = p.parse_args()
    if args.budget:
        budget(args.experiment, args.stage)
    else:
        audit(args.experiment, args.stage, args.workers)
