import os, json
os.environ["BCSIM_DETERMINISTIC_V6"] = "1"; os.environ["BCSIM_CPP_INPROC"] = "1"
from pathlib import Path
from collections import Counter
from bcsim import bounded, official_suite, population
if __name__ == "__main__":
    out = Path("results/sprint-baseline")
    opps = [Path(p) for p in ("sparring/cpp_nicked_v92", "sparring/cpp_nicked_v75", "sparring/cpp_leviathan3", "results/v7-base-bot", "sparring/nicked_v44", "sparring/nicked_lab")]
    jobs = population.jobs_for([Path("versions/v10h"), Path("versions/v10o")], opps, official_suite.sprint_maps(), [361001, 361002])
    games = bounded.run(jobs, 12, out, "sprint-baseline")
    for bot in ("v10h", "v10o"):
        w = Counter(); n = Counter()
        for g in games:
            if bot not in (g["bot_a"], g["bot_b"]): continue
            side = "A" if g["bot_a"] == bot else "B"; opp = g["bot_b"] if side == "A" else g["bot_a"]
            w[g["map"]] += g["winner"] == side; n[g["map"]] += 1; w[opp] += g["winner"] == side; n[opp] += 1
        print(bot, "total", sum(w[m] for m in n if m in [p.stem for p in official_suite.sprint_maps()]), "/", sum(n[m] for m in n if m in [p.stem for p in official_suite.sprint_maps()]))
        print("  ", {k: f"{w[k]}/{n[k]}" for k in n})
