"""Per-variant wins and queen survival for an ablate dir (queen rules)."""
import json, sys
from collections import Counter
from pathlib import Path
from bcsim import official_suite
A = Path(sys.argv[1]); pool = {official_suite.canonical_map(m) for m in official_suite.CURRENT_POOL}
for v in json.loads((A / "plan.json").read_text())["variants"]:
    f = A / "runs" / v / "games.jsonl"
    if not f.exists(): continue
    c = Counter(); qd = []
    for l in f.read_text().splitlines():
        g = json.loads(l)
        us = "A" if g["bot_a"] == v else "B"; th = "B" if us == "A" else "A"
        opp = g["bot_b"] if us == "A" else g["bot_a"]
        oq = g.get(f"{us.lower()}_queen") or 0; tq = g.get(f"{th.lower()}_queen") or 0
        c["n"] += 1; c["w"] += g["winner"] == us
        c["qalive"] += oq > 0; c["tq"] += tq > 0
        strong = any(s in opp for s in ("v92", "v75", "lab"))
        if strong: c["sn"] += 1; c["sw"] += g["winner"] == us
        if official_suite.canonical_map(g["map"]) in pool: c["pn"] += 1; c["pw"] += g["winner"] == us
        d = g.get("queen_death_round", {}).get(us)
        qd.append(d if d is not None else 500)
    qd.sort()
    print(f"{v:12} wins {c['w']}/{c['n']}  pool {c['pw']}/{c['pn']}  strong {c['sw']}/{c['sn']}  our queen alive {c['qalive']}  theirs {c['tq']}  queen death median {qd[len(qd)//2]}")
