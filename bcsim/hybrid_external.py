"""No-fit imitation diagnostic on the user's newer top-team replay archives.

These games motivated the research and are NOT a pristine unseen benchmark.
They were excluded from model fitting, epoch selection and initialization selection.
"""

import argparse
import json
import math
import os
import random
import sys
import zipfile
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from . import population, reconstruct, replay
from .paths import ROOT, bot_hash, file_hash


def job(args):
    archive, member, out = args
    import psutil
    psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if os.name == "nt" else 5)
    out = Path(out)
    sys.path.insert(0, str(out / "bots/linear"))
    import bc
    import action_value
    # Read exports as data; model inference uses the same portable score path.
    selection = json.loads((out / "models/selection.json").read_text())
    models = {n: json.loads((out / "models" / f"{selection[n]}.json").read_text())
              for n in ("linear", "mlp")}
    with zipfile.ZipFile(archive) as z:
        r = replay.decode(z.read(member))
    counts, correct, loss = Counter(), Counter(), Counter()
    rng = random.Random(31000 + int(Path(member).stem.removeprefix("M")))
    for turn in reconstruct.turns(r):
        counts["turns"] += 1
        if rng.random() >= 1 / 16:
            continue
        counts["sampled"] += 1
        if not turn.action or turn.action[0] != "move" or len(turn.action[1]) != 1:
            counts["non_single"] += 1
            continue
        obs = bc.Obs(turn.block)
        ds = action_value.candidates(obs, turn.team)
        if turn.action[1] not in ds:
            counts["outside_candidates"] += 1
            continue
        if len(ds) < 2:
            counts["forced"] += 1
            continue
        _, rows = action_value.features(obs, turn.team, ds)
        counts["rows"] += 1
        correct["uniform_expected"] += 1 / len(ds)
        correct["straight"] += (obs.facing if obs.facing in ds else ds[0]) == turn.action[1]
        for name, model in models.items():
            scores = [action_value.score(row, model) for row in rows]
            predicted = max(range(len(ds)), key=lambda i: (scores[i], ds[i] == obs.facing))
            correct[name] += ds[predicted] == turn.action[1]
            largest = max(scores)
            loss[name] += math.log(sum(math.exp(s - largest) for s in scores)) + largest - scores[ds.index(turn.action[1])]
    return {"archive": archive, "member": member, "map": r.map_name,
            "counts": dict(counts), "correct": dict(correct), "loss": dict(loss)}


def run(out, workers):
    folder = out / "external-imitation"
    folder.mkdir()
    archives = sorted((ROOT / "replays/topbotgames").glob("*.zip"))
    tasks, seen = [], set()
    for path in archives:
        with zipfile.ZipFile(path) as z:
            for member in z.namelist():
                if not member.endswith(".replay"):
                    continue
                assert member not in seen
                seen.add(member)
                tasks.append((str(path), member, str(out)))
    population.write_json(folder / "plan.json", {
        "archives": {str(p): file_hash(p) for p in archives}, "games": len(tasks),
        "models": {n: bot_hash(out / "bots" / n) for n in ("linear", "neural")},
        "sample_probability": 1 / 16, "code_hash": file_hash(Path(__file__)),
        "limits": "Newer games excluded from fitting, but previously inspected and used to motivate features. "
                  "This is conditional imitation, not live strength, with no fitting or reselection."})
    results = []
    with (folder / "games.jsonl").open("x") as log:
        for offset in range(0, len(tasks), 12):
            with ProcessPoolExecutor(workers) as pool:
                for future in as_completed([pool.submit(job, t) for t in tasks[offset:offset + 12]]):
                    row = future.result()
                    results.append(row)
                    log.write(json.dumps(row) + "\n"); log.flush()
                    print(f"external imitation {len(results)}/{len(tasks)}", flush=True)
    counts, correct, loss = Counter(), Counter(), Counter()
    for row in results:
        counts.update(row["counts"]); correct.update(row["correct"]); loss.update(row["loss"])
    metrics = {"counts": dict(counts), "accuracy": {n: v / counts["rows"] for n, v in correct.items()},
               "cross_entropy": {n: v / counts["rows"] for n, v in loss.items()}}
    population.write_json(folder / "metrics.json", metrics)
    print(json.dumps(metrics, indent=2), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("experiment", type=Path)
    p.add_argument("--workers", type=int, default=4)
    args = p.parse_args()
    run(args.experiment, args.workers)
