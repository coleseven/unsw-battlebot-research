import os, json
os.environ["BCSIM_DETERMINISTIC_V6"] = "1"; os.environ["BCSIM_CPP_INPROC"] = "1"
from pathlib import Path
from bcsim import guard, match, official_suite
maps = {p.stem: p for p in official_suite.ranked_maps()}
with guard.slot("v92-diag"):
    for m in ("Autarky", "schooltime", "big_empty"):
        for seed in (251001, 251002):
            out = Path(f"results/v92-diag/{m}-{seed}.replay")
            r = match.play(maps[m], Path("results/v10l-bot"), Path("sparring/cpp_nicked_v92"), seed=seed, replay_to=out)
            print(m, seed, r.winner, r.reason, "longest", r.a_longest, r.b_longest, "total", r.a_length, r.b_length, flush=True)
