"""Finite synthetic evaluator runtime probes, not match or worst-case claims."""

import argparse
import json
import os
from pathlib import Path

from . import population
from .match import InProcessBot
from .paths import bot_hash, file_hash


def inputs():
    """Valid local two-cell bodies; food/wall patterns deliberately synthetic."""
    rows = []
    for crowded in (False, True):
        for food in ("none", "present", "imminent", "far"):
            bodies = ["A 0 3 3 N 1", "A 0 3 4 N 0"]
            if crowded:
                # Twelve visible two-cell dragons, kept away from the three
                # immediate choices. Alternate teams; no overlapping bodies.
                did = 1
                for y in (0, 1, 5, 6):
                    for x in (0, 2, 4):
                        team = "A" if did % 2 == 0 else "B"
                        bodies += [f"{team} {did} {x} {y} W 1",
                                   f"{team} {did} {x + 1} {y} W 0"]
                        did += 1
            occupied = {(int(s.split()[2]), int(s.split()[3])) for s in bodies}
            block = ["ROUND 499", "DIR N", "LENGTH 2",
                     f"UNIT_COUNT {7 if crowded else 1}", "NUM_MSGS 0"]
            for k in range(49):
                x, y = k % 7, k // 7
                pearl = int(food == "present" and (x, y) not in occupied)
                timer = {"none": -1, "present": 15, "imminent": 0, "far": 500}[food]
                block.append(f"{x} {y} {pearl} {timer}")
            block += [f"DRAGON_BODIES {len(bodies)}", *bodies]
            block += [". . . . . . ."] * 8 + [". . . . . . . ."] * 7
            rows.append({"category": ("crowded_" if crowded else "open_") + food,
                         "init": "ID 0\nTEAM A\nMAP 32 32\nUNIT_LIMIT 64\n",
                         "block": "\n".join(block) + "\n"})
    return rows


def run(out):
    os.environ["UNSWBC_WARM"] = "1"
    from unswbc.sandbox import SandboxPool, SandboxBot
    probes = inputs()
    selection = json.loads((out / "evaluators-selection.json").read_text())
    rows = []
    for name in ("linear", "neural"):
        path = out / "bots" / name
        expected = bot_hash(path)
        if name == selection["selected"]:
            assert expected == selection["hash"]
        loader = InProcessBot(path)
        pool = SandboxPool(["python", "main.py"], cwd=str(path.resolve()), key="a")
        try:
            for sample in probes:
                native = loader.new_brain(sample["init"], 0)
                bc = native.turn.__func__.__globals__["bc"]
                obs = bc.Obs(sample["block"])
                expected_action = native.turn(obs)
                bot = SandboxBot(pool, init=sample["init"].encode(), name="0")
                try:
                    for phase in ("cold", "repeated"):
                        output = bot.ask(sample["block"].encode()).decode()
                        points, memory = bot.live
                        row = {"bot": name, "hash": expected, "category": sample["category"],
                               "phase": phase, "points": points, "memory_bytes": memory,
                               "error": bot.error, "output": output,
                               "expected_action": expected_action,
                               "action_matches": output.splitlines()[0] == expected_action if output else False}
                        rows.append(row)
                        print(json.dumps(row), flush=True)
                        if bot.error:
                            break
                finally:
                    bot.stop()
        finally:
            pool.close()
        assert bot_hash(path) == expected
    population.write_json(out / "synthetic-stress.json", {
        "source_hash": file_hash(Path(__file__)), "inputs": probes, "rows": rows,
        "limits": "Synthetic local observations and repeated identical blocks, not trajectories, "
                  "strength estimates, or a worst-case bound. No policy modifications."})
    assert len(rows) == 32
    assert all(not r["error"] and r["action_matches"] and "LOG crash " not in r["output"] and
               r["points"] < 100000000 and r["memory_bytes"] < 48 * 2**20 for r in rows)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("experiment", type=Path)
    run(p.parse_args().experiment)
