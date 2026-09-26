"""Strict complete-replay verification and stateful sandbox probes for hybrids."""

import argparse
import json
import os
from pathlib import Path

from . import arena, audit_jobs, fission_audit, population, reconstruct, replay
from .paths import ROOT, bot_hash


def one_game(args):
    if not args[1]:
        return fission_audit.one_game(args)
    name = Path(args[1]).name
    def observe(brain, obs, actual, turn, counts):
        counts[name + "_turns"] += 1
        counts[name + "_preserve_turns"] += brain.role.preserving
        counts[name + "_preserved_split_opportunities"] += (
            brain.role.preserving and obs.round < 450 and obs.length >= 4 and obs.unit_count < 64)
    counts, samples = fission_audit.one_game(args, observer=observe)
    return counts, {name + "__" + k: {"bot": name, **s} for k, s in samples.items()}


def audit(out, stage, workers):
    plan = json.loads((out / "plan.json").read_text())
    assert bot_hash(ROOT / "versions/v2") == plan["baseline_hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    games = [json.loads(l) for l in (out / stage / "games.jsonl").read_text().splitlines()]
    prov = json.loads((out / stage / "run.json").read_text())
    assert not arena.check_hashes(games, prov)
    if stage == "validation":
        names = [json.loads((out / f"{family}-selection.json").read_text())["selected"]
                 for family in ("roles", "evaluators")]
        names = [n for n in names if n]
        expected = (len(names) + 1) * 3 * len(plan["maps"]) * len(plan["validation_seeds"]) * 2
    else:
        names = json.loads((out / (stage.replace("-screen", "") + "-selection.json")).read_text())["names"]
        expected = (len(names) + 1) * len(plan["maps"]) * len(plan["screen_seeds"]) * 2
    assert len(games) == expected and not any(arena.is_error(g) for g in games)
    assert len({(g["map"], g["seed"], g["bot_a"], g["bot_b"]) for g in games}) == expected
    maps = {Path(p).stem: p for p in plan["maps"]}
    tasks = []
    for g in games:
        name = next((n for n in names if n in (g["bot_a"], g["bot_b"])), None)
        tasks.append((g, str(out / "bots" / name) if name else None, maps[g["map"]]))
    folder = out / stage / "audit"
    folder.mkdir(exist_ok=True)
    counts, samples = audit_jobs.run(tasks, workers, folder, one_game, "hybrid audit")
    assert counts["late_splits"] == 0
    population.write_json(folder / "replay-audit.json", {"counts": dict(counts), "samples": samples,
                                                       "hashes": {n: bot_hash(out / "bots" / n) for n in names}})
    print(json.dumps(dict(counts), indent=2), flush=True)


def budget(out, stage):
    os.environ["UNSWBC_WARM"] = "1"
    from unswbc.sandbox import SandboxPool, SandboxBot
    folder = out / stage / "audit"
    record = json.loads((folder / "replay-audit.json").read_text())
    rows = []
    for name, expected_hash in record["hashes"].items():
        path = out / "bots" / name
        assert bot_hash(path) == expected_hash
        pool = SandboxPool(["python", "main.py"], cwd=str(path.resolve()), key="a")
        try:
            for category, sample in record["samples"].items():
                if sample["bot"] != name:
                    continue
                history = []
                for t in reconstruct.turns(replay.load(sample["source"])):
                    if t.id == sample["id"]:
                        history.append(t)
                        if t.round == sample["round"]:
                            break
                assert history and history[-1].block == sample["block"]
                bot = SandboxBot(pool, init=sample["init"].encode(), name=str(sample["id"]))
                points, memory, errors = [], [], []
                try:
                    for t in history:
                        output = bot.ask(t.block.encode()).decode()
                        cpu, ram = bot.live
                        points.append(cpu); memory.append(ram)
                        if bot.error or "LOG crash " in output or not output.startswith(("MOVE ", "SPLIT ")):
                            errors.append({"round": t.round, "error": bot.error, "output": output})
                            break
                finally:
                    bot.stop()
                row = {"bot": name, "category": category, "history_turns": len(history),
                       "measured_turns": len(points), "max_points": max(points),
                       "max_memory_bytes": max(memory), "errors": errors}
                rows.append(row)
                print(json.dumps(row), flush=True)
        finally:
            pool.close()
    population.write_json(folder / "history-budget.json", {"probes": rows,
        "limits": "Recorded observation prefixes, not counterfactual match outcomes or worst-case guarantees."})
    assert rows and all(not r["errors"] and r["max_points"] < 100000000 and
                        r["max_memory_bytes"] < 48*2**20 for r in rows)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("experiment", type=Path)
    p.add_argument("--stage", choices=("roles-screen", "evaluators-screen", "validation"), required=True)
    p.add_argument("--workers", type=int, default=6)
    p.add_argument("--budget", action="store_true")
    args = p.parse_args()
    if args.budget:
        budget(args.experiment, args.stage)
    else:
        audit(args.experiment, args.stage, args.workers)
