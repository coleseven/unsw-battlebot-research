"""Fixed emergency-portal ablation, independent of grower-role tuning."""

import argparse
import json
import os
import shutil
import uuid
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from . import arena, audit_jobs, fission_audit, guarded, population, reconstruct
from .paths import ROOT, RESULTS, bot_hash, map_signature, resolve_maps


def make_variant(source, dest):
    population.snapshot(source, dest)
    (dest / "brain.py").rename(dest / "baseline_brain.py")
    shutil.copy2(ROOT / "experiments/portal_escape/brain.py", dest / "brain.py")
    shutil.copy2(ROOT / "framework/portal_escape.py", dest / "portal_escape.py")
    return dest


def run(workers):
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-portal-" + uuid.uuid4().hex[:6])
    out.mkdir()
    source = ROOT / "versions/v2"
    candidate = make_variant(source, out / "bots/portal_escape")
    reference = population.snapshot(source, out / "bots/reference_v2")
    (out / "maps").mkdir()
    maps = []
    for source_map in resolve_maps("all"):
        if not reconstruct.Board(source_map.read_text()).portals:
            continue
        path = out / "maps" / f"{source_map.stem}_{map_signature(source_map)}.map"
        shutil.copy2(source_map, path)
        maps.append(path)
    plan = {"question": "Can last-resort portal use improve v2 on portal maps without changing ordinary movement?",
            "maps": [str(p) for p in maps], "seeds": list(range(17000, 17024)),
            "selection": "none; one fixed candidate, no policy tuning or grower combination",
            "gate": "Direct v2 score 95% map-cluster lower bound > .5; no-invalid-action and runtime checks",
            "baseline_hash": bot_hash(source), "candidate_hash": bot_hash(candidate),
            "live_hash": bot_hash(ROOT / "mybot"), "workers": workers,
            "limits": "Five familiar portal maps; unobserved destinations remain uncertain. "
                      "Known legal ordinary moves and direct enemy-head trades stay unchanged. "
                      "Targeted fallback, not a portal-aware global planner or ladder-strength claim."}
    population.write_json(out / "plan.json", plan)
    (out / "implementation").mkdir()
    for name in ("portal_experiment.py", "bounded.py", "arena.py", "match.py", "paths.py", "guarded.py"):
        shutil.copy2(ROOT / "bcsim" / name, out / "implementation" / name)
    print(f"Experiment: {out}", flush=True)
    games = guarded.stage(out, "validation", [candidate], [reference], maps, plan["seeds"], workers, True)
    tally = population.tally(games, candidate.name)
    clusters = defaultdict(list)
    for g in games:
        clusters[g["map"]].append(arena.score_for(g, candidate.name))
    ci = arena.block_bootstrap(list(clusters.values()), iters=8000)
    result = {"wins": tally.w, "draws": tally.d, "losses": tally.l, "score": tally.score,
              "map_ci95": ci, "pair_ci95": tally.ci(), "performance_gate": ci[0] > .5,
              "map_scores": {m: sum(v) / len(v) for m, v in clusters.items()}}
    assert bot_hash(source) == plan["baseline_hash"] and bot_hash(ROOT / "mybot") == plan["live_hash"]
    population.write_json(out / "comparison.json", result)
    print(json.dumps(result, indent=2), flush=True)


def audit(out, workers):
    os.environ["RAYON_NUM_THREADS"] = "1"
    plan = json.loads((out / "plan.json").read_text())
    candidate = out / "bots/portal_escape"
    assert bot_hash(candidate) == plan["candidate_hash"]
    maps = {Path(p).stem: p for p in plan["maps"]}
    games = [json.loads(l) for l in (out / "validation/games.jsonl").read_text().splitlines()]
    expected = len(maps) * len(plan["seeds"]) * 2
    assert len(games) == expected and not any(arena.is_error(g) for g in games)
    assert len({(g["map"], g["seed"], g["bot_a"], g["bot_b"]) for g in games}) == expected
    assert not arena.check_hashes(games, json.loads((out / "validation/run.json").read_text()))
    tasks = [(g, str(candidate), maps[g["map"]]) for g in games]
    counts, samples = audit_jobs.run(tasks, workers, out, fission_audit.one_game, "portal audit")
    assert counts["late_splits"] == 0
    population.write_json(out / "replay-audit.json", {"counts": dict(counts), "samples": samples,
                                                    "hash": bot_hash(candidate)})
    print(json.dumps(dict(counts), indent=2), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--audit", type=Path)
    args = p.parse_args()
    if args.audit:
        audit(args.audit, args.workers)
    else:
        run(args.workers)
