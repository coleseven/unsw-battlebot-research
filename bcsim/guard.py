"""Machine-wide limits for heavy game runs: one experiment at a time, few workers.

On 28 Sep the PC blue-screened twice (0xBE, 0x1E) and GCC segfaulted once, each
time while two heavy jobs ran at once (12 + 12 and 12 + 6 game workers on 16
logical CPUs, plus the opponents' own processes). Single 12-worker jobs had run
for hours without trouble. So:

- `slot(label)`: a system-wide lock (results/.experiment.lock). A second heavy
  job waits for the first instead of stacking on top of it. Re-entrant within
  one process; a lock left by a dead process is taken over.
- `cap_workers(n)`: never more than MAX_WORKERS workers (default 8, half the
  logical CPUs here; override with BCSIM_MAX_WORKERS).

Every heavy entry point goes through these (bounded.run, tune replay scoring);
ad-hoc scripts that run games in parallel must use them too.
"""

from __future__ import annotations

import contextlib
import json
import os
import time
from pathlib import Path

from .paths import RESULTS

LOCK = RESULTS / ".experiment.lock"
MAX_WORKERS = int(os.environ.get("BCSIM_MAX_WORKERS", "8"))
_held = 0


def cap_workers(workers: int) -> int:
    if workers > MAX_WORKERS:
        print(f"guard: {workers} workers requested, capped at {MAX_WORKERS} "
              "(set BCSIM_MAX_WORKERS to change)", flush=True)
    return max(1, min(workers, MAX_WORKERS))


def _alive(pid: int) -> bool:
    try:
        import psutil
        return psutil.pid_exists(pid)
    except Exception:
        return True


@contextlib.contextmanager
def slot(label: str = "experiment", poll: float = 30.0):
    """Hold the machine-wide experiment lock for the duration of the block."""
    global _held
    if _held:                       # already ours (nested call in this process)
        _held += 1
        try:
            yield
        finally:
            _held -= 1
        return
    RESULTS.mkdir(exist_ok=True)
    waited = False
    while True:
        try:
            fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, "w") as f:
                json.dump({"pid": os.getpid(), "label": label, "since": time.time()}, f)
            break
        except FileExistsError:
            try:
                info = json.loads(LOCK.read_text())
            except Exception:
                info = {}
            pid = int(info.get("pid", 0) or 0)
            if pid and not _alive(pid):
                LOCK.unlink(missing_ok=True)      # left behind by a crash or kill
                continue
            if not waited:
                print(f"guard: waiting for running experiment {info.get('label')!r} (pid {pid})", flush=True)
                waited = True
            time.sleep(poll)
    _held = 1
    try:
        yield
    finally:
        _held = 0
        LOCK.unlink(missing_ok=True)
