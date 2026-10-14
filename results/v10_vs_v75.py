import os
from pathlib import Path
os.environ["BCSIM_DETERMINISTIC_V6"] = "1"; os.environ["BCSIM_CPP_INPROC"] = "1"
from bcsim import bounded, official_suite, population
if __name__ == "__main__":
    out = Path("results/v10-vs-v75")
    maps = official_suite.current_pool_maps()
    jobs = population.jobs_for([Path("versions/v10")], [Path("sparring/cpp_nicked_v75")], maps, [121001, 121002], out / "replays")
    games = bounded.run(jobs, 12, out, "v10-vs-v75")
    print(sum(g["winner"] == ("A" if g["bot_a"] == "v10" else "B") for g in games), "/", len(games), "v10 wins")
