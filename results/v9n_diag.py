import os, sys
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
os.environ["BCSIM_DETERMINISTIC_V6"] = "1"; os.environ["BCSIM_CPP_INPROC"] = "1"
def one(a):
    from bcsim import match, analyze
    bot, m, opp, seed, side = a
    out = Path(f"results/v9n-check/{Path(bot).name}_{Path(m).stem}_{Path(opp).name}_{seed}{side}.replay")
    A, B = (bot, opp) if side == "A" else (opp, bot)
    r = match.play(Path(m), Path(A), Path(B), seed=seed, replay_to=out)
    g = analyze.game_stats(out.read_bytes()); o = "B" if side == "A" else "A"
    fs, fo = g["teams"][side]["final"] or {}, g["teams"][o]["final"] or {}
    return (Path(bot).name, Path(m).stem, r.winner == side, fs.get("longest", 0), fs.get("total", 0), fo.get("longest", 0),
            g["teams"][side]["deaths"].get("kelp", 0), g["teams"][side]["sonar"])
if __name__ == "__main__":
    from bcsim import official_suite, match
    maps = [m for m in official_suite.ranked_maps() if m.stem in ("Slithery_Fight", "queen_of_spades", "Portals", "Autarky")]
    bots = ["results/v9n-all-bot", "results/v9n-room8-bot", "results/v9n-room16-bot"]; match.prebuild(bots)
    jobs = [(b, str(m), o, s, side) for b in bots for m in maps for o in ("sparring/cpp_nicked_v75", "sparring/cpp_leviathan3") for s in (101, 102) for side in "AB"]
    agg = defaultdict(lambda: [0, 0, 0, 0, 0, 0, 0])
    with ProcessPoolExecutor(6) as ex:
        for bot, mp, win, L, T, OL, kelp, son in ex.map(one, jobs):
            a = agg[(bot, mp)]; a[0] += win; a[1] += L; a[2] += T; a[3] += OL; a[4] += kelp; a[5] += 1; a[6] += son
    for (bot, mp), a in sorted(agg.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        n = a[5]; print(f"{mp:16} {bot:14} wins {a[0]}/{n}  our longest {a[1]/n:5.1f} (their {a[3]/n:5.1f})  our total {a[2]/n:6.1f}  kelp deaths {a[4]/n:6.1f}  sonar {a[6]/n:.0f}")
