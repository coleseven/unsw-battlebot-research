import os
from pathlib import Path
os.environ["BCSIM_DETERMINISTIC_V6"] = "1"; os.environ["BCSIM_CPP_INPROC"] = "1"
from bcsim import bounded, official_suite, population
if __name__ == "__main__":
    out = Path("results/v10-vs-v92")
    jobs = population.jobs_for([Path("versions/v10")], [Path("sparring/cpp_nicked_v92"), Path("sparring/cpp_nicked_v75")],
                               official_suite.current_pool_maps(), [141001, 141002])
    games = bounded.run(jobs, 12, out, "v10-vs-v92")
    for opp in ("cpp_nicked_v92", "cpp_nicked_v75"):
        rows = [g for g in games if opp in (g["bot_a"], g["bot_b"])]
        w = sum(g["winner"] == ("A" if g["bot_a"] == "v10" else "B") for g in rows)
        per = {}
        for g in rows:
            s = "A" if g["bot_a"] == "v10" else "B"; per.setdefault(g["map"], [0, 0]); per[g["map"]][0] += g["winner"] == s; per[g["map"]][1] += 1
        print(f"v10 vs {opp}: {w}/{len(rows)}", {m: f"{a}/{b}" for m, (a, b) in sorted(per.items())})
