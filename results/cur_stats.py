"""Per-variant stats for current-map runs: wins, queen outcome classes, per opponent and map."""
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
A = Path(sys.argv[1])
for v in json.loads((A / "plan.json").read_text())["variants"]:
    f = A / "runs" / v / "games.jsonl"
    if not f.exists(): continue
    c = Counter(); per = defaultdict(lambda: [0, 0]); maps = defaultdict(lambda: [0, 0])
    for l in f.read_text().splitlines():
        g = json.loads(l); us = "A" if g["bot_a"] == v else "B"; th = "B" if us == "A" else "A"
        opp = g["bot_b"] if us == "A" else g["bot_a"]
        oq = (g.get(f"{us.lower()}_queen") or 0) > 0; tq = (g.get(f"{th.lower()}_queen") or 0) > 0
        won = g["winner"] == us
        c["n"] += 1; c["w"] += won; c["qa"] += oq; c["tq"] += tq
        cls = "elim" if g["reason"] == "elimination" else ("ours" if oq and not tq else "theirs" if tq and not oq else "both" if oq else "none")
        c[cls] += 1; c[cls + "_w"] += won
        per[opp][0] += won; per[opp][1] += 1; maps[g["map"]][0] += won; maps[g["map"]][1] += 1
    print(f"{v:10} wins {c['w']}/{c['n']}  queen alive {c['qa']} theirs {c['tq']} | elim {c['elim_w']}/{c['elim']} onlyOurs {c['ours_w']}/{c['ours']} onlyTheirs {c['theirs_w']}/{c['theirs']} both {c['both_w']}/{c['both']} none {c['none_w']}/{c['none']}")
    print("            " + " ".join(f"{k.replace('cpp_','')[:9]} {a}/{b}" for k, (a, b) in sorted(per.items())))
