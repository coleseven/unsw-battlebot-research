"""Diagnostic (Sprint maps only): does map-book use cause the unseen-map drop?"""
import os
os.environ["BCSIM_DETERMINISTIC_V6"] = "1"; os.environ["BCSIM_CPP_INPROC"] = "1"
from pathlib import Path
from collections import Counter
from bcsim import bounded, official_suite, population, mover_teacher as mt
if __name__ == "__main__":
    bots = {"base": Path("results/v10q-bot"),
            "nobookmap": mt.variant("results/v10q-bot", "nobookmap", {"CPP_BOOK_MAP": 0}),
            "nobooks": mt.variant("results/v10q-bot", "nobooks", {"CPP_BOOK_MAP": 0, "PORTAL_BOOK": "false", "HUB_BOOK": "false"})}
    opps = [Path(p) for p in ("sparring/cpp_nicked_v92", "sparring/cpp_nicked_v75", "sparring/cpp_leviathan3", "results/v7-base-bot", "sparring/nicked_v44", "sparring/nicked_lab")]
    jobs = population.jobs_for(list(bots.values()), opps, official_suite.sprint_maps(), [421001, 421002])
    games = bounded.run(jobs, 12, Path("results/unseen-books-probe"), "unseen-books")
    for name, path in bots.items():
        w = Counter(); n = Counter()
        for g in games:
            if path.name not in (g["bot_a"], g["bot_b"]): continue
            side = "A" if g["bot_a"] == path.name else "B"
            w[g["map"]] += g["winner"] == side; n[g["map"]] += 1
        print(f"{name:10} {sum(w.values())}/{sum(n.values())}", {m: f"{w[m]}/{n[m]}" for m in n}, flush=True)
