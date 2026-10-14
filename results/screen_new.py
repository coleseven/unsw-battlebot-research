import json, os, sys
from pathlib import Path
os.environ["BCSIM_DETERMINISTIC_V6"] = "1"; os.environ["BCSIM_CPP_INPROC"] = "1"
from bcsim import bounded, official_suite, population
if __name__ == "__main__":
    out = Path(sys.argv[1]); bots = [Path(b) for b in sys.argv[2:]]
    maps = official_suite.current_pool_maps()
    jobs = population.jobs_for(bots, [Path("versions/v7-base")], maps, [91001, 91002])
    games = bounded.run(jobs, 10, out, "screen")
    res = {}
    for g in games:
        for b in bots:
            if b.name in (g["bot_a"], g["bot_b"]):
                s = "A" if g["bot_a"] == b.name else "B"
                r = res.setdefault(b.name, {"w": 0, "n": 0, "err": 0, "maps": {}})
                r["n"] += 1; r["w"] += g["winner"] == s; r["err"] += bool(g.get("error"))
                m = r["maps"].setdefault(g["map"], [0, 0]); m[0] += g["winner"] == s; m[1] += 1
    for k, r in sorted(res.items(), key=lambda kv: -kv[1]["w"]):
        print(f"{k:16} wins vs v7-base {r['w']}/{r['n']} errors {r['err']}  ", " ".join(f"{m[:6]}:{a}/{b}" for m, (a, b) in r["maps"].items()))
