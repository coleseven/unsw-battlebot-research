"""One-worker v2 regression for the visible-exit portal candidate."""

import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import guarded, population
from .paths import ROOT, RESULTS, bot_hash, file_hash, map_signature

SOURCE = RESULTS / "20260924-182411-v4-visible-portal-ada92a/bots/visible_portal"
V2 = ROOT / "versions/v2"
MAPS = tuple(ROOT / "maps" / (n + ".map") for n in
             ("Colosseum", "default", "queen_of_spades", "schooltime", "trophy"))


def prepare():
    assert bot_hash(V2) == "9f29ab4138b51d26"
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-v4-visible-portal-v2-" + uuid.uuid4().hex[:6])
    out.mkdir()
    population.snapshot(SOURCE, out / "bots/visible_portal")
    population.snapshot(V2, out / "bots/reference_v2")
    (out / "maps").mkdir()
    maps = []
    for source in MAPS:
        dest = out / "maps" / source.name
        shutil.copy2(source, dest)
        maps.append(str(dest))
    assert len({map_signature(Path(p)) for p in maps}) == len(maps) == 5
    sources = (ROOT / "bcsim/v4_visible_portal_v2.py", ROOT / "bcsim/match.py",
               ROOT / "bcsim/guarded.py", ROOT / "bcsim/bounded.py")
    plan = {"question": "Does visible-only portal additive still beat uploaded v2 on portal maps?",
            "candidate_hash": bot_hash(SOURCE), "v2_hash": bot_hash(V2),
            "live_hash": bot_hash(ROOT / "mybot"),
            "bot_hashes": {n: bot_hash(out / "bots" / n) for n in
                           ("visible_portal", "reference_v2")},
            "maps": maps, "map_hashes": {p: file_hash(Path(p)) for p in maps},
            "seed": 44007, "workers": 1, "games": 10,
            "selection": "Regression only. No promotion or submission; require clear v2 edge and no errors.",
            "source_hashes": {str(p.relative_to(ROOT)): file_hash(p) for p in sources}}
    population.write_json(out / "plan.json", plan)
    print(out, flush=True)


def screen(out):
    plan = json.loads((out / "plan.json").read_text())
    assert plan["workers"] == 1 and bot_hash(SOURCE) == plan["candidate_hash"]
    assert bot_hash(V2) == plan["v2_hash"] and bot_hash(ROOT / "mybot") == plan["live_hash"]
    for name, expected in plan["bot_hashes"].items():
        assert bot_hash(out / "bots" / name) == expected
    for path, expected in plan["map_hashes"].items():
        assert file_hash(Path(path)) == expected
    for path, expected in plan["source_hashes"].items():
        assert file_hash(ROOT / path) == expected
    bots = out / "bots"
    games = guarded.stage(out, "vs-v2", [bots / "visible_portal"],
                          [bots / "reference_v2"], [Path(p) for p in plan["maps"]],
                          [plan["seed"]], 1, True)
    assert len(games) == plan["games"]
    t = population.tally(games, "visible_portal")
    result = {"wins": t.w, "draws": t.d, "losses": t.l, "score": t.score,
              "is_promotion": False}
    population.write_json(out / "screen-comparison.json", result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", nargs="?", type=Path)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--screen", action="store_true")
    args = parser.parse_args()
    if args.prepare:
        prepare()
    elif args.screen and args.experiment:
        screen(args.experiment)
    else:
        parser.error("choose --prepare or an experiment path with --screen")
