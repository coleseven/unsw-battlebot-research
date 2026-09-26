"""Small, single-worker follow-up suitable for sharing the PC with a game.

No tuning: replay the frozen trap candidate against its frozen baseline on
Arena, three synthetic Arena variants, and the Schooltime regression control.
"""

import argparse
import json
import os
import pathlib
import shutil
import time
import uuid
from collections import defaultdict
from datetime import datetime

from . import arena, population, reconstruct, replay
from .paths import ROOT, RESULTS, bot_hash, file_hash, map_signature

PRIOR = RESULTS / "20260922-173739-movement-659d1f"


def arena_variant(text, kind):
    """Preserve bodies/food/layout except the declared intervention.

    Added edge orbits are reflected across both map axes, independent of
    whether the engine interprets xy as requiring each reflection.
    """
    if kind not in ("baffles", "pockets", "slow_food"):
        raise ValueError("unknown map variant")
    lines = text.splitlines()
    w, h = map(int, next(l for l in lines if l.startswith("MAP ")).split()[1:])
    edges = {}
    for line in lines:
        p = line.split()
        if p and p[0] == "EDGE":
            edges[int(p[1])] = (int(p[2]), int(p[3]))

    def add(axis, x, y):
        if axis == "v":
            orbit = {(x, y), ((w - x) % w, y), (x, h - 1 - y), ((w - x) % w, h - 1 - y)}
        else:
            orbit = {(x, y), (w - 1 - x, y), (x, (h - y) % h), (w - 1 - x, (h - y) % h)}
        for a, b in orbit:
            edges[(2 * b + (axis == "v")) * (w + 1) + a] = (1, -1)

    if kind == "baffles":
        add("v", 4, 2)
        add("v", 4, 3)
    elif kind == "pockets":
        add("h", 2, 3)
        add("h", 3, 3)
        add("v", 4, 1)
        add("v", 4, 2)
    out = []
    for line in lines:
        p = line.split()
        if p[0] == "MAP_NAME":
            out.append(f"MAP_NAME Arena_{kind}")
        elif p[0] == "EDGE_COUNT":
            out.append(f"EDGE_COUNT {len(edges)}")
            out += [f"EDGE {i} {k} {pid}" for i, (k, pid) in sorted(edges.items())]
        elif p[0] == "EDGE":
            continue
        elif p[0] == "TILE" and kind == "slow_food":
            p[3], p[4] = str(2 * int(p[3])), str(2 * int(p[4]))
            out.append(" ".join(p))
        else:
            out.append(line)
    return "\n".join(out) + "\n"


def validate_map(path, require_connected=True):
    """Check generated layouts; official maps may intentionally be partitioned."""
    board = reconstruct.Board(path.read_text())
    start = board.dragons[0][1][0]
    seen, todo = {start}, [start]
    while todo:
        x, y = todo.pop()
        for d in "NESW":
            dest = board.dest(x, y, d)
            if dest is not None and dest not in seen:
                seen.add(dest)
                todo.append(dest)
    if require_connected and not board.spawns <= seen:
        raise ValueError(f"unreachable pearl cells in {path}")
    from .match import engine
    notices = []
    engine().run(path.read_bytes(), lambda *a: b"SUICIDE\nENDTURN\n",
                 lambda *a: None, lambda *a: None, notices.append, 0)
    if notices:
        raise ValueError(f"engine would repair {path}: {notices}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, default=12)
    args = parser.parse_args()
    if not 1 <= args.seeds <= 40:
        parser.error("seeds must be 1-40 for this bounded follow-up")
    import psutil
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if os.name == "nt" else 5)
    os.environ["RAYON_NUM_THREADS"] = "1"
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-trap-followup-" + uuid.uuid4().hex[:6])
    out.mkdir(parents=True)
    candidate = population.snapshot(PRIOR / "bots/trap", out / "bots/trap")
    control = population.snapshot(PRIOR / "bots/control_450", out / "bots/control_450")
    (out / "maps").mkdir()
    maps = []
    for name in ("arena", "schooltime"):
        dest = out / "maps" / f"{name}.map"
        shutil.copy2(ROOT / "maps" / f"{name}.map", dest)
        maps.append(dest)
    source = (ROOT / "maps/arena.map").read_text()
    for kind in ("baffles", "pockets", "slow_food"):
        dest = out / "maps" / f"arena_{kind}.map"
        dest.write_text(arena_variant(source, kind), encoding="utf8")
        maps.append(dest)
    assert len({map_signature(m) for m in maps}) == len(maps)
    for m in maps:
        validate_map(m, require_connected=m.stem not in ("arena", "schooltime"))
    plan = {"question": "Does the unchanged trap gain repeat and transfer within an Arena map family?",
            "seeds": list(range(6000, 6000 + args.seeds)), "maps": [str(m) for m in maps],
            "policy_tuning": False, "workers": 1, "priority": "below normal", "gpu_work": False,
            "memory_guard": "stop between games below 4 GiB available or above 1 GiB worker RSS",
            "live_bot_hash": bot_hash(ROOT / "mybot"), "source_hashes": {p.name: bot_hash(p) for p in (candidate, control)},
            "runner_hash": file_hash(pathlib.Path(__file__)),
            "limits": "related synthetic maps and previously observed originals; exploratory transfer test, "
                      "not five independent map families or a fresh broad promotion test"}
    population.write_json(out / "plan.json", plan)
    population.write_json(out / "run.json", arena.provenance([candidate, control], maps, plan))
    shutil.copy2(pathlib.Path(__file__), out / "runner.py")
    print(f"Experiment: {out}\nOne below-normal worker; no GPU work.", flush=True)
    jobs = population.jobs_for([candidate], [control], maps, plan["seeds"])
    games, resources = [], []
    start_time = time.monotonic()
    stopped = None
    with (out / "games.jsonl").open("x", encoding="utf8") as f:
        for job in jobs:
            free, rss = psutil.virtual_memory().available, process.memory_info().rss
            resources.append({"available_bytes": free, "rss_bytes": rss, "priority": int(process.nice())})
            if free < 4 * 2**30 or rss > 2**30:
                stopped = "resource guard; partial results are not a completed experiment"
                break
            game = arena._job(job)
            games.append(game)
            f.write(json.dumps(game) + "\n")
            f.flush()
            if arena.is_error(game):
                stopped = "match error; experiment invalid"
                break
            if len(games) % 10 == 0:
                print(f"{len(games)}/{len(jobs)} games, {time.monotonic() - start_time:.0f}s; "
                      f"worker {rss / 2**20:.0f} MiB, available RAM {free / 2**30:.1f} GiB", flush=True)
    population.write_json(out / "resources.json", {"samples": resources, "stopped": stopped})
    if stopped:
        raise SystemExit(f"{stopped}; saved {out}")
    prov = json.loads((out / "run.json").read_text())
    assert not arena.check_hashes(games, prov)
    assert bot_hash(ROOT / "mybot") == plan["live_bot_hash"]
    summary = "# Trap transfer follow-up\n\n" + arena.summarize_eval(games, "trap")
    summary += ("\nRelated Arena variants are NOT independent map families. Per-map side-paired "
                "scores are exploratory; no live bot is promoted from this test.\n")
    by_map = defaultdict(arena.Tally)
    for g in games:
        by_map[g["map"]].add(arena.score_for(g, "trap"), tuple(g["block"]))
    comparisons = {m: {"wins": t.w, "draws": t.d, "losses": t.l, "score": t.score,
                       "ci95": t.ci()} for m, t in by_map.items()}
    population.write_json(out / "comparison.json", comparisons)
    (out / "summary.md").write_text(summary, encoding="utf8")
    print(summary, flush=True)


if __name__ == "__main__":
    main()
