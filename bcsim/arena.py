"""Parallel local testing.

  Evaluate one bot against a pool (every map, both sides, several seeds):
    python -m bcsim.arena eval mybot --vs greedy,hunter,splitter,turtle,wanderer
    python -m bcsim.arena eval mybot --vs v3 --maps server --seeds 8 --save-replays losses

  Round-robin tournament with Elo ratings:
    python -m bcsim.arena tournament mybot v3 v2 greedy hunter --seeds 2

  Snapshot the current bot so later versions can be tested against it:
    python -m bcsim.arena freeze            # copies mybot/ to versions/vN/

Matches run on every CPU core (one engine per worker process). Results go
to results/<timestamp>-<name>/ as games.jsonl and summary.md.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import pathlib
import shutil
import subprocess
import sys
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed

from .paths import RESULTS, ROOT, resolve_bot, resolve_maps

DEFAULT_POOL = "greedy,hunter,splitter,turtle,wanderer"


# -- workers ---------------------------------------------------------------------


def _init_worker() -> None:
    # One engine per process, built once; keep workers from fighting over cores.
    try:
        import psutil  # optional
        psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if os.name == "nt" else 5)
    except Exception:
        pass
    from .match import engine
    engine()


def _job(args: tuple) -> dict:
    from .match import play

    map_path, a, b, seed, replay_dir, _keep = args
    replay_to = None
    if replay_dir is not None:
        a_name, b_name, m_name = pathlib.Path(a).name, pathlib.Path(b).name, pathlib.Path(map_path).stem
        replay_to = pathlib.Path(replay_dir) / f"{a_name}-vs-{b_name}-{m_name}-s{seed}.replay"
    d = play(pathlib.Path(map_path), pathlib.Path(a), pathlib.Path(b),
             seed=seed, replay_to=replay_to).to_dict()
    if replay_to is not None and replay_to.exists():
        d["replay"] = str(replay_to)   # cmd_eval deletes the ones it doesn't keep
    return d


def run_jobs(jobs: list[tuple], workers: int, label: str) -> list[dict]:
    out = []
    start = time.perf_counter()
    last = 0.0
    if workers <= 1:
        _init_worker()
        for j in jobs:
            out.append(_job(j))
            _progress(len(out), len(jobs), start, label)
        print()
        return out
    with ProcessPoolExecutor(workers, initializer=_init_worker) as pool:
        futures = [pool.submit(_job, j) for j in jobs]
        for f in as_completed(futures):
            out.append(f.result())
            now = time.perf_counter()
            if now - last > 0.5 or len(out) == len(jobs):
                _progress(len(out), len(jobs), start, label)
                last = now
    print()
    return out


def _progress(done: int, total: int, start: float, label: str) -> None:
    el = time.perf_counter() - start
    rate = done / el if el else 0
    eta = (total - done) / rate if rate else 0
    print(f"\r{label}: {done}/{total} games  {rate:.1f} games/s  eta {eta:.0f}s   ", end="", flush=True)


# -- stats -----------------------------------------------------------------------


def wilson(score: float, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = score / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def elo_gap(p: float) -> float:
    p = min(max(p, 1e-3), 1 - 1e-3)
    return -400 * math.log10(1 / p - 1)


def score_for(game: dict, bot: str) -> float | None:
    """1 win, 0.5 draw, 0 loss from `bot`'s point of view."""
    side = "A" if game["bot_a"] == bot else "B" if game["bot_b"] == bot else None
    if side is None:
        return None
    if game["winner"] is None:
        return 0.5
    return 1.0 if game["winner"] == side else 0.0


# -- commands --------------------------------------------------------------------


def _out_dir(name: str) -> pathlib.Path:
    d = RESULTS / f"{time.strftime('%Y%m%d-%H%M%S')}-{name}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _git_rev() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True).stdout.strip()
    except OSError:
        return "?"


def cmd_eval(args) -> None:
    focus = resolve_bot(args.bot)
    pool = [resolve_bot(n) for n in args.vs.split(",") if n]
    maps = resolve_maps(args.maps)
    out = _out_dir(focus.name)
    replay_dir = out / "replays" if args.save_replays != "none" else None

    jobs = []
    for opp, m, s in itertools.product(pool, maps, range(args.seeds)):
        jobs.append((str(m), str(focus), str(opp), s, replay_dir, args.save_replays))
        jobs.append((str(m), str(opp), str(focus), s, replay_dir, args.save_replays))
    print(f"{focus.name} vs {', '.join(p.name for p in pool)} on {len(maps)} maps x "
          f"{args.seeds} seeds x 2 sides = {len(jobs)} games, {args.workers} workers")
    games = run_jobs(jobs, args.workers, focus.name)

    if replay_dir is not None and args.save_replays == "losses":
        for g in games:
            if score_for(g, focus.name) == 1.0 and g.get("replay"):
                pathlib.Path(g["replay"]).unlink(missing_ok=True)

    with (out / "games.jsonl").open("w", encoding="utf8") as f:
        for g in games:
            f.write(json.dumps(g) + "\n")
    summary = summarize_eval(games, focus.name, pool, maps)
    header = (f"# {focus.name} evaluation\n\n{time.strftime('%Y-%m-%d %H:%M')} · git {_git_rev()} · "
              f"{len(games)} games\n\n")
    (out / "summary.md").write_text(header + summary, encoding="utf8")
    print(summary)
    print(f"saved to {out}")


def summarize_eval(games: list[dict], focus: str, pool, maps) -> str:
    by_opp = defaultdict(list)
    by_map = defaultdict(list)
    deaths = defaultdict(int)
    errors = [g for g in games if g.get("error")]
    for g in games:
        s = score_for(g, focus)
        opp = g["bot_b"] if g["bot_a"] == focus else g["bot_a"]
        by_opp[opp].append(s)
        by_map[g["map"]].append(s)
        side = "A" if g["bot_a"] == focus else "B"
        for k, v in g.get("deaths", {}).items():
            if k.startswith(side + ":"):
                deaths[k[2:]] += v

    names = {"W": "hit kelp", "S": "hit itself", "O": "hit other body",
             "H": "head-to-head", "A": "no valid action/timeout"}
    lines = ["| opponent | score | win % | 95% CI | Elo diff | games |", "|---|---|---|---|---|---|"]
    total = []
    for opp, ss in sorted(by_opp.items()):
        total += ss
        lo, hi = wilson(sum(ss), len(ss))
        p = sum(ss) / len(ss)
        lines.append(f"| {opp} | {sum(ss):g}/{len(ss)} | {100 * p:.0f}% | {100 * lo:.0f}-{100 * hi:.0f}% | "
                     f"{elo_gap(p):+.0f} | {len(ss)} |")
    p = sum(total) / len(total) if total else 0
    lo, hi = wilson(sum(total), len(total))
    lines.append(f"| **overall** | {sum(total):g}/{len(total)} | **{100 * p:.0f}%** | "
                 f"{100 * lo:.0f}-{100 * hi:.0f}% | {elo_gap(p):+.0f} | {len(total)} |")
    lines += ["", "| map | win % | games |", "|---|---|---|"]
    for m, ss in sorted(by_map.items(), key=lambda kv: sum(kv[1]) / len(kv[1])):
        lines.append(f"| {m} | {100 * sum(ss) / len(ss):.0f}% | {len(ss)} |")
    if deaths:
        lines += ["", f"{focus} dragon deaths: " + ", ".join(
            f"{names.get(k, k)} {v}" for k, v in sorted(deaths.items(), key=lambda kv: -kv[1]))]
    if errors:
        lines += ["", f"**{len(errors)} games errored**, e.g. {errors[0]['error']}"]
    return "\n".join(lines) + "\n"


def cmd_tournament(args) -> None:
    bots = [resolve_bot(n) for n in args.bots]
    maps = resolve_maps(args.maps)
    out = _out_dir("tournament")
    jobs = []
    for a, b in itertools.combinations(bots, 2):
        for m, s in itertools.product(maps, range(args.seeds)):
            jobs.append((str(m), str(a), str(b), s, None, "none"))
            jobs.append((str(m), str(b), str(a), s, None, "none"))
    print(f"{len(bots)} bots, {len(maps)} maps, {len(jobs)} games, {args.workers} workers")
    games = run_jobs(jobs, args.workers, "tournament")
    with (out / "games.jsonl").open("w", encoding="utf8") as f:
        for g in games:
            f.write(json.dumps(g) + "\n")

    names = [b.name for b in bots]
    ratings = fit_elo(games, names)
    pair = defaultdict(lambda: [0.0, 0])
    for g in games:
        s = score_for(g, g["bot_a"])
        pair[g["bot_a"], g["bot_b"]][0] += s
        pair[g["bot_a"], g["bot_b"]][1] += 1
        pair[g["bot_b"], g["bot_a"]][0] += 1 - s
        pair[g["bot_b"], g["bot_a"]][1] += 1
    order = sorted(names, key=lambda n: -ratings[n])
    lines = ["| # | bot | Elo | " + " | ".join(order) + " |",
             "|---|---|---|" + "---|" * len(order)]
    for i, n in enumerate(order, 1):
        cells = []
        for m in order:
            if m == n:
                cells.append("-")
            else:
                s, c = pair[n, m]
                cells.append(f"{100 * s / c:.0f}%" if c else "")
        lines.append(f"| {i} | {n} | {ratings[n]:.0f} | " + " | ".join(cells) + " |")
    text = "\n".join(lines) + "\n"
    (out / "summary.md").write_text(f"# Tournament\n\n{time.strftime('%Y-%m-%d %H:%M')} · "
                                    f"{len(games)} games\n\n" + text, encoding="utf8")
    print(text)
    print(f"saved to {out}")


def fit_elo(games: list[dict], names: list[str], iters: int = 2000) -> dict[str, float]:
    """Maximum-likelihood Elo (Bradley–Terry) from game results, mean 1500."""
    r = {n: 0.0 for n in names}
    results = [(g["bot_a"], g["bot_b"], score_for(g, g["bot_a"])) for g in games if not g.get("error")]
    for _ in range(iters):
        grad = {n: 0.0 for n in names}
        for a, b, s in results:
            e = 1 / (1 + 10 ** ((r[b] - r[a]) / 400))
            grad[a] += s - e
            grad[b] -= s - e
        for n in names:
            r[n] += 8 * grad[n] / max(1, len(results) / len(names))
        mean = sum(r.values()) / len(r)
        for n in names:
            r[n] -= mean
    return {n: 1500 + v for n, v in r.items()}


def cmd_freeze(args) -> None:
    src = resolve_bot(args.bot)
    versions = ROOT / "versions"
    versions.mkdir(exist_ok=True)
    if args.name:
        name = args.name
    else:
        nums = [int(p.name[1:]) for p in versions.glob("v*") if p.name[1:].isdigit()]
        name = f"v{max(nums, default=0) + 1}"
    dst = versions / name
    if dst.exists():
        raise SystemExit(f"{dst} already exists")
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    (dst / "FROZEN.txt").write_text(f"frozen from {src.name} at {time.strftime('%Y-%m-%d %H:%M')}, "
                                    f"git {_git_rev()}\n", encoding="utf8")
    print(f"froze {src.name} -> {dst}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    workers = max(1, (os.cpu_count() or 2) - 1)

    e = sub.add_parser("eval", help="one bot vs a pool of opponents")
    e.add_argument("bot")
    e.add_argument("--vs", default=DEFAULT_POOL, help=f"comma list (default {DEFAULT_POOL})")
    e.add_argument("--maps", default="all", help="all | bundled | server | names/globs, comma separated")
    e.add_argument("--seeds", type=int, default=2)
    e.add_argument("--workers", type=int, default=workers)
    e.add_argument("--save-replays", choices=["none", "losses", "all"], default="losses")
    e.set_defaults(func=cmd_eval)

    t = sub.add_parser("tournament", help="round robin with Elo")
    t.add_argument("bots", nargs="+")
    t.add_argument("--maps", default="all")
    t.add_argument("--seeds", type=int, default=1)
    t.add_argument("--workers", type=int, default=workers)
    t.set_defaults(func=cmd_tournament)

    f = sub.add_parser("freeze", help="snapshot a bot into versions/")
    f.add_argument("bot", nargs="?", default="mybot")
    f.add_argument("--name")
    f.set_defaults(func=cmd_freeze)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
