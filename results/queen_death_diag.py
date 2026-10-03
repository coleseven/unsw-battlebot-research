"""Classify how our queen died in an ablate's replays (per variant): cause, killer
side, round bucket, queen length, opponent, map. Usage: queen_death_diag.py FOLDER VARIANT"""
import json, sys
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from bcsim import analyze

def one(args):
    path, us = args
    try:
        s = analyze.game_stats(Path(path).read_bytes())
    except Exception as e:
        return None
    q = s["teams"][us]["queen"]
    if q["alive"]:
        return {"alive": True, "len": q["length"]}
    for rnd, t, why, killer, ln, age, d, other in s["deaths"]:
        if t == us and d == q["id"]:
            who = "own" if killer == us else "enemy" if killer else "-"
            return {"alive": False, "round": rnd, "why": analyze.CAUSE[why], "who": who, "len": ln}
    return None

if __name__ == "__main__":
    # FOLDER VARIANT: FOLDER/games.jsonl with kept replays (from queen_replays.py)
    A = Path(sys.argv[1]); vs = sys.argv[2:]
    for v in vs:
        rows = [json.loads(l) for l in (A / "games.jsonl").read_text().splitlines()]
        jobs = [(g["replay"], "A" if g["bot_a"] == v else "B") for g in rows]
        with ProcessPoolExecutor(4) as ex:
            res = list(ex.map(one, jobs, chunksize=8))
        c = Counter(); byopp = defaultdict(Counter); bymap = defaultdict(Counter); rb = Counter(); lens = Counter()
        for g, r in zip(rows, res):
            if r is None: c["?"] += 1; continue
            if r["alive"]: c["alive"] += 1; continue
            key = f"{r['why']}/{r['who']}"
            c[key] += 1
            opp = g["bot_b"] if g["bot_a"] == v else g["bot_a"]
            byopp[opp][key] += 1; bymap[g["map"]]["dead"] += 1
            rb[min(r["round"] // 50 * 50, 450)] += 1; lens[min(r["len"], 6)] += 1
        print(f"== {v}: {len(rows)} games")
        print("  causes:", dict(c.most_common()))
        print("  death round:", dict(sorted(rb.items())))
        print("  queen len at death:", dict(sorted(lens.items())))
        print("  deaths by map:", {m: x["dead"] for m, x in sorted(bymap.items(), key=lambda kv: -kv[1]["dead"])})
        for o, x in sorted(byopp.items()): print(f"  {o:20}", dict(x.most_common()))
