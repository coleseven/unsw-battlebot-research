"""Read-only check for the final writeup: sample battles after the 7 Oct 23:10 UTC upload,
download replays, and look for v12z's signatures (paid sprint steps by our dragons, sprint
rams on the enemy queen, paid queen flight). Saves results/live-review-final/games.json."""
import json, gzip, pathlib
from collections import Counter
from bcsim import scrape, analyze, replay as rp, reconstruct
out = pathlib.Path("results/live-review-final"); out.mkdir(exist_ok=True)
rows = [r for r in json.load(open("results/final_ladder_battles.json")) if r["games"] == 5 and r["at"] >= "2026-10-07T23:10"]
rows.sort(key=lambda r: r["at"])
pick = rows[:6] + rows[len(rows)//2 - 3: len(rows)//2 + 3] + rows[-8:]
games = []
for b in pick:
    d = scrape.battle_games(b["id"]); m = d["battle"]["match"]; us = "A" if m["teamAId"] == 590 else "B"; th = "B" if us == "A" else "A"
    for g in d["games"]:
        if not g.get("hasReplay"): continue
        f = out / f"{g['id']}.replay"
        if not f.exists(): f.write_bytes(scrape.fetch(f"{scrape.SITE}/api/matches/{g['id']}/replay"))
        raw = f.read_bytes(); raw = gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw
        r = rp.decode(raw); board = reconstruct.Board(r.map_text)
        body, team = {}, {}
        for i, (t, cs) in enumerate(board.dragons): body[i], team[i] = list(cs), t
        oq = next(i for i in (0, 1) if team.get(i) == us); tq = next(i for i in (0, 1) if team.get(i) == th)
        c = Counter(); actor = None; action = None; start_len = 0; rnd = 0; events = []
        for ev in r.events:
            k = ev[0]
            if k == rp.ROUND_START: rnd = ev[1]
            elif k == rp.TURN_START:
                actor = ev[1]; action = None; start_len = len(body.get(actor, []))
            elif k == rp.DRAGON_ACTION and ev[1] == actor:
                action = ev[2]
                if action and action[0] == "move" and team.get(actor) == us:
                    free = (start_len + 3) // 4
                    if len(action[1]) > free:
                        c["our_paid_moves"] += 1
                        if actor == oq: c["queen_paid_flight"] += 1; events.append((rnd, "queen paid move", action[1], start_len))
            elif k == rp.DRAGON_UPDATE:
                dd, h, t = ev[1], ev[3], ev[4]; bb = body.get(dd)
                if bb is None: continue
                if bb[0] != h: bb.insert(0, h)
                if t in bb: del bb[len(bb) - bb[::-1].index(t):]
            elif k == rp.DRAGON_SPLIT:
                _, p, ch, t, _, pb, cb = ev; body[p], body[ch] = list(pb), list(cb); team[ch] = t
            elif k == rp.DRAGON_DEATH:
                dd, why = ev[1], ev[2]
                if dd == tq and why == "H" and actor is not None and team.get(actor) == us and actor != dd:
                    paid = action and action[0] == "move" and len(action[1]) > (start_len + 3) // 4
                    c["their_queen_rammed_by_us"] += 1; c["...with a paid step"] += bool(paid)
                    events.append((rnd, "we rammed their queen", action[1] if action else None, start_len, "paid" if paid else "free"))
                if dd == oq and why == "H" and actor is not None and team.get(actor) == th:
                    c["our_queen_rammed"] += 1; events.append((rnd, "our queen rammed", action[1] if action else None, start_len))
                body.pop(dd, None)
        s = analyze.game_stats(raw)
        q = s["teams"][us]["queen"]["alive"]; tqa = s["teams"][th]["queen"]["alive"]; end = (s["end"] or "").lower()
        cls = "elim" if "elim" in end else "onlyOurs" if q and not tqa else "onlyTheirs" if tqa and not q else "both" if q and tqa else "none"
        games.append({"battle": b["id"], "at": b["at"], "opp": b["opp"], "opp_elo": b["opp_elo"], "game": g["id"], "map": g["mapName"], "us": us,
                      "won": g["winner"] == us.lower(), "cls": cls, "rounds": s["rounds"], "counts": dict(c), "events": events[:12],
                      "final": {"ours": s["teams"][us]["final"], "theirs": s["teams"][th]["final"]}})
json.dump(games, open(out / "games.json", "w"), indent=0, default=str)
tot = Counter()
for g in games: tot.update(g["counts"])
print(len(games), "games in", len(pick), "battles; won", sum(g["won"] for g in games))
print("totals:", dict(tot))
print("games with any paid move by us:", sum(1 for g in games if g["counts"].get("our_paid_moves")), "/", len(games))
