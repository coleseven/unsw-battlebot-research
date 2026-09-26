"""Full-compute, full-map bot-change screen with frozen inputs and both sides.

Prepare:
  python -m bcsim.full_change_test --prepare --candidate PATH --vs PATH PATH ...
Run:
  python -m bcsim.full_change_test RESULT_DIR --screen
"""

import argparse
import importlib.metadata
import json
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import guarded, local_v6_clock, map_matrix, match, official_suite, population
from .paths import ROOT, RESULTS, bot_hash, file_hash, resolve_bot


def prepare(candidate_source: Path, opponent_sources: list[Path], workers: int, seeds: int = 1):
    if not opponent_sources or len({str(p) for p in opponent_sources}) != len(opponent_sources):
        raise ValueError("provide distinct opponents")
    if candidate_source in opponent_sources:
        raise ValueError("candidate cannot also be an opponent")
    if not 1 <= workers <= 16:
        raise ValueError("workers must be 1-16")
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") +
                     "-full-change-" + uuid.uuid4().hex[:6])
    out.mkdir()
    sources = {"candidate": candidate_source}
    sources.update({p.name: p for p in opponent_sources})
    if len(sources) != len(opponent_sources) + 1:
        raise ValueError("opponents must have distinct directory names")
    for name, path in sources.items():
        population.snapshot(path, out / "bots" / name)
    (out / "maps").mkdir()
    maps = []
    for source in official_suite.official_maps():
        dest = out / "maps" / source.name
        shutil.copy2(source, dest)
        maps.append(dest)
    official_suite.require_coverage(maps)
    population.write_json(out / "plan.json", {
        "question": "Does this unchanged candidate improve across every official map?",
        "coverage": "all 11 distinct official maps, both sides, every opponent",
        "seeds": [53001 + i for i in range(seeds)], "workers": workers,
        "limits": "unswbc >= 1.1 seeds the engine (pearl spawns) per match, so each seed is a distinct game; "
                  "the same seed replays identically.",
        "unswbc": importlib.metadata.version("unswbc"),
        "candidate_source": str(candidate_source),
        "opponent_sources": {name: str(path) for name, path in sources.items()
                             if name != "candidate"},
        "source_hashes": {name: bot_hash(path) for name, path in sources.items()},
        "bot_hashes": {name: bot_hash(out / "bots" / name) for name in sources},
        "maps": [str(p) for p in maps],
        "map_hashes": {str(p): file_hash(p) for p in maps},
        "live_hash": bot_hash(ROOT / "mybot"),
        "runner_hash": file_hash(Path(__file__)),
        "suite_hash": file_hash(Path(official_suite.__file__)),
        "match_hash": file_hash(Path(match.__file__)),
        "local_clock_hash": file_hash(Path(local_v6_clock.__file__)),
        "deterministic_v6_clock": os.environ.get("BCSIM_DETERMINISTIC_V6") == "1",
    })
    print(out, flush=True)


def screen(out: Path):
    plan = json.loads((out / "plan.json").read_text())
    assert file_hash(Path(__file__)) == plan["runner_hash"]
    assert file_hash(Path(official_suite.__file__)) == plan["suite_hash"]
    assert file_hash(Path(match.__file__)) == plan["match_hash"]
    assert file_hash(Path(local_v6_clock.__file__)) == plan["local_clock_hash"]
    assert (os.environ.get("BCSIM_DETERMINISTIC_V6") == "1") == plan["deterministic_v6_clock"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    sources = {"candidate": Path(plan["candidate_source"])}
    sources.update({name: Path(path) for name, path in plan["opponent_sources"].items()})
    for name, path in sources.items():
        assert bot_hash(path) == plan["source_hashes"][name]
        assert bot_hash(out / "bots" / name) == plan["bot_hashes"][name]
    maps = [Path(p) for p in plan["maps"]]
    official_suite.require_coverage(maps)
    for path, expected in plan["map_hashes"].items():
        assert file_hash(Path(path)) == expected
    bots = out / "bots"
    opponents = [bots / name for name in plan["opponent_sources"]]
    games = guarded.stage(out, "full", [bots / "candidate"], opponents,
                          maps, plan.get("seeds", [plan.get("seed")]), plan["workers"], True)
    by_opponent = {}
    for name in plan["opponent_sources"]:
        selected = [g for g in games if name in (g["bot_a"], g["bot_b"])]
        tally = population.tally(selected, "candidate")
        by_opponent[name] = {"wins": tally.w, "draws": tally.d,
                             "losses": tally.l, "score": tally.score}
    result = {"maps": [p.stem for p in maps], "games": len(games),
              "workers": plan["workers"], "opponents": by_opponent}
    population.write_json(out / "comparison.json", result)
    if len(plan.get("seeds", [None])) == 1:   # the matrix shows one game per side
        with (out / "map_matrix.md").open("x", encoding="utf8") as f:
            f.write(map_matrix.render(games, "candidate", list(plan["opponent_sources"]),
                                      result["maps"]))
    else:
        per_map = {}
        for g in games:
            side = "A" if g["bot_a"] == "candidate" else "B"
            w = per_map.setdefault(g["map"], [0, 0])
            w[0] += g["winner"] == side
            w[1] += 1
        result["per_map_wins"] = {m: f"{w}/{n}" for m, (w, n) in sorted(per_map.items())}
        population.write_json(out / "comparison.json", result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", nargs="?", type=Path)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--screen", action="store_true")
    parser.add_argument("--candidate", type=str)
    parser.add_argument("--vs", nargs="+")
    parser.add_argument("--workers", type=int, default=official_suite.DEFAULT_WORKERS)
    parser.add_argument("--seeds", type=int, default=1, help="distinct engine seeds per map/side/opponent")
    args = parser.parse_args()
    if args.prepare and args.candidate and args.vs:
        prepare(resolve_bot(args.candidate), [resolve_bot(p) for p in args.vs],
                args.workers, args.seeds)
    elif args.screen and args.experiment:
        screen(args.experiment)
    else:
        parser.error("prepare requires --candidate and --vs; screen requires RESULT_DIR")
