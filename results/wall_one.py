"""Print the 7x7 surroundings of our queen at its fatal turn (wall death)."""
import sys
from pathlib import Path
from bcsim import reconstruct, replay as rp
path, us = sys.argv[1], sys.argv[2]
r = rp.decode(Path(path).read_bytes()); board = reconstruct.Board(r.map_text); w, h = board.w, board.h
body, team = {}, {}
for i, (t, c) in enumerate(board.dragons): body[i], team[i] = list(c), t
q = next(i for i in (0, 1) if team.get(i) == us)
frames = []; rnd = 0; actor = None; logs = []
def frame():
    hx, hy = body[q][0]; rows = []
    own = {c: (d, i) for d, b in body.items() for i, c in enumerate(b)}
    for dy in range(-3, 4):
        row = ""
        for dx in range(-3, 4):
            c = ((hx + dx) % w, (hy + dy) % h)
            if c in own:
                d, i = own[c]; ch = ("Q" if d == q else ("H" if i == 0 else "o")) if team[d] == us else ("E" if i == 0 else "x")
            else: ch = "."
            wl = board.edge(*c, "W") == -2
            row += ("|" if wl else " ") + ch
        rows.append(row)
        rows.append("".join((" -" if board.edge(((hx + dx) % w), (hy + dy) % h, "S") == -2 else "  ") for dx in range(-3, 4)))
    return rows
for ev in r.events:
    k = ev[0]
    if k == rp.ROUND_START: rnd = ev[1]
    elif k == rp.TURN_START:
        actor = ev[1]
        if actor == q: frames.append((rnd, frame())); logs = []
    elif k == rp.DRAGON_LOG and ev[1] == q: logs.append(ev[2])
    elif k == rp.DRAGON_ACTION and ev[1] == q: act = ev[2]
    elif k == rp.DRAGON_UPDATE:
        d, head, tail = ev[1], ev[3], ev[4]; b = body.get(d)
        if b is None: continue
        if b[0] != head: b.insert(0, head)
        if tail in b: del b[len(b) - b[::-1].index(tail):]
    elif k == rp.DRAGON_SPLIT:
        _, p, c, t, _, pb, cb = ev; body[p], body[c] = list(pb), list(cb); team[c] = t
    elif k == rp.DRAGON_DEATH:
        if ev[1] == q:
            for rr, f in frames[-2:]:
                print("round", rr); print("\n".join(f))
            print("action", act, "cause", ev[2], "logs", logs[-3:]); break
        body.pop(ev[1], None)
