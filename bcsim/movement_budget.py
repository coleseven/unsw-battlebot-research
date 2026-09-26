"""Sampled CPU-point probe through unswbc's actual judge Python sandbox.

Not a full sandbox match or worst-case guarantee. Every observation is tested
as a cold turn and repeated warm turn, with that dragon's correct init data.
"""

import argparse
import json
import os
from pathlib import Path

from . import replay, reconstruct, population
from .match import InProcessBot
from .paths import bot_hash


def samples(prior, experiment):
    games = [json.loads(s) for s in (prior / "holdout/games.jsonl").read_text().splitlines()]
    loader = InProcessBot(experiment / "bots/sprint")
    probe = loader.new_brain("ID 0\nTEAM A\nMAP 16 16\nUNIT_LIMIT 64\n", 0)
    helper = probe.turn.__func__.__globals__["local_safety"]
    bc = helper.bc
    chosen, seen_maps = {}, set()
    for g in games:
        if "stop_450" not in (g["bot_a"], g["bot_b"]) or g["map"] in seen_maps:
            continue
        seen_maps.add(g["map"])
        r = replay.load(g["replay"])
        board = reconstruct.Board(r.map_text)
        side = "A" if g["bot_a"] == "stop_450" else "B"
        for t in reconstruct.turns(r):
            if t.team != side:
                continue
            o = bc.Obs(t.block)
            item = {"source": g["replay"], "round": t.round, "id": t.id,
                    "init": f"ID {t.id}\nTEAM {side}\nMAP {board.w} {board.h}\nUNIT_LIMIT 64\n",
                    "block": t.block}
            values = {"long": o.length, "dense": sum(p is not None for p in o.occ),
                      "enemy_heads": len(o.enemy_heads(side))}
            for category, value in values.items():
                if category not in chosen or value > chosen[category][0]:
                    chosen[category] = (value, item)
            if o.round >= 450 or o.length < 8:
                action = helper.choose(o, side, "MOVE " + o.facing, "sprint")
                if len(action.split()[1]) == 2:
                    chosen.setdefault("sprint_trigger", (1, item))
            if o.round in (0, 100, 300, 460):
                chosen.setdefault(f"round_{o.round}", (1, item))
        if len(seen_maps) == 3:
            break
    return [{"category": category, **item} for category, (_, item) in chosen.items()]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("experiment", type=Path)
    p.add_argument("prior", type=Path)
    args = p.parse_args()
    os.environ["UNSWBC_WARM"] = "1"
    from unswbc.sandbox import SandboxPool, SandboxBot
    inputs = samples(args.prior, args.experiment)
    population.write_json(args.experiment / "budget-inputs.json", inputs)
    rows = []
    for name in ("control_450", "trap", "sprint"):
        path = args.experiment / "bots" / name
        print(f"sandbox: building {name}, {len(inputs)} cold/warm probes", flush=True)
        pool = SandboxPool(["python", "main.py"], cwd=str(path.resolve()), team="a")
        try:
            for sample in inputs:
                bot = SandboxBot(pool, init=sample["init"].encode(), name=str(sample["id"]))
                try:
                    for phase in ("cold", "warm"):
                        output = bot.ask(sample["block"].encode()).decode()
                        points, memory = bot.live
                        row = {"bot": name, "hash": bot_hash(path), "category": sample["category"],
                               "phase": phase, "points": points, "memory_bytes": memory,
                               "error": bot.error, "output": output}
                        rows.append(row)
                        print(json.dumps(row), flush=True)
                        if bot.error:
                            break
                finally:
                    bot.stop()
        finally:
            pool.close()
    summary = {}
    for name in ("control_450", "trap", "sprint"):
        r = [row for row in rows if row["bot"] == name]
        summary[name] = {"turns": len(r), "max_points": max(row["points"] for row in r),
                         "max_memory_bytes": max(row["memory_bytes"] for row in r),
                         "failures": sum(bool(row["error"]) or "crash" in row["output"] or
                                         not row["output"].startswith(("MOVE ", "SPLIT ")) for row in r)}
    population.write_json(args.experiment / "budget.json", {"summary": summary, "turns": rows,
                           "limits": "sampled observations, repeated cold/warm; not full games or a worst-case guarantee"})
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
