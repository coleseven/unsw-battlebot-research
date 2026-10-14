import json, statistics as st
from collections import Counter, defaultdict
from pathlib import Path
from bcsim import analyze
def base_map(m):
    import re; return re.sub(r"_[0-9a-f]{8}$", "", m or "").lower()
if __name__ == "__main__":
    rows = [json.loads(l) for l in open("data/index.jsonl", encoding="utf8")]
    rs = [r for r in rows if r["at"] >= "2026-09-28T13:15" and 590 in (r["a"]["id"], r["b"]["id"])]
    paths, meta = [], {}
    for r in rs:
        s = "A" if r["a"]["id"] == 590 else "B"; o = r["b" if s == "A" else "a"]
        for g in r["games"]:
            p = Path("data/replays") / g["file"]
            if p.exists(): paths.append(str(p)); meta[g["file"]] = (s, base_map(g["map"]), o["name"], o["elo"], r["ranked"])
    games = analyze.collect(paths, workers=1)
    per = defaultdict(lambda: [0, 0]); kinds = Counter(); byopp = defaultdict(lambda: [0, 0, 0])
    loss_rows = []; deaths = {"us": Counter(), "them": Counter()}; early = defaultdict(list)
    for g, p in zip(games, paths):
        s, mp, opp, oelo, ranked = meta[Path(p).name]; o = "B" if s == "A" else "A"
        win = g["winner"] == s; per[mp][0] += win; per[mp][1] += 1
        byopp[opp][0] += win; byopp[opp][1] += 1; byopp[opp][2] = oelo
        for d in g["deaths"]: deaths["us" if d[1] == s else "them"][d[2]] += 1
        fs, fo = g["teams"][s]["final"] or {}, g["teams"][o]["final"] or {}
        tl = {x["round"]: x for x in g["timeline"]}
        if 100 in tl: early[win].append((tl[100][s][1], tl[100][o][1]))
        if not win:
            if g["end"] != "round_limit": k = "eliminated"
            elif fs.get("longest", 0) < fo.get("longest", 0) and fs.get("total", 0) >= fo.get("total", 0): k = "tiebreak: shorter king, more total"
            elif fs.get("longest", 0) < fo.get("longest", 0): k = "round 500: shorter king and less total"
            else: k = "round 500: other"
            kinds[k] += 1
            loss_rows.append((mp, opp, oelo, g["end"], g["rounds"], f"{fs.get('longest')}/{fs.get('total')} vs {fo.get('longest')}/{fo.get('total')}"))
    n = len(games); w = sum(v[0] for v in per.values())
    print(f"{n} games, {w} wins ({w/n:.0%})")
    print("per map:", {m: f"{a}/{b}" for m, (a, b) in sorted(per.items(), key=lambda kv: kv[1][0]/kv[1][1])})
    print("loss types:", dict(kinds))
    print("by opponent (wins/games, elo):", sorted(((a, b, e, k) for k, (a, b, e) in byopp.items()), key=lambda x: -x[2])[:14])
    print("deaths per game us:", {k: round(v/n, 1) for k, v in deaths["us"].most_common()}, "| them:", {k: round(v/n, 1) for k, v in deaths["them"].most_common()})
    for win in (True, False):
        v = early[win]
        if v: print(("wins" if win else "losses"), "total length at r100 us/them (median):", st.median(a for a, b in v), "/", st.median(b for a, b in v))
    print("losses:"); [print("  ", *r) for r in sorted(loss_rows, key=lambda r: r[3])]
