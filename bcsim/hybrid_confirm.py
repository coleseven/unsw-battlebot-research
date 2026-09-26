"""Schedule the unchanged hybrid validation design in independent chunks.

Run the selected role plus its shared control while the evaluator screen is
still running. Add the selected evaluator afterward, then verify and merge.
This changes scheduling only: same candidates, maps, seeds, sides and gates.
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

from . import arena, guarded, population
from .paths import ROOT, bot_hash


def selected(out, family):
    row = json.loads((out / f"{family}-selection.json").read_text())
    name = row["selected"]
    if name:
        assert bot_hash(out / "bots" / name) == row["hash"]
    return name


def run(out, part, workers):
    plan = json.loads((out / "plan.json").read_text())
    role = selected(out, "roles")
    if part == "core":
        names = ["control_450"] + ([role] if role else [])
    else:
        name = selected(out, "evaluators")
        if not name:
            print("No evaluator selected; no extra validation matches.", flush=True)
            return
        names = [name]
    assert bot_hash(ROOT / "versions/v2") == plan["baseline_hash"]
    guarded.stage(out, "validation-" + part, [out / "bots" / n for n in names],
                  [out / "bots" / n for n in ("reference_v2", "splitter", "hunter")],
                  [Path(p) for p in plan["maps"]], plan["validation_seeds"], workers, True)


def merge(out):
    plan = json.loads((out / "plan.json").read_text())
    names = [n for n in (selected(out, "roles"), selected(out, "evaluators")) if n]
    folders = [out / "validation-core"]
    if selected(out, "evaluators"):
        folders.append(out / "validation-evaluator")
    games = []
    for folder in folders:
        batch = [json.loads(l) for l in (folder / "games.jsonl").read_text().splitlines()]
        assert (folder / "summary.md").is_file(), "stage not complete"
        assert not arena.check_hashes(batch, json.loads((folder / "run.json").read_text()))
        games.extend(batch)
    candidates = [out / "bots" / n for n in ["control_450"] + names]
    opponents = [out / "bots" / n for n in ("reference_v2", "splitter", "hunter")]
    maps = [Path(p) for p in plan["maps"]]
    expected = population.jobs_for(candidates, opponents, maps, plan["validation_seeds"])
    expected_keys = {(Path(m).stem, Path(a).name, Path(b).name, s) for m, a, b, s, _, _ in expected}
    actual_keys = {(g["map"], g["bot_a"], g["bot_b"], g["seed"]) for g in games}
    assert len(games) == len(actual_keys) == len(expected_keys)
    assert actual_keys == expected_keys and not any(arena.is_error(g) for g in games)
    folder = out / "validation"
    folder.mkdir()
    provenance = arena.provenance(candidates + opponents, maps,
                                 {"seeds": plan["validation_seeds"], "source_stages": [str(p) for p in folders]})
    population.write_json(folder / "run.json", provenance)
    with (folder / "games.jsonl").open("x") as f:
        for game in games:
            f.write(json.dumps(game) + "\n")
    with (folder / "summary.md").open("x") as f:
        f.write("\n".join(f"# {p.name}\n\n" + arena.summarize_eval(games, p.name) for p in candidates))
    results = {}
    for name in names:
        direct = [g for g in games if name in (g["bot_a"], g["bot_b"]) and
                  "reference_v2" in (g["bot_a"], g["bot_b"])]
        by_map = defaultdict(list)
        for game in direct:
            by_map[game["map"]].append(arena.score_for(game, name))
        ci = arena.block_bootstrap(list(by_map.values()), iters=8000)
        delta = population.paired_delta(games, name, "control_450")
        tally = population.tally(direct, name)
        results[name] = {"direct": {"wins": tally.w, "draws": tally.d, "losses": tally.l,
                                    "score": tally.score, "map_ci95": ci},
                         "paired_pool": delta,
                         "performance_gate": ci[0] > .5 and delta["map_cluster_ci95"][0] > 0}
    assert bot_hash(ROOT / "versions/v2") == plan["baseline_hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    population.write_json(out / "comparison.json", results)
    print(json.dumps(results, indent=2), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("experiment", type=Path)
    p.add_argument("--part", choices=("core", "evaluator"))
    p.add_argument("--merge", action="store_true")
    p.add_argument("--workers", type=int, default=4)
    args = p.parse_args()
    if args.merge:
        merge(args.experiment)
    elif args.part:
        run(args.experiment, args.part, args.workers)
    else:
        p.error("choose --part or --merge")
