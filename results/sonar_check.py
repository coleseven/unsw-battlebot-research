import os
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
os.environ["BCSIM_DETERMINISTIC_V6"] = "1"; os.environ["BCSIM_CPP_INPROC"] = "1"
def one(args):
    from bcsim import match, analyze, replay as rp
    bot, mapname, seed = args
    out = Path(f"results/v8-sonar-check/{Path(bot).name}_{mapname}_{seed}.replay")
    r = match.play(Path(f"maps/server/{mapname}.map") if Path(f"maps/server/{mapname}.map").exists() else Path(f"maps/{mapname}.map"), Path(bot), Path("sparring/cpp_nicked_v75"), seed=seed, replay_to=out)
    g = analyze.game_stats(out.read_bytes()); tl = {x["round"]: x for x in g["timeline"]}
    blob = rp.decode(out.read_bytes()); rnd = 0; eat = 0; actor = None
    for ev in blob.events:
        if ev[0] == rp.ROUND_START: rnd = ev[1]
        elif ev[0] == rp.TURN_START: actor = ev[1]
    return (Path(bot).name, mapname, seed, r.winner, g["teams"]["A"]["sonar"], g["teams"]["A"]["pearls"], g["teams"]["B"]["pearls"], tl.get(100, {}).get("A"), tl.get(100, {}).get("B"), r.deaths.get("A:A", 0))
if __name__ == "__main__":
    from bcsim import match
    match.prebuild(["results/v8-dev2-bot", "results/v8-sonar-bot"])
    jobs = [(b, m, s) for m in ("Prisoners_Dilemma", "Portals", "Trauma", "Autarky") for s in (1, 2, 3, 4) for b in ("results/v8-dev2-bot", "results/v8-sonar-bot")]
    with ProcessPoolExecutor(6) as ex:
        for row in ex.map(one, jobs): print(row)
