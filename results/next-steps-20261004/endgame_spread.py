"""At round 460 and 480: our workers alive, their lengths, and walking-free torus
distance from each worker's head to our longest dragon's head; same for the
opponent. Reads collector_cases.json + late/replays."""
import json, statistics, sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from bcsim import reconstruct, replay as rp
D = Path("results/next-steps-20261004")
def dist(board, a, b):
    return min((a[0]-b[0]) % board.w, (b[0]-a[0]) % board.w) + min((a[1]-b[1]) % board.h, (b[1]-a[1]) % board.h)
def one(args):
    path, us = args
    r = rp.decode(Path(path).read_bytes()); board = reconstruct.Board(r.map_text)
    body, team = {}, {}
    for i, (t, c) in enumerate(board.dragons): body[i], team[i] = list(c), t
    out = {}; rnd = 0
    for ev in r.events:
        k = ev[0]
        if k == rp.ROUND_START:
            rnd = ev[1]
            if rnd in (420, 460, 480):
                snap = {}
                for t in "AB":
                    mine = [(len(b), d) for d, b in body.items() if team[d] == t]
                    if not mine: snap[t] = None; continue
                    L, king = max(mine)
                    ws = [(len(body[d]), dist(board, body[d][0], body[king][0])) for l, d in mine if d != king]
                    snap[t] = {"king": L, "workers": len(ws), "wlen": sum(l for l, _ in ws), "near6": sum(l for l, dd in ws if dd <= 6), "far": sum(l for l, dd in ws if dd > 12)}
                out[rnd] = snap
        elif k == rp.DRAGON_UPDATE:
            d, head, tail = ev[1], ev[3], ev[4]; b = body.get(d)
            if b is None: continue
            if b[0] != head: b.insert(0, head)
            if tail in b: del b[len(b) - b[::-1].index(tail):]
        elif k == rp.DRAGON_SPLIT:
            _, p, c, t, _, pb, cb = ev; body[p], body[c] = list(pb), list(cb); team[c] = t
        elif k == rp.DRAGON_DEATH: body.pop(ev[1], None)
    return out
if __name__ == "__main__":
    rows = json.load(open(D / "collector_cases.json"))
    jobs = []
    for c in rows:
        a, b = ("base", c["opponent"]) if c["side"] == "A" else (c["opponent"], "base")
        jobs.append((str(D / "late/replays" / f"{a}-vs-{b}-{c['map']}-s{c['seed']}.replay"), c["side"]))
    with ProcessPoolExecutor(4) as ex: res = list(ex.map(one, jobs, chunksize=8))
    for cls in ("could_not_deliver", "could_not_produce", "delivered_then_died", "win"):
        for rnd in (420, 460, 480):
            vals = []
            for c, x in zip(rows, res):
                if c["cls"] != cls or rnd not in x: continue
                us = c["side"]; th = "B" if us == "A" else "A"
                if x[rnd][us] and x[rnd][th]: vals.append((x[rnd][us], x[rnd][th]))
            if not vals: continue
            med = lambda f: statistics.median(f(v) for v in vals)
            print(f"{cls:20} r{rnd}: n={len(vals)} OUR king {med(lambda v: v[0]['king'])} workers {med(lambda v: v[0]['workers'])} worker-len {med(lambda v: v[0]['wlen'])} (<=6 of king {med(lambda v: v[0]['near6'])}, >12 {med(lambda v: v[0]['far'])}) | THEIR king {med(lambda v: v[1]['king'])} workers {med(lambda v: v[1]['workers'])} worker-len {med(lambda v: v[1]['wlen'])} (<=6 {med(lambda v: v[1]['near6'])}, >12 {med(lambda v: v[1]['far'])})")
