import json, statistics as st
from collections import Counter, defaultdict
from pathlib import Path
from bcsim import analyze

if __name__ == "__main__":
    rows = [json.loads(l) for l in open("data/index.jsonl", encoding="utf8")]
    rows = [r for r in rows if 6688 in (r.get("submission_a"), r.get("submission_b")) and r["ranked"]]
    paths, side = [], {}
    for r in rows:
        s = "A" if r["submission_a"] == 6688 else "B"
        for g in r["games"]:
            p = Path("data/replays") / g["file"]
            paths.append(p)
            side[g["file"]] = (s, g["map"])
    games = analyze.collect([str(p) for p in paths], workers=1)
    agg = {"us": Counter(), "them": Counter()}
    lens, age = defaultdict(list), defaultdict(list)
    wall_round = []
    permap = defaultdict(lambda: [0, 0, 0, 0, 0, 0])
    for g, p in zip(games, paths):
        s, mp = side[p.name]
        for d in g["deaths"]:
            rnd, t, why, killer, L, a = d[:6]
            who = "us" if t == s else "them"
            agg[who][why] += 1
            lens[(who, why)].append(L)
            age[(who, why)].append(a)
            if who == "us" and why == "W":
                wall_round.append(rnd)
        pm = permap[mp]
        pm[0] += sum(1 for d in g["deaths"] if d[1] == s and d[2] == "W")
        pm[1] += sum(1 for d in g["deaths"] if d[1] != s and d[2] == "W")
        pm[4] += sum(1 for d in g["deaths"] if d[1] == s and d[2] == "H")
        pm[5] += sum(1 for d in g["deaths"] if d[1] != s and d[2] == "H")
        pm[2] += 1
        pm[3] += g["winner"] == s
    n = len(games)
    print("games", n)
    for who in agg:
        print(who, {k: round(v / n, 1) for k, v in agg[who].most_common()})
    for k in sorted(lens):
        print(k, "n", len(lens[k]), "med len", st.median(lens[k]), "med age", st.median(age[k]))
    print("our wall deaths by round bucket", sorted(Counter(r // 100 * 100 for r in wall_round).items()))
    print("map: kelp us/them per game, head-on us/them per game, games, wins")
    for m, v in sorted(permap.items(), key=lambda kv: -kv[1][0] / kv[1][2]):
        print(f"  {m:20} kelp {v[0]/v[2]:5.1f} {v[1]/v[2]:5.1f}  headon {v[4]/v[2]:5.1f} {v[5]/v[2]:5.1f}  {v[2]:3} {v[3]}")
