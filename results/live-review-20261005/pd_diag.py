"""Prisoners Dilemma live games: growth (pearls eaten, measured as body growth), deaths by
cause and splits per 40-round window, ours vs theirs; losses vs wins."""
import json, gzip, pathlib
from collections import Counter, defaultdict
from bcsim import replay as rp, reconstruct
D = pathlib.Path("results/live-review-20261005")
games = [g for g in json.load(open(D / "games.json")) if g["grp"] == "new" and g["map"] == "Prisoners Dilemma"]
agg = {True: defaultdict(Counter), False: defaultdict(Counter)}; n = Counter()
for g in games:
    raw = (D / f"{g['game']}.replay").read_bytes()
    if raw[:2] == b"\x1f\x8b": raw = gzip.decompress(raw)
    r = rp.decode(raw); board = reconstruct.Board(r.map_text)
    body, team = {}, {}
    for i, (t, cs) in enumerate(board.dragons): body[i], team[i] = list(cs), t
    us = g["us"]; rnd = 0; n[g["won"]] += 1
    A = agg[g["won"]]
    for ev in r.events:
        k = ev[0]
        if k == rp.ROUND_START: rnd = ev[1]
        w = min(rnd // 40 * 40, 160)
        if k == rp.DRAGON_UPDATE:
            d, h, t = ev[1], ev[3], ev[4]; bb = body.get(d)
            if bb is None: continue
            before = len(bb)
            if bb[0] != h: bb.insert(0, h)
            if t in bb: del bb[len(bb) - bb[::-1].index(t):]
            if len(bb) > before: A[w][("us" if team[d] == us else "th", "grow")] += len(bb) - before
        elif k == rp.DRAGON_SPLIT:
            _, p, ch, t, _, pb, cb = ev; body[p], body[ch] = list(pb), list(cb); team[ch] = t
            A[w][("us" if t == us else "th", "split")] += 1
        elif k == rp.DRAGON_DEATH:
            d = ev[1]
            if d in team: A[w][("us" if team[d] == us else "th", "die_" + ev[2])] += 1
            body.pop(d, None)
print("PD games: wins", n[True], "losses", n[False])
for won in (False, True):
    print("== " + ("WINS" if won else "LOSSES"))
    for w in sorted(agg[won]):
        c = agg[won][w]; m = n[won]
        f = lambda s: f"grow {c[(s,'grow')]/m:4.1f} split {c[(s,'split')]/m:4.1f} W {c[(s,'die_W')]/m:4.1f} H {c[(s,'die_H')]/m:4.1f} O {c[(s,'die_O')]/m:4.1f} A {c[(s,'die_A')]/m:4.1f}"
        print(f"  r{w:3}+  US {f('us')} | THEM {f('th')}")
