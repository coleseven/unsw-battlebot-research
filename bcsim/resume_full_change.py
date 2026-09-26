"""Resume only missing jobs from a guarded full-suite RAM stop.

Preserves the partial log; writes a separate completed/ log and final reports.
"""

import argparse
import json
from pathlib import Path

from . import arena, bounded, map_matrix, official_suite, population
from .paths import ROOT, bot_hash, file_hash


def key(game):
    return game["map"], game["bot_a"], game["bot_b"], game["seed"]


def job_key(job):
    map_path, a, b, seed, _, _ = job
    return Path(map_path).stem, Path(a).name, Path(b).name, seed


def resume(out: Path, workers: int):
    plan = json.loads((out / "plan.json").read_text())
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    names = ["candidate", *plan["opponent_sources"]]
    bots = out / "bots"
    for name in names:
        assert bot_hash(bots / name) == plan["bot_hashes"][name]
    maps = [Path(p) for p in plan["maps"]]
    official_suite.require_coverage(maps)
    for path, expected in plan["map_hashes"].items():
        assert file_hash(Path(path)) == expected
    folder = out / "full"
    original = [json.loads(line) for line in (folder / "games.jsonl").read_text().splitlines()]
    if len({key(g) for g in original}) != len(original):
        raise ValueError("duplicate games in partial log")
    jobs = population.jobs_for([bots / "candidate"], [bots / name for name in names[1:]],
                               maps, [plan["seed"]], folder / "replays")
    logged = {key(g) for g in original}
    missing = [job for job in jobs if job_key(job) not in logged]
    print(f"resuming {len(missing)} of {len(jobs)} games with {workers} workers", flush=True)
    new = bounded.run(missing, workers, out / "resume", "resume") if missing else []
    games = original + new
    if len(games) != len(jobs) or {key(g) for g in games} != {job_key(j) for j in jobs}:
        raise ValueError("completed log does not cover every planned game exactly once")
    provenance = json.loads((folder / "run.json").read_text())
    warnings = arena.check_hashes(games, provenance)
    if warnings or any(arena.is_error(g) for g in games):
        raise RuntimeError(f"hash or game error: {warnings}")
    games.sort(key=key)
    complete = out / "completed"
    complete.mkdir()
    with (complete / "games.jsonl").open("x", encoding="utf8") as log:
        for game in games:
            log.write(json.dumps(game) + "\n")
    (complete / "summary.md").write_text(
        "# candidate\n\n" + arena.summarize_eval(games, "candidate"), encoding="utf8")
    result = {"maps": [p.stem for p in maps], "games": len(games),
              "original_games": len(original), "resumed_games": len(new),
              "original_workers": plan["workers"], "resume_workers": workers,
              "opponents": {}}
    for name in names[1:]:
        selected = [g for g in games if name in (g["bot_a"], g["bot_b"])]
        tally = population.tally(selected, "candidate")
        result["opponents"][name] = {"wins": tally.w, "draws": tally.d,
                                      "losses": tally.l, "score": tally.score}
    population.write_json(out / "comparison.json", result)
    with (out / "map_matrix.md").open("x", encoding="utf8") as f:
        f.write(map_matrix.render(games, "candidate", names[1:], result["maps"]))
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", type=Path)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    resume(args.experiment, args.workers)
