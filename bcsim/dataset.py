"""Build a training dataset from scraped replays (all CPU cores).

    python -m bcsim.dataset                    # every replay in data/replays
    python -m bcsim.dataset --min-elo 1800 --winners-only

Writes one compressed shard per game to data/dataset/<game>.npz holding:
    grid    uint8   [N, 17, 7, 7]   features.encode (see framework/features.py)
    scalar  float32 [N, 5]
    kind, dir, steps, split  int16 [N]   the action taken (features.action_label)
    round, dragon, team      int16 [N]
    won     float32 [N]  1 / 0.5 / 0 — did this dragon's team win the game
    elo     int16   [N]  that team's rating at the time
    points  int64   [N]  CPU points used that turn (-1 if not recorded)
Load everything with bcsim.dataset.load_all().
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from .paths import DATA, FRAMEWORK

OUT = DATA / "dataset"
REPLAYS = DATA / "replays"


def _index() -> dict[int, dict]:
    """game id -> {winner, elo_a, elo_b, name_a, name_b}"""
    out = {}
    path = DATA / "index.jsonl"
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf8").splitlines():
        if not line.strip():
            continue
        b = json.loads(line)
        for g in b["games"]:
            out[g["game"]] = {"winner": g["winner"], "elo_a": b["a"]["elo"], "elo_b": b["b"]["elo"],
                              "name_a": b["a"]["name"], "name_b": b["b"]["name"]}
    return out


def _build(args: tuple) -> tuple[int, int]:
    game, meta, winners_only, min_elo = args
    sys.path.insert(0, str(FRAMEWORK))
    import bc
    import features
    from . import replay as rp
    from .reconstruct import turns

    out = OUT / f"{game}.npz"
    if out.is_file():
        return game, -1
    try:
        rep = rp.load(REPLAYS / f"{game}.replay")
    except Exception:
        return game, 0
    winner = meta.get("winner")   # "a" / "b" / None(draw) from the site
    if winner is None and rep.result:
        winner = (rep.result.get("winner") or "").lower() or None
    cols = {k: [] for k in ("grid", "scalar", "kind", "dir", "steps", "split", "round",
                            "dragon", "team", "won", "elo", "points")}
    for t in turns(rep, str(game)):
        won = 0.5 if winner is None else float(winner.upper() == t.team)
        elo = meta.get("elo_a" if t.team == "A" else "elo_b", 0)
        if winners_only and won < 1:
            continue
        if elo < min_elo:
            continue
        g, s = features.encode(bc.Obs(t.block), t.team, t.id)
        kind, d, steps, split = features.action_label(t.action)
        for k, v in (("grid", g), ("scalar", s), ("kind", kind), ("dir", d), ("steps", steps),
                     ("split", split), ("round", t.round), ("dragon", t.id),
                     ("team", 0 if t.team == "A" else 1), ("won", won), ("elo", elo),
                     ("points", -1 if t.points is None else t.points)):
            cols[k].append(v)
    n = len(cols["kind"])
    if n == 0:
        return game, 0
    dtypes = {"grid": np.uint8, "scalar": np.float32, "won": np.float32, "points": np.int64}
    arrays = {k: np.asarray(v, dtype=dtypes.get(k, np.int16)) for k, v in cols.items()}
    tmp = OUT / f"{game}.tmp.npz"
    np.savez_compressed(tmp, **arrays)
    os.replace(tmp, out)
    return game, n


def shards(pattern: str = "*.npz") -> list:
    return [f for f in sorted(OUT.glob(pattern)) if not f.name.endswith(".tmp.npz")]


def load_all(pattern: str = "*.npz", fraction: float = 1.0, seed: int = 0,
             where=None) -> dict[str, np.ndarray]:
    """Concatenate shards into memory. The full corpus is tens of millions of
    turns (~0.8 KB each), so pass `fraction` (random share of each shard's
    turns) and/or `where(z) -> bool mask` to keep RAM in check, e.g.
    where=lambda z: (z["won"] == 1) & (z["elo"] >= 1800)."""
    rng = np.random.default_rng(seed)
    parts: dict[str, list] = {}
    for f in shards(pattern):
        with np.load(f) as z:
            n = len(z["kind"])
            keep = np.ones(n, bool) if where is None else where(z)
            if fraction < 1.0:
                keep &= rng.random(n) < fraction
            for k in z.files:
                parts.setdefault(k, []).append(z[k][keep])
    return {k: np.concatenate(v) for k, v in parts.items()}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--winners-only", action="store_true", help="keep only the winning team's turns")
    ap.add_argument("--min-elo", type=int, default=0, help="keep only turns by teams rated >= this")
    ap.add_argument("--rebuild", action="store_true")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    if args.rebuild:
        for f in OUT.glob("*.npz"):
            f.unlink()
    index = _index()
    games = sorted(int(p.stem) for p in REPLAYS.glob("*.replay"))
    jobs = [(g, index.get(g, {}), args.winners_only, args.min_elo) for g in games]
    start = time.perf_counter()
    total = done = 0
    with ProcessPoolExecutor(args.workers) as pool:
        for game, n in pool.map(_build, jobs, chunksize=4):
            done += 1
            total += max(n, 0)
            if done % 25 == 0 or done == len(jobs):
                el = time.perf_counter() - start
                print(f"\r{done}/{len(jobs)} games  {total} new samples  {done / el:.1f} games/s", end="", flush=True)
    print(f"\ndataset in {OUT}")


if __name__ == "__main__":
    main()
