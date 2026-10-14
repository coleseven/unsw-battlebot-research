import json, statistics as st
from collections import Counter, defaultdict
from pathlib import Path
from bcsim import analyze
if __name__ == "__main__":
    rows = [json.loads(l) for l in open("data/index.jsonl", encoding="utf8")]
    rs = [r for r in rows if 7946 in (r.get("submission_a"), r.get("submission_b")) and r["ranked"]]
    paths, side = [], {}
    for r in rs:
        s = "A" if r["submission_a"] == 7946 else "B"
        for g in r["games"]:
            paths.append(str(Path("data/replays") / g["file"])); side[g["file"]] = (s, g["map"])
    games = analyze.collect(paths, workers=1)
    agg = {True: defaultdict(Counter), False: defaultdict(Counter)}; n = Counter()
    first_split = defaultdict(list); r50 = defaultdict(list)
    for g, p in zip(games, paths):
        s, mp = side[Path(p).name]; o = "B" if s == "A" else "A"; win = g["winner"] == s; n[win] += 1
        for d in g["deaths"]:
            if d[0] <= 100:
                who = "us" if d[1] == s else "them"
                agg[win][who][d[2]] += 1
                if who == "us" and d[3] == o: agg[win]["us_killed_by_them"][d[2]] += 1
        tl = {x["round"]: x for x in g["timeline"]}
        for rr in (30, 60, 100):
            if rr in tl: r50[(win, rr)].append((tl[rr][s][0], tl[rr][s][1], tl[rr][o][0], tl[rr][o][1]))
        first_split[win].append(g["teams"][s].get("first_split"))
    for win in (True, False):
        print("WINS" if win else "LOSSES", n[win], "games; deaths in rounds 0-100 per game:")
        for who in ("us", "them", "us_killed_by_them"):
            print("  ", who, {k: round(v / n[win], 1) for k, v in agg[win][who].most_common()})
        for rr in (30, 60, 100):
            v = r50[(win, rr)]
            print(f"   r{rr}: us alive/total {st.median(x[0] for x in v)}/{st.median(x[1] for x in v)}  them {st.median(x[2] for x in v)}/{st.median(x[3] for x in v)}")
        fs = [x for x in first_split[win] if x is not None]
        print("   first split round median", st.median(fs) if fs else None)
