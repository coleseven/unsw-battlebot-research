"""For queen deaths by kelp/wall ('W'): at the start of the queen's fatal turn, how
many first steps were free (not kelp, not a body cell; any tail counts as free)?
0 = boxed in; >0 = the queen chose a wall with a free move available.
Usage: queen_wall_diag.py FOLDER VARIANT"""
import json, sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from bcsim import reconstruct, replay as rp

def one(args):
    path, us = args
    r = rp.decode(Path(path).read_bytes())
    board = reconstruct.Board(r.map_text)
    body, team = {}, {}
    for i, (t, coords) in enumerate(board.dragons):
        body[i], team[i] = list(coords), t
    q = next((i for i in (0, 1) if team.get(i) == us), None)
    qturns = [0, 0]; split_free = -1; split_child = 0
    actor = action = None; snap = None; steps = 0; rnd = 0; split_rnd = -99
    for ev in r.events:
        k = ev[0]
        if k == rp.ROUND_START: rnd = ev[1]
        elif k == rp.TURN_START:
            actor, action, steps = ev[1], None, 0
            if actor == q and q in body:
                hx, hy = body[q][0]
                occ = {c for d, b in body.items() for c in (b[:-1] if d == q and len(b) > 1 else b)}
                eheads = [b[0] for d, b in body.items() if team[d] != us]
                free = []
                for dch in "NESW":
                    c = board.dest(hx, hy, dch)
                    if c is not None and c not in occ and (len(body[q]) < 2 or c != body[q][1]): free.append(dch)
                safe = [dch for dch in free if not any(min((board.dest(hx, hy, dch)[0]-ex) % board.w, (ex-board.dest(hx, hy, dch)[0]) % board.w) + min((board.dest(hx, hy, dch)[1]-ey) % board.h, (ey-board.dest(hx, hy, dch)[1]) % board.h) <= 1 for ex, ey in eheads)]
                qturns[0] += 1; qturns[1] += rnd - split_rnd <= 2
                snap = {"free": free, "safe": safe, "len": len(body[q]), "rnd": rnd}
        elif k == rp.DRAGON_ACTION:
            if ev[1] == actor: action = ev[2]; snap_cpu = (ev[3], ev[4], ev[5])
        elif k == rp.DRAGON_UPDATE:
            d, head, tail = ev[1], ev[3], ev[4]
            b = body.get(d)
            if b is None: continue
            if d == actor: steps += 1
            if b[0] != head: b.insert(0, head)
            if tail in b: del b[len(b) - b[::-1].index(tail):]
        elif k == rp.DRAGON_SPLIT:
            _, parent, child, t, _, pbody, cbody = ev
            body[parent], body[child] = list(pbody), list(cbody); team[child] = t
            if parent == q: split_rnd = rnd; split_free = len(snap['free']) if snap else -1; split_child = len(cbody)
        elif k == rp.DRAGON_DEATH:
            d, why = ev[1], ev[2]
            if d == q:
                if why != "W": return None
                mv = action[1] if action and action[0] == "move" else None
                return {"free": len(snap["free"]) if snap else -1, "action": action[0] if action else None,
                        "nsteps": len(mv) if mv else 0, "step": steps, "cpu": snap_cpu if actor == q else None,
                        "actor_is_queen": actor == q, "path": path, "safe": len(snap["safe"]) if snap else -1, "split": rnd - split_rnd <= 2, "qturns": qturns, "split_free": split_free, "split_child": split_child, "len": snap["len"] if snap else 0}
            body.pop(d, None)
    return None

if __name__ == "__main__":
    A, v = Path(sys.argv[1]), sys.argv[2]
    rows = [json.loads(l) for l in (A / "games.jsonl").read_text().splitlines()]
    jobs = [(g["replay"], "A" if g["bot_a"] == v else "B") for g in rows]
    with ProcessPoolExecutor(4) as ex:
        res = [x for x in ex.map(one, jobs, chunksize=8) if x]
    c = Counter((x["free"], x["safe"], x["split"]) for x in res)
    print(len(res), "wall deaths: (free first steps, of which not next to an enemy head, queen split in last 2 rounds) ->")
    for k, n in c.most_common(): print("  ", k, n)
    print("recent-split deaths: (free moves at the split turn, child length) ->", Counter((x["split_free"], x["split_child"]) for x in res if x["split"]).most_common(12))
    tq = sum(x["qturns"][0] for x in res); ts = sum(x["qturns"][1] for x in res)
    print(f"base rate in these games: {ts}/{tq} queen turns within 2 rounds of a queen split ({ts/tq:.1%})")
    print("cpu (points, exceeded, tle) samples:", Counter((x["cpu"][1], x["cpu"][2]) for x in res if x["cpu"]))
    ex = [x["path"] for x in res if x["free"] > 0][:8]
    print("examples with a free move:", *ex, sep="\n  ")
