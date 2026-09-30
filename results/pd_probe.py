"""PD-only diagnostic probe vs nicked v92 (not a full-suite result)."""
import os, re, shutil, sys
os.environ["BCSIM_DETERMINISTIC_V6"] = "1"; os.environ["BCSIM_CPP_INPROC"] = "1"
from pathlib import Path
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from bcsim import guard, match, reconstruct, replay as rp

VARIANTS = {
    "sonarhub": {"CPP_SONAR_HUB": 1},
    "sonarhub_nogoal": {"CPP_SONAR_HUB": 1, "GOAL": "false"},
    "sonarhub_whub3": {"CPP_SONAR_HUB": 1, "W_HUB": 215.0},
    "sonarhub_every2": {"CPP_SONAR_HUB": 1, "CPP_SONAR_EVERY": 2},
}
RICH = {(x, y) for x in (14, 17) for y in (0, 1, 2, 13, 14, 15)}
MAP = Path("maps/server/Prisoners_Dilemma.map")

def make(name, over):
    d = Path(f"results/pd-probe/{name}-bot")
    if d.exists(): shutil.rmtree(d)
    shutil.copytree("results/v10m-bot", d, ignore=shutil.ignore_patterns(".unswbc-build"))
    p = d / "params.hpp"; s = p.read_text()
    for k, v in over.items():
        s, n = re.subn(rf"(inline constexpr \w+ {k} = )[^;]+;", rf"\g<1>{v};", s); assert n == 1, k
    p.write_text(s)
    return d

def play(args):
    name, seed, us = args
    bot = Path(f"results/pd-probe/{name}-bot"); opp = Path("sparring/cpp_nicked_v92")
    a, b = (bot, opp) if us == "A" else (opp, bot)
    out = Path(f"results/pd-probe/{name}-{seed}-{us}.replay")
    r = match.play(MAP, a, b, seed=seed, replay_to=out)
    board = reconstruct.Board(MAP.read_text()); rr = rp.load(out)
    team = {i: t for i, (t, _) in enumerate(board.dragons)}; head = {i: c[0] for i, (t, c) in enumerate(board.dragons)}
    eat = Counter(); actor = None; rnd = 0
    for ev in rr.events:
        if ev[0] == rp.ROUND_START: rnd = ev[1]
        elif ev[0] == rp.TURN_START: actor = ev[1]
        elif ev[0] == rp.DRAGON_SPLIT: team[ev[2]] = ev[3]
        elif ev[0] == rp.DRAGON_UPDATE: head[ev[1]] = tuple(ev[3])
        elif ev[0] == rp.TILE_CHANGE and not ev[3] and team.get(actor) == us:
            eat["all"] += 1; eat["rich"] += head.get(actor) in RICH; eat["r150"] += rnd < 150
    return name, r.winner == us, r.reason, r.rounds, eat["all"], eat["rich"], eat["r150"]

if __name__ == "__main__":
    for n, o in VARIANTS.items(): make(n, o)
    jobs = [(n, s, us) for n in VARIANTS for s in (281004, 281005, 281006) for us in "AB"]
    with guard.slot("pd-probe"), ProcessPoolExecutor(guard.cap_workers(10)) as pool:
        res = list(pool.map(play, jobs))
    agg = {}
    for name, win, reason, rounds, allp, rich, r150 in res:
        a = agg.setdefault(name, Counter()); a["n"] += 1; a["w"] += win; a["pearls"] += allp; a["rich"] += rich; a["r150"] += r150; a["rounds"] += rounds
    for n, a in agg.items():
        print(f"{n:22} wins {a['w']}/{a['n']}  pearls/game {a['pearls']/a['n']:.0f}  rich {a['rich']/a['n']:.0f}  before r150 {a['r150']/a['n']:.0f}  mean rounds {a['rounds']/a['n']:.0f}")
