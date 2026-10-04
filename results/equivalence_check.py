"""Disabled-switch equivalence: the control and a candidate base (new code, new
switches off) play identical games; every record must match exactly.
Usage: equivalence_check.py CONTROL CANDIDATE OUTDIR [opponent ...]"""
import json, sys
from pathlib import Path
from bcsim import queen_runtime

FIELDS = ("winner", "reason", "rounds", "a_dragons", "b_dragons", "a_length", "b_length",
          "a_longest", "b_longest", "deaths", "a_queen", "b_queen", "queen_death_round")

if __name__ == "__main__":
    queen_runtime.activate()
    from bcsim import bounded, official_suite
    control, cand, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    opps = [Path(o) for o in sys.argv[4:]] or [Path("sparring/cpp_nicked_v92"), Path("results/opp-raider")]
    maps = official_suite.current_maps()
    seed = 791001
    res = {}
    for bot in (control, cand):
        jobs = []
        for o in opps:
            for m in maps:
                for a, b in ((bot, o), (o, bot)):
                    jobs.append((str(m), str(a), str(b), seed, None, [o.name, m.stem, seed]))
        games = bounded.run(jobs, 12, out / bot.name, f"equivalence {bot.name}")
        res[bot.name] = {(g["map"], g["bot_a"] == bot.name, g["bot_b"] if g["bot_a"] == bot.name else g["bot_a"]):
                         {f: g.get(f) for f in FIELDS} for g in games}
    a, b = res[control.name], res[cand.name]
    diff = [k for k in a if a[k] != b.get(k)]
    print(f"{len(a)} games each; identical {len(a) - len(diff)}; different {len(diff)}", flush=True)
    for k in diff[:10]: print("  DIFF", k, a[k], b.get(k))
    print("EQUIVALENCE", "PASS" if not diff and len(a) == len(b) else "FAIL", flush=True)
