"""Boxed-in queen deaths: at the queen's previous turn, the exits (static, after the
move) of each free option and of the move actually taken. Usage: FOLDER VARIANT"""
import json, sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from bcsim import reconstruct, replay as rp

def exits_after(board, body, q, cell, occ):
    # free non-reverse cells from `cell` once the queen's head is there (its tail moved)
    n = 0
    for d in "NESW":
        c = board.dest(*cell, d)
        if c is not None and c not in occ and c != body[q][0]: n += 1
    return n

def one(args):
    path, us = args
    r = rp.decode(Path(path).read_bytes()); board = reconstruct.Board(r.map_text)
    body, team = {}, {}
    for i, (t, c) in enumerate(board.dragons): body[i], team[i] = list(c), t
    q = next((i for i in (0, 1) if team.get(i) == us), None)
    hist = []; rnd = 0; actor = None; split_rnd = -99
    for ev in r.events:
        k = ev[0]
        if k == rp.ROUND_START: rnd = ev[1]
        elif k == rp.TURN_START:
            actor = ev[1]
            if actor == q and q in body:
                b = body[q]; hx, hy = b[0]
                occ = {c for d, bb in body.items() for c in (bb[:-1] if d == q and len(bb) > 1 else bb)}
                eheads = [bb[0] for d, bb in body.items() if team[d] != us]
                opts = {}
                for d in "NESW":
                    c = board.dest(hx, hy, d)
                    if c is None or c in occ or (len(b) > 1 and c == b[1]): continue
                    near = any(min((c[0]-x) % board.w, (x-c[0]) % board.w) + min((c[1]-y) % board.h, (y-c[1]) % board.h) <= 1 for x, y in eheads)
                    opts[d] = (exits_after(board, body, q, c, occ - {b[-1]} | {b[0]}), near)
                hist.append({"rnd": rnd, "opts": opts, "taken": None})
        elif k == rp.DRAGON_ACTION and ev[1] == q and hist and hist[-1]["rnd"] == rnd:
            a = ev[2]; hist[-1]["taken"] = a[1][0] if a and a[0] == "move" else (a[0] if a else None)
        elif k == rp.DRAGON_UPDATE:
            d, head, tail = ev[1], ev[3], ev[4]; b = body.get(d)
            if b is None: continue
            if b[0] != head: b.insert(0, head)
            if tail in b: del b[len(b) - b[::-1].index(tail):]
        elif k == rp.DRAGON_SPLIT:
            _, p, c, t, _, pb, cb = ev; body[p], body[c] = list(pb), list(cb); team[c] = t
            if p == q: split_rnd = rnd
        elif k == rp.DRAGON_DEATH:
            if ev[1] == q:
                if ev[2] != "W" or rnd - split_rnd <= 2 or len(hist) < 2: return None
                prev = hist[-2]
                t = prev["taken"]; o = prev["opts"]
                best = max((e for e, _ in o.values()), default=-1)
                return {"n_opts": len(o), "taken_exits": o[t][0] if t in o else None, "best_exits": best,
                        "best_safe": max((e for e, near in o.values() if not near), default=-1), "taken": t, "path": path}
            body.pop(ev[1], None)
    return None

if __name__ == "__main__":
    A, v = Path(sys.argv[1]), sys.argv[2]
    rows = [json.loads(l) for l in (A / "games.jsonl").read_text().splitlines()]
    with ProcessPoolExecutor(4) as ex:
        res = [x for x in ex.map(one, [(g["replay"], "A" if g["bot_a"] == v else "B") for g in rows], chunksize=8) if x]
    print(len(res), "boxed-in deaths without a recent split; previous turn: (options, exits after taken move, best exits, best exits not next to an enemy head)")
    for k, n in Counter((x["n_opts"], x["taken_exits"], x["best_exits"], x["best_safe"]) for x in res).most_common(15): print("  ", k, n)
    print("examples (taken 0 exits, a better option existed):", *[x["path"] + " " + str(x["taken"]) for x in res if x["taken_exits"] == 0 and x["best_safe"] > 0][:6], sep="\n  ")
