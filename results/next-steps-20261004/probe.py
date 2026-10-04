"""Diagnostic probe: each BOT vs opponents/turtle on each MAP, both sides, one seed;
prints pearls eaten by our queen / workers in rounds 0-119.
Usage: probe.py MAPS(comma) BOT [BOT ...]"""
import sys
from collections import Counter
from pathlib import Path
from bcsim import queen_runtime

def eats(rp, reconstruct, rep, side):
    r = rp.decode(rep.read_bytes()); board = reconstruct.Board(r.map_text)
    team = {i: t for i, (t, c) in enumerate(board.dragons)}
    pearls = set(); actor = None; per = Counter(); rnd = 0
    for ev in r.events:
        if ev[0] == rp.ROUND_START: rnd = ev[1]
        if rnd >= 120: break
        elif ev[0] == rp.TURN_START: actor = ev[1]
        elif ev[0] == rp.DRAGON_SPLIT: team[ev[2]] = ev[3]
        elif ev[0] == rp.TILE_CHANGE:
            if ev[3]: pearls.add((ev[1], ev[2]))
            elif (ev[1], ev[2]) in pearls:
                pearls.discard((ev[1], ev[2]))
                if team.get(actor) == side: per["queen" if actor <= 1 else "worker"] += 1
    return dict(per)

if __name__ == "__main__":
    queen_runtime.activate()
    from bcsim import match, guard, reconstruct, replay as rp
    out = Path("results/next-steps-20261004/probe")
    with guard.slot("probe"):
        for m in sys.argv[1].split(","):
            for bot in sys.argv[2:]:
                for side in "AB":
                    a, b = (bot, "opponents/turtle") if side == "A" else ("opponents/turtle", bot)
                    rep = out / f"{Path(bot).name}-{side}-{m}.replay"
                    match.play(Path(f"maps/v129/{m}.map"), Path(a), Path(b), seed=771001, replay_to=rep)
                    print(f"{m:14} {Path(bot).name:14} as {side}: eaten r0-119 {eats(rp, reconstruct, rep, side)}", flush=True)
