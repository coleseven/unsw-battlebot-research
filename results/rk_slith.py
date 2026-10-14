import os, sys, json
from pathlib import Path
from collections import Counter
os.environ["BCSIM_DETERMINISTIC_V6"] = "1"
from bcsim import match, analyze, replay as rp
if __name__ == "__main__":
    m = Path("maps/server") / (sys.argv[1] + ".map")
    out = Path("results/rk_" + sys.argv[1] + ".replay")
    r = match.play(m, Path(os.environ.get("BOT","versions/v6")), Path(sys.argv[2]), replay_to=out)
    print(r.winner, r.a_length, r.b_length, r.deaths, round(r.seconds))
    g = analyze.game_stats(out.read_bytes())
    w = [d for d in g["deaths"] if d[1] == "A" and d[2] == "W"]
    print("A wall deaths", len(w), "ages", Counter(min(d[5], 30) for d in w).most_common(8), "lens", Counter(d[4] for d in w).most_common(5))
    print("rounds", Counter(d[0] // 50 * 50 for d in w))
