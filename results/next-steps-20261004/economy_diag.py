"""Economy reconstruction for the selected cases (legal-replay reconstruction; an
analyst view, not bot inputs). Per side and per 20-round window (rounds 0-119),
plus whole game:
  nat / drop    pearls eaten that appeared on a spawner tile (natural) / elsewhere
                (dropped by deaths or feeding)
  wturns        living worker-turns (dragons other than ids 0/1)
  passed        worker-turns starting with a pearl one open step away that the
                worker did not eat that turn
  dry20         worker-turns more than 20 own turns after that worker last ate
  spawn_cov     mean number of spawner tiles within 3 steps of any of the side's
                heads, per round
  splits, deaths by cause (W kelp, H head-on, O body, S self, A no move)
  deficit_len / deficit_pop   first round from which our total length /
                dragon count stays below the opponent's for the rest of the game
Usage: economy_diag.py   (reads selected_cases.json and cases/replays)"""
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
from bcsim import reconstruct, replay as rp

W = 20; EARLY = 120

def dist(board, a, b):
    return min((a[0]-b[0]) % board.w, (b[0]-a[0]) % board.w) + min((a[1]-b[1]) % board.h, (b[1]-a[1]) % board.h)

def analyse(path, us):
    r = rp.decode(Path(path).read_bytes()); board = reconstruct.Board(r.map_text)
    them = "B" if us == "A" else "A"
    body, team = {}, {}
    for i, (t, c) in enumerate(board.dragons): body[i], team[i] = list(c), t
    pearls = set(); origin = {}
    stats = {t: defaultdict(Counter) for t in "AB"}   # window -> counter; window "all"
    last_ate = {}; own_turns = Counter()
    rnd = 0; actor = None; act = None; start_adj = None; ate = False
    lens = []   # (round, lenA, lenB, popA, popB)
    spawns = list(board.spawns)
    def win(t): return min(rnd // W * W, EARLY) if rnd < EARLY else "late"
    for ev in r.events:
        k = ev[0]
        if k == rp.ROUND_START:
            rnd = ev[1]
            L = {t: sum(len(b) for d, b in body.items() if team[d] == t) for t in "AB"}
            P = {t: sum(1 for d in body if team[d] == t) for t in "AB"}
            lens.append((rnd, L[us], L[them], P[us], P[them]))
            for t in "AB":
                heads = [b[0] for d, b in body.items() if team[d] == t]
                cov = sum(1 for s in spawns if any(dist(board, s, h) <= 3 for h in heads))
                for wkey in (win(t), "all"):
                    stats[t][wkey]["cov_sum"] += cov; stats[t][wkey]["rounds"] += 1
        elif k == rp.TILE_CHANGE:
            x, y, has = ev[1], ev[2], ev[3]
            if has:
                pearls.add((x, y)); origin[(x, y)] = "nat" if (x, y) in board.spawns else "drop"
            else:
                if (x, y) in pearls and actor in body:
                    t = team[actor]
                    o = origin.get((x, y), "drop")
                    for wkey in (win(t), "all"): stats[t][wkey][o] += 1
                    last_ate[actor] = own_turns[actor]; ate = True
                pearls.discard((x, y))
        elif k == rp.TURN_START:
            actor = ev[1]; ate = False; start_adj = None
            if actor in body:
                t = team[actor]; own_turns[actor] += 1
                if actor > 1:
                    hx, hy = body[actor][0]
                    adj = any((c := board.dest(hx, hy, d)) is not None and c in pearls for d in "NESW")
                    start_adj = adj
                    for wkey in (win(t), "all"):
                        stats[t][wkey]["wturns"] += 1
                        if own_turns[actor] - last_ate.get(actor, 0) > 20: stats[t][wkey]["dry20"] += 1
        elif k == rp.DRAGON_ACTION:
            pass
        elif k == rp.DRAGON_UPDATE:
            d, head, tail = ev[1], ev[3], ev[4]; b = body.get(d)
            if b is None: continue
            if b[0] != head: b.insert(0, head)
            if tail in b: del b[len(b) - b[::-1].index(tail):]
        elif k == rp.DRAGON_SPLIT:
            _, p, c, t, _, pb, cb = ev; body[p], body[c] = list(pb), list(cb); team[c] = t
            last_ate[c] = own_turns[c]
            for wkey in (win(t), "all"): stats[t][wkey]["splits"] += 1
        elif k == rp.DRAGON_DEATH:
            d, why = ev[1], ev[2]
            if d in team:
                for wkey in (win(team[d]), "all"): stats[team[d]][wkey]["death_" + why] += 1
            body.pop(d, None)
        # close a worker turn: passed-over pearl
        if k in (rp.TURN_START, rp.ROUND_START) and False: pass
        if k == rp.TURN_START and False: pass
        if k == rp.DRAGON_UPDATE and ev[1] == actor and start_adj and not ate and actor in team and actor > 1:
            for wkey in (win(team[actor]), "all"): stats[team[actor]][wkey]["passed"] += 1
            start_adj = None
    def first_persistent(i, j):
        bad = None
        for row in lens:
            if row[i] < row[j]:
                if bad is None: bad = row[0]
            else: bad = None
        return bad
    return {"us": us, "stats": {t: {w: dict(c) for w, c in s.items()} for t, s in stats.items()},
            "deficit_len": first_persistent(1, 2), "deficit_pop": first_persistent(3, 4),
            "rounds": rnd, "end": lens[-1] if lens else None, "lens": lens[::10]}

if __name__ == "__main__":
    D = Path("results/next-steps-20261004")
    cases = json.load(open(D / "selected_cases.json"))
    out = []
    for c in cases:
        a, b = ("base", c["opponent"]) if c["side"] == "A" else (c["opponent"], "base")
        rep = D / "cases/replays" / f"{a}-vs-{b}-{c['map']}-s{c['seed']}.replay"
        res = analyse(rep, c["side"])
        out.append({**c, **res})
    (D / "economy_cases.json").write_text(json.dumps(out, indent=1))
    print(len(out), "cases analysed")
