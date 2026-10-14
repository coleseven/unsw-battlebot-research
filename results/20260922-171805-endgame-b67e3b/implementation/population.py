"""Run a predeclared, two-stage population ablation with frozen inputs.

    python -B -m bcsim.population --workers 4

Does not change mybot, opponents, versions, or datasets. Everything generated
is inside a new results directory. This is in-process evaluation, not a judge
CPU-budget test. Seeds change bot RNG, not the map's engine configuration.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import statistics
import uuid
from collections import defaultdict
from datetime import datetime

from . import arena
from .paths import ROOT, RESULTS, bot_files, file_hash, map_signature, resolve_maps

CAPS = (0, 2, 4, 8, 64)
TEMPLATE = ROOT / "experiments" / "population" / "brain.py"


def write_json(path, value):
    with path.open("x", encoding="utf8") as f:
        json.dump(value, f, indent=2)
        f.write("\n")


def snapshot(source, destination):
    destination.mkdir(parents=True, exist_ok=False)
    for f in bot_files(source):
        dest = destination / f.relative_to(source)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dest)
    return destination


def make_variant(source, destination, cap):
    if cap not in CAPS:
        raise ValueError("unsupported population cap")
    if (source / "movement.py").exists() or (source / "population_config.py").exists():
        raise ValueError("baseline already contains experiment module names")
    snapshot(source, destination)
    (destination / "brain.py").rename(destination / "movement.py")
    shutil.copy2(TEMPLATE, destination / "brain.py")
    (destination / "population_config.py").write_text(f"CAP = {cap}\n", encoding="utf8")
    return destination


def reserve_maps(maps):
    ordered = sorted(maps, key=map_signature)
    if len(ordered) < 8:
        raise ValueError("need at least eight unique maps for this design")
    if len({map_signature(p) for p in ordered}) != len(ordered):
        raise ValueError("duplicate map configurations")
    return ordered[:4], ordered[4:]


def jobs_for(candidates, opponents, maps, seeds, replay_dir=None):
    jobs = []
    for candidate in candidates:
        for opponent in opponents:
            for m in maps:
                for seed in seeds:
                    block = [opponent.name, m.stem, seed]
                    for a, b in ((candidate, opponent), (opponent, candidate)):
                        jobs.append((str(m), str(a), str(b), seed,
                                     str(replay_dir) if replay_dir else None, block))
    return jobs


def tally(games, candidate):
    t = arena.Tally()
    for g in games:
        if candidate in (g["bot_a"], g["bot_b"]):
            t.add(arena.score_for(g, candidate), tuple(g["block"]), arena.is_error(g))
    return t


def paired_delta(games, candidate, control):
    """Require matched successful games; bootstrap differences, not two CIs.

    Map-cluster CI resamples all seeds/opponents/sides of a map together.
    The finer opponent+map+seed interval is also provided for transparency.
    """
    by_bot = {}
    for bot in (candidate, control):
        scores = {}
        for g in games:
            if bot not in (g["bot_a"], g["bot_b"]):
                continue
            score = arena.score_for(g, bot)
            if score is None:
                raise ValueError("paired comparison contains an error")
            side = "A" if g["bot_a"] == bot else "B"
            key = (*g["block"], side)
            if key in scores:
                raise ValueError("duplicate paired game")
            scores[key] = score
        by_bot[bot] = scores
    a, b = by_bot[candidate], by_bot[control]
    if not a or a.keys() != b.keys():
        raise ValueError("candidate and control games are not matched")
    blocks, maps = defaultdict(list), defaultdict(list)
    for key in sorted(a):
        delta = a[key] - b[key]
        blocks[key[:3]].append(delta)
        maps[key[1]].append(delta)
    if len(maps) < 2:
        raise ValueError("need multiple maps for uncertainty")
    return {"difference": statistics.mean(a[k] - b[k] for k in a),
            "map_cluster_ci95": arena.block_bootstrap(list(maps.values())),
            "paired_block_ci95": arena.block_bootstrap(list(blocks.values())),
            "maps": len(maps), "blocks": len(blocks), "matched_games": len(a)}


def stage(out, name, candidates, opponents, maps, seeds, workers, keep_replays=False):
    folder = out / name
    folder.mkdir()
    prov = arena.provenance(candidates + opponents, maps,
                            {"seeds": list(seeds), "workers": workers, "stage": name})
    write_json(folder / "run.json", prov)
    jobs = jobs_for(candidates, opponents, maps, seeds,
                    folder / "replays" if keep_replays else None)
    games = arena.run_jobs(jobs, workers, name)
    games.sort(key=lambda g: (g["bot_a"], g["bot_b"], g["map"], g["seed"]))
    with (folder / "games.jsonl").open("x", encoding="utf8") as f:
        for game in games:
            f.write(json.dumps(game) + "\n")
    warnings = arena.check_hashes(games, prov)
    errors = sum(arena.is_error(g) for g in games)
    if warnings or errors or len(games) != len(jobs):
        raise RuntimeError(f"stage invalid: {errors} errors; {warnings}; inspect {folder}")
    body = "\n\n".join(f"## {p.name}\n\n{arena.summarize_eval(games, p.name)}"
                       for p in candidates)
    (folder / "summary.md").write_text(body + "\n", encoding="utf8")
    return games


def audit_saved_run(out):
    """Recheck map identity without replaying games or reselecting a policy.

    Keep original evidence intact; exclusions are based ONLY on map identity.
    Useful when map canonicalization changes after a run. A duplicate inside
    screening invalidates selection and requires a new experiment instead.
    """
    plan = json.loads((out / "plan.json").read_text())
    selected = json.loads((out / "selection.json").read_text())["selected"]
    screen = [pathlib.Path(p) for p in plan["screen_maps"]]
    seen = {map_signature(m) for m in screen}
    if len(seen) != len(screen):
        raise ValueError("screen contains duplicate maps; cannot retain selection")
    kept, excluded = [], {}
    for name in plan["holdout_maps"]:
        m = pathlib.Path(name)
        sig = map_signature(m)
        if sig in seen:
            excluded[m.stem] = "same semantic map as screening or an earlier held-out map"
        else:
            kept.append(m.stem)
            seen.add(sig)
    games = [json.loads(line) for line in (out / "holdout" / "games.jsonl").read_text().splitlines()]
    filtered = [g for g in games if g["map"] in kept]
    delta = paired_delta(filtered, selected, plan["control"])
    audit = out / "map-audit"
    audit.mkdir(exist_ok=False)
    write_json(audit / "comparison.json", {**delta, "kept_maps": kept,
               "excluded_maps": excluded, "excluded_games": len(games) - len(filtered),
               "map_identity_code_hash": file_hash(ROOT / "bcsim" / "paths.py"),
               "selection_changed": False})
    with (audit / "games.jsonl").open("x", encoding="utf8") as f:
        for g in filtered:
            f.write(json.dumps(g) + "\n")
    body = "# Corrected population result after map-identity audit\n\n"
    body += (f"Excluded {len(games) - len(filtered)} games solely by map identity. "
             "Original results are retained, but their seven-map holdout is superseded. "
             "Screening selection is unchanged.\n\n")
    body += "\n\n".join(f"## {p}\n\n{arena.summarize_eval(filtered, p)}"
                          for p in (plan["control"], selected))
    lo, hi = delta["map_cluster_ci95"]
    body += (f"\nPaired improvement: {100 * delta['difference']:.2f} percentage points; "
             f"95% map-cluster interval [{100 * lo:.2f}, {100 * hi:.2f}] points. "
             f"Only {delta['maps']} distinct held-out maps; conditional local evidence only.\n")
    (audit / "summary.md").write_text(body, encoding="utf8")
    print(body)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--audit", type=pathlib.Path, help="audit maps in an existing result directory")
    args = parser.parse_args()
    if args.audit:
        audit_saved_run(args.audit.resolve())
        return
    if args.workers < 1:
        parser.error("workers must be positive")
    screen, holdout = reserve_maps(resolve_maps("all"))
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-population-" + uuid.uuid4().hex[:6])
    out.mkdir(parents=True, exist_ok=False)
    candidates = [make_variant(ROOT / "mybot", out / "bots" / f"pop_{cap:02d}", cap)
                  for cap in CAPS]
    opponents = [snapshot(ROOT / rel, out / "bots" / name)
                 for rel, name in (("versions/v1", "v1"), ("opponents/splitter", "splitter"),
                                   ("opponents/hunter", "hunter"))]
    map_dir = out / "maps"
    map_dir.mkdir()
    copied = {}
    for m in screen + holdout:
        dest = map_dir / f"{m.stem}_{map_signature(m)}.map"
        shutil.copy2(m, dest)
        copied[m] = dest
    plan = {
        "question": "Does splitting improve fixed greedy movement, and which live population cap?",
        "caps": CAPS, "split_threshold": 8, "split_size": "length // 2",
        "control": "pop_00", "opponents": [p.name for p in opponents],
        "screen_maps": [str(copied[p]) for p in screen], "screen_seeds": [0, 1],
        "holdout_maps": [str(copied[p]) for p in holdout], "holdout_seeds": list(range(1000, 1004)),
        "selection": "highest screen match score among split caps; exact ties prefer smaller cap",
        "confirmation": "selected cap vs no-split on identical reserved matchups; map-cluster delta CI",
        "limits": "local scripted opponents; finite maps; bot RNG seeds only; in-process, not CPU-metered",
        "runner_hash": file_hash(pathlib.Path(__file__)), "template_hash": file_hash(TEMPLATE),
        "baseline_hash": arena.bot_hash(ROOT / "mybot"),
    }
    write_json(out / "plan.json", plan)  # written BEFORE any experimental game
    print(f"Experiment: {out}", flush=True)
    games = stage(out, "screen", candidates, opponents, [copied[m] for m in screen],
                  plan["screen_seeds"], args.workers)
    ranking = sorted(candidates[1:], key=lambda p: (-tally(games, p.name).score, int(p.name[4:])))
    chosen = ranking[0]
    selection = {"selected": chosen.name,
                 "screen_scores": {p.name: tally(games, p.name).score for p in candidates}}
    write_json(out / "selection.json", selection)  # irrevocable before holdout
    print(json.dumps(selection, indent=2), flush=True)
    confirmation = stage(out, "holdout", [candidates[0], chosen], opponents,
                         [copied[m] for m in holdout], plan["holdout_seeds"], args.workers, True)
    delta = paired_delta(confirmation, chosen.name, candidates[0].name)
    write_json(out / "comparison.json", delta)
    lines = ["# Population experiment", "", f"Selected on screen only: {chosen.name}.", "",
             "| policy | screen score | held-out score |", "|---|---:|---:|"]
    for p in candidates:
        held = tally(confirmation, p.name)
        held_text = f"{held.score:.1%}" if held.n else "not tested"
        lines.append(f"| {p.name} | {tally(games, p.name).score:.1%} | {held_text} |")
    lo, hi = delta["map_cluster_ci95"]
    lines += ["", f"Held-out improvement over no-split: {delta['difference']:+.1%}; "
              f"95% map-cluster bootstrap interval [{lo:+.1%}, {hi:+.1%}].", "",
              f"Only {delta['maps']} reserved maps: this is conditional local-pool evidence, "
              "not a ladder-strength or CPU-budget claim. Map families may overlap between stages.", "",
              "Score = wins + half draws, divided by games. Errors invalidate the stage.", "",
              "mybot and all original bots/data remain unchanged. See plan.json, both stage "
              "summaries, raw games and held-out replays for audit."]
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
