"""Screen two fixed memory ablations; only an unchanged winner validates."""

import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import guarded, growers, population
from .paths import ROOT, RESULTS, bot_hash, map_signature, resolve_maps

MODES = ("terrain_memory", "portal_memory")


def make_variant(source, dest, portals):
    population.snapshot(source, dest)
    (dest / "brain.py").rename(dest / "baseline_brain.py")
    shutil.copy2(ROOT / "experiments/navigation/brain.py", dest / "brain.py")
    shutil.copy2(ROOT / "framework/navigation.py", dest / "navigation.py")
    (dest / "navigation_config.py").write_text(f"PORTALS = {portals!r}\n", encoding="utf8")
    return dest


def prepare():
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-navigation-" + uuid.uuid4().hex[:6])
    out.mkdir()
    source = ROOT / "versions/v2"
    for name in ("control_450", "reference_v2"):
        population.snapshot(source, out / "bots" / name)
    for name in MODES:
        make_variant(source, out / "bots" / name, name == "portal_memory")
    for name in ("splitter", "hunter"):
        population.snapshot(guarded.MOVEMENT / "bots" / name, out / "bots" / name)
    (out / "maps").mkdir()
    maps = []
    for source_map in resolve_maps("all"):
        dest = out / "maps" / f"{source_map.stem}_{map_signature(source_map)}.map"
        shutil.copy2(source_map, dest)
        maps.append(dest)
    plan = {"question": "Does bounded per-dragon terrain memory help, and does known-pair portal routing add value?",
            "modes": list(MODES), "maps": [str(m) for m in maps],
            "live_hash": bot_hash(ROOT / "mybot"), "baseline_hash": bot_hash(source),
            "candidate_hashes": {n: bot_hash(out / "bots" / n) for n in MODES},
            "screen_seeds": list(range(20000, 20004)), "validation_seeds": list(range(21000, 21008)),
            "selection": "After judge-runtime preflight, screen both candidates and control against v2. "
                         "Highest new score above .5 advances unchanged; ties prefer terrain_memory. "
                         "No winner means stop. Screen is 216 games; selected validation is 864 games.",
            "gate": "Fresh-seed validation direct v2 map-cluster CI lower > .5 AND paired pool gain "
                    "map-cluster CI lower > 0, plus exact replay and judge-budget checks. "
                    "Novel-map confirmation needed before promotion if validation passes.",
            "limits": "96 expanded nodes, 12 steps; food sightings expire after 8 rounds. "
                      "Static terrain persists. No shared memory or sonar. Unknown occupancy is uncertain. "
                      "No unpaired portal traversal; no emergency portal fallback combination."}
    population.write_json(out / "plan.json", plan)
    (out / "implementation").mkdir()
    for name in ("navigation_experiment.py", "growers.py", "guarded.py", "bounded.py", "fission_audit.py"):
        shutil.copy2(ROOT / "bcsim" / name, out / "implementation" / name)
    print(out, flush=True)


def screen(out, workers):
    plan = json.loads((out / "plan.json").read_text())
    for n in MODES:
        assert bot_hash(out / "bots" / n) == plan["candidate_hashes"][n]
        preflight = json.loads((out / f"sandbox-{n}.json").read_text())
        assert not preflight["errors"] and not preflight["exception"]
        assert preflight["hash"] == plan["candidate_hashes"][n]
        assert preflight["metrics"]["max_points"] < 100000000
        assert preflight["metrics"]["max_memory_bytes"] < 48*2**20
    candidates = [out / "bots" / n for n in ("control_450", *MODES)]
    games = guarded.stage(out, "screen", candidates, [out / "bots/reference_v2"],
                          [Path(p) for p in plan["maps"]], plan["screen_seeds"], workers, True)
    scores = {n: population.tally(games, n).score for n in MODES}
    best = max(MODES, key=scores.get)
    selection = {"scores": scores, "selected": best if scores[best] > .5 else None,
                 "hash": bot_hash(out / "bots" / best)}
    population.write_json(out / "selection.json", selection)
    print(json.dumps(selection, indent=2), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--prepare", action="store_true")
    p.add_argument("--screen", type=Path)
    p.add_argument("--validate", type=Path)
    p.add_argument("--audit", type=Path)
    p.add_argument("--budget", type=Path)
    p.add_argument("--workers", type=int, choices=range(1, 9), default=8)
    args = p.parse_args()
    if args.prepare:
        prepare()
    elif args.screen:
        screen(args.screen, args.workers)
    elif args.validate:
        growers.validate(args.validate, args.workers)
    elif args.audit:
        growers.audit(args.audit, args.workers)
    elif args.budget:
        from .guarded_audit import budget
        budget(args.budget)
    else:
        p.error("choose --prepare, --screen, --validate, --audit or --budget")
