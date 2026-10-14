"""Predeclared guarded-trap screening, followed by one selected validation."""

import argparse
import json
import pathlib
import shutil
import uuid
from collections import defaultdict
from datetime import datetime

from . import arena, bounded, population
from .paths import ROOT, RESULTS, bot_hash, map_signature, resolve_maps

BASE = RESULTS / "20260922-171805-endgame-b67e3b/bots/stop_450"
MOVEMENT = RESULTS / "20260922-173739-movement-659d1f"
TRANSFER = RESULTS / "20260922-175423-trap-followup-a1e642"
MODES = ("head_guard", "tail_guard", "food_guard")


def make_variant(source, dest, mode):
    if mode not in MODES:
        raise ValueError(mode)
    population.snapshot(source, dest)
    (dest / "brain.py").rename(dest / "baseline_brain.py")
    shutil.copy2(ROOT / "experiments/guarded/brain.py", dest / "brain.py")
    for name in ("local_safety.py", "guarded_safety.py"):
        shutil.copy2(ROOT / "framework" / name, dest / name)
    (dest / "guarded_config.py").write_text(f"MODE = {mode!r}\n", encoding="utf8")
    return dest


def stage(out, name, candidates, opponents, maps, seeds, workers, replays=False):
    folder = out / name
    folder.mkdir()
    prov = arena.provenance(candidates + opponents, maps, {"seeds": list(seeds), "workers": workers})
    population.write_json(folder / "run.json", prov)
    jobs = population.jobs_for(candidates, opponents, maps, seeds, folder / "replays" if replays else None)
    games = bounded.run(jobs, workers, folder, name)
    assert not arena.check_hashes(games, prov)
    text = "\n".join(f"# {p.name}\n\n" + arena.summarize_eval(games, p.name) for p in candidates)
    (folder / "summary.md").write_text(text, encoding="utf8")
    return games


def screen(workers):
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-guarded-" + uuid.uuid4().hex[:6])
    out.mkdir()
    control = population.snapshot(BASE, out / "bots/control_450")
    reference = population.snapshot(BASE, out / "bots/reference_450")
    old = population.snapshot(MOVEMENT / "bots/trap", out / "bots/trap")
    candidates = [old] + [make_variant(BASE, out / "bots" / mode, mode) for mode in MODES]
    for name in ("splitter", "hunter"):
        population.snapshot(MOVEMENT / "bots" / name, out / "bots" / name)
    (out / "maps").mkdir()
    official, stress = [], []
    for source in resolve_maps("all"):
        dest = out / "maps" / f"official_{source.stem}_{map_signature(source)}.map"
        shutil.copy2(source, dest)
        official.append(dest)
    for kind in ("baffles", "pockets", "slow_food"):
        source = TRANSFER / "maps" / f"arena_{kind}.map"
        dest = out / "maps" / source.name
        shutil.copy2(source, dest)
        stress.append(dest)
    plan = {"question": "Can explicit head-risk, tail-release, or food guards repair trap-policy transfer?",
            "modes": list(MODES), "control": str(control), "live_hash": bot_hash(ROOT / "mybot"),
            "official_maps": [str(p) for p in official], "stress_maps": [str(p) for p in stress],
            "screen_seeds": [7000, 7001], "validation_seeds": list(range(8000, 8008)),
            "stress_seeds": list(range(8100, 8108)),
            "selection": "Highest official-map screen score among the three new modes, ties in listed mode order. "
                         "Must exceed .5; old trap is diagnostic only. Exactly one candidate validates unchanged.",
            "gate": "Official-map direct reference score 95% map-cluster lower bound > .5 AND paired "
                    "pool-score improvement 95% map-cluster lower bound > 0; stress combined score >= .5 "
                    "and no stress-map score below .375; sampled sandbox and replay audit required.",
            "limits": "All maps are now familiar; validation reserves bot RNG seeds, NOT unseen map families. "
                      "Synthetic Arena maps are a related stress family. No tuning after selection.",
            "workers": workers, "worker_batch": "fresh pool each 12*workers games; 1 GiB RSS / 4 GiB available guards"}
    population.write_json(out / "plan.json", plan)
    (out / "implementation").mkdir()
    for name in ("guarded.py", "bounded.py", "arena.py", "match.py", "population.py", "paths.py"):
        shutil.copy2(ROOT / "bcsim" / name, out / "implementation" / name)
    print(f"Experiment: {out}", flush=True)
    games = stage(out, "screen", candidates, [reference], official + stress, plan["screen_seeds"], workers)
    scores = {mode: population.tally([g for g in games if g["map"].startswith("official_")], mode).score
              for mode in MODES}
    selected = max(MODES, key=scores.get)
    selection = {"scores": scores, "selected": selected if scores[selected] > .5 else None,
                 "hash": bot_hash(out / "bots" / selected)}
    population.write_json(out / "selection.json", selection)
    print(json.dumps(selection, indent=2), flush=True)
    return out


def validate(out, workers):
    plan = json.loads((out / "plan.json").read_text())
    selection = json.loads((out / "selection.json").read_text())
    if not selection["selected"]:
        raise ValueError("No candidate passed screening")
    candidate = out / "bots" / selection["selected"]
    assert bot_hash(candidate) == selection["hash"]
    control = out / "bots/control_450"
    opponents = [out / "bots" / n for n in ("reference_450", "splitter", "hunter")]
    official, stress = ([pathlib.Path(p) for p in plan[key]] for key in ("official_maps", "stress_maps"))
    games = stage(out, "validation", [control, candidate], opponents, official,
                  plan["validation_seeds"], workers, True)
    transfer = stage(out, "stress", [candidate], opponents[:1], stress, plan["stress_seeds"], workers, True)
    delta = population.paired_delta(games, candidate.name, control.name)
    direct_games = [g for g in games if "reference_450" in (g["bot_a"], g["bot_b"])
                    and candidate.name in (g["bot_a"], g["bot_b"])]
    clusters = defaultdict(list)
    for g in direct_games:
        clusters[g["map"]].append(arena.score_for(g, candidate.name))
    direct = population.tally(direct_games, candidate.name)
    ci = arena.block_bootstrap(list(clusters.values()), iters=8000)
    stress_scores = {m.stem: population.tally([g for g in transfer if g["map"] == m.stem], candidate.name).score
                     for m in stress}
    result = {"candidate": candidate.name, "hash": bot_hash(candidate), "paired_pool": delta,
              "direct": {"wins": direct.w, "draws": direct.d, "losses": direct.l, "score": direct.score,
                         "map_ci95": ci, "pair_ci95": direct.ci()}, "stress_scores": stress_scores,
              "performance_gate": ci[0] > .5 and delta["map_cluster_ci95"][0] > 0 and
                                  sum(stress_scores.values()) / len(stress_scores) >= .5 and
                                  min(stress_scores.values()) >= .375}
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    population.write_json(out / "comparison.json", result)
    print(json.dumps(result, indent=2), flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workers", type=int, default=6)
    p.add_argument("--validate", type=pathlib.Path)
    args = p.parse_args()
    if args.validate:
        validate(args.validate, args.workers)
    else:
        screen(args.workers)


if __name__ == "__main__":
    main()
