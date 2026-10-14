import json
from collections import Counter
from pathlib import Path
from bcsim import analyze
if __name__ == "__main__":
    rows = [json.loads(l) for l in open("data/index.jsonl", encoding="utf8")]
    rs = [r for r in rows if 7946 in (r.get("submission_a"), r.get("submission_b")) and r["ranked"]]
    paths, meta = [], {}
    for r in rs:
        s = "A" if r["submission_a"] == 7946 else "B"
        opp = r["b" if s == "A" else "a"]["name"]
        for g in r["games"]:
            paths.append(str(Path("data/replays") / g["file"])); meta[g["file"]] = (s, g["map"], opp)
    games = analyze.collect(paths, workers=1)
    stall = Counter(); tot = Counter(); ex = []
    for g, p in zip(games, paths):
        s, mp, opp = meta[Path(p).name]
        tl = {x["round"]: x for x in g["timeline"]}
        if 30 in tl and 100 in tl:
            grew = tl[100][s][1] - tl[30][s][1]
            st_ = grew <= 3
            tot[mp] += 1; stall[mp] += st_
            if st_: ex.append((mp, opp, Path(p).name, g["winner"] == s, tl[30][s], tl[100][s], tl[100]["B" if s == "A" else "A"]))
    print({m: f"{stall[m]}/{tot[m]}" for m in tot})
    for e in ex[:30]: print(e)
