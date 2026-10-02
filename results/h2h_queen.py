"""Head-to-heads under queen rules (1.2.3): v11ms vs v10o (live), and v11ms+queen safety vs v11ms."""
import os
os.environ["BCSIM_DETERMINISTIC_V6"] = "1"; os.environ["BCSIM_CPP_INPROC"] = "1"
from bcsim import queen_runtime
queen_runtime.activate()
from pathlib import Path
from collections import Counter
from bcsim import bounded, official_suite, population, mover_teacher as mt
if __name__ == "__main__":
    qs = mt.variant("versions/v11ms", "v11ms_qsafe", {"CPP_QUEEN": 1, "CPP_QUEEN_KB": 1, "CPP_QUEEN_SAFE_MULT": 4.0,
                    "CPP_QUEEN_REACH_PEN": 400.0, "CPP_QUEEN_REACH_EXTRA": 2, "CPP_QUEEN_DEADEND": 12,
                    "CPP_QUEEN_GUARD_PEN": 200.0, "CPP_QUEEN_GUARD_R": 2})
    seeds = [511001, 511002, 511003, 511004]
    jobs = population.jobs_for([Path("versions/v11ms")], [Path("versions/v10o")], official_suite.ranked_maps(), seeds)
    jobs += population.jobs_for([qs], [Path("versions/v11ms")], official_suite.ranked_maps(), seeds)
    games = bounded.run(jobs, 12, Path("results/h2h-queen"), "h2h-queen")
    for me, opp in (("v11ms", "v10o"), ("v11ms_qsafe", "v11ms")):
        c = Counter()
        for g in games:
            if {g["bot_a"], g["bot_b"]} != {me, opp}: continue
            side = "A" if g["bot_a"] == me else "B"; th = "B" if side == "A" else "A"
            c["n"] += 1; c["w"] += g["winner"] == side; c["d"] += g["winner"] is None
            c["myq"] += (g.get(f"{side.lower()}_queen") or 0) > 0; c["thq"] += (g.get(f"{th.lower()}_queen") or 0) > 0
        print(f"{me} vs {opp}: wins {c['w']}/{c['n']} draws {c['d']}  queen alive {c['myq']} vs {c['thq']}", flush=True)
