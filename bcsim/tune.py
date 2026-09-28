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
opponents and sides; F = mean over maps + w * worst map (w = --worst-weight, default 0.25). Any game error
scores the candidate F = -2. With --seeds N each generation plays N fresh engine seeds (unswbc >= 1.1 seeds pearl spawns); older plans use one fixed seed.
Every generation is checkpointed (CMA state plus every evaluated vector).
Set BCSIM_DETERMINISTIC_V6=1 for Python v6-core bots (judge-calibrated clock).
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import pickle
import random
import re
import shutil
import statistics
import uuid
from concurrent.futures.process import BrokenProcessPool
from datetime import datetime
from pathlib import Path

from . import analyze, bounded, margin, official_suite, population
from .paths import RESULTS, bot_hash, resolve_bot

SCREEN = ("default_small", "Devil", "queen_of_spades", "trophy", "big_empty")


def write_params(path: Path, values: dict) -> None:
    """Rewrite named settings in a Python or C/C++ parameter file. Numbers and
    booleans (Python True/False, C++ true/false) are supported."""
    text = path.read_text(encoding="utf8")
    for name, value in values.items():
        if isinstance(value, bool):
            num = r"(?:True|False|true|false)"
            py_lit, cpp_lit = ("True", "true") if value else ("False", "false")
        else:
            num = r"[-+0-9.eE]+"
            py_lit = cpp_lit = repr(value) if isinstance(value, float) else str(value)
        patterns = (
            (rf"^({re.escape(name)}\s*=\s*){num}", r"\g<1>" + py_lit),                          # Python
            (rf"^(\s*(?:(?:static|inline)\s+)*constexpr\s+[\w:<> ]+\s+{re.escape(name)}\s*=\s*){num}(f?\s*;)",
             r"\g<1>" + cpp_lit + r"\g<2>"),                                                     # C++
            (rf"^(\s*#\s*define\s+{re.escape(name)}\s+){num}", r"\g<1>" + cpp_lit),             # C macro
        )
        for pattern, repl in patterns:
            text, count = re.subn(pattern, repl, text, count=1, flags=re.M)
            if count:
                break
        else:
            raise ValueError(f"{name} not found as a setting in {path}")
    path.write_bytes(text.encode("utf8"))


def bounds(spec):
    """(low, high, is_int) of a space entry: [low, high], [low, high, "int"], or a
    group multiplier {"low": .., "high": .., "scale": [NAME, ...]}."""
    if isinstance(spec, dict):
        return spec["low"], spec["high"], False
    return spec[0], spec[1], len(spec) > 2 and spec[2] == "int"


def decode(x, space):
    values = {}
    for xi, (name, spec) in zip(x, space.items()):
        low, high, is_int = bounds(spec)
        v = float(low + min(1.0, max(0.0, float(xi))) * (high - low))
        values[name] = int(round(v)) if is_int else float(round(v, 4))
    return values


def encode(values, space):
    out = []
    for name, spec in space.items():
        low, high, _ = bounds(spec)
        out.append((values[name] - low) / (high - low))
    return out


def expand(values, space, base_values):
    """Parameter-file settings for one candidate: a group multiplier scales each
    member weight from its base value (members must be floating-point weights);
    ordinary entries pass through."""
    out = {}
    for name, value in values.items():
        spec = space[name]
        if isinstance(spec, dict):
            for member in spec["scale"]:
                out[member] = float(round(base_values[member] * value, 4))
        else:
            out[name] = value
    return out


def _read_number(text, name, path):
    m = (re.search(rf"^{re.escape(name)}\s*=\s*([-+0-9.eE]+)", text, re.M) or
         re.search(rf"constexpr\s+[\w:<> ]+\s+{re.escape(name)}\s*=\s*([-+0-9.eE]+)", text) or
         re.search(rf"#\s*define\s+{re.escape(name)}\s+([-+0-9.eE]+)", text))
    if not m:
        raise ValueError(f"{name} not found in {path}")
    return float(m.group(1))


def read_current(path: Path, space) -> dict:
    """Start point in the space: current values, or 1.0 for group multipliers."""
    text = path.read_text(encoding="utf8")
    return {name: 1.0 if isinstance(spec, dict) else _read_number(text, name, path)
            for name, spec in space.items()}


def read_members(path: Path, space) -> dict:
    """Base values of every weight a group multiplier scales."""
    text = path.read_text(encoding="utf8")
    return {m: _read_number(text, m, path)
            for spec in space.values() if isinstance(spec, dict) for m in spec["scale"]}


def gen_seeds(plan, gen):
    """Engine seeds for one generation. unswbc >= 1.1 seeds the pearl spawns,
    so fresh seeds each generation keep CMA-ES from fitting one pearl layout;
    every candidate in a generation still plays the same seeds. Plans made
    before seeds_per_gen existed keep their single fixed seed."""
    n = plan.get("seeds_per_gen")
    if not n:
        return [plan["seed"]]
    return [plan["seed"] + gen * n + i for i in range(n)]


def _side_margins(replay):
    """Both sides' objectives for one replay (a worker job: decoding dominates scoring)."""
    stats = analyze.game_stats(Path(replay).read_bytes())
    out = {}
    for side in "AB":
        m = margin.game_margin(stats, side)
        out[side] = {"margin": m["margin"], "aligned": m["aligned"]}
    return out


def replay_margins(games, workers):
    """Margins for every error-free game's replay, decoded in parallel."""
    replays = [g["replay"] for g in games if not g.get("error") and g.get("replay")]
    if workers <= 1 or len(replays) < 2:
        return {r: _side_margins(r) for r in replays}
    from concurrent.futures import ProcessPoolExecutor
    from .guard import cap_workers, slot
    with slot("replay scoring"), ProcessPoolExecutor(max_workers=cap_workers(workers)) as ex:
        return dict(zip(replays, ex.map(_side_margins, replays, chunksize=8)))


def score(games, candidate, margins=None, objective="margin", worst_weight=0.25):
    per_map = {}
    for game in games:
        if game.get("error"):
            return -2.0, {"error": game["error"]}
        side = "A" if game["bot_a"] == candidate else "B"
        if margins is not None and game["replay"] in margins:
            value = margins[game["replay"]][side][objective]
        else:
            value = _side_margins(game["replay"])[side][objective]
        per_map.setdefault(game["map"].lower(), []).append(value)
    means = {m: statistics.fmean(v) for m, v in per_map.items()}
    return statistics.fmean(means.values()) + worst_weight * min(means.values()), means


def prepare(args):
    base = resolve_bot(args.base)
    space = json.loads(Path(args.space).read_text(encoding="utf8"))
    maps = official_suite.official_maps()
    if args.maps == "ranked":
        maps = official_suite.ranked_maps()
    elif args.maps == "current":
        maps = official_suite.current_pool_maps()
    elif args.maps == "screen":
        maps = [m for m in maps if m.stem in SCREEN]
    elif args.maps not in ("all", "ranked", "current"):
        wanted = {name.strip().lower() for name in args.maps.split(",")}
        maps = [m for m in maps if m.stem.lower() in wanted]
        if len(maps) != len(wanted):
            raise ValueError(f"unknown map in {args.maps}")
    # ladder maps outside the official suite (e.g. maps/server/Slithery_Fight.map)
    for extra in args.extra_maps:
        path = Path(extra)
        if not path.is_file():
            raise ValueError(f"missing extra map {path}")
        if official_suite.map_signature(path) in {official_suite.map_signature(m) for m in maps}:
            raise ValueError(f"{path} duplicates a map already in the pool")
        maps.append(path)
    out =RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-tune-" + uuid.uuid4().hex[:6])
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
    if args.fixed:
        # settings decided outside the search (e.g. switches settled by paired A/B tests)
        write_params(out / "base" / args.params, json.loads(args.fixed))
    start = read_current(out / "base" / args.params, space)
    members = read_members(out / "base" / args.params, space)
    population.write_json(out / "plan.json", {
        "base": str(base), "base_hash": bot_hash(out / "base"), "params": args.params,
        "space": space, "start": start, "base_values": members, "opponents": [o.name for o in opponents],
        "maps": [m.stem for m in maps], "seed": args.seed, "seeds_per_gen": args.seeds,
        "objective": args.objective, "worst_weight": args.worst_weight,
        "backend": args.backend, "eval_mean": args.eval_mean, "map_sample": args.map_sample,
        "warm_from": str(Path(args.warm_from).resolve()) if args.warm_from else None,
        "fixed": json.loads(args.fixed) if args.fixed else {},
        "unswbc": importlib.metadata.version("unswbc"), "popsize": args.popsize,
        "generations": args.gens, "sigma": args.sigma,
        "deterministic_v6_clock": os.environ.get("BCSIM_DETERMINISTIC_V6") == "1"})
    print(out)


class _PyCMA:
    """pycma backend (plans made before the backend option: the default)."""

    def __init__(self, x0, sigma, popsize, cov=None):
        import cma
        if cov is not None:
            raise ValueError("warm start needs the cmaes backend")
        opts = {"popsize": popsize, "bounds": [0, 1], "seed": 1, "verbose": -9,
                "tolflatfitness": 10, "tolfun": 1e-12}
        self.es = cma.CMAEvolutionStrategy(x0, sigma, opts)

    @property
    def gen(self):
        return self.es.countiter

    def stop(self):
        return bool(self.es.stop())

    def ask(self):
        return [list(map(float, x)) for x in self.es.ask()]

    def tell(self, xs, fitness):
        self.es.tell(xs, fitness)

    @property
    def mean(self):
        return [float(v) for v in self.es.mean]


class _CMAesLRA:
    """cmaes (CyberAgentAILab) backend with learning-rate adaptation
    (Nomura et al., GECCO 2023): the learning rate is adapted to keep the
    update's signal-to-noise ratio constant, which suits our noisy scores
    (measured SNR about 1 per generation, 27 Sep)."""

    def __init__(self, x0, sigma, popsize, cov=None):
        import numpy as np
        from cmaes import CMA
        n = len(x0)
        self.opt = CMA(mean=np.array(x0, dtype=float), sigma=sigma,
                       bounds=np.array([[0.0, 1.0]] * n), seed=1, population_size=popsize,
                       cov=None if cov is None else np.array(cov, dtype=float), lr_adapt=True)

    @property
    def gen(self):
        return self.opt.generation

    def stop(self):
        return bool(self.opt.should_stop())

    def ask(self):
        return [list(map(float, self.opt.ask())) for _ in range(self.opt.population_size)]

    def tell(self, xs, fitness):
        import numpy as np
        self.opt.tell([(np.array(x), f) for x, f in zip(xs, fitness)])

    @property
    def mean(self):
        return [float(v) for v in self.opt.mean]


BACKENDS = {"pycma": _PyCMA, "cmaes-lra": _CMAesLRA}


def warm_start(plan, space):
    """(x0, cov) in `space` from a previous run's CMA state (WS-CMA-ES style):
    shared parameters take the old mean and covariance, rescaled from the old
    bounds to the new ones; new parameters start at plan["start"] with unit
    variance and no covariance."""
    import numpy as np
    src = Path(plan["warm_from"])
    old_space = json.loads((src / "plan.json").read_text(encoding="utf8"))["space"]
    state = pickle.loads((src / "cma.pkl").read_bytes())
    if hasattr(state, "es"):
        state = state.es
    if hasattr(state, "sm"):                 # pycma
        old_mean = np.array(state.mean, dtype=float)
        old_cov = np.array(state.sm.C, dtype=float)
    else:                                    # cmaes backend wrapper
        old_mean = np.array(state.opt.mean, dtype=float)
        old_cov = np.array(state.opt._C, dtype=float)
    old_names = list(old_space)
    values = decode(old_mean, old_space)
    names = list(space)
    x0 = []
    for name in names:
        low, high, _ = bounds(space[name])
        v = values[name] if name in values else plan["start"][name]
        x0.append(min(1.0, max(0.0, (v - low) / (high - low))))
    cov = np.eye(len(names))
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            if a in old_space and b in old_space:
                (la, ha, _), (lb, hb, _) = bounds(old_space[a]), bounds(old_space[b])
                (na, ma, _), (nb, mb, _) = bounds(space[a]), bounds(space[b])
                scale = ((ha - la) / (ma - na)) * ((hb - lb) / (mb - nb))
                cov[i, j] = old_cov[old_names.index(a), old_names.index(b)] * scale
    cov = (cov + cov.T) / 2
    w, v = np.linalg.eigh(cov)
    cov = v @ np.diag(np.maximum(w, 1e-6)) @ v.T   # keep it positive definite
    return x0, cov.tolist()


def gen_maps(plan, maps, gen):
    """Maps for one generation. With map_sample "pair", each map and its
    perturbed copy (<stem>_p<k>) form a group and one of each group is drawn per
    generation (the same for every candidate): half the games per generation,
    every layout still played every generation."""
    if plan.get("map_sample") != "pair":
        return maps
    groups = {}
    for m in maps:
        groups.setdefault(re.sub(r"_p\d+$", "", m.stem), []).append(m)
    rng = random.Random(plan["seed"] * 7919 + gen)
    return [rng.choice(sorted(g)) for _, g in sorted(groups.items())]


def _evaluate(out, plan, space, gen, xs, n_cma, workers):
    """Play one generation: the n_cma CMA samples, plus the distribution mean
    as candidate "cmean" when xs holds one more."""
    maps = gen_maps(plan, [out / "maps" / f"{m}.map" for m in plan["maps"]], gen)
    opponents = [out / "opponents" / name for name in plan["opponents"]]
    gen_dir = out / f"gen{gen:03d}"
    for attempt in range(3):
        if gen_dir.exists():
            shutil.rmtree(gen_dir)   # an interrupted generation is replayed whole
        candidates = []
        for i, x in enumerate(xs):
            bot = gen_dir / "bots" / ("cmean" if i >= n_cma else f"c{i:02d}")
            population.snapshot(out / "base", bot)
            write_params(bot / plan["params"],
                         expand(decode(x, space), space, plan.get("base_values", {})))
            candidates.append(bot)
        jobs = population.jobs_for(candidates, opponents, maps, gen_seeds(plan, gen), gen_dir / "replays")
        try:
            return candidates, bounded.run(jobs, workers, gen_dir, f"gen{gen}"), gen_dir
        except BrokenProcessPool:
            # rare CPython/wasmtime worker crash ("_PyThreadState_Attach");
            # games are deterministic, so replaying the generation is exact
            print(f"gen {gen}: worker pool crashed, replaying (attempt {attempt + 2})", flush=True)
    raise RuntimeError(f"gen {gen}: worker pool crashed three times")


def run(out: Path, workers: int):
    plan = json.loads((out / "plan.json").read_text(encoding="utf8"))
    if (os.environ.get("BCSIM_DETERMINISTIC_V6") == "1") != plan["deterministic_v6_clock"]:
        raise ValueError("BCSIM_DETERMINISTIC_V6 must match the plan")
    space = plan["space"]
    backend = plan.get("backend", "pycma")
    state = out / "cma.pkl"
    if state.exists():
        es = pickle.loads(state.read_bytes())
        if backend == "pycma" and not isinstance(es, _PyCMA):
            wrapped = _PyCMA.__new__(_PyCMA)
            wrapped.es = es                  # a pre-backend run: cma.pkl holds the bare pycma object
            es = wrapped
    else:
        x0 = [min(1.0, max(0.0, v)) for v in encode(plan["start"], space)]
        cov = None
        if plan.get("warm_from"):
            x0, cov = warm_start(plan, space)
        es = BACKENDS[backend](x0, plan["sigma"], plan["popsize"], cov)
    log = out / "evaluations.jsonl"
    while es.gen < plan["generations"] and not es.stop():
        gen = es.gen
        xs = es.ask()
        evaluated = xs + ([[min(1.0, max(0.0, v)) for v in es.mean]] if plan.get("eval_mean") else [])
        candidates, games, gen_dir = _evaluate(out, plan, space, gen, evaluated, len(xs), workers)
        margins = replay_margins(games, workers)
        fitness, rows = [], []
        for i, bot in enumerate(candidates):
            mine = [g for g in games if bot.name in (g["bot_a"], g["bot_b"])]
            f, detail = score(mine, bot.name, margins, plan.get("objective", "margin"),
                              plan.get("worst_weight", 0.25))
            wins = sum(g["winner"] == ("A" if g["bot_a"] == bot.name else "B") for g in mine)
            if i < len(xs):
                fitness.append(-f)   # CMA-ES minimises; the mean candidate is only measured
            rows.append({"gen": gen, "cand": bot.name, "F": f, "wins": wins, "games": len(mine),
                         "params": decode(evaluated[i], space), "per_map": detail})
        es.tell(xs, fitness)
        with log.open("a", encoding="utf8") as fh:
            for row in rows:
                fh.write(json.dumps(row) + "\n")
        state.write_bytes(pickle.dumps(es))
        shutil.rmtree(gen_dir / "replays", ignore_errors=True)   # keep scores, drop replays
        cands = [r for r in rows if r["cand"] != "cmean"]
        best = max(cands, key=lambda r: r["F"])
        mean_row = next((r for r in rows if r["cand"] == "cmean"), None)
        print(f"gen {gen}: best F {best['F']:+.3f} ({best['wins']}/{best['games']} wins) "
              f"mean F {statistics.fmean(r['F'] for r in cands):+.3f}"
              + (f" | distribution mean F {mean_row['F']:+.3f} ({mean_row['wins']}/{mean_row['games']} wins)"
                 if mean_row else ""), flush=True)
    rows = [json.loads(line) for line in log.read_text(encoding="utf8").splitlines()]
    means = [r for r in rows if r["cand"] == "cmean"]
    pick = means[-1] if means else max(rows, key=lambda r: r["F"])
    population.write_json(out / f"final-{datetime.now():%H%M%S}.json",
                          {"recommended": pick, "why": "last distribution mean" if means else "best single"})
    print("recommended:", json.dumps(pick["params"]), f"F {pick['F']:+.3f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("result", nargs="?", type=Path)
    ap.add_argument("--prepare", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--base")
    ap.add_argument("--params")
    ap.add_argument("--space")
    ap.add_argument("--vs", nargs="+")
    ap.add_argument("--maps", default="ranked",
                    help="ranked (all 15: official 11 + ladder 4), current (the 10 in today's ranked "
                         "rotation), all (official 11), screen (5), "
                         "or comma-separated official map stems")
    ap.add_argument("--extra-maps", nargs="*", default=[],
                    help="additional .map files (ladder maps outside the official suite)")
    ap.add_argument("--seed", type=int, default=53001)
    ap.add_argument("--objective", choices=["aligned", "margin"], default="aligned",
                    help="per-game score: aligned (win + longest dragon + length) or margin (length only)")
    ap.add_argument("--backend", choices=sorted(BACKENDS), default="pycma",
                    help="pycma, or cmaes-lra (learning-rate adaptation for noisy scores)")
    ap.add_argument("--eval-mean", action="store_true",
                    help="also play the distribution mean each generation (progress on shared seeds; the final pick)")
    ap.add_argument("--map-sample", choices=["all", "pair"], default="all",
                    help="pair: per generation play one of each map / perturbed-copy pair")
    ap.add_argument("--warm-from", help="previous tune result dir: start from its CMA mean and covariance")
    ap.add_argument("--fixed", help='JSON settings written into the base before tuning, e.g. {"CPP_VOR": 0}')
    ap.add_argument("--worst-weight", type=float, default=0.25,
                    help="F = mean over maps + this x worst map (0 = plain mean, lowest noise)")
    ap.add_argument("--seeds", type=int, default=1,
                    help="engine seeds per generation (fresh each generation)")
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
