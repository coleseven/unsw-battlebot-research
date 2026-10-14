"""Checkpointed experiment jobs with fresh worker pools between bounded batches.

Native engine/callback state may contribute to observed RSS growth. Recycling
processes bounds lifetime accumulation without modifying installed dependencies
or relying on private Wasmtime cleanup APIs. No game result is changed.
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from . import arena


def measured_job(job):
    import psutil
    process = psutil.Process()
    if psutil.virtual_memory().available < 4 * 2**30:
        raise RuntimeError("Less than 4 GiB RAM available; experiment stopped")
    game = arena._job(job)
    game["worker"] = {"pid": os.getpid(), "rss_bytes": process.memory_info().rss}
    return game


def run(jobs, workers, folder, label="experiment", batch_per_worker=12):
    """Save each result immediately; fail closed on errors, preserve partial work.

    Every pool processes at most workers*batch_per_worker jobs TOTAL. A fast
    worker could receive more than batch_per_worker, so this is not advertised
    as a per-worker task cap. Even single-worker runs use a child process.
    """
    if not 1 <= workers <= 8 or not 1 <= batch_per_worker <= 16:
        raise ValueError("workers must be 1-8 and batch_per_worker 1-16")
    os.environ["RAYON_NUM_THREADS"] = "1"
    folder.mkdir(parents=True, exist_ok=True)
    results, start = [], time.monotonic()
    batch_size = workers * batch_per_worker
    with (folder / "games.jsonl").open("x", encoding="utf8") as log:
        for offset in range(0, len(jobs), batch_size):
            with ProcessPoolExecutor(workers, initializer=arena._init_worker) as pool:
                futures = [pool.submit(measured_job, job) for job in jobs[offset:offset + batch_size]]
                for future in as_completed(futures):
                    game = future.result()
                    results.append(game)
                    log.write(json.dumps(game) + "\n")
                    log.flush()
                    if arena.is_error(game):
                        raise RuntimeError(f"Match failed; partial results saved: {game}")
                    if game["worker"]["rss_bytes"] > 2**30:
                        raise RuntimeError("Worker exceeded 1 GiB RSS; partial results saved")
                    if len(results) % 24 == 0 or len(results) == len(jobs):
                        print(f"{label}: {len(results)}/{len(jobs)} games, "
                              f"{time.monotonic() - start:.0f}s", flush=True)
    return results
