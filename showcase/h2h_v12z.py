"""Direct head-to-head for the writeup: v12z vs v12x on the 17 current maps (1.2.9),
both sides, four fresh seeds (136 games). Replays kept in showcase/replays/h2h-v12z."""
import os, json
os.environ["BCSIM_DETERMINISTIC_V6"] = "1"; os.environ["BCSIM_CPP_INPROC"] = "1"
from bcsim import queen_runtime
queen_runtime.activate()
from pathlib import Path
from collections import Counter
from bcsim import bounded, official_suite

if __name__ == "__main__":
    new, old = "versions/v12z", "versions/v12x"
    out = "showcase/replays/h2h-v12z"
    jobs = []
    for seed in (1041001, 1041002, 1041003, 1041004):
        for m in official_suite.current_maps():
            for a, b in ((new, old), (old, new)):
                jobs.append((str(m), a, b, seed, out, ["v12x", Path(m).stem, seed]))
    games = bounded.run(jobs, 12, Path("showcase/run-h2h-v12z"), "h2h v12z")
    Path("showcase/games-h2h-v12z.json").write_text(json.dumps(games, indent=0, default=str))
    c = Counter(); bym = {}
    for g in games:
        side = "A" if g["bot_a"] == "v12z" else "B"; th = "B" if side == "A" else "A"
        w = g["winner"] == side
        c["n"] += 1; c["w"] += w; c["d"] += g["winner"] is None
        c["myq"] += (g.get(f"{side.lower()}_queen") or 0) > 0; c["thq"] += (g.get(f"{th.lower()}_queen") or 0) > 0
        m = official_suite.canonical_map(Path(g["map"]).stem); bym.setdefault(m, [0, 0]); bym[m][0] += w; bym[m][1] += 1
    print(f"v12z vs v12x: wins {c['w']}/{c['n']} draws {c['d']}  queen alive {c['myq']} vs {c['thq']}")
    print(" ".join(f"{m} {w}/{n}" for m, (w, n) in sorted(bym.items())))
