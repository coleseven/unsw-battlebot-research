import json, statistics as st
from collections import Counter, defaultdict
from pathlib import Path
from bcsim import analyze
if __name__ == "__main__":
    rows = [json.loads(l) for l in open("data/index.jsonl", encoding="utf8")]
    rs = [r for r in rows if r["at"] >= "2026-09-28T13:15" and 590 in (r["a"]["id"], r["b"]["id"]) and r["ranked"]]
    paths, meta = [], {}
    for r in rs:
        s = "A" if r["a"]["id"] == 590 else "B"; opp = r["b" if s == "A" else "a"]["name"]
        for g in r["games"]:
            paths.append(str(Path("data/replays") / g["file"])); meta[g["file"]] = (s, g["map"], opp)
    games = analyze.collect(paths, workers=1)
    per = defaultdict(lambda: [0, 0]); stall = []; lines = []
    for g, p in zip(games, paths):
        s, mp, opp = meta[Path(p).name]; o = "B" if s == "A" else "A"
        win = g["winner"] == s; base = mp.split("_")[0] if mp[-9:-8] == "_" else mp
        per[mp][0] += win; per[mp][1] += 1
        tl = {x["round"]: x for x in g["timeline"]}
        fs, fo = g["teams"][s]["final"] or {}, g["teams"][o]["final"] or {}
        grew = (tl[100][s][1] - tl[30][s][1]) if 30 in tl and 100 in tl else None
        dth = Counter(d[2] for d in g["deaths"] if d[1] == s)
        lines.append((win, mp, opp, g["end"], g["rounds"], f"us {fs.get('longest')}/{fs.get('total')} them {fo.get('longest')}/{fo.get('total')}",
                      f"grow30-100 {grew}", f"r100 us {tl.get(100, {}).get(s)} them {tl.get(100, {}).get(o)}", dict(dth)))
    print("per map:", {m: f"{a}/{n}" for m, (a, n) in sorted(per.items())})
    for l in sorted(lines, key=lambda l: (l[0], l[1])):
        print(("WIN " if l[0] else "LOSS"), *l[1:])
