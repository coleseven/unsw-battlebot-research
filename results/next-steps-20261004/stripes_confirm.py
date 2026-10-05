"""v11t vs a candidate on Stripes only: 11 opponents x 2 sides x seeds; prints wins."""
import json, sys
from pathlib import Path
from bcsim import queen_runtime
if __name__ == "__main__":
    queen_runtime.activate()
    from bcsim import bounded
    cand, out = Path(sys.argv[1]), Path(sys.argv[2])
    seeds = range(881001, 881007)
    opps = [Path(o) for o in ("sparring/cpp_nicked_v92", "sparring/cpp_nicked_v75", "sparring/cpp_leviathan3", "results/v7-base-bot",
                              "sparring/nicked_v44", "sparring/nicked_lab", "results/opp-careful-queen", "results/opp-raider",
                              "results/opp-growth-queen", "results/opp-economy", "versions/v11q")]
    m = Path("maps/v129/stripes.map")
    res = {}
    for bot in (Path("versions/v11t"), cand):
        jobs = [(str(m), str(a), str(b), s, None, [o.name, "stripes", s]) for o in opps for s in seeds for a, b in ((bot, o), (o, bot))]
        games = bounded.run(jobs, 12, out / bot.name, f"stripes {bot.name}")
        w = sum(g["winner"] == ("A" if g["bot_a"] == bot.name else "B") for g in games)
        res[bot.name] = (w, len(games)); print(bot.name, "wins", w, "/", len(games), flush=True)
    print("STRIPES", res, flush=True)
