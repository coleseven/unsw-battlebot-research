"""Read-only: fetch our ranked battle list back to 2026-10-01 and save it (for the final writeup)."""
import json
from bcsim import scrape
rows = []
for page in range(1, 140):
    p = scrape.battle_page(page, team=590, ranked_only=True)
    if not p["battles"]: break
    stop = False
    for b in p["battles"]:
        us = "a" if b["a"]["id"] == 590 else "b"; th = "b" if us == "a" else "a"
        res = b["resultsA"] if us == "a" else ["win" if r == "loss" else "loss" if r == "win" else r for r in b["resultsA"]]
        rows.append({"id": b["id"], "at": b["at"], "opp": b[th]["name"], "opp_elo": b[th]["elo"], "our_elo": b[us]["elo"],
                     "wins": res.count("win"), "games": len(res), "delta": b.get("eloChange" + us.upper())})
        if b["at"] < "2026-10-01": stop = True
    if stop: break
json.dump(rows, open("results/final_ladder_battles.json", "w"), indent=0)
print(len(rows), "battles", rows[-1]["at"], "->", rows[0]["at"])
