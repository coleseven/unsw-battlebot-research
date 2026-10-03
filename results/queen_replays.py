"""Replay (deterministically) the games of an ablate variant where our queen died,
keeping replays, for queen_death_diag. Usage: queen_replays.py RESULT VARIANT OUTDIR"""
from bcsim import queen_runtime
queen_runtime.activate()
import json, sys
from pathlib import Path
from bcsim import bounded

A, v, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
plan = json.loads((A / "plan.json").read_text())
jobs, rows = [], []
for l in (A / "runs" / v / "games.jsonl").read_text().splitlines():
    g = json.loads(l)
    us = "a" if g["bot_a"] == v else "b"
    if (g.get(f"{us}_queen") or 0) > 0: continue
    path = lambda n: str(A / "variants" / n) if n == v else str(A / "opponents" / n)
    jobs.append((str(A / "maps" / f"{g['map']}.map"), path(g["bot_a"]), path(g["bot_b"]), g["seed"], str(out / "replays"), g["block"]))
    rows.append(g)
print(len(jobs), "queen-death games", flush=True)
games = bounded.run(jobs, 12, out, f"queen-replays {v}")
# determinism check against the original records
orig = {(g["map"], g["bot_a"], g["bot_b"], g["seed"]): g for g in rows}
same = sum(orig.get((g["map"], g["bot_a"], g["bot_b"], g["seed"]), {}).get("winner") == g["winner"] for g in games)
print(f"replayed {len(games)}, same winner {same}", flush=True)
