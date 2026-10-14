import os
from pathlib import Path
os.environ["BCSIM_DETERMINISTIC_V6"] = "1"; os.environ["BCSIM_CPP_INPROC"] = "1"
from bcsim import bounded, official_suite, population
if __name__ == "__main__":
    maps = [m for m in official_suite.ranked_maps() if m.stem in ("Prisoners_Dilemma", "Portals", "queen_of_spades", "Trauma", "Autarky")]
    bots = [Path(f"results/{n}-bot") for n in ("v8-book", "v8-age", "v8-vor", "v8-trap", "v8-all")] + [Path("versions/v7-base")]
    jobs = population.jobs_for(bots, [Path("sparring/cpp_nicked_v75")], maps, [93001, 93002])
    games = bounded.run(jobs, 12, Path("results/v8-sanity"), "sanity")
    for b in bots:
        rows = [g for g in games if b.name in (g["bot_a"], g["bot_b"])]
        err = sum(bool(g.get("error")) for g in rows)
        per = {}
        for g in rows:
            s = "A" if g["bot_a"] == b.name else "B"; per.setdefault(g["map"], [0, 0]); per[g["map"]][0] += g["winner"] == s; per[g["map"]][1] += 1
        print(f"{b.name:10} vs nicked v75: {sum(v[0] for v in per.values())}/{len(rows)} errors {err}  " + " ".join(f"{m[:8]}:{a}/{n}" for m, (a, n) in per.items()))
