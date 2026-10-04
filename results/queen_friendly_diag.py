"""Own dragon moving into our queen's head: the worker's length, its action, and how
many free first steps it had (not kelp, not a body, not reversing). Usage: FOLDER VARIANT"""
import json, sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from bcsim import reconstruct, replay as rp

def one(args):
    path, us = args
    r = rp.decode(Path(path).read_bytes()); board = reconstruct.Board(r.map_text)
    body, team = {}, {}
    for i, (t, c) in enumerate(board.dragons): body[i], team[i] = list(c), t
    q = next((i for i in (0, 1) if team.get(i) == us), None)
    actor = None; snap = None; action = None
    for ev in r.events:
        k = ev[0]
        if k == rp.TURN_START:
            actor = ev[1]; action = None
            if actor in body and team[actor] == us and actor != q:
                b = body[actor]; hx, hy = b[0]
                occ = {c for d, bb in body.items() for c in (bb[:-1] if d == actor and len(bb) > 1 else bb)}
                free = [d for d in "NESW" if (c := board.dest(hx, hy, d)) is not None and c not in occ and (len(b) < 2 or c != b[1])]
                snap = {"len": len(b), "free": len(free)}
        elif k == rp.DRAGON_ACTION and ev[1] == actor: action = ev[2]
        elif k == rp.DRAGON_UPDATE:
            d, head, tail = ev[1], ev[3], ev[4]; b = body.get(d)
            if b is None: continue
            if b[0] != head: b.insert(0, head)
            if tail in b: del b[len(b) - b[::-1].index(tail):]
        elif k == rp.DRAGON_SPLIT:
            _, p, c, t, _, pb, cb = ev; body[p], body[c] = list(pb), list(cb); team[c] = t
        elif k == rp.DRAGON_DEATH:
            if ev[1] == q:
                if ev[2] != "H" or actor == q or actor not in team or team[actor] != us: return None
                return {"len": snap["len"], "free": snap["free"], "steps": len(action[1]) if action and action[0] == "move" else 0, "path": path}
            body.pop(ev[1], None)
    return None

if __name__ == "__main__":
    A, v = Path(sys.argv[1]), sys.argv[2]
    rows = [json.loads(l) for l in (A / "games.jsonl").read_text().splitlines()]
    with ProcessPoolExecutor(4) as ex:
        res = [x for x in ex.map(one, [(g["replay"], "A" if g["bot_a"] == v else "B") for g in rows], chunksize=8) if x]
    print(len(res), "own dragon moved into the queen: (worker length, free first steps, steps in its move) ->")
    for k, n in Counter((x["len"], x["free"], x["steps"]) for x in res).most_common(12): print("  ", k, n)
