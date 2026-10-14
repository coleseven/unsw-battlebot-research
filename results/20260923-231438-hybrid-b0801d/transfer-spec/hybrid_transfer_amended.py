"""Predeclared new-layout transfer and linear-vs-neural diagnostic.

Only run after the unchanged linear finalist passes the official-map gate.
No model selection or fitting uses these results. Synthetic families are
stress tests, not the competition's opponent or map distribution.
"""

import argparse
import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path

from . import arena, audit_jobs, bounded, fission_audit, hybrid_audit, novel_maps, population, portal_followup, trap_followup
from .paths import ROOT, bot_hash, file_hash, map_signature

SPECS = (
    ("open_small", "open", 16, 16, 0., .85, 9, 21, 34001),
    ("open_large", "open", 28, 20, 0., .65, 15, 34, 34002),
    ("baffles_small", "baffles", 14, 18, .14, .85, 7, 17, 34003),
    ("baffles_large", "baffles", 24, 18, .20, .55, 11, 26, 34004),
    ("dense_small", "dense", 16, 20, .30, .80, 9, 22, 34005),
    ("dense_large", "dense", 24, 22, .37, .60, 12, 31, 34006),
    ("scarce_small", "scarce", 18, 14, .24, .25, 21, 42, 34007),
    ("scarce_large", "scarce", 22, 18, .33, .25, 21, 42, 34008),
)


def load_plan(out):
    amended = out / "transfer-spec/plan-deterministic-pairs.json"
    return json.loads((amended if amended.exists() else out / "transfer-spec/plan.json").read_text())


def deduplicate(out):
    """Pre-game amendment: no seed pseudoreplication for two deterministic bots."""
    assert not (out / "transfer").exists(), "amendment must precede all transfer games"
    original_path = out / "transfer-spec/plan.json"
    plan = json.loads(original_path.read_text())
    plan["pair_seeds"] = {f"{a}_vs_{b}": ([plan["seeds"][0]] if b == "neural" else plan["seeds"])
                          for a, b in plan["pairs"]}
    plan["expected_games"] = len(plan["maps"]) * 2 * sum(len(s) for s in plan["pair_seeds"].values())
    plan["amendment"] = {
        "original_plan_hash": file_hash(original_path),
        "reason": "Both learned evaluators choose deterministically; bot RNG seeds change neither side "
                  "in linear-vs-neural games. Keep one game per map/side for that pair. "
                  "All eight seeds retained against stochastic v2. No transfer results exist yet."}
    population.write_json(out / "transfer-spec/plan-deterministic-pairs.json", plan)
    shutil.copy2(Path(__file__), out / "transfer-spec/hybrid_transfer_amended.py")
    print(json.dumps({"games": plan["expected_games"], "amendment": plan["amendment"]}), flush=True)


def prepare(out):
    folder = out / "transfer-spec"
    folder.mkdir()
    maps, families, specs = [], {}, []
    for portals in (False, True):
        for i, base in enumerate(SPECS):
            spec = (*base[:-1], 35001 + i, 4 if i % 2 == 0 else 8) if portals else base
            name = ("portal_" if portals else "plain_") + base[0]
            path = folder / f"{name}.map"
            text = portal_followup.generate(spec) if portals else novel_maps.generate(spec)
            with path.open("x", encoding="utf8") as f:
                f.write(text)
            trap_followup.validate_map(path)
            maps.append(str(path)); families[path.stem] = base[1]
            specs.append({"name": name, "spec": spec})
    assert len({map_signature(Path(p)) for p in maps}) == 16
    original = json.loads((out / "plan.json").read_text())
    assert not ({map_signature(Path(p)) for p in maps} & {map_signature(Path(p)) for p in original["maps"]})
    plan = {"question": "Does unchanged linear improvement transfer, and how does its neural control compare?",
            "maps": maps, "families": families, "specs": specs, "seeds": list(range(32000, 32008)),
            "pairs": [["linear", "reference_v2"], ["neural", "reference_v2"], ["linear", "neural"]],
            "hashes": {n: bot_hash(out / "bots" / n) for n in ("linear", "neural", "reference_v2")},
            "map_hashes": {p: file_hash(Path(p)) for p in maps}, "expected_games": 768,
            "condition": "Run only if linear passes the original fresh-seed official-map performance gate.",
            "gate": "Linear versus v2 family-cluster 95% lower bound > .5 and every map score >= .375. "
                    "Neural comparisons are diagnostic and do not select a replacement.",
            "limits": "Four related procedural families; not the competition distribution. "
                      "Fresh geometry and bot RNG seeds, no training or tuning. No portal navigation added."}
    population.write_json(folder / "plan.json", plan)
    for source in (Path(__file__), ROOT / "bcsim/novel_maps.py", ROOT / "bcsim/portal_followup.py"):
        shutil.copy2(source, folder / source.name)
    print(json.dumps({"maps": len(maps), "games": 768, "condition": plan["condition"]}), flush=True)


def run(out, workers):
    comparison = json.loads((out / "comparison.json").read_text())
    if not comparison["linear"]["performance_gate"]:
        population.write_json(out / "transfer-spec/skipped.json", {"reason": "Linear did not pass official-map gate."})
        print("Transfer skipped: official-map gate failed.", flush=True)
        return
    plan = load_plan(out)
    for name, expected in plan["hashes"].items():
        assert bot_hash(out / "bots" / name) == expected
    for path, expected in plan["map_hashes"].items():
        assert file_hash(Path(path)) == expected
    folder = out / "transfer"
    folder.mkdir()
    maps = [Path(p) for p in plan["maps"]]
    bots = {n: out / "bots" / n for n in plan["hashes"]}
    provenance = arena.provenance(list(bots.values()), maps, {"seeds": plan["seeds"], "workers": workers})
    population.write_json(folder / "run.json", provenance)
    jobs = []
    for candidate, opponent in plan["pairs"]:
        seeds = plan.get("pair_seeds", {}).get(f"{candidate}_vs_{opponent}", plan["seeds"])
        jobs.extend(population.jobs_for([bots[candidate]], [bots[opponent]], maps, seeds, folder / "replays"))
    assert len(jobs) == plan["expected_games"]
    games = bounded.run(jobs, workers, folder, "hybrid transfer")
    assert not arena.check_hashes(games, provenance)
    results = {}
    for name, opponent in plan["pairs"]:
        pair = [g for g in games if {g["bot_a"], g["bot_b"]} == {name, opponent}]
        clusters, by_map = defaultdict(list), defaultdict(list)
        for g in pair:
            score = arena.score_for(g, name)
            clusters[plan["families"][g["map"]]].append(score)
            by_map[g["map"]].append(score)
        tally = population.tally(pair, name)
        ci = arena.block_bootstrap(list(clusters.values()), iters=8000)
        scores = {m: sum(s) / len(s) for m, s in by_map.items()}
        results[f"{name}_vs_{opponent}"] = {"wins": tally.w, "draws": tally.d, "losses": tally.l,
            "score": tally.score, "family_ci95": ci, "map_scores": scores,
            "threshold_passed": ci[0] > .5 and min(scores.values()) >= .375}
    population.write_json(folder / "comparison.json", results)
    print(json.dumps(results, indent=2), flush=True)


def one_game(args):
    game, primary, mapfile = args
    counts, samples = Counter(), {}
    for name in ("linear", "neural"):
        if name not in (game["bot_a"], game["bot_b"]):
            continue
        path = Path(primary).parent / name
        current, probes = fission_audit.one_game((game, str(path), mapfile))
        current.pop("games")
        counts.update(current)
        counts[name + "_turns"] += current["verified_candidate_turns"]
        samples.update({name + "__" + k: {"bot": name, **v} for k, v in probes.items()})
    counts["games"] = 1
    return dict(counts), samples


def audit(out, workers):
    plan = load_plan(out)
    folder = out / "transfer"
    games = [json.loads(l) for l in (folder / "games.jsonl").read_text().splitlines()]
    assert len(games) == plan["expected_games"]
    assert len({(g["map"], g["seed"], g["bot_a"], g["bot_b"]) for g in games}) == len(games)
    assert not arena.check_hashes(games, json.loads((folder / "run.json").read_text()))
    maps = {Path(p).stem: p for p in plan["maps"]}
    tasks = []
    for game in games:
        primary = "linear" if "linear" in (game["bot_a"], game["bot_b"]) else "neural"
        # Include both candidate hashes in the checkpoint fingerprint when a
        # game audits both sides; audit_jobs otherwise hashes only primary.
        enriched = {**game, "audited_model_hashes": plan["hashes"]}
        tasks.append((enriched, str(out / "bots" / primary), maps[game["map"]]))
    audit_folder = folder / "audit"
    audit_folder.mkdir(exist_ok=True)
    counts, samples = audit_jobs.run(tasks, workers, audit_folder, one_game, "hybrid transfer audit")
    assert counts["late_splits"] == 0
    population.write_json(audit_folder / "replay-audit.json", {"counts": dict(counts), "samples": samples,
                       "hashes": {n: plan["hashes"][n] for n in ("linear", "neural")}})
    print(json.dumps(dict(counts)), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("experiment", type=Path)
    p.add_argument("--prepare", action="store_true")
    p.add_argument("--deduplicate", action="store_true")
    p.add_argument("--audit", action="store_true")
    p.add_argument("--budget", action="store_true")
    p.add_argument("--workers", type=int, default=6)
    args = p.parse_args()
    if args.deduplicate:
        deduplicate(args.experiment)
    elif args.prepare:
        prepare(args.experiment)
    elif args.audit:
        audit(args.experiment, args.workers)
    elif args.budget:
        hybrid_audit.budget(args.experiment, "transfer")
    else:
        run(args.experiment, args.workers)
