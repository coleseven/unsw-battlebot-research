"""Live v12x losses: anatomy of enemy head-ons that kill our queen."""
import json, gzip, pathlib, sys
from collections import Counter
from bcsim import replay as rp, reconstruct
D = pathlib.Path("results/live-review-20261005")
def dist(board, a, b):
    return min((a[0]-b[0]) % board.w, (b[0]-a[0]) % board.w) + min((a[1]-b[1]) % board.h, (b[1]-a[1]) % board.h)
def cheb(board, a, b):
    return max(min((a[0]-b[0]) % board.w, (b[0]-a[0]) % board.w), min((a[1]-b[1]) % board.h, (b[1]-a[1]) % board.h))
maps = set(sys.argv[1:]) or None
games = [g for g in json.load(open(D / "games.json")) if g["grp"] == "new" and not g["won"] and (maps is None or g["map"] in maps)]
rows = []
for g in games:
    b = (D / f"{g['game']}.replay").read_bytes()
    if b[:2] == b"\x1f\x8b": b = gzip.decompress(b)
    r = rp.decode(b); board = reconstruct.Board(r.map_text)
    body, team = {}, {}
    for i, (t, cs) in enumerate(board.dragons): body[i], team[i] = list(cs), t
    us = g["us"]; q = next(i for i in (0, 1) if team.get(i) == us)
    actor = None; action = None; rnd = 0; prev = None; cur = None
    for ev in r.events:
        k = ev[0]
        if k == rp.ROUND_START: rnd = ev[1]
        elif k == rp.TURN_START:
            actor = ev[1]; action = None
            if actor == q and q in body:
                prev = cur
                qh = body[q][0]
                cur = {"rnd": rnd, "qlen": len(body[q]), "enemies": [(d, bb[0], len(bb)) for d, bb in body.items() if team[d] != us]}
        elif k == rp.DRAGON_ACTION and ev[1] == actor: action = ev[2]
        elif k == rp.DRAGON_UPDATE:
            d, h, t = ev[1], ev[3], ev[4]; bb = body.get(d)
            if bb is None: continue
            if bb[0] != h: bb.insert(0, h)
            if t in bb: del bb[len(bb) - bb[::-1].index(t):]
        elif k == rp.DRAGON_SPLIT: _, p, ch, t, _, pb, cb = ev; body[p], body[ch] = list(pb), list(cb); team[ch] = t
        elif k == rp.DRAGON_DEATH:
            if ev[1] == q:
                if ev[2] == "H" and actor in team and team[actor] != us and cur:
                    rl = len(body[actor]) if actor in body else 0
                    steps = len(action[1]) if action and action[0] == "move" else 0
                    qh = body[q][0]
                    e0 = next((e for e in cur["enemies"] if e[0] == actor), None)
                    rows.append({"map": g["map"], "rnd": rnd, "qlen": len(body[q]), "rlen": rl, "steps": steps,
                                 "free": (rl + 3) // 4 if rl else 0,
                                 "seen": e0 is not None and cheb(board, e0[1], qh) <= 3,
                                 "d0": dist(board, e0[1], qh) if e0 else -1})
                break
            body.pop(ev[1], None)
print(len(rows), "enemy rams killing our queen in", len(games), "losses")
print("rammer steps that turn (free steps):", Counter((r["steps"], r["free"]) for r in rows).most_common(8))
print("rammer within queen's 7x7 view at queen's last turn:", Counter(r["seen"] for r in rows))
print("distance rammer->queen head at queen's last turn:", sorted(Counter(r["d0"] for r in rows).items()))
print("queen length:", sorted(Counter(r["qlen"] for r in rows).items()), "rammer length:", sorted(Counter(min(r["rlen"], 10) for r in rows).items()))
print("by map:", Counter(r["map"] for r in rows).most_common())
