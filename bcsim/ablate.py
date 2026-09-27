"""Leave-one-group-out feature ablation with paired, multi-seed comparison.

Prepare (freezes the base bot, variants, opponents, maps and seeds):
    python -m bcsim.ablate --prepare --base results/v7-base-bot --params params.hpp \\
        --groups experiments/features/groups_v7.json --vs results/v7-base-bot sparring/nicked \\
        --extra-maps maps/server/Autarky.map ... --seeds 3
Run or resume (one variant at a time; finished variants are kept):
    python -m bcsim.ablate RESULT_DIR --run [--workers 8]
Report (also written by --run):
    python -m bcsim.ablate RESULT_DIR --report

The groups file maps a variant name to settings ({"W_PEARL": 0.0,
"GOAL": false, ...}); variant "base" (unchanged) is always added. Every
variant plays every opponent on every map, both sides and every seed
(unswbc >= 1.1 seeds pearl spawns), so each variant's games pair one-to-one
with base's. The report gives each variant's mean margin difference from base
(bcsim.margin, positive = the variant is better, i.e. removing the group
helps) with a 95% bootstrap CI resampling (map, seed) blocks, by opponent and
for official vs extra maps. `--prepare --groups none --seeds 6` measures
noise: the report then suggests how many seeds a given CI width needs.
Set BCSIM_DETERMINISTIC_V6=1 when a Python v6-core bot plays.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import statistics
import uuid
from concurrent.futures.process import BrokenProcessPool
from datetime import datetime
from pathlib import Path

from . import bounded, official_suite, population, tune
from .paths import RESULTS, bot_hash, resolve_bot

BASE = "base"


def prepare(args):
    base = resolve_bot(args.base)
    groups = {} if args.groups == "none" else json.loads(Path(args.groups).read_text(encoding="utf8"))
    if BASE in groups:
        raise ValueError(f"'{BASE}' is reserved for the unchanged bot")
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-ablate-" + uuid.uuid4().hex[:6])
    out.mkdir()
    variants = {BASE: {}, **groups}
    for name, settings in variants.items():
        population.snapshot(base, out / "variants" / name)
        if settings:
            tune.write_params(out / "variants" / name / args.params, settings)
    opponents = []
    for source in args.vs:
        path = resolve_bot(source)
        if path.name in variants:
            raise ValueError(f"opponent name {path.name} clashes with a variant")
        population.snapshot(path, out / "opponents" / path.name)
        opponents.append(path.name)
    (out / "maps").mkdir()
    official = official_suite.official_maps()
    official_suite.require_coverage(official)
    signatures = {official_suite.map_signature(m) for m in official}
    extra = []
    extras = (official_suite.ladder_extra_maps() if args.extra_maps is None else
              [Path(m) for m in args.extra_maps])
    for source in extras:
        if official_suite.map_signature(source) in signatures:
            raise ValueError(f"{source} duplicates an official map")
        signatures.add(official_suite.map_signature(source))
        extra.append(source)
    for m in official + extra:
        shutil.copy2(m, out / "maps" / m.name)
    population.write_json(out / "plan.json", {
        "base": str(base), "base_hash": bot_hash(base), "params": args.params,
        "variants": variants, "opponents": opponents,
        "official_maps": [m.stem for m in official], "extra_maps": [m.stem for m in extra],
        "seeds": [args.seed + i for i in range(args.seeds)], "objective": "aligned",
        "unswbc": __import__("importlib.metadata").metadata.version("unswbc"),
        "deterministic_v6_clock": os.environ.get("BCSIM_DETERMINISTIC_V6") == "1"})
    print(out)


def _maps(out, plan):
    return [out / "maps" / f"{m}.map" for m in plan["official_maps"] + plan["extra_maps"]]


def _expected(plan):
    maps = len(plan["official_maps"]) + len(plan["extra_maps"])
    return len(plan["opponents"]) * maps * len(plan["seeds"]) * 2


def run(out: Path, workers: int):
    plan = json.loads((out / "plan.json").read_text(encoding="utf8"))
    if (os.environ.get("BCSIM_DETERMINISTIC_V6") == "1") != plan["deterministic_v6_clock"]:
        raise ValueError("BCSIM_DETERMINISTIC_V6 must match the plan")
    opponents = [out / "opponents" / o for o in plan["opponents"]]
    maps = _maps(out, plan)
    for name in plan["variants"]:
        folder = out / "runs" / name
        log = folder / "games.jsonl"
        if log.is_file() and len(log.read_text(encoding="utf8").splitlines()) == _expected(plan):
            continue
        for attempt in range(3):
            if folder.exists():
                shutil.rmtree(folder)   # a partial variant is replayed whole (games are deterministic)
            jobs = population.jobs_for([out / "variants" / name], opponents, maps,
                                       plan["seeds"], folder / "replays")
            try:
                games = bounded.run(jobs, workers, folder, name)
                break
            except BrokenProcessPool:
                print(f"{name}: worker pool crashed, replaying (attempt {attempt + 2})", flush=True)
        else:
            raise RuntimeError(f"{name}: worker pool crashed three times")
        margins = tune.replay_margins(games, workers)
        rows = []
        for g in games:
            side = "A" if g["bot_a"] == name else "B"
            rows.append({"opponent": g["bot_b"] if side == "A" else g["bot_a"], "map": g["map"],
                         "seed": g["seed"], "side": side, "margin": margins[g["replay"]][side]["margin"],
                         "aligned": margins[g["replay"]][side]["aligned"],
                         "win": g["winner"] == side})
        population.write_json(folder / "margins.json", rows)
        shutil.rmtree(folder / "replays", ignore_errors=True)
    report(out)


def _bootstrap(diffs_by_block, reps=2000, seed=0):
    """Mean of per-game differences with a 95% CI, resampling (map, seed) blocks."""
    blocks = list(diffs_by_block.values())
    flat = [d for b in blocks for d in b]
    rng = random.Random(seed)
    means = []
    for _ in range(reps):
        sample = [d for _ in blocks for d in rng.choice(blocks)]
        means.append(statistics.fmean(sample))
    means.sort()
    return statistics.fmean(flat), means[int(0.025 * reps)], means[int(0.975 * reps) - 1]


def _load(out, plan):
    data = {}
    for name in plan["variants"]:
        path = out / "runs" / name / "margins.json"
        if path.is_file():
            data[name] = {(r["opponent"], r["map"], r["seed"], r["side"]): r
                          for r in json.loads(path.read_text(encoding="utf8"))}
    return data


def report(out: Path):
    plan = json.loads((out / "plan.json").read_text(encoding="utf8"))
    data = _load(out, plan)
    if BASE not in data:
        print("base variant not finished yet")
        return
    base = data[BASE]
    official = set(plan["official_maps"])
    pool = set(official_suite.CURRENT_POOL)
    key = plan.get("objective", "margin")
    for rows in data.values():          # report in the plan's objective
        for r in rows.values():
            r["margin"] = r.get(key, r["margin"])
    lines = [f"# Ablation report: {out.name}", "",
             f"{len(plan['seeds'])} seeds, opponents {', '.join(plan['opponents'])}; "
             f"{len(plan['official_maps'])} official + {len(plan['extra_maps'])} extra maps, both sides. "
             f"Objective: {key}. Delta = variant score minus base score on the same (opponent, map, seed, side); "
             "positive means removing the group helped. 95% CI resamples (map, seed) blocks.", ""]
    base_rows = list(base.values())
    lines.append(f"base: mean margin {statistics.fmean(r['margin'] for r in base_rows):+.3f}, "
                 f"wins {sum(r['win'] for r in base_rows)}/{len(base_rows)}; by opponent: " +
                 ", ".join(f"{o} {statistics.fmean(r['margin'] for r in base_rows if r['opponent'] == o):+.3f}"
                           for o in plan["opponents"]))
    lines += ["", "| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | " +
              " | ".join(f"vs {o}" for o in plan["opponents"]) + " | official | extra | wins |",
              "|---|---|---|---|---|---|" + "---|" * len(plan["opponents"]) + "---|---|---|"]
    summary = {}
    for name, rows in data.items():
        if name == BASE:
            continue
        def diffs(keep):
            by_block = {}
            for key, r in rows.items():
                if key in base and keep(key):
                    by_block.setdefault((key[1], key[2]), []).append(r["margin"] - base[key]["margin"])
            return by_block
        allb = diffs(lambda k: True)
        mean, lo, hi = _bootstrap(allb)
        verdict = "harmful (drop)" if lo > 0 else "essential" if hi < 0 else "neutral"
        per_opp = [statistics.fmean(d for b in diffs(lambda k, o=o: k[0] == o).values() for d in b)
                   for o in plan["opponents"]]
        off = diffs(lambda k: k[1] in official)
        ext = diffs(lambda k: k[1] not in official)
        cur = diffs(lambda k: k[1] in pool)
        guard = diffs(lambda k: k[1] not in pool)
        cmean, clo, chi = _bootstrap(cur) if cur else (0.0, 0.0, 0.0)
        fmt = lambda b: f"{statistics.fmean(d for v in b.values() for d in v):+.3f}" if b else "-"
        wins = sum(r["win"] for r in rows.values())
        cverdict = "harmful (drop)" if clo > 0 else "essential" if chi < 0 else "neutral"
        summary[name] = {"delta": mean, "lo": lo, "hi": hi, "verdict": verdict,
                         "pool_delta": cmean, "pool_lo": clo, "pool_hi": chi, "pool_verdict": cverdict}
        lines.append(f"| {name} | {cmean:+.3f} [{clo:+.3f}, {chi:+.3f}] | {cverdict} | {fmt(guard)} | "
                     f"{mean:+.3f} [{lo:+.3f}, {hi:+.3f}] | {verdict} | " +
                     " | ".join(f"{d:+.3f}" for d in per_opp) +
                     f" | {fmt(off)} | {fmt(ext)} | {wins}/{len(rows)} |")
    # noise: the seed-to-seed spread of base's margin in the same (opponent, map,
    # side) cell. Pairing cancels map and side effects, so a variant close to
    # base has per-game difference variance of about 2 * within^2; the overall
    # mean averages games_per_seed games for each of K seeds.
    cells = {}
    for key, r in base.items():
        cells.setdefault((key[0], key[1], key[3]), []).append(r["margin"])
    spread = [statistics.variance(v) for v in cells.values() if len(v) > 1]
    if spread:
        within = statistics.fmean(spread) ** 0.5
        per_seed = len(cells)
        lines += ["", f"Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell "
                  f"{within:.3f} over {per_seed} cells. Expected paired CI half-width with K seeds, "
                  f"1.96 * sqrt(2 * {within:.3f}^2 / ({per_seed} * K)): " +
                  ", ".join(f"K={k}: {1.96 * (2 * within ** 2 / (per_seed * k)) ** 0.5:.3f}"
                            for k in (2, 3, 4, 6, 8))]
    elif summary:
        widths = [(s["hi"] - s["lo"]) / 2 for s in summary.values()]
        lines += ["", f"Noise: observed CI half-width {statistics.fmean(widths):.3f} with "
                  f"{len(plan['seeds'])} seed(s); run with 2+ seeds for a per-cell estimate."]
    text = "\n".join(lines) + "\n"
    (out / "report.md").write_text(text, encoding="utf8")
    (out / "report.json").write_text(json.dumps(summary, indent=2), encoding="utf8")
    print(text)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("result", nargs="?", type=Path)
    ap.add_argument("--prepare", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--base")
    ap.add_argument("--params")
    ap.add_argument("--groups", help="groups JSON, or 'none' for base only (noise measurement)")
    ap.add_argument("--vs", nargs="+")
    ap.add_argument("--extra-maps", nargs="*", default=None,
                    help="maps beyond the official 11 (default: the 4 ladder maps; pass none to omit)")
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--seed", type=int, default=61001)
    ap.add_argument("--workers", type=int, default=official_suite.DEFAULT_WORKERS)
    a = ap.parse_args()
    if a.prepare:
        if not (a.base and a.params and a.groups and a.vs):
            ap.error("--prepare needs --base, --params, --groups and --vs")
        prepare(a)
    elif a.run and a.result:
        run(a.result, a.workers)
    elif a.report and a.result:
        report(a.result)
    else:
        ap.error("use --prepare ..., RESULT --run, or RESULT --report")


if __name__ == "__main__":
    main()
