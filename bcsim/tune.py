"""CMA-ES parameter tuning for any bot whose numbers live in one parameter file.

Prepare (freezes the base bot, opponents, maps and search space):
    python -m bcsim.tune --prepare --base results/v61b-goal-bot --params core_params.py \\
        --space tune_space.json --vs sparring/nicked versions/v6 --maps screen
Run or resume:
    python -m bcsim.tune RESULT_DIR --run [--workers N]

The parameter file may be Python (`NAME = value`) or C/C++
(`constexpr ... NAME = value;` or `#define NAME value`); only the named numbers
are rewritten in each candidate copy. The space file maps NAME -> [low, high]
or [low, high, "int"]; CMA-ES works in [0, 1] per parameter.

Objective (V6_CORE_PLAN.md section 4.2): for every game, the time-averaged
team-length share margin (bcsim.margin.game_margin); per map, the mean over
opponents and sides; F = mean over maps + 0.25 * worst map. Any game error
scores the candidate F = -2. Games are deterministic, so one seed is used.
Every generation is checkpointed (CMA state plus every evaluated vector).
Set BCSIM_DETERMINISTIC_V6=1 for Python v6-core bots (judge-calibrated clock).
"""

from __future__ import annotations

import argparse
import json
import os
import pickle
import re
import shutil
import statistics
import uuid
from datetime import datetime
from pathlib import Path

from . import analyze, bounded, margin, official_suite, population
from .paths import RESULTS, bot_hash, resolve_bot

SCREEN = ("default_small", "Devil", "queen_of_spades", "trophy", "big_empty")


def write_params(path: Path, values: dict) -> None:
    text = path.read_text(encoding="utf8")
    for name, value in values.items():
        literal = repr(value) if isinstance(value, float) else str(value)
        patterns = (
            (rf"^({re.escape(name)}\s*=\s*)[-+0-9.eE]+", r"\g<1>" + literal),                   # Python
            (rf"^(\s*(?:static\s+)?constexpr\s+[\w:<> ]+\s+{re.escape(name)}\s*=\s*)[-+0-9.eE]+(f?\s*;)",
             r"\g<1>" + literal + r"\g<2>"),                                                     # C++
            (rf"^(\s*#\s*define\s+{re.escape(name)}\s+)[-+0-9.eE]+", r"\g<1>" + literal),        # C macro
        )
        for pattern, repl in patterns:
            text, count = re.subn(pattern, repl, text, count=1, flags=re.M)
            if count:
                break
        else:
            raise ValueError(f"{name} not found as a numeric setting in {path}")
    path.write_bytes(text.encode("utf8"))


def decode(x, space):
    values = {}
    for xi, (name, spec) in zip(x, space.items()):
        low, high = spec[0], spec[1]
        v = float(low + min(1.0, max(0.0, float(xi))) * (high - low))
        values[name] = int(round(v)) if len(spec) > 2 and spec[2] == "int" else float(round(v, 4))
    return values


def encode(values, space):
    return [(values[name] - spec[0]) / (spec[1] - spec[0]) for name, spec in space.items()]


def read_current(path: Path, space) -> dict:
    text = path.read_text(encoding="utf8")
    out = {}
    for name, spec in space.items():
        m = (re.search(rf"^{re.escape(name)}\s*=\s*([-+0-9.eE]+)", text, re.M) or
             re.search(rf"constexpr\s+[\w:<> ]+\s+{re.escape(name)}\s*=\s*([-+0-9.eE]+)", text) or
             re.search(rf"#\s*define\s+{re.escape(name)}\s+([-+0-9.eE]+)", text))
        if not m:
            raise ValueError(f"{name} not found in {path}")
        out[name] = float(m.group(1))
    return out


def score(games, candidate):
    per_map = {}
    for game in games:
        if game.get("error"):
            return -2.0, {"error": game["error"]}
        side = "A" if game["bot_a"] == candidate else "B"
        stats = analyze.game_stats(Path(game["replay"]).read_bytes())
        per_map.setdefault(game["map"].lower(), []).append(margin.game_margin(stats, side)["margin"])
    means = {m: statistics.fmean(v) for m, v in per_map.items()}
    return statistics.fmean(means.values()) + 0.25 * min(means.values()), means


def prepare(args):
    base = resolve_bot(args.base)
    space = json.loads(Path(args.space).read_text(encoding="utf8"))
    maps = official_suite.official_maps()
    if args.maps == "screen":
        maps = [m for m in maps if m.stem in SCREEN]
    elif args.maps != "all":
        wanted = {name.strip().lower() for name in args.maps.split(",")}
        maps = [m for m in maps if m.stem.lower() in wanted]
        if len(maps) != len(wanted):
            raise ValueError(f"unknown map in {args.maps}")
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-tune-" + uuid.uuid4().hex[:6])
    out.mkdir()
    population.snapshot(base, out / "base")
    opponents = []
    for source in args.vs:
        dest = out / "opponents" / resolve_bot(source).name
        population.snapshot(resolve_bot(source), dest)
        opponents.append(dest)
    (out / "maps").mkdir()
    for m in maps:
        shutil.copy2(m, out / "maps" / m.name)
    start = read_current(out / "base" / args.params, space)
    population.write_json(out / "plan.json", {
        "base": str(base), "base_hash": bot_hash(out / "base"), "params": args.params,
        "space": space, "start": start, "opponents": [o.name for o in opponents],
        "maps": [m.stem for m in maps], "seed": args.seed, "popsize": args.popsize,
        "generations": args.gens, "sigma": args.sigma,
        "deterministic_v6_clock": os.environ.get("BCSIM_DETERMINISTIC_V6") == "1"})
    print(out)


def run(out: Path, workers: int):
    import cma
    plan = json.loads((out / "plan.json").read_text(encoding="utf8"))
    if (os.environ.get("BCSIM_DETERMINISTIC_V6") == "1") != plan["deterministic_v6_clock"]:
        raise ValueError("BCSIM_DETERMINISTIC_V6 must match the plan")
    space = plan["space"]
    maps = [out / "maps" / f"{m}.map" for m in plan["maps"]]
    opponents = [out / "opponents" / name for name in plan["opponents"]]
    state = out / "cma.pkl"
    if state.exists():
        es = pickle.loads(state.read_bytes())
    else:
        x0 = [min(1.0, max(0.0, v)) for v in encode(plan["start"], space)]
        es = cma.CMAEvolutionStrategy(x0, plan["sigma"], {
            "popsize": plan["popsize"], "bounds": [0, 1], "seed": 1, "verbose": -9,
            "tolflatfitness": 10, "tolfun": 1e-12})
    log = out / "evaluations.jsonl"
    while es.countiter < plan["generations"] and not es.stop():
        gen = es.countiter
        xs = es.ask()
        gen_dir = out / f"gen{gen:03d}"
        if gen_dir.exists():
            shutil.rmtree(gen_dir)   # an interrupted generation is replayed whole
        candidates = []
        for i, x in enumerate(xs):
            bot = gen_dir / "bots" / f"c{i:02d}"
            population.snapshot(out / "base", bot)
            write_params(bot / plan["params"], decode(x, space))
            candidates.append(bot)
        jobs = population.jobs_for(candidates, opponents, maps, [plan["seed"]], gen_dir / "replays")
        games = bounded.run(jobs, workers, gen_dir, f"gen{gen}")
        fitness, rows = [], []
        for i, bot in enumerate(candidates):
            mine = [g for g in games if bot.name in (g["bot_a"], g["bot_b"])]
            f, detail = score(mine, bot.name)
            wins = sum(g["winner"] == ("A" if g["bot_a"] == bot.name else "B") for g in mine)
            fitness.append(-f)   # CMA-ES minimises
            rows.append({"gen": gen, "cand": bot.name, "F": f, "wins": wins, "games": len(mine),
                         "params": decode(xs[i], space), "per_map": detail})
        es.tell(xs, fitness)
        with log.open("a", encoding="utf8") as fh:
            for row in rows:
                fh.write(json.dumps(row) + "\n")
        state.write_bytes(pickle.dumps(es))
        shutil.rmtree(gen_dir / "replays", ignore_errors=True)   # keep scores, drop replays
        best = max(rows, key=lambda r: r["F"])
        print(f"gen {gen}: best F {best['F']:+.3f} ({best['wins']}/{best['games']} wins) "
              f"mean F {statistics.fmean(r['F'] for r in rows):+.3f}", flush=True)
    rows = [json.loads(line) for line in log.read_text(encoding="utf8").splitlines()]
    best = max(rows, key=lambda r: r["F"])
    population.write_json(out / f"best-{datetime.now():%H%M%S}.json", best)
    print("best overall:", json.dumps(best["params"]), f"F {best['F']:+.3f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("result", nargs="?", type=Path)
    ap.add_argument("--prepare", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--base")
    ap.add_argument("--params")
    ap.add_argument("--space")
    ap.add_argument("--vs", nargs="+")
    ap.add_argument("--maps", default="screen",
                    help="screen (5 hardest), all (11), or comma-separated map stems")
    ap.add_argument("--seed", type=int, default=53001)
    ap.add_argument("--popsize", type=int, default=12)
    ap.add_argument("--gens", type=int, default=25)
    ap.add_argument("--sigma", type=float, default=0.25)
    ap.add_argument("--workers", type=int, default=official_suite.DEFAULT_WORKERS)
    a = ap.parse_args()
    if a.prepare:
        if not (a.base and a.params and a.space and a.vs):
            ap.error("--prepare needs --base, --params, --space and --vs")
        prepare(a)
    elif a.run and a.result:
        run(a.result, a.workers)
    else:
        ap.error("use --prepare ... or RESULT --run")


if __name__ == "__main__":
    main()
