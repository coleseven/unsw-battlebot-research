"""Parallel local testing.

  Evaluate one bot against a pool (every map, both sides, several seeds):
    python -m bcsim.arena eval mybot --vs greedy,hunter,splitter,turtle,wanderer
    python -m bcsim.arena eval mybot --vs v3 --maps server --seeds 8 --save-replays losses

  Round-robin tournament with Elo ratings:
    python -m bcsim.arena tournament mybot v3 v2 greedy hunter --seeds 2

  Snapshot the current bot so later versions can be tested against it:
    python -m bcsim.arena freeze            # copies mybot/ to versions/vN/

Matches run on every CPU core (one engine per worker process). Results go
to results/<timestamp>-<name>/: games.jsonl (one line per game), summary.md
and run.json (code/engine/map hashes, git state, settings).

Scoring: a game scores 1 win / 0.5 draw / 0 loss. "Score" is the mean of
that (match score); "win rate" counts wins only. Errored games count toward
neither, nor toward Elo, and are reported in their own column.

Uncertainty: the games of one opponent+map+seed (one per side; in a
tournament, one bot pair+map+seed) form a block. "score 95% CI" is a
percentile bootstrap of the mean match score, resampling whole blocks, so
the two sides of a pairing stay together and side advantage cancels instead
of inflating the spread. It estimates how the score would vary over new
maps/seeds drawn like these, for this exact code; it says nothing about
opponents or maps outside the pool. Small samples: with fewer than 2 blocks
the interval is reported as 0-100%; with only a few blocks the percentile
bootstrap is too narrow (it cannot see variation that never occurred -- e.g.
if every block splits 1-1 the interval collapses to exactly 50%), so treat
fewer than ~20 blocks as a screen, not a verdict. Games are deterministic for
a given map, seed and code, so re-running identical settings adds no evidence.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import pathlib
import random
import shutil
import subprocess
import sys
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed

from .paths import (FRAMEWORK, JUDGE_PACKAGES, RESULTS, ROOT, bot_files, bot_hash,
                    file_hash, imports, map_signature, resolve_bot, resolve_maps)

DEFAULT_POOL = "greedy,hunter,splitter,turtle,wanderer"
BOOTSTRAP_ITERS = 2000
FEW_BLOCKS = 20        # below this, summaries warn that intervals are too narrow


# -- workers ---------------------------------------------------------------------


def _init_worker() -> None:
    # One engine per process, built once; lower priority keeps the desktop usable.
    try:
        import psutil  # optional
        psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if os.name == "nt" else 5)
    except Exception:
        pass
    from .match import engine
    engine()


def _job(args: tuple) -> dict:
    from .match import play

    map_path, a, b, seed, replay_dir, block = args
    replay_to = None
    if replay_dir is not None:
        a_name, b_name, m_name = pathlib.Path(a).name, pathlib.Path(b).name, pathlib.Path(map_path).stem
        replay_to = pathlib.Path(replay_dir) / f"{a_name}-vs-{b_name}-{m_name}-s{seed}.replay"
    try:
        d = play(pathlib.Path(map_path), pathlib.Path(a), pathlib.Path(b),
                 seed=seed, replay_to=replay_to).to_dict()
    except Exception as exc:  # e.g. a bot that fails to load
        d = {"map": pathlib.Path(map_path).stem, "bot_a": pathlib.Path(a).name,
             "bot_b": pathlib.Path(b).name, "seed": seed, "winner": None, "reason": "error",
             "error": f"{type(exc).__name__}: {exc}", "deaths": {}}
    d["block"] = block
    if replay_to is not None and replay_to.exists():
        d["replay"] = str(replay_to)   # cmd_eval deletes the ones it doesn't keep
    return d


def run_jobs(jobs: list[tuple], workers: int, label: str) -> list[dict]:
    from .match import prebuild
    prebuild([bot for job in jobs for bot in (job[1], job[2])])
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


def is_error(game: dict) -> bool:
    return bool(game.get("error")) or game.get("reason") == "error"


def score_for(game: dict, bot: str) -> float | None:
    """1 win, 0.5 draw, 0 loss from `bot`'s point of view; None if the bot
    did not play or the game errored."""
    if is_error(game):
        return None
    side = "A" if game["bot_a"] == bot else "B" if game["bot_b"] == bot else None
    if side is None:
        return None
    if game["winner"] is None:
        return 0.5
    return 1.0 if game["winner"] == side else 0.0


def block_bootstrap(blocks: list[list[float]], iters: int = BOOTSTRAP_ITERS,
                    seed: int = 0, level: float = 0.95) -> tuple[float, float]:
    """Percentile CI for the mean game score, resampling whole blocks (e.g.
    both sides of one map+seed) so paired games are not treated as
    independent. Deterministic for a given seed. With fewer than two blocks
    there is no spread to estimate, so the interval is (0, 1)."""
    blocks = [b for b in blocks if b]
    if len(blocks) < 2:
        return (0.0, 1.0)
    rng = random.Random(seed)
    sums = [(sum(b), len(b)) for b in blocks]
    n = len(sums)
    means = []
    for _ in range(iters):
        s = c = 0
        for _ in range(n):
            bs, bc = sums[rng.randrange(n)]
            s += bs
            c += bc
        means.append(s / c)
    means.sort()
    lo = means[int((1 - level) / 2 * iters)]
    hi = means[min(iters - 1, int((1 + level) / 2 * iters))]
    return (lo, hi)


def elo_gap(p: float) -> float:
    p = min(max(p, 1e-3), 1 - 1e-3)
    return -400 * math.log10(1 / p - 1)


class Tally:
    """Win/draw/loss counts and per-block scores for one slice of games."""

    def __init__(self) -> None:
        self.w = self.d = self.l = 0
        self.errors = 0
        self.blocks: dict = defaultdict(list)

    def add(self, score: float | None, block, error: bool = False) -> None:
        if error:
            self.errors += 1
            return
        if score is None:
            return
        self.w += score == 1.0
        self.d += score == 0.5
        self.l += score == 0.0
        self.blocks[block].append(score)

    @property
    def n(self) -> int:
        return self.w + self.d + self.l

    @property
    def score(self) -> float:
        return (self.w + 0.5 * self.d) / self.n if self.n else float("nan")

    @property
    def win_rate(self) -> float:
        return self.w / self.n if self.n else float("nan")

    def ci(self) -> tuple[float, float]:
        return block_bootstrap(list(self.blocks.values()))

    def row(self, name: str) -> str:
        if not self.n:
            return f"| {name} | - | - | - | - | - | 0 | {self.errors} |"
        lo, hi = self.ci()
        return (f"| {name} | {self.w}-{self.d}-{self.l} | {100 * self.win_rate:.0f}% | "
                f"{100 * self.score:.0f}% | {100 * lo:.0f}-{100 * hi:.0f}% | "
                f"{elo_gap(self.score):+.0f} | {len(self.blocks)} | {self.errors} |")


TALLY_HEADER = ["| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |",
                "|---|---|---|---|---|---|---|---|"]


# -- provenance ------------------------------------------------------------------


def _git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    except OSError:
        return ""


def git_state() -> str:
    rev = _git("rev-parse", "--short", "HEAD") or "?"
    return rev + ("+dirty" if _git("status", "--porcelain", "--untracked-files=no") else "")


def provenance(bots: list[pathlib.Path], maps: list[pathlib.Path], settings: dict) -> dict:
    try:
        from importlib.metadata import version

        from unswbc.engine import WASM_PATH
        toolkit = {"unswbc": version("unswbc"), "engine": file_hash(WASM_PATH)}
    except Exception:
        toolkit = {}
    return {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "git": git_state(),
        "python": sys.version.split()[0],
        **toolkit,
        "bots": {b.name: {"path": str(b), "hash": bot_hash(b)} for b in bots},
        "maps": {m.stem: {"file": file_hash(m), "signature": map_signature(m)} for m in maps},
        "settings": {k: v for k, v in settings.items() if k != "func"},
    }


def check_hashes(games: list[dict], prov: dict) -> list[str]:
    """Warn if any game ran code other than what was on disk at the start."""
    want = {name: b["hash"] for name, b in prov["bots"].items()}
    seen = defaultdict(set)
    for g in games:
        for side in "ab":
            h = g.get(f"hash_{side}")
            if h:
                seen[g[f"bot_{side}"]].add(h)
    out = []
    for name, hs in sorted(seen.items()):
        if hs != {want.get(name)}:
            out.append(f"{name}: code changed during the run (ran {sorted(hs)}, "
                       f"expected {want.get(name)})")
    return out


def _out_dir(name: str) -> pathlib.Path:
    d = RESULTS / f"{time.strftime('%Y%m%d-%H%M%S')}-{name}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _save(out: pathlib.Path, games: list[dict], prov: dict, title: str, body: str) -> None:
    with (out / "games.jsonl").open("w", encoding="utf8") as f:
        for g in games:
            f.write(json.dumps(g) + "\n")
    (out / "run.json").write_text(json.dumps(prov, indent=2, default=str), encoding="utf8")
    bots = ", ".join(f"{n} {b['hash']}" for n, b in prov["bots"].items())
    header = (f"# {title}\n\n{prov['time']} - git {prov['git']} - {len(games)} games\n\n"
              f"code: {bots}\n\n")
    (out / "summary.md").write_text(header + body, encoding="utf8")


# -- commands --------------------------------------------------------------------


def cmd_eval(args) -> None:
    focus = resolve_bot(args.bot)
    pool = [resolve_bot(n) for n in args.vs.split(",") if n]
    maps = resolve_maps(args.maps)
    out = _out_dir(focus.name)
    replay_dir = out / "replays" if args.save_replays != "none" else None
    prov = provenance([focus, *pool], maps, vars(args))

    jobs = []
    for opp, m, s in itertools.product(pool, maps, range(args.seeds)):
        block = [opp.name, m.stem, s]
        jobs.append((str(m), str(focus), str(opp), s, replay_dir, block))
        jobs.append((str(m), str(opp), str(focus), s, replay_dir, block))
    print(f"{focus.name} vs {', '.join(p.name for p in pool)} on {len(maps)} maps x "
          f"{args.seeds} seeds x 2 sides = {len(jobs)} games, {args.workers} workers")
    games = run_jobs(jobs, args.workers, focus.name)

    if replay_dir is not None and args.save_replays == "losses":
        for g in games:
            if score_for(g, focus.name) == 1.0 and g.get("replay"):
                pathlib.Path(g["replay"]).unlink(missing_ok=True)

    summary = summarize_eval(games, focus.name)
    warnings = check_hashes(games, prov)
    if warnings:
        summary += "\n**Warning:** " + "; ".join(warnings) + "\n"
    _save(out, games, prov, f"{focus.name} evaluation", summary)
    print(summary)
    print(f"saved to {out}")


def summarize_eval(games: list[dict], focus: str) -> str:
    by_opp: dict[str, Tally] = defaultdict(Tally)
    by_map: dict[str, Tally] = defaultdict(Tally)
    total = Tally()
    deaths = defaultdict(int)
    errors = [g for g in games if is_error(g)]
    for g in games:
        if focus not in (g["bot_a"], g["bot_b"]):
            continue
        opp = g["bot_b"] if g["bot_a"] == focus else g["bot_a"]
        block = tuple(g.get("block") or (opp, g["map"], g["seed"]))
        s, err = score_for(g, focus), is_error(g)
        by_opp[opp].add(s, block, err)
        by_map[g["map"]].add(s, block, err)
        total.add(s, block, err)
        if not err:
            side = "A" if g["bot_a"] == focus else "B"
            for k, v in g.get("deaths", {}).items():
                if k.startswith(side + ":"):
                    deaths[k[2:]] += v

    names = {"W": "hit kelp", "S": "hit itself", "O": "hit other body",
             "H": "head-to-head", "A": "no valid action/timeout"}
    lines = list(TALLY_HEADER)
    lines += [t.row(opp) for opp, t in sorted(by_opp.items())]
    lines.append(total.row("**overall**"))
    lines += ["", "| map | W-D-L | win rate | score | games | errors |", "|---|---|---|---|---|---|"]
    for m, t in sorted(by_map.items(), key=lambda kv: (kv[1].score if kv[1].n else 2)):
        if t.n:
            lines.append(f"| {m} | {t.w}-{t.d}-{t.l} | {100 * t.win_rate:.0f}% | "
                         f"{100 * t.score:.0f}% | {t.n} | {t.errors} |")
        else:
            lines.append(f"| {m} | - | - | - | 0 | {t.errors} |")
    if deaths:
        lines += ["", f"{focus} dragon deaths: " + ", ".join(
            f"{names.get(k, k)} {v}" for k, v in sorted(deaths.items(), key=lambda kv: -kv[1]))]
    lines += ["", "Score counts a draw as half a win; win rate counts wins only. "
              "CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together)."]
    few = sorted(opp for opp, t in by_opp.items() if 0 < len(t.blocks) < FEW_BLOCKS)
    if few:
        lines.append(f"Fewer than {FEW_BLOCKS} blocks for {', '.join(few)}: those intervals understate "
                     "the uncertainty (a result that never varied gets a zero-width interval); "
                     "add maps or seeds before trusting them.")
    if errors:
        lines += ["", f"**{len(errors)} games errored and are excluded from all scores**, "
                  f"e.g. {errors[0].get('error')}"]
    return "\n".join(lines) + "\n"


def cmd_tournament(args) -> None:
    bots = [resolve_bot(n) for n in args.bots]
    maps = resolve_maps(args.maps)
    out = _out_dir("tournament")
    prov = provenance(bots, maps, vars(args))
    jobs = []
    for a, b in itertools.combinations(bots, 2):
        for m, s in itertools.product(maps, range(args.seeds)):
            block = [a.name, b.name, m.stem, s]
            jobs.append((str(m), str(a), str(b), s, None, block))
            jobs.append((str(m), str(b), str(a), s, None, block))
    print(f"{len(bots)} bots, {len(maps)} maps, {len(jobs)} games, {args.workers} workers")
    games = run_jobs(jobs, args.workers, "tournament")
    text = summarize_tournament(games, [b.name for b in bots])
    warnings = check_hashes(games, prov)
    if warnings:
        text += "\n**Warning:** " + "; ".join(warnings) + "\n"
    _save(out, games, prov, "Tournament", text)
    print(text)
    print(f"saved to {out}")


def summarize_tournament(games: list[dict], names: list[str]) -> str:
    valid = [g for g in games if not is_error(g)]
    ratings = fit_elo(valid, names)
    pair: dict[tuple, Tally] = defaultdict(Tally)
    for g in games:
        a, b = g["bot_a"], g["bot_b"]
        block = tuple(g.get("block") or (a, b, g["map"], g["seed"]))
        err = is_error(g)
        pair[a, b].add(score_for(g, a), block, err)
        pair[b, a].add(score_for(g, b), block, err)
    order = sorted(names, key=lambda n: -ratings[n])
    lines = ["| # | bot | Elo | " + " | ".join(order) + " |",
             "|---|---|---|" + "---|" * len(order)]
    for i, n in enumerate(order, 1):
        cells = []
        for m in order:
            t = pair.get((n, m))
            cells.append("-" if m == n or t is None or not t.n else f"{100 * t.score:.0f}%")
        lines.append(f"| {i} | {n} | {ratings[n]:.0f} | " + " | ".join(cells) + " |")
    lines += ["", "Cells: row bot's match score vs column bot (draw = half a win)."]
    n_err = len(games) - len(valid)
    if n_err:
        lines += ["", f"**{n_err} games errored and are excluded**, e.g. "
                  f"{next(g for g in games if is_error(g)).get('error')}"]
    return "\n".join(lines) + "\n"


def fit_elo(games: list[dict], names: list[str], iters: int = 2000) -> dict[str, float]:
    """Maximum-likelihood Elo (Bradley–Terry) from game results, mean 1500.
    Errored games are ignored."""
    r = {n: 0.0 for n in names}
    results = [(g["bot_a"], g["bot_b"], score_for(g, g["bot_a"])) for g in games]
    results = [x for x in results if x[2] is not None]
    if not results:
        return {n: 1500.0 for n in names}
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


# -- freeze ----------------------------------------------------------------------


def freeze(src: pathlib.Path, versions: pathlib.Path, framework: pathlib.Path = FRAMEWORK,
           name: str | None = None) -> pathlib.Path:
    """Copy a bot into versions/<name>, pulling in any framework module it
    imports but does not carry, and check the snapshot loads. Build output
    and caches are left behind."""
    versions.mkdir(parents=True, exist_ok=True)
    if not name:
        nums = [int(p.name[1:]) for p in versions.glob("v*") if p.name[1:].isdigit()]
        name = f"v{max(nums, default=0) + 1}"
    dst = versions / name
    if dst.exists():
        raise SystemExit(f"{dst} already exists")
    tmp = versions / f".{name}.tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    for f in bot_files(src):
        target = tmp / f.relative_to(src)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, target)

    added, missing = [], set()
    todo = sorted(tmp.glob("*.py"))
    while todo:
        f = todo.pop()
        for mod in imports(f):
            if (tmp / f"{mod}.py").is_file() or (tmp / mod).is_dir():
                continue
            if (framework / f"{mod}.py").is_file():
                shutil.copy2(framework / f"{mod}.py", tmp / f"{mod}.py")
                added.append(f"{mod}.py")
                todo.append(tmp / f"{mod}.py")
            elif mod not in sys.stdlib_module_names and mod not in JUDGE_PACKAGES:
                missing.add(mod)
    if missing:
        shutil.rmtree(tmp)
        raise SystemExit(f"cannot freeze {src.name}: imports {sorted(missing)}, which are not in the "
                         f"bot, the framework, the standard library or {sorted(JUDGE_PACKAGES)}")

    stale = [f.name for f in sorted(tmp.glob("*.py"))
             if (framework / f.name).is_file() and f.name not in added
             and f.read_bytes() != (framework / f.name).read_bytes()]

    if (tmp / "brain.py").is_file():   # prove it imports and builds a Brain
        from .match import InProcessBot
        try:
            InProcessBot(tmp).new_brain("ID 0\nTEAM A\nMAP 16 16\nUNIT_LIMIT 64\n", seed=0)
        except Exception as exc:
            shutil.rmtree(tmp)
            raise SystemExit(f"cannot freeze {src.name}: snapshot fails to load: "
                             f"{type(exc).__name__}: {exc}") from exc

    note = [f"frozen from {src.name} at {time.strftime('%Y-%m-%d %H:%M')}",
            f"git {git_state()}", f"bot hash {bot_hash(tmp)}"]
    if added:
        note.append("added from framework: " + ", ".join(added))
    if stale:
        note.append("differs from framework (bot's own copy kept): " + ", ".join(stale))
    (tmp / "FROZEN.txt").write_text("\n".join(note) + "\n", encoding="utf8")
    tmp.rename(dst)
    return dst


def cmd_freeze(args) -> None:
    dst = freeze(resolve_bot(args.bot), ROOT / "versions", name=args.name)
    print(f"froze {args.bot} -> {dst}")
    print((dst / "FROZEN.txt").read_text(encoding="utf8"), end="")


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
