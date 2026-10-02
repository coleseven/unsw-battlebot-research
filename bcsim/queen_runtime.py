"""Run tooling against the isolated queen-rules toolkit; preserve .venv.

    .venv/Scripts/python -m bcsim.queen_runtime unittest discover -s tests -p test_queen_rules.py
    .venv/Scripts/python -m bcsim.queen_runtime bcsim.queen_baseline

Install unswbc==1.2.3 with pip --no-deps --target results/queen-runtime-packages/1.2.3.
The inherited .venv supplies dependencies. Child processes inherit this runtime.
"""
import os
from pathlib import Path
import runpy
import sys

VERSION = "1.2.3"
PACKAGE = Path(__file__).resolve().parents[1] / "results/queen-runtime-packages" / VERSION


def activate():
    if "unswbc" in sys.modules:
        raise RuntimeError("activate queen runtime before importing unswbc")
    if not (PACKAGE / "unswbc/unswbc_engine.wasm").is_file():
        raise RuntimeError(f"install unswbc=={VERSION} into {PACKAGE} first")
    sys.path.insert(0, str(PACKAGE))
    os.environ["PYTHONPATH"] = str(PACKAGE) + os.pathsep + os.environ.get("PYTHONPATH", "")
    import unswbc
    if unswbc.__version__ != VERSION:
        raise RuntimeError(f"wrong toolkit loaded: {unswbc.__file__}")
    return PACKAGE


if __name__ == "__main__":
    activate()
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    module = sys.argv[1]
    sys.argv = sys.argv[1:]
    runpy.run_module(module, run_name="__main__", alter_sys=True)
