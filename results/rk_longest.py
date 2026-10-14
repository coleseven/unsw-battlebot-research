import json
from pathlib import Path
from bcsim import analyze
if __name__ == "__main__":
    rows = [json.loads(l) for l in open("data/index.jsonl", encoding="utf8")]
    for sub in (6688, 7946):
        rs = [r for r in rows if sub in (r.get("submission_a"), r.get("submission_b")) and r["ranked"]]
        paths, side = [], {}
        for r in rs:
            s = "A" if r["submission_a"] == sub else "B"
            for g in r["games"]:
                paths.append(str(Path("data/replays") / g["file"])); side[g["file"]] = s
        games = analyze.collect(paths, workers=1)
        n = lim = 0; lost_total_ahead = won_total_behind = elim_l = 0; gap = []
        for g, p in zip(games, paths):
            s = side[Path(p).name]; o = "B" if s == "A" else "A"; n += 1
            fs, fo = g["teams"][s]["final"] or {}, g["teams"][o]["final"] or {}
            win = g["winner"] == s
            if g["end"] != "round_limit" and not str(g["end"]).startswith("round"):
                elim_l += not win; continue
            lim += 1
            if not win and fs.get("total", 0) > fo.get("total", 0): lost_total_ahead += 1; gap.append((fs.get("longest"), fo.get("longest"), fs.get("total"), fo.get("total")))
            if win and fs.get("total", 0) < fo.get("total", 0): won_total_behind += 1
        print(f"sub {sub}: {n} games, {lim} to round 500; losses despite MORE total length: {lost_total_ahead}; wins despite less total: {won_total_behind}; eliminated losses {elim_l}")
        print("   (our longest, their longest, our total, their total):", gap[:12])
    print(json.dumps(games[0]["teams"]["A"]["final"]), games[0]["end"])
