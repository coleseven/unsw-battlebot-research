"""Refit the v3 local move ranker (24 features, linear softmax over the legal
moves) on the decisions of a stronger bot in local games.

    python -m bcsim.ranker_v4 --corpus OUT --teacher sparring/cpp_nicked_v92
    python -m bcsim.ranker_v4 --extract OUT
    python -m bcsim.ranker_v4 --train OUT
    python -m bcsim.ranker_v4 --write OUT --into results/<bot>   # model.hpp

Local replays carry the full observation (public ones redact timers and
sonar), so reconstruct.turns rebuilds each dragon's exact block. Only the
teacher's single-step moves with at least two candidate moves are examples,
as in the original v3 training (bcsim/hybrid.py). Games are split into
train/dev/test by (map, seed) so no game leaks across partitions. This
learns behaviour from played games, not anyone's source code.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from . import bounded, guard, official_suite, population, reconstruct, replay
from .paths import FRAMEWORK

OPPONENTS = ["versions/v10h", "sparring/cpp_nicked_v75", "sparring/cpp_leviathan3",
             "sparring/nicked_lab", "results/v7-base-bot"]
SAMPLE = 0.25


def corpus(out: Path, teacher: str, seeds: int, seed: int) -> None:
    os.environ.setdefault("BCSIM_DETERMINISTIC_V6", "1")
    os.environ.setdefault("BCSIM_CPP_INPROC", "1")
    out.mkdir(parents=True, exist_ok=True)
    maps = official_suite.ranked_maps()
    jobs = population.jobs_for([Path(teacher)], [Path(o) for o in OPPONENTS], maps,
                               [seed + i for i in range(seeds)], out / "replays")
    population.write_json(out / "plan.json", {"teacher": Path(teacher).name, "opponents": OPPONENTS,
                                              "maps": [m.stem for m in maps], "seeds": seeds, "seed": seed})
    bounded.run(jobs, guard.cap_workers(12), out / "games", "ranker-corpus")


def _partition(name: str) -> str:
    # replay names end in -<map>-s<seed>.replay: hash (map, seed) into 70/15/15
    h = sum(ord(c) * (i + 1) for i, c in enumerate("-".join(name.rsplit("-", 2)[-2:]))) % 20
    return "train" if h < 14 else "dev" if h < 17 else "test"


def _extract_one(args):
    path, teacher, dest = args
    sys.path.insert(0, str(FRAMEWORK))
    import numpy as np
    import bc
    import action_value
    r = replay.load(path)
    side = "A" if Path(r.bot_a).name == teacher or r.bot_a == teacher else "B"
    rng = random.Random(hash(Path(path).name) & 0xFFFFFFFF)
    xs, masks, ys, rounds = [], [], [], []
    for turn in reconstruct.turns(r):
        if turn.team != side or rng.random() >= SAMPLE:
            continue
        if not turn.action or turn.action[0] != "move" or len(turn.action[1]) != 1:
            continue
        obs = bc.Obs(turn.block)
        directions = action_value.candidates(obs, turn.team)
        if turn.action[1] not in directions or len(directions) < 2:
            continue
        _, values = action_value.features(obs, turn.team, directions)
        x = np.zeros((4, len(action_value.FEATURES)), dtype=np.float32)
        m = np.zeros(4, dtype=bool)
        for d, v in zip(directions, values):
            x[bc.DIRS.index(d)] = v
            m[bc.DIRS.index(d)] = True
        xs.append(x); masks.append(m); ys.append(bc.DIRS.index(turn.action[1])); rounds.append(turn.round)
    name = Path(path).stem
    np.savez_compressed(Path(dest) / f"{name}.npz", x=np.asarray(xs, dtype=np.float32).reshape(-1, 4, len(action_value.FEATURES)),
                        mask=np.asarray(masks, dtype=bool).reshape(-1, 4), y=np.asarray(ys, dtype=np.int64),
                        rounds=np.asarray(rounds, dtype=np.int16))
    return name, len(ys)


def extract(out: Path, workers: int) -> None:
    plan = json.loads((out / "plan.json").read_text())
    dest = out / "data"
    dest.mkdir(exist_ok=True)
    todo = [p for p in sorted((out / "replays").glob("*.replay")) if not (dest / f"{p.stem}.npz").exists()]
    rows = 0
    with guard.slot("ranker-extract"), ProcessPoolExecutor(guard.cap_workers(workers)) as pool:
        for i, (name, n) in enumerate(pool.map(_extract_one, [(str(p), plan["teacher"], str(dest)) for p in todo])):
            rows += n
            if i % 20 == 0:
                print(f"extracted {i + 1}/{len(todo)} games, {rows} examples", flush=True)
    print(f"done: {len(list(dest.glob('*.npz')))} games", flush=True)


def _load(out: Path):
    import numpy as np
    parts = {"train": [], "dev": [], "test": []}
    for p in sorted((out / "data").glob("*.npz")):
        with np.load(p) as z:
            if len(z["y"]):
                parts[_partition(p.stem)].append({k: z[k].copy() for k in ("x", "mask", "y")})
    return {k: {f: np.concatenate([a[f] for a in v]) for f in ("x", "mask", "y")} for k, v in parts.items() if v}


def _metrics(w, b, part):
    import numpy as np
    s = part["x"] @ w + b
    s = np.where(part["mask"], s, -1e9)
    s = s - s.max(1, keepdims=True)
    logp = s - np.log(np.exp(s).sum(1, keepdims=True))
    n = len(part["y"])
    return {"n": n, "acc": float((s.argmax(1) == part["y"]).mean()),
            "nll": float(-logp[np.arange(n), part["y"]].mean())}


def train(out: Path) -> None:
    import numpy as np
    import torch
    parts = _load(out)
    sys.path.insert(0, str(FRAMEWORK))
    import action_value
    ns = {}
    exec((Path("versions/v3/action_model.py")).read_text(encoding="utf8"), ns)
    old_w, old_b = np.array(ns["MODEL"]["weight"]), ns["MODEL"]["bias"]
    t = {k: torch.from_numpy(parts["train"][k]) for k in ("x", "mask", "y")}
    best = None
    for l2 in (0.0, 1e-4, 1e-3, 1e-2):
        torch.manual_seed(0)
        w = torch.zeros(t["x"].shape[-1], dtype=torch.float32, requires_grad=True)
        opt = torch.optim.LBFGS([w], max_iter=200, line_search_fn="strong_wolfe")
        def closure():
            opt.zero_grad()
            s = (t["x"] @ w).masked_fill(~t["mask"], -1e9)
            loss = torch.nn.functional.cross_entropy(s, t["y"]) + l2 * (w * w).sum()
            loss.backward()
            return loss
        opt.step(closure)
        wn = w.detach().numpy().astype(float)
        dev = _metrics(wn, 0.0, parts["dev"])
        print(f"l2 {l2}: dev acc {dev['acc']:.4f} nll {dev['nll']:.4f}", flush=True)
        if best is None or dev["nll"] < best[1]["nll"]:
            best = (wn, dev, l2)
    w, dev, l2 = best
    report = {"l2": l2, "features": list(action_value.FEATURES),
              "weight": [float(v) for v in w], "bias": 0.0,
              "scale_vs_v3": float(np.linalg.norm(w) / np.linalg.norm(old_w)),
              **{f"{k}_new": _metrics(w, 0.0, parts[k]) for k in parts},
              **{f"{k}_v3": _metrics(old_w, old_b, parts[k]) for k in parts}}
    population.write_json(out / "model.json", report)
    for k in parts:
        print(f"{k}: new {report[k + '_new']}  v3 {report[k + '_v3']}")
    print("weight change (new vs v3):")
    for name, a, b in zip(action_value.FEATURES, w, old_w):
        print(f"  {name:24} {b:+8.3f} -> {a:+8.3f}")


def write(out: Path, into: Path) -> None:
    m = json.loads((out / "model.json").read_text())
    text = ("// Refit by bcsim.ranker_v4 from " + out.name + " (teacher moves). Do not edit by hand.\n\n"
            "#pragma once\n#include <array>\n\nnamespace model {\n\n"
            f"inline constexpr std::array<double, {len(m['weight'])}> WEIGHT = {{"
            + ", ".join(repr(v) for v in m["weight"]) + "};\n"
            f"inline constexpr double BIAS = {m['bias']!r};\n\n}}  // namespace model\n")
    (into / "model.hpp").write_text(text, encoding="utf8")
    print("wrote", into / "model.hpp")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpus", type=Path)
    ap.add_argument("--teacher", default="sparring/cpp_nicked_v92")
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--seed", type=int, default=291001)
    ap.add_argument("--extract", type=Path)
    ap.add_argument("--train", type=Path)
    ap.add_argument("--write", type=Path)
    ap.add_argument("--into", type=Path)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    if a.corpus:
        corpus(a.corpus, a.teacher, a.seeds, a.seed)
    if a.extract:
        extract(a.extract, a.workers)
    if a.train:
        train(a.train)
    if a.write:
        write(a.write, a.into)


if __name__ == "__main__":
    main()
