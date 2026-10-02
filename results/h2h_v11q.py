"""Head-to-heads under queen rules (1.2.3): v11ms vs v10o (live), and v11ms+queen safety vs v11ms."""
import os
os.environ["BCSIM_DETERMINISTIC_V6"] = "1"; os.environ["BCSIM_CPP_INPROC"] = "1"
from bcsim import queen_runtime
queen_runtime.activate()
from pathlib import Path
from collections import Counter
from bcsim import bounded, official_suite, population, mover_teacher as mt
if __name__ == "__main__":
    qs = Path("versions/v11q")
    seeds = [551001, 551002, 551003, 551004]
    jobs = population.jobs_for([Path("versions/v11q")], [Path("versions/v10o")], official_suite.ranked_maps(), seeds)
    jobs += population.jobs_for([qs], [Path("versions/v11ms")], official_suite.ranked_maps(), seeds)
    games = bounded.run(jobs, 12, Path("results/h2h-v11q"), "h2h-queen")
    for me, opp in (("v11q", "v10o"), ("v11q", "v11ms")):
        c = Counter()
        for g in games:
            if {g["bot_a"], g["bot_b"]} != {me, opp}: continue
            side = "A" if g["bot_a"] == me else "B"; th = "B" if side == "A" else "A"
            c["n"] += 1; c["w"] += g["winner"] == side; c["d"] += g["winner"] is None
            c["myq"] += (g.get(f"{side.lower()}_queen") or 0) > 0; c["thq"] += (g.get(f"{th.lower()}_queen") or 0) > 0
        print(f"{me} vs {opp}: wins {c['w']}/{c['n']} draws {c['d']}  queen alive {c['myq']} vs {c['thq']}", flush=True)
