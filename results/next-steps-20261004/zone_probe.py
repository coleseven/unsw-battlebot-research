"""Weakhold access probe: each BOT vs turtle, both sides, seed 771001; share of our
head-rounds (30-199) in the central maze (11 <= x < 29) and pearls eaten r0-199."""
import sys
from collections import Counter
from pathlib import Path
from bcsim import queen_runtime
if __name__ == "__main__":
    queen_runtime.activate()
    from bcsim import match, guard, reconstruct, replay as rp
    out = Path("results/next-steps-20261004/probe")
    with guard.slot("zone probe"):
        for bot in sys.argv[1:]:
            for side in "AB":
                a, b = (bot, "opponents/turtle") if side == "A" else ("opponents/turtle", bot)
                rep = out / f"{Path(bot).name}-{side}-weakhold.replay"
                match.play(Path("maps/v129/weakhold.map"), Path(a), Path(b), seed=771001, replay_to=rep)
                r = rp.decode(rep.read_bytes()); board = reconstruct.Board(r.map_text)
                body, team = {}, {}
                for i, (t, cs) in enumerate(board.dragons): body[i], team[i] = list(cs), t
                z = Counter(); pearls = set(); actor = None; eat = 0; rnd = 0
                for ev in r.events:
                    k = ev[0]
                    if k == rp.ROUND_START:
                        rnd = ev[1]
                        if rnd >= 200: break
                        if rnd >= 30:
                            for d, bb in body.items():
                                if team[d] == side: z["c" if 11 <= bb[0][0] < 29 else "home"] += 1
                    elif k == rp.TURN_START: actor = ev[1]
                    elif k == rp.TILE_CHANGE:
                        if ev[3]: pearls.add((ev[1], ev[2]))
                        elif (ev[1], ev[2]) in pearls:
                            pearls.discard((ev[1], ev[2])); eat += team.get(actor) == side
                    elif k == rp.DRAGON_UPDATE:
                        d, h, t = ev[1], ev[3], ev[4]; bb = body.get(d)
                        if bb is None: continue
                        if bb[0] != h: bb.insert(0, h)
                        if t in bb: del bb[len(bb) - bb[::-1].index(t):]
                    elif k == rp.DRAGON_SPLIT: _, p, ch, t, _, pb, cb = ev; body[p], body[ch] = list(pb), list(cb); team[ch] = t
                    elif k == rp.DRAGON_DEATH: body.pop(ev[1], None)
                tot = sum(z.values()) or 1
                print(f"{Path(bot).name:14} as {side}: centre share {z['c']/tot:.2f}, eaten r0-199 {eat}", flush=True)
