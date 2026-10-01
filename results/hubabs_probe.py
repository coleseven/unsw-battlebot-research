from pathlib import Path
from collections import defaultdict
import unswbc.engine as E
from bcsim import guard, match, official_suite, replay as rp
maps = {p.stem: p for p in official_suite.ranked_maps()}
with guard.slot("hubabs"):
    for m in ("Prisoners_Dilemma", "Slithery_Fight", "Portals", "Autarky"):
        out = Path(f"results/pd-diag/hubabs-{m}.replay")
        match.play(maps[m], Path("results/v10n-hubdbg-bot"), Path("sparring/cpp_nicked_v92"), seed=321001, replay_to=out, debug=E.DEBUG_ALL)
        vals = defaultdict(list)
        for ev in rp.load(out).events:
            if ev[0] == rp.DRAGON_LOG and "HUB" in str(ev[2]):
                p = str(ev[2]).split(); rnd = int(p[1][1:]); a = float(p[p.index("abs") + 1])
                if a > 0: vals[rnd // 50 * 50].append(a)
        print(m, {r: (round(min(v), 2), round(sorted(v)[len(v)//2], 2), round(max(v), 2), len(v)) for r, v in sorted(vals.items())}, flush=True)
