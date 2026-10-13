"""Round-by-round summary of one replay, for picking the moments to show.

    .venv/Scripts/python showcase/timeline.py <replay> [every=50]

Prints, per team: dragons, total length, longest dragon and queen length every N rounds,
then the key events: first split, queen deaths (round, cause, killer, paid steps), suicides
(feeding) per 100 rounds and paid sprint moves. Works on local and server (gzip) replays.
Rules assumed for "free steps": ceil(length at start of turn / 4), the queen-era rule.
"""
import gzip, sys
from collections import Counter
from pathlib import Path
from bcsim import replay as rp, reconstruct


def summarise(path, every=50):
    b = Path(path).read_bytes()
    if b[:2] == b"\x1f\x8b": b = gzip.decompress(b)
    r = rp.decode(b); board = reconstruct.Board(r.map_text)
    body, team = {}, {}
    for i, (t, cs) in enumerate(board.dragons): body[i], team[i] = list(cs), t
    queens = {team[i]: i for i in (0, 1) if i in team}
    out = {"map": r.map_name, "size": (board.w, board.h), "a": r.bot_a, "b": r.bot_b, "result": r.result,
           "snaps": [], "events": [], "suicides": Counter(), "paid": Counter(), "splits": Counter()}
    rnd = 0; actor = None; action = None; start_len = 0; first_split = {}

    def snap():
        row = {"rnd": rnd}
        for t in "AB":
            ls = [len(bb) for d, bb in body.items() if team[d] == t]
            q = queens.get(t)
            row[t] = (len(ls), sum(ls), max(ls, default=0), len(body[q]) if q in body else 0)
        out["snaps"].append(row)

    for ev in r.events:
        k = ev[0]
        if k == rp.ROUND_START:
            rnd = ev[1]
            if rnd % every == 0: snap()
        elif k == rp.TURN_START:
            actor = ev[1]; action = None; start_len = len(body.get(actor, ()))
        elif k == rp.DRAGON_ACTION and ev[1] == actor:
            action = ev[2]
            if action and action[0] == "move" and start_len:
                paid = len(action[1]) - (start_len + 3) // 4
                if paid > 0: out["paid"][(team[actor], rnd // 100)] += 1
            elif action and action[0] == "suicide":
                out["suicides"][(team.get(actor), rnd // 100)] += 1
        elif k == rp.DRAGON_UPDATE:
            d, h, t = ev[1], ev[3], ev[4]; bb = body.get(d)
            if bb is None: continue
            if bb[0] != h: bb.insert(0, h)
            if t in bb: del bb[len(bb) - bb[::-1].index(t):]
        elif k == rp.DRAGON_SPLIT:
            _, p, ch, t, _, pb, cb = ev; body[p], body[ch] = list(pb), list(cb); team[ch] = t
            out["splits"][(t, rnd // 100)] += 1
            if t not in first_split:
                first_split[t] = rnd; out["events"].append((rnd, f"first split by team {t} (dragon {p})"))
        elif k == rp.DRAGON_DEATH:
            d = ev[1]
            if d in queens.values():
                t = team[d]; who = ""
                if actor is not None and actor != d and actor in team:
                    steps = len(action[1]) if action and action[0] == "move" else 0
                    who = (f" by dragon {actor} of team {team[actor]} (length {start_len}, {steps} steps, "
                           f"{max(0, steps - (start_len + 3) // 4)} paid)")
                elif actor == d:
                    who = " on its own move" + (" (no action)" if action and action[0] == "suicide" else "")
                out["events"].append((rnd, f"QUEEN of team {t} dies, cause {ev[2]}, length {len(body.get(d, ()))}{who}"))
            body.pop(d, None)
    snap()
    return out


if __name__ == "__main__":
    o = summarise(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 50)
    print(f"{o['map']} {o['size']}  A={o['a']}  B={o['b']}  result={o['result']}")
    print("round | A dragons/total/longest/queen | B dragons/total/longest/queen")
    for s in o["snaps"]:
        print(f"{s['rnd']:5d} | {s['A'][0]:3d} {s['A'][1]:4d} {s['A'][2]:3d} q{s['A'][3]:<3d} | {s['B'][0]:3d} {s['B'][1]:4d} {s['B'][2]:3d} q{s['B'][3]:<3d}")
    for e in sorted(o["events"]): print(f"  r{e[0]}: {e[1]}")
    for name in ("splits", "suicides", "paid"):
        c = o[name]
        if c: print(f"  {name} per 100 rounds:", {t: [c.get((t, i), 0) for i in range(5)] for t in "AB"})
