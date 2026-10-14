import os, sys, json, time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
os.environ["BCSIM_DETERMINISTIC_V6"] = "1"

def one(args):
    mode, m, a, b, seed = args
    os.environ["BCSIM_CPP_INPROC"] = mode
    from bcsim import match
    r = match.play(Path(m), Path(a), Path(b), seed=seed)
    return mode, m, a, b, seed, r.winner, r.rounds, r.a_length, r.b_length, r.deaths, r.error, round(r.seconds, 1)

if __name__ == "__main__":
    maps = ["maps/default_small.map", "maps/Devil.map" if Path("maps/Devil.map").exists() else "maps/server/Devil.map", "maps/big_empty.map", "maps/server/Portals.map"]
    opps = ["sparring/nicked", "results/v61b-goal-bot", "versions/v7-base"]
    jobs = []
    for mode in ("0", "1"):
        for m in maps:
            for o in opps:
                jobs += [(mode, m, "results/v7-base-bot", o, 5), (mode, m, o, "results/v7-base-bot", 5)]
    out = {}
    os.environ["BCSIM_CPP_INPROC"] = "1"
    from bcsim import match
    match.prebuild(["results/v7-base-bot", "versions/v7-base"])
    for mode in ("0", "1"):
        t = time.time()
        with ProcessPoolExecutor(8) as ex:
            res = list(ex.map(one, [j for j in jobs if j[0] == mode]))
        out[mode] = (res, time.time() - t)
    same = sum(x[5:11] == y[5:11] for x, y in zip(out["0"][0], out["1"][0]))
    print("identical", same, "of", len(out["0"][0]))
    for x, y in zip(out["0"][0], out["1"][0]):
        if x[5:11] != y[5:11]: print("DIFF", x[1:5], x[5:9], y[5:9])
    for mode in ("0", "1"):
        res, wall = out[mode]
        by = {}
        for r in res:
            opp = r[3] if r[2] == "results/v7-base-bot" else r[2]
            by.setdefault(opp, []).append(r[-1])
        print("mode", mode, "wall", round(wall), "s;", {k: round(sum(v) / len(v), 1) for k, v in by.items()})
