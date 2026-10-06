"""How often does the v3 ranker term decide a move? v12x debug build (CPP_MOVE_DEBUG) vs
nicked v92, both sides, on MAPS; for each decision with >= 2 candidate moves, compare
argmax(total) with argmax(total - v3 part). Split by whether any candidate had food."""
import sys, re
from collections import Counter, defaultdict
from pathlib import Path
from bcsim import queen_runtime
MD = re.compile(r"MD (\d+) (\d+) (\w) food ([\d.-]+) .* v3 ([\d.-]+) tot ([\d.-]+)")
if __name__ == "__main__":
    queen_runtime.activate()
    import unswbc.engine as E
    from bcsim import match, guard, replay as rp
    out = Path("results/ranker-flip"); out.mkdir(exist_ok=True)
    stats = defaultdict(Counter)
    with guard.slot("ranker flip"):
        for m in sys.argv[1].split(","):
            for side in "AB":
                a, b = ("results/v12x-dbg", "sparring/cpp_nicked_v92") if side == "A" else ("sparring/cpp_nicked_v92", "results/v12x-dbg")
                rep = out / f"{m}-{side}.replay"
                match.play(Path(f"maps/v129/{m}.map"), Path(a), Path(b), seed=931001, replay_to=rep, debug=E.DEBUG_ALL)
                r = rp.decode(rep.read_bytes())
                dec = defaultdict(list)
                for ev in r.events:
                    if ev[0] == rp.DRAGON_LOG:
                        x = MD.search(ev[2])
                        if x: dec[(int(x[1]), int(x[2]))].append((x[3], float(x[4]), float(x[5]), float(x[6])))
                for key, opts in dec.items():
                    if len(opts) < 2: continue
                    best = max(opts, key=lambda o: o[3])[0]
                    nov3 = max(opts, key=lambda o: o[3] - o[2])[0]
                    food = any(o[1] > 0 for o in opts)
                    k = "food" if food else "nofood"
                    stats[m][k + "_n"] += 1; stats[m][k + "_flip"] += best != nov3
    for m, c in stats.items():
        f = lambda k: f"{c[k + '_flip']}/{c[k + '_n']} ({c[k + '_flip'] / max(1, c[k + '_n']):.0%})"
        print(f"{m:16} v3 flips the choice: with food in reach {f('food')}, without {f('nofood')}", flush=True)
