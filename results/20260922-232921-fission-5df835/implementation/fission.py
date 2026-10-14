"""Independent coarse reproduction-size search, not combined with movement tuning."""

import argparse
import json
import pathlib
import shutil
import uuid
from collections import defaultdict
from datetime import datetime

from . import arena, guarded, population
from .paths import ROOT, RESULTS, bot_hash, map_signature, resolve_maps

MODES = {"split4": (4, False), "split6": (6, False), "split10": (10, False),
         "split12": (12, False), "child2": (8, True)}


def make_variant(source, dest, threshold, small_child=False):
    if threshold < 4:
        raise ValueError("split threshold must leave at least two segments per dragon")
    population.snapshot(source, dest)
    shutil.copy2(ROOT / "experiments/fission/brain.py", dest / "brain.py")
    (dest / "fission_config.py").write_text(f"THRESHOLD = {threshold}\nSMALL_CHILD = {small_child!r}\n", encoding="utf8")
    return dest


def screen(workers):
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-fission-" + uuid.uuid4().hex[:6])
    out.mkdir()
    control = population.snapshot(guarded.BASE, out / "bots/control_450")
    reference = population.snapshot(guarded.BASE, out / "bots/reference_450")
    candidates = [control] + [make_variant(guarded.BASE, out / "bots" / name, *config)
                              for name, config in MODES.items()]
    for name in ("splitter", "hunter"):
        population.snapshot(guarded.MOVEMENT / "bots" / name, out / "bots" / name)
    (out / "maps").mkdir()
    maps = []
    for source in resolve_maps("all"):
        dest = out / "maps" / f"{source.stem}_{map_signature(source)}.map"
        shutil.copy2(source, dest)
        maps.append(dest)
    plan = {"question": "Change split threshold or offspring size while movement and round-450 cutoff stay fixed",
            "modes": MODES, "live_hash": bot_hash(ROOT / "mybot"), "maps": [str(m) for m in maps],
            "screen_seeds": [9000, 9001], "validation_seeds": list(range(10000, 10008)),
            "selection": "Highest official-map screen score among new candidates, ties in mode order; "
                         "must exceed .5. Exactly one validates unchanged, no movement combination yet.",
            "gate": "Direct baseline score 95% map-cluster lower bound > .5 AND paired pool gain "
                    "95% map-cluster lower bound > 0. Replay and judge-runtime verification also required.",
            "limits": "Fresh bot RNG seeds, familiar maps/opponents; not unseen-map or ladder evidence.",
            "workers": workers}
    population.write_json(out / "plan.json", plan)
    (out / "implementation").mkdir()
    for name in ("fission.py", "guarded.py", "bounded.py", "arena.py", "match.py", "population.py", "paths.py"):
        shutil.copy2(ROOT / "bcsim" / name, out / "implementation" / name)
    print(f"Experiment: {out}", flush=True)
    games = guarded.stage(out, "screen", candidates, [reference], maps, plan["screen_seeds"], workers)
    scores = {name: population.tally(games, name).score for name in MODES}
    selected = max(MODES, key=scores.get)
    selection = {"scores": scores, "selected": selected if scores[selected] > .5 else None,
                 "hash": bot_hash(out / "bots" / selected)}
    population.write_json(out / "selection.json", selection)
    print(json.dumps(selection, indent=2), flush=True)


def validate(out, workers):
    plan = json.loads((out / "plan.json").read_text())
    selection = json.loads((out / "selection.json").read_text())
    if not selection["selected"]:
        raise ValueError("No candidate passed screening")
    candidate = out / "bots" / selection["selected"]
    assert bot_hash(candidate) == selection["hash"]
    control = out / "bots/control_450"
    opponents = [out / "bots" / n for n in ("reference_450", "splitter", "hunter")]
    maps = [pathlib.Path(p) for p in plan["maps"]]
    games = guarded.stage(out, "validation", [control, candidate], opponents, maps,
                          plan["validation_seeds"], workers, True)
    delta = population.paired_delta(games, candidate.name, control.name)
    direct_games = [g for g in games if "reference_450" in (g["bot_a"], g["bot_b"])
                    and candidate.name in (g["bot_a"], g["bot_b"])]
    clusters = defaultdict(list)
    for g in direct_games:
        clusters[g["map"]].append(arena.score_for(g, candidate.name))
    direct = population.tally(direct_games, candidate.name)
    ci = arena.block_bootstrap(list(clusters.values()), iters=8000)
    result = {"candidate": candidate.name, "hash": bot_hash(candidate), "paired_pool": delta,
              "direct": {"wins": direct.w, "draws": direct.d, "losses": direct.l, "score": direct.score,
                         "map_ci95": ci, "pair_ci95": direct.ci()},
              "performance_gate": ci[0] > .5 and delta["map_cluster_ci95"][0] > 0}
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    population.write_json(out / "comparison.json", result)
    print(json.dumps(result, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--validate", type=pathlib.Path)
    args = parser.parse_args()
    if args.validate:
        validate(args.validate, args.workers)
    else:
        screen(args.workers)


if __name__ == "__main__":
    main()
