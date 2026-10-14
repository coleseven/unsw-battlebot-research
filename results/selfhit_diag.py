import glob
from collections import Counter
from pathlib import Path
from bcsim import replay as rp, reconstruct
if __name__ == "__main__":
    kinds = Counter(); n = 0; boxed = Counter(); rel = Counter(); ages = Counter()
    for f in sorted(glob.glob("results/v9n-check/v9n-base-bot_*.replay")):
        side = Path(f).stem[-1]; n += 1
        r = rp.decode(Path(f).read_bytes()); board = reconstruct.Board(r.map_text)
        w, h = board.w, board.h
        body, team, born, parent = {}, {}, {}, {}
        for i, (t, coords) in enumerate(board.dragons): body[i], team[i], born[i] = list(coords), t, 0
        rnd = 0; actor = None; act = None; last_act = {}
        for ev in r.events:
            k = ev[0]
            if k == rp.ROUND_START: rnd = ev[1]
            elif k == rp.TURN_START: actor = ev[1]
            elif k == rp.DRAGON_ACTION: last_act[ev[1]] = ev[2]
            elif k == rp.DRAGON_SPLIT:
                _, p, c, t, _, pb, cb = ev; body[p], body[c] = list(pb), list(cb); team[c] = t; born[c] = rnd; parent[c] = p
            elif k == rp.DRAGON_UPDATE:
                d, head, tail = ev[1], ev[3], ev[4]; b = body.get(d)
                if b is None: continue
                if b[0] != head: b.insert(0, head)
                if tail in b: del b[len(b) - b[::-1].index(tail):]
            elif k == rp.DRAGON_DEATH:
                d, why = ev[1], ev[2]
                if team.get(d) == side and why in ("O", "H") and d == actor:
                    b = body.get(d, [])
                    if b:
                        hx, hy = b[0]
                        # which cell did it move into? find the occupant of its target among teammates
                        act = last_act.get(d)
                        occ = {}
                        for o, ob in body.items():
                            if o != d:
                                for c in ob: occ[c] = o
                        free = 0
                        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                            c = ((hx + dx) % w, (hy + dy) % h)
                            if c not in occ and (len(b) < 2 or c != b[1]): free += 1
                        victim = None
                        if act and act[0] == "move":
                            step = act[1][0]; ddx, ddy = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}[step]
                            victim = occ.get(((hx + ddx) % w, (hy + ddy) % h))
                        if victim is not None and team.get(victim) == side:
                            kinds[why] += 1
                            boxed["no free neighbour (forced)" if free == 0 else "had a free neighbour"] += 1
                            fam = "parent/child" if parent.get(d) == victim or parent.get(victim) == d else "sibling" if parent.get(d) is not None and parent.get(d) == parent.get(victim) else "unrelated"
                            rel[fam] += 1; ages[min(rnd - born.get(d, 0), 20) // 5 * 5] += 1
                body.pop(d, None)
    print(n, "games; own-team deaths by our moving dragon, per game:", {k: round(v / n, 1) for k, v in kinds.items()})
    print("  boxed in?", dict(boxed)); print("  relation to the teammate hit:", dict(rel)); print("  age of our dying dragon:", sorted(ages.items()))
