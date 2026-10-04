"""Queen head-on deaths: who moved (queen or the other dragon), the other's length,
and at the queen's last turn the options not next to any enemy head. Usage: FOLDER VARIANT"""
import json, sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from bcsim import reconstruct, replay as rp

def dist(board, a, b):
    return min((a[0]-b[0]) % board.w, (b[0]-a[0]) % board.w) + min((a[1]-b[1]) % board.h, (b[1]-a[1]) % board.h)

def one(args):
    path, us = args
    r = rp.decode(Path(path).read_bytes()); board = reconstruct.Board(r.map_text)
    body, team = {}, {}
    for i, (t, c) in enumerate(board.dragons): body[i], team[i] = list(c), t
    q = next((i for i in (0, 1) if team.get(i) == us), None)
    actor = None; last = None; rnd = 0; pending = None; trace = []
    for ev in r.events:
        k = ev[0]
        if k == rp.ROUND_START: rnd = ev[1]
        elif k == rp.TURN_START:
            actor = ev[1]
            if actor == q and q in body:
                b = body[q]; hx, hy = b[0]
                occ = {c for d, bb in body.items() for c in (bb[:-1] if d == q and len(bb) > 1 else bb)}
                eh = [(bb[0], len(bb)) for d, bb in body.items() if team[d] != us]
                opts = []; dmap = {}
                for d in "NESW":
                    c = board.dest(hx, hy, d)
                    if c is None or c in occ or (len(b) > 1 and c == b[1]): continue
                    opts.append(min((dist(board, c, e) - (l + 3) // 4 for e, l in eh), default=9)); dmap[c] = opts[-1]
                near = min((dist(board, b[0], e) for e, l in eh), default=99)
                last = {"rnd": rnd, "opts": opts, "near": near, "len": len(b), "dmap": dmap, "taken": None}
        elif k == rp.DRAGON_UPDATE:
            d, head, tail = ev[1], ev[3], ev[4]; b = body.get(d)
            if b is None: continue
            trace.append((rnd, d, team.get(d), len(b), b[0], head))
            if d == q and last is not None and last['taken'] is None and last['rnd'] == rnd: last['taken'] = last['dmap'].get(head, 'portal/other')
            if b[0] != head: b.insert(0, head)
            if tail in b: del b[len(b) - b[::-1].index(tail):]
        elif k == rp.DRAGON_SPLIT:
            _, p, c, t, _, pb, cb = ev; body[p], body[c] = list(pb), list(cb); team[c] = t
        elif k == rp.DRAGON_DEATH:
            d, why = ev[1], ev[2]
            if why == "H" and pending is None and d != q: pending = (d, len(body[d]), team[d])
            if d == q:
                if why != "H": return None
                other = pending if pending and pending[0] != q else None
                if actor != q and actor in body: other = (actor, len(body[actor]), team[actor])
                return {"queen_moved": actor == q, "other_team": ("own" if other and other[2] == us else "enemy") if other else "?",
                        "other_len": other[1] if other else 0, "same_round": last and last["rnd"] == rnd,
                        "safe_opts": sum(o >= 1 for o in last["opts"]) if last else -1, "n_opts": len(last["opts"]) if last else -1,
                        "near": last["near"] if last else -1, "taken_margin": last["taken"] if last else None, "path": path, "trace": trace[-12:]}
            body.pop(d, None)
        if k == rp.TURN_START: pending = None
    return None

if __name__ == "__main__":
    A, v = Path(sys.argv[1]), sys.argv[2]
    rows = [json.loads(l) for l in (A / "games.jsonl").read_text().splitlines()]
    with ProcessPoolExecutor(4) as ex:
        res = [x for x in ex.map(one, [(g["replay"], "A" if g["bot_a"] == v else "B") for g in rows], chunksize=8) if x]
    print(len(res), "queen head-on deaths")
    print("  (queen moved, other team):", Counter((x["queen_moved"], x["other_team"]) for x in res).most_common())
    print("  other length:", sorted(Counter(min(x["other_len"], 9) for x in res).items()))
    en = [x for x in res if x["other_team"] == "enemy"]
    print("  enemy, queen moved: (options, options out of every enemy's reach) ->", Counter((x["n_opts"], x["safe_opts"]) for x in en if x["queen_moved"]).most_common(10))
    print("  enemy moved, an out-of-reach option existed: same round as the queen's turn?", Counter(x["same_round"] for x in en if not x["queen_moved"] and x["safe_opts"] > 0))
    print("  enemy moved, an out-of-reach option existed: (queen took a move whose reach margin was) ->", Counter(x["taken_margin"] for x in en if not x["queen_moved"] and x["safe_opts"] > 0).most_common(8))
    print("  enemy, enemy moved: (options, out of reach) ->", Counter((x["n_opts"], x["safe_opts"]) for x in en if not x["queen_moved"]).most_common(10))
    ex1 = [x for x in en if not x["queen_moved"] and x["taken_margin"] == 1][:3]
    for x in ex1:
        print(x["path"])
        for t in x["trace"]: print("    ", t)
