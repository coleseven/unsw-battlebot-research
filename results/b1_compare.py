import json, random, statistics as st
from pathlib import Path
from bcsim import official_suite as o, tune
if __name__ == "__main__":
    dirs = dict(l.split() for l in open("results/v9-validate-dirs.txt"))
    pool = set(o.CURRENT_POOL)
    data = {}
    for c, d in dirs.items():
        games = [json.loads(l) for l in open(Path(d) / "full" / "games.jsonl")]
        m = tune.replay_margins(games, 12)
        rows = {}
        for g in games:
            s = "A" if g["bot_a"] == "candidate" else "B"
            opp = g["bot_b"] if s == "A" else g["bot_a"]
            rows[(opp, g["map"], g["seed"], s)] = (m[g["replay"]][s]["aligned"], g["winner"] == s)
        data[c] = rows
    b1, b0 = data["results/v9-g5-bot"], data["versions/v7-base"]
    keys = [k for k in b1 if k in b0]
    def summary(sel, label):
        ks = [k for k in keys if sel(k)]
        d = {}
        for k in ks: d.setdefault((k[1], k[2]), []).append(b1[k][0] - b0[k][0])
        blocks = list(d.values()); rng = random.Random(0); means = []
        for _ in range(2000): means.append(st.fmean([x for _ in blocks for x in rng.choice(blocks)]))
        means.sort()
        print(f"{label:28} n={len(ks):3}  B1 wins {sum(b1[k][1] for k in ks):3}  B0 wins {sum(b0[k][1] for k in ks):3}  "
              f"delta {st.fmean(x for b in blocks for x in b):+.3f} [{means[50]:+.3f}, {means[1949]:+.3f}]")
    summary(lambda k: True, "all 15 maps")
    summary(lambda k: k[1] in pool, "current pool (10)")
    summary(lambda k: k[1] not in pool, "guard (5)")
    for opp in sorted({k[0] for k in keys}):
        summary(lambda k, o=opp: k[0] == o and k[1] in pool, f"pool vs {opp}")
    per = {}
    for k in keys:
        if k[1] in pool: per.setdefault(k[1], [0, 0, 0]); per[k[1]][0] += b1[k][1]; per[k[1]][1] += b0[k][1]; per[k[1]][2] += 1
    print("per pool map (B1 wins, B0 wins, games):", per)
