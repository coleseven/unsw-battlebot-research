"""v12x vs opp-raider and opp-hunter: 17 maps x 2 sides x 2 seeds; our wins and queen-alive rate."""
import json
from pathlib import Path
from bcsim import queen_runtime
if __name__ == "__main__":
    queen_runtime.activate()
    from bcsim import bounded, official_suite
    out = Path("results/sprinter-check")
    bot = Path("versions/v12x")
    for opp in (Path("results/opp-raider"), Path("results/opp-sprinter")):
        jobs = [(str(m), str(a), str(b), s, None, [opp.name, m.stem, s]) for m in official_suite.current_maps() for s in (911001, 911002) for a, b in ((bot, opp), (opp, bot))]
        games = bounded.run(jobs, 12, out / opp.name, f"sprinter check {opp.name}")
        w = qa = tq = 0
        for g in games:
            us = "a" if g["bot_a"] == "v12x" else "b"; th = "b" if us == "a" else "a"
            w += g["winner"] == us.upper(); qa += (g.get(f"{us}_queen") or 0) > 0; tq += (g.get(f"{th}_queen") or 0) > 0
        print(f"{opp.name}: v12x wins {w}/{len(games)}, our queen alive {qa}, theirs {tq}", flush=True)
