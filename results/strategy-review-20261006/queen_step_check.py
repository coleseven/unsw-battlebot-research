"""For each enemy ram that killed our queen (Astra's queen-ram-audit cases): at the queen's
last turn, did its chosen move end within FREE-step reach of the rammer (and of any visible
enemy head), and did a legal alternative exist outside every visible enemy's free reach?"""
import json, gzip, pathlib
from collections import Counter
from bcsim import replay as rp, reconstruct
D = pathlib.Path("results/live-review-20261005")
A = json.load(open("results/strategy-review-20261006/queen-ram-audit.json"))
def dist(b, p, q):
    return min((p[0]-q[0]) % b.w, (q[0]-p[0]) % b.w) + min((p[1]-q[1]) % b.h, (q[1]-p[1]) % b.h)
out = Counter(); rows = []
for c in A["cases"]:
    raw = (D / f"{c['game']}.replay").read_bytes()
    if raw[:2] == b"\x1f\x8b": raw = gzip.decompress(raw)
    r = rp.decode(raw); board = reconstruct.Board(r.map_text)
    body, team = {}, {}
    for i, (t, cs) in enumerate(board.dragons): body[i], team[i] = list(cs), t
    us = c["our_team"]; q = next(i for i in (0, 1) if team.get(i) == us)
    rnd = 0; snap = None
    for ev in r.events:
        k = ev[0]
        if k == rp.ROUND_START: rnd = ev[1]
        if k == rp.TURN_START and ev[1] == q and rnd == c["queen_last_turn_round"]:
            b = body[q]; hx, hy = b[0]
            occ = {cell for d, bb in body.items() for cell in (bb[:-1] if d == q and len(bb) > 1 else bb)}
            enemies = [(bb[0], len(bb)) for d, bb in body.items() if team[d] != us]
            vis = [(e, l) for e, l in enemies if max(min((e[0]-hx) % board.w, (hx-e[0]) % board.w), min((e[1]-hy) % board.h, (hy-e[1]) % board.h)) <= 3]
            opts = {}
            for dd in "NESW":
                cell = board.dest(hx, hy, dd)
                if cell is None or cell in occ or (len(b) > 1 and cell == b[1]): continue
                opts[dd] = min((dist(board, cell, e) - (l + 3) // 4 for e, l in vis), default=9)   # >0: outside every visible free reach
            snap = opts
            break
        if k == rp.DRAGON_UPDATE:
            d, h, t = ev[1], ev[3], ev[4]; bb = body.get(d)
            if bb is None: continue
            if bb[0] != h: bb.insert(0, h)
            if t in bb: del bb[len(bb) - bb[::-1].index(t):]
        elif k == rp.DRAGON_SPLIT: _, p, ch, t, _, pb, cb = ev; body[p], body[ch] = list(pb), list(cb); team[ch] = t
        elif k == rp.DRAGON_DEATH: body.pop(ev[1], None)
    if snap is None: out["no snapshot"] += 1; continue
    qh0, qh1 = tuple(c["queen_head_at_last_turn"]), tuple(c["queen_head_at_death"])
    taken = next((dd for dd in "NESW" if board.dest(*qh0, dd) == qh1), None)
    tm = snap.get(taken)
    safe_alt = any(v > 0 for dd, v in snap.items() if dd != taken)
    key = ("taken outside all free reach" if tm is not None and tm > 0 else "taken inside a free reach" if tm is not None else "taken unknown/portal",
           "a free-safe alternative existed" if safe_alt else "no free-safe alternative", "paid ram" if c["paid_executed"] else "free ram")
    out[key] += 1
for k, v in out.most_common(): print(v, k)
