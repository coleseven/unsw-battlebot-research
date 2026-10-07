"""PD: growth on the 8 fast tiles (columns 14 and 17), by team and column, rounds 0-199;
which column is 'ours' depends on side (team A starts in column 14)."""
import json, gzip, pathlib
from collections import Counter
from bcsim import replay as rp, reconstruct
D = pathlib.Path("results/live-review-20261005")
FAST = {(14,0),(17,0),(14,1),(17,1),(14,14),(17,14),(14,15),(17,15)}
games = [g for g in json.load(open(D / "games.json")) if g["grp"] == "new" and g["map"] == "Prisoners Dilemma"]
for won in (False, True):
    tot = Counter(); n = 0; firstsplit = []
    for g in [x for x in games if x["won"] == won]:
        raw = (D / f"{g['game']}.replay").read_bytes()
        if raw[:2] == b"\x1f\x8b": raw = gzip.decompress(raw)
        r = rp.decode(raw); board = reconstruct.Board(r.map_text)
        body, team = {}, {}
        for i, (t, cs) in enumerate(board.dragons): body[i], team[i] = list(cs), t
        us = g["us"]; own_col = 14 if us == "A" else 17
        big = {t: next(i for i, (tt, cs) in enumerate(board.dragons) if tt == t and len(cs) >= 10) for t in "AB"}
        rnd = 0; n += 1; fs = None
        for ev in r.events:
            k = ev[0]
            if k == rp.ROUND_START: rnd = ev[1]
            if rnd >= 200: break
            if k == rp.DRAGON_UPDATE:
                d, h, t = ev[1], ev[3], ev[4]; bb = body.get(d)
                if bb is None: continue
                before = len(bb)
                if bb[0] != h: bb.insert(0, h)
                if t in bb: del bb[len(bb) - bb[::-1].index(t):]
                if len(bb) > before and tuple(h) in FAST:
                    who = "us" if team[d] == us else "them"
                    col = "our column" if h[0] == own_col else "their column"
                    tot[(who, col)] += 1
            elif k == rp.DRAGON_SPLIT:
                _, p, ch, t, _, pb, cb = ev; body[p], body[ch] = list(pb), list(cb); team[ch] = t
                if p == big[us] and fs is None: fs = rnd
            elif k == rp.DRAGON_DEATH: body.pop(ev[1], None)
        firstsplit.append(fs)
    print(("WINS" if won else "LOSSES"), n, "games; fast-tile eats per game r0-199:", {f"{a}/{b}": round(v / n, 1) for (a, b), v in sorted(tot.items())},
          "| our big dragon first split round:", sorted(x for x in firstsplit if x is not None)[:12])
