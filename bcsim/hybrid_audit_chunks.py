"""Audit completed confirmation chunks early, then reuse exact-input cache.

The worker and cache fingerprints are identical to hybrid_audit.audit. The
final combined audit validates every cached signature and audits only the
remaining selected-evaluator games. This is scheduling, not reduced coverage.
"""

import argparse
import json
import shutil
from pathlib import Path

from . import arena, audit_jobs, hybrid_audit, population
from .paths import ROOT, bot_hash, file_hash


def core(out, workers):
    plan = json.loads((out / "plan.json").read_text())
    selection = json.loads((out / "roles-selection.json").read_text())
    name = selection["selected"]
    if name:
        assert bot_hash(out / "bots" / name) == selection["hash"]
    assert bot_hash(ROOT / "versions/v2") == plan["baseline_hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    source = out / "validation-core"
    assert (source / "summary.md").exists(), "confirmation chunk still running"
    games = [json.loads(l) for l in (source / "games.jsonl").read_text().splitlines()]
    assert not arena.check_hashes(games, json.loads((source / "run.json").read_text()))
    maps = {Path(p).stem: p for p in plan["maps"]}
    names = ["control_450"] + ([name] if name else [])
    expected = population.jobs_for([out / "bots" / n for n in names],
        [out / "bots" / n for n in ("reference_v2", "splitter", "hunter")],
        [Path(p) for p in plan["maps"]], plan["validation_seeds"])
    keys = {(Path(m).stem, Path(a).name, Path(b).name, s) for m, a, b, s, _, _ in expected}
    assert len(games) == len(keys)
    assert {(g["map"], g["bot_a"], g["bot_b"], g["seed"]) for g in games} == keys
    folder = out / "validation-audit-staging"
    folder.mkdir(exist_ok=True)
    tasks = [(g, str(out / "bots" / name) if name and name in (g["bot_a"], g["bot_b"]) else None,
              maps[g["map"]]) for g in games]
    counts, samples = audit_jobs.run(tasks, workers, folder, hybrid_audit.one_game, "confirmation core audit")
    assert counts["late_splits"] == 0
    population.write_json(folder / "completed.json", {"counts": dict(counts), "samples": samples,
        "worker_source_hash": file_hash(ROOT / "bcsim/hybrid_audit.py"),
        "fission_source_hash": file_hash(ROOT / "bcsim/fission_audit.py")})
    print(json.dumps(dict(counts)), flush=True)


def seed_cache(out):
    source = out / "validation-audit-staging"
    record = json.loads((source / "completed.json").read_text())
    assert file_hash(ROOT / "bcsim/hybrid_audit.py") == record["worker_source_hash"]
    assert file_hash(ROOT / "bcsim/fission_audit.py") == record["fission_source_hash"]
    assert (out / "validation/run.json").exists(), "merge confirmation first"
    target = out / "validation/audit"
    target.mkdir(exist_ok=True)
    destination = target / "audit-progress.jsonl"
    assert not destination.exists(), "refusing to overwrite an existing audit cache"
    shutil.copy2(source / "audit-progress.jsonl", destination)
    print(f"Seeded exact-input verification cache for {record['counts']['games']} games", flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("experiment", type=Path)
    p.add_argument("--seed-cache", action="store_true")
    p.add_argument("--workers", type=int, default=4)
    args = p.parse_args()
    if args.seed_cache:
        seed_cache(args.experiment)
    else:
        core(args.experiment, args.workers)
