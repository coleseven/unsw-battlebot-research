"""M2 provisional-student check (NEW_MOVER_PLAN.md section 5, pilot gate).

Fit a linear residual on pairwise preferences from part of the pilot's source
games and score its choices on the reserved games, using outcomes already
recorded for every candidate. Labels: final longest-dragon margin (ours minus
theirs) and, separately, the game result. Groups are whole source games.

    python -m bcsim.mover_pilot_check results/mover-m2
"""
from __future__ import annotations

import json
import random
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np


def load(d: Path):
    dec = json.loads((d / "decisions.json").read_text())
    lab = defaultdict(dict)
    for r in map(json.loads, (d / "labels.jsonl").read_text().splitlines()):
        lab[r["key"]][r["dir"]] = r
    rows = []
    for i, x in enumerate(dec):
        L = lab[i]
        if len(L) != len(x["cands"]):
            continue
        dirs = list(x["cands"])
        F = np.array([x["cands"][k] for k in dirs], dtype=float)
        s0 = F[:, 36].copy()
        margin = np.array([L[k]["our_longest"] - L[k]["their_longest"] for k in dirs], dtype=float)
        result = np.array([L[k]["result"] for k in dirs], dtype=float)
        row = {"game": x["source"]["replay"], "dirs": dirs, "F": F, "s0": s0, "margin": margin,
               "result": result, "chosen": dirs.index(x["chosen"])}
        for h in ("20", "40", "80"):
            def hv(k, what):
                hz = L[k].get("horizon", {}).get(h)
                if hz and hz["reached"]:
                    return hz["our_" + what] - hz["their_" + what]
                return L[k]["our_" + what] - L[k]["their_" + what]   # game over before h: final state
            if all("horizon" in L[k] for k in dirs):
                row[f"h{h}_total"] = np.array([hv(k, "total") for k in dirs], dtype=float)
                row[f"h{h}_longest"] = np.array([hv(k, "longest") for k in dirs], dtype=float)
        rows.append(row)
    return rows


def prep(rows, scale, mean, std):
    out = []
    for r in rows:
        F = r["F"].copy()
        m = r["s0"].mean()
        F[:, 36] = (r["s0"] - m) / scale
        F[:, 37] = F[:, 37] / scale
        F[:, 38] = (r["s0"] - r["F"][:, 37] - m) / scale
        out.append((F - mean) / std)
    return out


def fit(X, rows, label, l2=1e-2, resid=1e-2, steps=400, lr=0.05):
    """Pairwise logistic loss on q = q0 + 2 tanh(w.x); weight 1 per decision."""
    w = np.zeros(X[0].shape[1])
    for _ in range(steps):
        g = l2 * w
        for x, r in zip(X, rows):
            y = r[label]
            q0 = r["F"][:, 36] * 0  # q0 enters through x[36]; residual only learns the correction
            pairs = [(a, b) for a in range(len(y)) for b in range(len(y)) if y[a] > y[b]]
            if not pairs:
                continue
            f = x @ w
            r_ = 2 * np.tanh(f)
            base = (r["s0"] - r["s0"].mean()) / SCALE
            q = base + r_
            for a, b in pairs:
                p = 1 / (1 + np.exp(-(q[a] - q[b])))
                coef = -(1 - p) / len(pairs)
                da = 2 * (1 - np.tanh(f[a]) ** 2) * x[a]
                db = 2 * (1 - np.tanh(f[b]) ** 2) * x[b]
                g += coef * (da - db)
            g += resid * (r_ @ ((2 * (1 - np.tanh(f) ** 2))[:, None] * x)) / len(y)
        w -= lr * g / len(X)
    return w


SCALE = 1.0
L2, RESID = 0.05, 0.05


def main() -> None:
    global SCALE
    d = Path(sys.argv[1] if len(sys.argv) > 1 else "results/mover-m2")
    rows = load(d)
    games = sorted({r["game"] for r in rows})
    rng = random.Random(7)
    rng.shuffle(games)
    held = set(games[: len(games) // 3])
    train = [r for r in rows if r["game"] not in held]
    test = [r for r in rows if r["game"] in held]
    ranges = [r["s0"].max() - r["s0"].min() for r in train if r["s0"].max() > r["s0"].min()]
    SCALE = max(1.0, float(np.median(ranges)))
    allF = np.vstack([r["F"] for r in train])
    mean, std = allF.mean(0), allF.std(0) + 1e-6
    Xtr, Xte = prep(train, SCALE, mean, std), prep(test, SCALE, mean, std)
    report = {"decisions": len(rows), "train": len(train), "test": len(test), "score_scale": SCALE}
    labels = [l for l in ("margin", "result", "h20_total", "h40_total", "h80_total", "h40_longest", "h80_longest")
              if all(l in r for r in rows)]
    for label in labels:
        w = fit(Xtr, train, label, l2=L2, resid=RESID)
        report[label] = {}
        for tau in (0.0, 0.5, 1.0):
            ev = {k: [0.0, 0.0] for k in (label, "margin", "result")}
            overrides = better = worse = 0
            for x, r in zip(Xte, test):
                base = (r["s0"] - r["s0"].mean()) / SCALE
                q = base + 2 * np.tanh(x @ w)
                a0 = r["chosen"]
                a = int(np.argmax(q)) if q.max() - q[a0] > tau else a0
                for k in ev:
                    ev[k][0] += r[k][a0]; ev[k][1] += r[k][a]
                if a != a0:
                    overrides += 1
                    better += r[label][a] > r[label][a0]; worse += r[label][a] < r[label][a0]
            report[label][f"tau{tau}"] = {"overrides": overrides, "better": better, "worse": worse,
                                          **{f"{k}_incumbent_vs_student": v for k, v in ev.items()}}
    (d / "pilot_student.json").write_text(json.dumps(report, indent=1, default=float), encoding="utf8")
    print(json.dumps(report, indent=1, default=float))


if __name__ == "__main__":
    main()
