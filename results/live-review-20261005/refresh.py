"""Incremental refresh of live v12x games (since 2026-10-05T14:04Z) into games.json, plus a summary."""
import json, pathlib, gzip, statistics
from collections import Counter, defaultdict
from bcsim import scrape, analyze
out = pathlib.Path("results/live-review-20261005")
games = json.load(open(out / "games.json"))
known = {g["game"] for g in games}; seen_b = {g["battle"] for g in games}
new_battles = []
for page in range(1, 40):
    p = scrape.battle_page(page, team=590, ranked_only=True)
    bs = [b for b in p["battles"] if b["at"] >= "2026-10-05T14:04"]
    new_battles += bs
    if len(bs) < len(p["battles"]) or not p["battles"]: break
for b in new_battles:
    if b["id"] in seen_b: continue
    d = scrape.battle_games(b["id"]); m = d["battle"]["match"]; us = "A" if m["teamAId"] == 590 else "B"
    th = "b" if us == "A" else "a"
    for g in d["games"]:
        if not g.get("hasReplay") or g["id"] in known: continue
        blob = scrape.fetch(f"{scrape.SITE}/api/matches/{g['id']}/replay"); (out / f"{g['id']}.replay").write_bytes(blob)
        raw = gzip.decompress(blob) if blob[:2] == b"\x1f\x8b" else blob
        s = analyze.game_stats(raw); t2 = "B" if us == "A" else "A"
        q = s["teams"][us]["queen"]["alive"]; tq = s["teams"][t2]["queen"]["alive"]; end = (s["end"] or "").lower()
        cls = "elim" if "elim" in end else "onlyOurs" if q and not tq else "onlyTheirs" if tq and not q else "both" if q and tq else "none"
        games.append({"grp": "new", "battle": b["id"], "at": b["at"], "opp": b[th]["name"], "opp_elo": b[th]["elo"], "game": g["id"], "map": g["mapName"], "us": us, "won": g["winner"] == us.lower(), "cls": cls})
json.dump(games, open(out / "games.json", "w"), indent=0)
gg = [g for g in games if g["grp"] == "new"]
lb = new_battles[0]; ours = lb["a"] if lb["a"]["id"] == 590 else lb["b"]
print(f"v12x games {len(gg)} in {len({g['battle'] for g in gg})} battles: won {sum(g['won'] for g in gg)} ({sum(g['won'] for g in gg)/len(gg):.0%}); mean opp elo {statistics.mean(g['opp_elo'] for g in gg):.0f}; latest our elo {ours['elo']} at {lb['at'][:16]}")
c = Counter((g["cls"], g["won"]) for g in gg)
print("classes:", {k: f"{c[(k, True)]}-{c[(k, False)]}" for k in ("elim", "onlyOurs", "onlyTheirs", "both", "none")})
m = defaultdict(lambda: [0, 0])
for g in gg: m[g["map"]][0] += g["won"]; m[g["map"]][1] += 1
print("maps:", " | ".join(f"{k} {a}/{b} ({a/b:.0%})" for k, (a, b) in sorted(m.items(), key=lambda kv: kv[1][0] / kv[1][1])))
