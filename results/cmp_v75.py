import glob, json, statistics as st
from collections import Counter, defaultdict
from pathlib import Path
from bcsim import analyze
if __name__ == "__main__":
    games = [json.loads(l) for l in open("results/v10-vs-v75/games.jsonl")]
    rows = defaultdict(list); curves = defaultdict(lambda: defaultdict(list)); per = defaultdict(lambda: [0, 0])
    for g in games:
        s = "A" if g["bot_a"] == "v10" else "B"; o = "B" if s == "A" else "A"
        st_ = analyze.game_stats(Path(g["replay"]).read_bytes())
        win = g["winner"] == s; per[g["map"]][0] += win; per[g["map"]][1] += 1
        for who, t in (("v10", s), ("v75", o)):
            T = st_["teams"][t]
            rows[who].append({"pearls": T["pearls"], "splits": T["splits"], "sprints": T["sprints"], "extra_steps": T["extra_steps"],
                              "moves": T["moves"], "feed(A)": T["deaths"].get("no-move", 0), "self(S)": T["deaths"].get("self", 0),
                              "kelp": T["deaths"].get("kelp", 0), "headon": T["deaths"].get("head-on", 0), "body": T["deaths"].get("body", 0),
                              "kills": T["kills"], "peak_alive": T["peak_alive"][0], "final_longest": (T["final"] or {}).get("longest", 0),
                              "final_total": (T["final"] or {}).get("total", 0), "last_split": T["last_split"] or 0})
            for x in st_["timeline"]:
                if x["round"] in (50, 100, 200, 300, 400, 450, 490):
                    curves[who][x["round"]].append((x[t][0], x[t][1], x[t][2]))
    print("per map v10 wins:", {m: f"{a}/{b}" for m, (a, b) in sorted(per.items())})
    keys = list(rows["v10"][0])
    print(f"{'stat (median/game)':18} {'v10':>8} {'v75':>8}")
    for k in keys:
        print(f"{k:18} {st.median(r[k] for r in rows['v10']):8.1f} {st.median(r[k] for r in rows['v75']):8.1f}")
    print("round: alive/total/longest (median)")
    for rr in (50, 100, 200, 300, 400, 450, 490):
        f = lambda who: "/".join(str(st.median(c[i] for c in curves[who][rr])) for i in range(3)) if curves[who][rr] else "-"
        print(f"  r{rr}: v10 {f('v10'):>14}   v75 {f('v75'):>14}")
