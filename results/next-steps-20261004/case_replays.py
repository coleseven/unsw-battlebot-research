"""Replay the 24 selected C10-base games deterministically, keeping replays, and
check each reproduces its recorded winner."""
import json
from pathlib import Path
from bcsim import queen_runtime

if __name__ == "__main__":
    queen_runtime.activate()
    from bcsim import bounded
    RUN = Path("results/20261003-224713-ablate-d440c5")
    out = Path("results/next-steps-20261004/cases")
    cases = json.load(open("results/next-steps-20261004/selected_cases.json"))
    base = str(RUN / "variants/base")
    jobs = []
    for c in cases:
        opp = str(RUN / "opponents" / c["opponent"])
        a, b = (base, opp) if c["side"] == "A" else (opp, base)
        jobs.append((str(RUN / "maps" / f"{c['map']}.map"), a, b, c["seed"], str(out / "replays"), [c["opponent"], c["map"], c["seed"]]))
    games = bounded.run(jobs, 12, out, "case replays")
    rec = {(g["map"], g["bot_a"], g["bot_b"], g["seed"]): g["winner"] for g in map(json.loads, open(RUN / "runs/base/games.jsonl"))}
    same = sum(rec.get((g["map"], g["bot_a"], g["bot_b"], g["seed"])) == g["winner"] for g in games)
    print(f"replayed {len(games)}, same winner as recorded {same}", flush=True)
