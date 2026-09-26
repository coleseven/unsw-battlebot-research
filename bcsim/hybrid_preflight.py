"""Judge-metered observations, including late-game evaluator execution."""

import argparse
import json
import os
from pathlib import Path

from . import population
from .paths import ROOT, bot_hash


def run(out):
    os.environ["UNSWBC_WARM"] = "1"
    from unswbc.sandbox import SandboxPool, SandboxBot
    inputs = json.loads((ROOT / "results/20260922-173739-movement-659d1f/budget-inputs.json").read_text())
    rows = []
    for name in ("heuristic", "linear", "neural"):
        path = out / "bots" / name
        pool = SandboxPool(["python", "main.py"], cwd=str(path.resolve()), team="a")
        try:
            for sample in inputs:
                for mode in ("recorded", "force_late_movement"):
                    block = sample["block"]
                    if mode == "force_late_movement":
                        lines = block.splitlines()
                        lines[0] = "ROUND 499"
                        block = "\n".join(lines) + "\n"
                    bot = SandboxBot(pool, init=sample["init"].encode(), name=str(sample["id"]))
                    try:
                        output = bot.ask(block.encode()).decode()
                        points, memory = bot.live
                        row = {"bot": name, "hash": bot_hash(path), "category": sample["category"],
                               "mode": mode, "points": points, "memory_bytes": memory,
                               "error": bot.error, "output": output}
                        rows.append(row)
                        print(name, sample["category"], mode, points, bot.error, flush=True)
                    finally:
                        bot.stop()
        finally:
            pool.close()
    population.write_json(out / "preflight.json", {"rows": rows,
        "limits": "Finite cold-start observation probes; round-499 variants are synthetic stress inputs."})
    assert rows and all(not r["error"] and "crash" not in r["output"] and
                        r["points"] < 100000000 and r["memory_bytes"] < 48*2**20 for r in rows)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("experiment", type=Path)
    run(p.parse_args().experiment)
