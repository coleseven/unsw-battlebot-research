"""Endgame cutoff / grower-role experiment against frozen v2.

The plan is saved before screening. Select exactly one candidate; confirm on
new seeds without retuning. No changes to active mybot or existing versions.
"""

import argparse
import json
import os
import shutil
import uuid
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from . import arena, audit_jobs, fission_audit, guarded, guarded_audit, population
from .paths import ROOT, RESULTS, bot_hash, map_signature, resolve_maps

BASE = ROOT / "versions/v2"
MODES = {"stop425": (425, None), "stop400": (400, None), "stop350": (350, None),
         "quarter350": (475, 350), "quarter400": (475, 400)}


def make_variant(source, dest, cutoff, grower_cutoff=None):
    if type(cutoff) is not int or not 0 <= cutoff <= 500:
        raise ValueError("invalid cutoff")
    if grower_cutoff is not None and (type(grower_cutoff) is not int or not 0 <= grower_cutoff <= cutoff):
        raise ValueError("invalid grower cutoff")
    population.snapshot(source, dest)
    shutil.copy2(ROOT / "experiments/growers/brain.py", dest / "brain.py")
    (dest / "grower_config.py").write_text(f"CUTOFF = {cutoff}\nGROWER_CUTOFF = {grower_cutoff!r}\n", encoding="utf8")
    return dest


def screen(workers):
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-growers-" + uuid.uuid4().hex[:6])
    out.mkdir()
    control = population.snapshot(BASE, out / "bots/control_450")
    reference = population.snapshot(BASE, out / "bots/reference_v2")
    candidates = [control] + [make_variant(BASE, out / "bots" / n, *c) for n, c in MODES.items()]
    for name in ("splitter", "hunter"):
        population.snapshot(guarded.MOVEMENT / "bots" / name, out / "bots" / name)
    (out / "maps").mkdir()
    maps = []
    for source in resolve_maps("all"):
        dest = out / "maps" / f"{source.stem}_{map_signature(source)}.map"
        shutil.copy2(source, dest)
        maps.append(dest)
    plan = {"question": "Can earlier growth or a quarter of dedicated growers improve v2's round-limit losses?",
            "modes": MODES, "live_hash": bot_hash(ROOT / "mybot"), "baseline_hash": bot_hash(BASE),
            "maps": [str(m) for m in maps], "screen_seeds": [15000, 15001],
            "validation_seeds": list(range(16000, 16008)),
            "selection": "Highest screen score among new policies, ties in declared mode order; score must exceed .5. "
                         "Exactly one policy validates unchanged. Movement, split threshold and split size stay fixed.",
            "gate": "Direct v2 score 95% map-cluster lower bound > .5 AND paired pool gain "
                    "95% map-cluster lower bound > 0; replay and sandbox checks required before promotion.",
            "limits": "Familiar official maps and scripted opponents. New bot RNG seeds, not unseen map families. "
                      "Role assignment is local and deterministic, not a globally elected champion.",
            "workers": workers}
    population.write_json(out / "plan.json", plan)
    (out / "implementation").mkdir()
    for name in ("growers.py", "guarded.py", "bounded.py", "arena.py", "match.py", "paths.py", "population.py"):
        shutil.copy2(ROOT / "bcsim" / name, out / "implementation" / name)
    print(f"Experiment: {out}", flush=True)
    games = guarded.stage(out, "screen", candidates, [reference], maps, plan["screen_seeds"], workers)
    scores = {name: population.tally(games, name).score for name in MODES}
    best = max(MODES, key=scores.get)
    selection = {"scores": scores, "selected": best if scores[best] > .5 else None,
                 "hash": bot_hash(out / "bots" / best)}
    population.write_json(out / "selection.json", selection)
    print(json.dumps(selection, indent=2), flush=True)


def validate(out, workers):
    plan = json.loads((out / "plan.json").read_text())
    selection = json.loads((out / "selection.json").read_text())
    if not selection["selected"]:
        raise ValueError("No candidate selected")
    candidate = out / "bots" / selection["selected"]
    assert bot_hash(candidate) == selection["hash"]
    control = out / "bots/control_450"
    opponents = [out / "bots" / n for n in ("reference_v2", "splitter", "hunter")]
    maps = [Path(p) for p in plan["maps"]]
    games = guarded.stage(out, "validation", [control, candidate], opponents, maps,
                          plan["validation_seeds"], workers, True)
    delta = population.paired_delta(games, candidate.name, control.name)
    direct_games = [g for g in games if "reference_v2" in (g["bot_a"], g["bot_b"])
                    and candidate.name in (g["bot_a"], g["bot_b"])]
    by_map = defaultdict(list)
    for g in direct_games:
        by_map[g["map"]].append(arena.score_for(g, candidate.name))
    direct = population.tally(direct_games, candidate.name)
    ci = arena.block_bootstrap(list(by_map.values()), iters=8000)
    result = {"candidate": candidate.name, "hash": bot_hash(candidate), "paired_pool": delta,
              "direct": {"wins": direct.w, "draws": direct.d, "losses": direct.l, "score": direct.score,
                         "map_ci95": ci, "pair_ci95": direct.ci()},
              "performance_gate": ci[0] > .5 and delta["map_cluster_ci95"][0] > 0}
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    assert bot_hash(BASE) == plan["baseline_hash"]
    population.write_json(out / "comparison.json", result)
    print(json.dumps(result, indent=2), flush=True)


def audit(out, workers):
    os.environ["RAYON_NUM_THREADS"] = "1"
    plan = json.loads((out / "plan.json").read_text())
    selection = json.loads((out / "selection.json").read_text())
    candidate = out / "bots" / selection["selected"]
    assert bot_hash(candidate) == selection["hash"]
    assert bot_hash(BASE) == plan["baseline_hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    maps = {Path(p).stem: p for p in plan["maps"]}
    games = [json.loads(l) for l in (out / "validation/games.jsonl").read_text().splitlines()]
    expected = len(maps) * len(plan["validation_seeds"]) * 3 * 2 * 2
    assert len(games) == expected and not any(arena.is_error(g) for g in games)
    assert len({(g["map"], g["seed"], g["bot_a"], g["bot_b"]) for g in games}) == expected
    assert not arena.check_hashes(games, json.loads((out / "validation/run.json").read_text()))
    tasks = [(g, str(candidate) if candidate.name in (g["bot_a"], g["bot_b"]) else None, maps[g["map"]]) for g in games]
    counts, samples = audit_jobs.run(tasks, workers, out, fission_audit.one_game, "grower audit")
    # late_splits is descriptive: ordinary role dragons may reproduce to 475.
    population.write_json(out / "replay-audit.json", {"counts": dict(counts), "samples": samples,
                                                    "hash": bot_hash(candidate)})
    print(json.dumps(dict(counts), indent=2), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workers", type=int, default=6)
    p.add_argument("--validate", type=Path)
    p.add_argument("--audit", type=Path)
    p.add_argument("--budget", type=Path)
    args = p.parse_args()
    if args.validate:
        validate(args.validate, args.workers)
    elif args.audit:
        audit(args.audit, args.workers)
    elif args.budget:
        guarded_audit.budget(args.budget)
    else:
        screen(args.workers)
