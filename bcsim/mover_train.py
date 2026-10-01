"""Train the R5 mover residual on pilot labels and export framework/mover_r5.json.

    python -m bcsim.mover_train results/mover-m2b --label result --kind linear

Linear residual (f = w.x) exported through the C++ MLP as two hidden units,
relu(w.x) - relu(-w.x) = w.x. Normalisation (score scale, feature mean/std) is
frozen from the training decisions and written with the weights, exactly as
bcsim.mover_pilot_check.prep applies it (the C++ mover_forward mirrors it).
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from . import mover_pilot_check as mpc
from .mover_teacher import FEATURES


def train(pilot: Path, label: str, l2: float, resid: float) -> dict:
    rows = mpc.load(pilot)
    ranges = [r["s0"].max() - r["s0"].min() for r in rows if r["s0"].max() > r["s0"].min()]
    mpc.SCALE = max(1.0, float(np.median(ranges)))
    F = np.vstack([r["F"] for r in rows])
    mean, std = F.mean(0), F.std(0) + 1e-6
    X = mpc.prep(rows, mpc.SCALE, mean, std)
    w = mpc.fit(X, rows, label, l2=l2, resid=resid)
    hidden, n = 24, 64
    w1 = np.zeros((hidden, n)); w1[0] = w; w1[1] = -w
    w2 = np.zeros(hidden); w2[0], w2[1] = 1.0, -1.0
    labels_hash = hashlib.sha256((pilot / "labels.jsonl").read_bytes()).hexdigest()[:16]
    return {"schema": "R5-v1-64", "kind": "linear-as-2-relu", "label": label, "l2": l2, "resid": resid,
            "pilot": str(pilot), "labels_sha256_16": labels_hash, "decisions": len(rows),
            "base_policy_hash": "f9d00cd150ff2c53", "features": FEATURES,
            "score_scale": mpc.SCALE, "mean": mean.tolist(), "std": std.tolist(),
            "w1": w1.reshape(-1).tolist(), "b1": [0.0] * hidden, "w2": w2.tolist(), "b2": 0.0,
            "linear_w": w.tolist()}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pilot", type=Path)
    ap.add_argument("--label", default="result")
    ap.add_argument("--l2", type=float, default=mpc.L2)
    ap.add_argument("--resid", type=float, default=mpc.RESID)
    ap.add_argument("--out", type=Path, default=Path("framework/mover_r5.json"))
    a = ap.parse_args()
    m = train(a.pilot, a.label, a.l2, a.resid)
    a.out.write_text(json.dumps(m, indent=1), encoding="utf8")
    order = np.argsort(-np.abs(np.array(m["linear_w"])))[:12]
    print(f"wrote {a.out}: {m['decisions']} decisions, label {a.label}, score scale {m['score_scale']:.2f}")
    for j in order:
        print(f"  {FEATURES[j]:24} {m['linear_w'][j]:+.3f}")


if __name__ == "__main__":
    main()
