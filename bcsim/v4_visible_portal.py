"""One-worker confirmation screen of visible-exit-only portal addition."""

import argparse
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from . import guarded, population
from .paths import ROOT, RESULTS, bot_hash, file_hash, foreign_imports, map_signature

BASE = RESULTS / "20260924-172250-v4-additive-9c22dc/bots/additive"
V3 = ROOT / "versions/v3"
MAPS = tuple(ROOT / "maps" / (n + ".map") for n in
             ("Colosseum", "default", "queen_of_spades", "schooltime", "trophy"))
STRESS = RESULTS / "20260923-091759-portal-followup-206dc9/maps/new_dense_small.map"


def make_candidate(dest):
    population.snapshot(BASE, dest)
    (dest / "brain.py").rename(dest / "additive_brain.py")
    shutil.copy2(ROOT / "experiments/v4/additive_visible_portal_brain.py", dest / "brain.py")
    shutil.copy2(ROOT / "framework/portal_escape.py", dest / "portal_escape.py")
    shutil.copy2(ROOT / "framework/portal_visible.py", dest / "portal_visible.py")
    assert not foreign_imports(dest)
    return dest


def prepare():
    assert bot_hash(BASE) == "bf33497158a49a7b"
    assert bot_hash(V3) == "69382825b699723d"
    assert len({map_signature(p) for p in MAPS}) == 5
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-v4-visible-portal-" + uuid.uuid4().hex[:6])
    out.mkdir()
    population.snapshot(BASE, out / "bots/additive")
    population.snapshot(V3, out / "bots/reference_v3")
    make_candidate(out / "bots/visible_portal")
    (out / "maps").mkdir()
    official = []
    for source in MAPS:
        dest = out / "maps" / source.name
        shutil.copy2(source, dest)
        official.append(str(dest))
    stress = out / "maps" / STRESS.name
    shutil.copy2(STRESS, stress)
    sources = (ROOT / "experiments/v4/additive_visible_portal_brain.py",
               ROOT / "framework/portal_escape.py", ROOT / "framework/portal_visible.py",
               ROOT / "bcsim/v4_visible_portal.py", ROOT / "bcsim/match.py",
               ROOT / "bcsim/guarded.py", ROOT / "bcsim/bounded.py")
    plan = {"question": "Can visible-empty portal exits avoid the unknown-exit losses while adding useful escapes?",
            "baseline_hash": bot_hash(BASE), "v3_hash": bot_hash(V3),
            "live_hash": bot_hash(ROOT / "mybot"),
            "bot_hashes": {n: bot_hash(out / "bots" / n) for n in
                           ("additive", "reference_v3", "visible_portal")},
            "official_maps": official, "stress_map": str(stress),
            "map_hashes": {p: file_hash(Path(p)) for p in (*official, str(stress))},
            "seed": 44006, "workers": 1, "official_games": 20, "stress_games": 2,
            "selection": "One fixed visible-only candidate. Require nonnegative paired official "
                         "score, actual confirmed portal use, no errors; even passing is "
                         "exploratory until judge sandbox and broader maps. No automatic upload.",
            "limits": "Official maps familiar; one new seed and one synthetic stress map. "
                      "Only redirects, not forced baseline portal fallbacks, are visible-only.",
            "source_hashes": {str(p.relative_to(ROOT)): file_hash(p) for p in sources}}
    population.write_json(out / "plan.json", plan)
    print(out, flush=True)


def screen(out):
    plan = json.loads((out / "plan.json").read_text())
    assert plan["workers"] == 1 and bot_hash(BASE) == plan["baseline_hash"]
    assert bot_hash(V3) == plan["v3_hash"] and bot_hash(ROOT / "mybot") == plan["live_hash"]
    for name, expected in plan["bot_hashes"].items():
        assert bot_hash(out / "bots" / name) == expected
    for path, expected in plan["map_hashes"].items():
        assert file_hash(Path(path)) == expected
    for path, expected in plan["source_hashes"].items():
        assert file_hash(ROOT / path) == expected
    bots = out / "bots"
    official = guarded.stage(out, "official", [bots / "additive", bots / "visible_portal"],
                             [bots / "reference_v3"], [Path(p) for p in plan["official_maps"]],
                             [plan["seed"]], 1, True)
    stress = guarded.stage(out, "stress", [bots / "visible_portal"], [bots / "additive"],
                           [Path(plan["stress_map"])], [plan["seed"]], 1, True)
    assert len(official) == plan["official_games"] and len(stress) == plan["stress_games"]
    scores = {}
    for name in ("additive", "visible_portal"):
        t = population.tally(official, name)
        scores[name + "_vs_v3"] = {"wins": t.w, "draws": t.d, "losses": t.l,
                                   "score": t.score}
    t = population.tally(stress, "visible_portal")
    scores["visible_portal_vs_additive_stress"] = {"wins": t.w, "draws": t.d,
                                                   "losses": t.l, "score": t.score}
    comparison = {"scores": scores,
                  "paired_vs_v3_delta": population.paired_delta(official, "visible_portal", "additive"),
                  "is_promotion": False}
    population.write_json(out / "screen-comparison.json", comparison)
    print(json.dumps(comparison, indent=2), flush=True)


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
