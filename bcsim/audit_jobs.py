"""Checkpoint exact replay audits independently from game-running checkpoints."""

import hashlib
import json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from types import SimpleNamespace

from . import arena
from .paths import bot_hash, file_hash, map_signature


def verify_map(mapfile, replay_text):
    # Reuse the existing semantic normalizer without changing its path API or
    # writing a temporary map. The engine is allowed to reorder map records.
    embedded = SimpleNamespace(read_text=lambda **kwargs: replay_text)
    assert map_signature(Path(mapfile)) == map_signature(embedded), "replay map differs semantically"


def run(tasks, workers, folder, function, label):
    logpath = folder / "audit-progress.jsonl"
    cached, signatures = {}, {}
    if logpath.exists():
        for line in logpath.read_text(encoding="utf8").splitlines():
            row = json.loads(line)
            if row["key"] in cached:
                raise ValueError("duplicate audit checkpoint")
            cached[row["key"]] = row
    for task in tasks:
        game, botpath, mapfile = task
        bot_sig = bot_hash(Path(botpath)) if botpath else None
        data = [game, bot_sig, file_hash(Path(mapfile)), file_hash(Path(game["replay"]))]
        sig = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
        key = str(Path(game["replay"]).resolve())
        signatures[key] = sig
        if key in cached and cached[key]["input_hash"] != sig:
            raise ValueError(f"audit inputs changed: {key}")
    if set(cached) - set(signatures):
        raise ValueError("checkpoint contains unrelated games")
    pending = [t for t in tasks if str(Path(t[0]["replay"]).resolve()) not in cached]
    with logpath.open("a", encoding="utf8") as log:
        for offset in range(0, len(pending), workers * 12):
            batch = pending[offset:offset + workers * 12]
            with ProcessPoolExecutor(workers, initializer=arena._init_worker) as pool:
                for task, (counts, samples) in zip(batch, pool.map(function, batch)):
                    key = str(Path(task[0]["replay"]).resolve())
                    row = {"key": key, "input_hash": signatures[key], "counts": counts, "samples": samples}
                    log.write(json.dumps(row) + "\n")
                    log.flush()
                    cached[key] = row
            actions = sum(r["counts"].get("verified_candidate_turns", 0) for r in cached.values())
            print(f"{label}: {len(cached)}/{len(tasks)} replays, {actions} actions matched", flush=True)
    counts, samples = Counter(), {}
    for row in cached.values():
        counts.update(row["counts"])
        for category, sample in row["samples"].items():
            if category not in samples or sample["score"] > samples[category]["score"]:
                samples[category] = sample
    return counts, samples
