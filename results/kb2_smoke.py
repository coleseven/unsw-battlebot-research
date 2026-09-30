import os
os.environ["BCSIM_DETERMINISTIC_V6"] = "1"; os.environ["BCSIM_CPP_INPROC"] = "1"
from pathlib import Path
from bcsim import guard, match
with guard.slot("kb2-smoke"):
    for m in ("maps/default.map", "maps/schooltime.map"):
        for bot in ("results/v10j-bot", "results/v10j-kb2-bot"):
            r = match.play(Path(m), Path(bot), Path("sparring/cpp_nicked_v75"), seed=201001)
            print(Path(m).stem, Path(bot).name, r.winner, r.reason, "len", r.a_length, r.b_length, "longest", r.a_longest, r.b_longest, "deaths", {k: v for k, v in r.deaths.items() if k.startswith("A")})
