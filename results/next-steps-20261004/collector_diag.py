"""Late-game conversion in both-queens-dead games (C10 base, replays in late/).
Per game, our side:
  donations      own worker deaths on an empty action / suicide (the feeding mechanic:
                 the dead dragon drops pearls); donor length, round
  pickup         each pearl appearing on the donor's cells that turn, then eaten by:
                 recipient (the longest own dragon whose head was within 4 (the feeding range) of the
                 donor's head), other own, enemy, or never (by game end)
  peak           the longest length any own dragon reached after round 300, and
                 whether that dragon was alive at the end
  margin         our longest minus their longest at rounds 300 / 400 / 450 / end
Class (losses):  delivered_then_died: some own dragon after round 300 was longer
                 than their final longest, then died
                 could_not_deliver: our end total length > their final longest,
                 but no own dragon ever exceeded it
                 could_not_produce: otherwise"""
import json, sys
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from bcsim import reconstruct, replay as rp

D = Path("results/next-steps-20261004")

def dist(board, a, b):
    return min((a[0]-b[0]) % board.w, (b[0]-a[0]) % board.w) + min((a[1]-b[1]) % board.h, (b[1]-a[1]) % board.h)

def analyse(args):
    path, us = args
    r = rp.decode(Path(path).read_bytes()); board = reconstruct.Board(r.map_text)
    th = "B" if us == "A" else "A"
    body, team = {}, {}
    for i, (t, c) in enumerate(board.dragons): body[i], team[i] = list(c), t
    rnd = 0; actor = None; action = None
    pending = None            # (donor cells, recipient id, round) for the current turn
    donated = {}              # pearl cell -> (recipient, round)
    pickups = Counter(); donations = []; pick_delay = []
    peak = {}                 # dragon -> max length after r300
    margins = {}
    for ev in r.events:
        k = ev[0]
        if k == rp.ROUND_START:
            rnd = ev[1]
            if rnd in (300, 400, 450):
                lo = max((len(b) for d, b in body.items() if team[d] == us), default=0)
                lt = max((len(b) for d, b in body.items() if team[d] == th), default=0)
                margins[rnd] = lo - lt
            if rnd >= 300:
                for d, b in body.items():
                    if team[d] == us: peak[d] = max(peak.get(d, 0), len(b))
        elif k == rp.TURN_START:
            actor, action, pending = ev[1], None, None
        elif k == rp.DRAGON_ACTION:
            if ev[1] == actor: action = ev[2]
        elif k == rp.TILE_CHANGE:
            x, y, has = ev[1], ev[2], ev[3]
            if has and pending and (x, y) in pending[0]:
                donated[(x, y)] = (pending[1], pending[2])
            elif not has and (x, y) in donated:
                rec, r0 = donated.pop((x, y))
                who = "enemy" if team.get(actor) == th else ("recipient" if actor == rec and rec is not None else "other_own")
                pickups[who] += 1
                if who == "recipient": pick_delay.append(rnd - r0)
        elif k == rp.DRAGON_UPDATE:
            d, head, tail = ev[1], ev[3], ev[4]; b = body.get(d)
            if b is None: continue
            if b[0] != head: b.insert(0, head)
            if tail in b: del b[len(b) - b[::-1].index(tail):]
        elif k == rp.DRAGON_SPLIT:
            _, p, c, t, _, pb, cb = ev; body[p], body[c] = list(pb), list(cb); team[c] = t
        elif k == rp.DRAGON_DEATH:
            d, why = ev[1], ev[2]
            if d in body and team[d] == us and d == actor and why == "A" and (action is None or action[0] == "suicide"):
                b = body[d]; h = b[0]
                near = [(len(ob), o) for o, ob in body.items() if team[o] == us and o != d and dist(board, ob[0], h) <= 4]
                rec = max(near)[1] if near else None
                donations.append({"round": rnd, "len": len(b), "recipient_len": max(near)[0] if near else 0})
                pending = (set(b), rec, rnd)
            body.pop(d, None)
    lo = max((len(b) for d, b in body.items() if team[d] == us), default=0)
    lt = max((len(b) for d, b in body.items() if team[d] == th), default=0)
    margins["end"] = lo - lt
    total_us = sum(len(b) for d, b in body.items() if team[d] == us)
    pk = max(peak.values(), default=0)
    peak_alive = any(d in body for d, v in peak.items() if v == pk) if pk else False
    pickups["never"] += len(donated)
    return {"donations": donations, "pickups": dict(pickups), "pick_delay": pick_delay, "margins": margins,
            "peak_after300": pk, "peak_alive": peak_alive, "their_final_longest": lt, "our_final_longest": lo,
            "our_total": total_us}

def classify(x, won):
    if won: return "win"
    if x["peak_after300"] > x["their_final_longest"] and not x["peak_alive"]: return "delivered_then_died"
    if x["our_total"] > x["their_final_longest"]: return "could_not_deliver"
    return "could_not_produce"

if __name__ == "__main__":
    cases = json.load(open(D / "late_cases.json"))
    jobs = []
    for c in cases:
        a, b = ("base", c["opponent"]) if c["side"] == "A" else (c["opponent"], "base")
        jobs.append((str(D / "late/replays" / f"{a}-vs-{b}-{c['map']}-s{c['seed']}.replay"), c["side"]))
    with ProcessPoolExecutor(4) as ex:
        res = list(ex.map(analyse, jobs, chunksize=8))
    rows = []
    for c, x in zip(cases, res):
        x.update(c); x["cls"] = classify(x, c["class"] == "both_dead_win"); rows.append(x)
    (D / "collector_cases.json").write_text(json.dumps(rows, indent=0))
    for grp in ("both_dead_loss", "both_dead_win"):
        g = [x for x in rows if x["class"] == grp]
        don = [len(x["donations"]) for x in g]
        pk = Counter(); [pk.update(x["pickups"]) for x in g]
        print(f"== {grp}: {len(g)} games; donations per game mean {sum(don)/len(g):.1f} (games with any {sum(1 for n in don if n)});"
              f" donated pearls eaten by {dict(pk)}")
        if grp == "both_dead_loss": print("   classes:", Counter(x["cls"] for x in g).most_common())
        for key in (300, 400, 450, "end"):
            ms = sorted(x["margins"].get(key, x["margins"].get(str(key), 0)) for x in g)
            print(f"   longest margin at {key}: median {ms[len(ms)//2]}, >0 in {sum(m > 0 for m in ms)}")
    loss = [x for x in rows if x["class"] == "both_dead_loss"]
    for cls in ("delivered_then_died", "could_not_deliver", "could_not_produce"):
        g = [x for x in loss if x["cls"] == cls]
        if not g: continue
        print(f"-- {cls}: {len(g)}; maps {Counter(x['map'] for x in g).most_common(5)}; donations/game {sum(len(x['donations']) for x in g)/len(g):.1f};"
              f" mean peak after 300 {sum(x['peak_after300'] for x in g)/len(g):.1f} vs their final longest {sum(x['their_final_longest'] for x in g)/len(g):.1f}")
