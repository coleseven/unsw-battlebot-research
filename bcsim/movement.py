"""Two independent fixed movement experiments; no tuning on validation."""

import argparse
import json
import pathlib
import shutil
import uuid
from datetime import datetime

from . import arena, endgame, population
from .paths import ROOT, RESULTS, bot_hash, file_hash, map_signature, resolve_maps

PRIOR = RESULTS / "20260922-171805-endgame-b67e3b"
TEMPLATE = ROOT / "experiments/movement/brain.py"


def make_variant(source, dest, mode):
    if mode not in ("trap", "sprint"):
        raise ValueError("mode must be trap or sprint")
    if any((source / n).exists() for n in ("baseline_brain.py", "local_safety.py", "movement_config.py")):
        raise ValueError("source already carries movement experiment modules")
    population.snapshot(source, dest)
    (dest / "brain.py").rename(dest / "baseline_brain.py")
    shutil.copy2(TEMPLATE, dest / "brain.py")
    shutil.copy2(ROOT / "framework/local_safety.py", dest / "local_safety.py")
    (dest / "movement_config.py").write_text(f"MODE = {mode!r}\n", encoding="utf8")
    return dest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--prior", type=pathlib.Path, default=PRIOR)
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("workers must be positive")
    source = args.prior / "bots/stop_450"
    if not source.is_dir():
        parser.error("prior must contain the frozen bots/stop_450 baseline")
    screen, holdout = population.reserve_maps(resolve_maps("all"))
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-movement-" + uuid.uuid4().hex[:6])
    out.mkdir(parents=True)
    control = population.snapshot(source, out / "bots/control_450")
    reference = population.snapshot(source, out / "bots/reference_450")
    candidates = [control] + [make_variant(source, out / "bots" / mode, mode) for mode in ("trap", "sprint")]
    opponents = [reference] + [population.snapshot(args.prior / "bots" / name, out / "bots" / name)
                               for name in ("splitter", "hunter")]
    (out / "maps").mkdir()
    copies = {}
    for m in screen + holdout:
        dest = out / "maps" / f"{m.stem}_{map_signature(m)}.map"
        shutil.copy2(m, dest)
        copies[m] = dest
    (out / "implementation").mkdir()
    for name in ("movement.py", "population.py", "endgame.py", "arena.py", "match.py", "paths.py", "replay.py"):
        shutil.copy2(ROOT / "bcsim" / name, out / "implementation" / name)
    plan = {"question": "Separate trap-avoidance and emergency-sprint ablations on the frozen stop-450 bot",
            "variants": [p.name for p in candidates], "opponents": [p.name for p in opponents],
            "baseline_path": str(source.resolve()), "baseline_hash": bot_hash(source),
            "live_bot_hash": bot_hash(ROOT / "mybot"), "runner_hash": file_hash(pathlib.Path(__file__)),
            "geometry_hash": file_hash(ROOT / "framework/local_safety.py"),
            "map_identity_hash": file_hash(ROOT / "bcsim/paths.py"),
            "screen_maps": [str(copies[m]) for m in screen], "screen_seeds": [4000, 4001],
            "holdout_maps": [str(copies[m]) for m in holdout], "holdout_seeds": list(range(5000, 5004)),
            "selection": "none: both fixed variants proceed unchanged, regardless of screening results",
            "success_gate": "paired overall map-cluster lower bound > 0 AND direct reference_450 lower bound > .5",
            "intervals": "97.5% per experiment (Bonferroni adjustment for two variants); approximate bootstrap",
            "limits": "local familiar maps, static visible occupancy, unknown boundaries optimistic; "
                      "no enemy sprint model or portal use; runtime metering evaluated separately"}
    population.write_json(out / "plan.json", plan)
    print(f"Experiment: {out}", flush=True)
    population.stage(out, "screen", candidates, opponents, [copies[m] for m in screen],
                     plan["screen_seeds"], args.workers)
    games = population.stage(out, "holdout", candidates, opponents, [copies[m] for m in holdout],
                             plan["holdout_seeds"], args.workers, True)
    comparisons = {}
    for candidate in candidates[1:]:
        delta = population.paired_delta(games, candidate.name, control.name)
        by_map = {}
        for p in (control.name, candidate.name):
            by_map[p] = {}
            for g in games:
                if p in (g["bot_a"], g["bot_b"]):
                    side = g["bot_a"] == p
                    by_map[p][(g["map"], *g["block"], side)] = arena.score_for(g, p)
        blocks = {}
        for key, score in by_map[candidate.name].items():
            blocks.setdefault(key[0], []).append(score - by_map[control.name][key])
        ci = arena.block_bootstrap(list(blocks.values()), level=.975, iters=8000)
        direct = population.tally([g for g in games if "reference_450" in (g["bot_a"], g["bot_b"])], candidate.name)
        direct_ci = arena.block_bootstrap(list(direct.blocks.values()), level=.975, iters=8000)
        comparisons[candidate.name] = {**delta, "map_cluster_ci975": ci, "direct_score": direct.score,
                                      "direct_ci975": direct_ci,
                                      "success_gate_passed": ci[0] > 0 and direct_ci[0] > .5}
    result = {"comparisons": comparisons,
              "diagnostics": {p.name: endgame.diagnostics(games, p.name) for p in candidates}}
    population.write_json(out / "comparison.json", result)
    lines = ["# Independent movement experiments", "", "| Policy | Validation score | W-D-L vs round-450 baseline | Gate |",
             "|---|---:|---|---|"]
    for p in candidates:
        t = population.tally(games, p.name)
        direct = population.tally([g for g in games if "reference_450" in (g["bot_a"], g["bot_b"])], p.name)
        lines.append(f"| {p.name} | {t.score:.1%} | {direct.w}-{direct.d}-{direct.l} | "
                     f"{comparisons.get(p.name, {}).get('success_gate_passed', 'control')} |")
    for name, c in comparisons.items():
        lo, hi = c["map_cluster_ci975"]
        lines += ["", f"{name}: paired gain {100 * c['difference']:+.2f} percentage points; "
                  f"97.5% map-cluster interval [{100 * lo:+.2f}, {100 * hi:+.2f}]."]
    lines += ["", "Five validation maps; no policy tuning after screening. No combination tested. "
              "Live bot and prior snapshots unchanged. Sandbox CPU verification is separate."]
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
