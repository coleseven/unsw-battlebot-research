"""Like queen_stats, plus per-opponent wins and our final queen length when alive."""
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
from bcsim import official_suite
A = Path(sys.argv[1]); pool = {official_suite.canonical_map(m) for m in official_suite.CURRENT_POOL}
for v in json.loads((A / "plan.json").read_text())["variants"]:
    f = A / "runs" / v / "games.jsonl"
    if not f.exists(): continue
    c = Counter(); per = defaultdict(lambda: [0, 0]); qlen = []
    for l in f.read_text().splitlines():
        g = json.loads(l)
        us = "A" if g["bot_a"] == v else "B"; th = "B" if us == "A" else "A"
        opp = g["bot_b"] if us == "A" else g["bot_a"]
        oq = g.get(f"{us.lower()}_queen") or 0; tq = g.get(f"{th.lower()}_queen") or 0
        c["n"] += 1; c["w"] += g["winner"] == us; c["qa"] += oq > 0; c["tq"] += tq > 0
        if official_suite.canonical_map(g["map"]) in pool: c["pn"] += 1; c["pw"] += g["winner"] == us
        per[opp][0] += g["winner"] == us; per[opp][1] += 1
        if oq > 0: qlen.append(oq)
    qlen.sort()
    print(f"{v:10} wins {c['w']}/{c['n']} pool {c['pw']}/{c['pn']} queen alive {c['qa']} (median len {qlen[len(qlen)//2] if qlen else 0}) theirs {c['tq']} | " +
          " ".join(f"{k.replace('cpp_','')[:9]} {a}/{b}" for k, (a, b) in sorted(per.items())))
