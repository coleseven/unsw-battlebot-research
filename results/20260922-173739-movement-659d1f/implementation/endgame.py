"""Controlled endgame experiment; no live-bot changes or submission.

    python -B -m bcsim.endgame --workers 4

Screen fixed split cutoffs, then confirm the selected one against perpetual
splitting with unchanged greedy movement. Inputs/results live in a new folder.
"""

import argparse
import json
import pathlib
import shutil
import uuid
from collections import Counter
from datetime import datetime

from . import arena, population
from .paths import ROOT, RESULTS, bot_hash, file_hash, map_signature, resolve_maps

CUTOFFS = (None, 200, 300, 400, 450)
TEMPLATE = ROOT / "experiments" / "endgame" / "brain.py"


def make_variant(source, destination, cutoff):
    if cutoff is not None and (type(cutoff) is not int or not 0 <= cutoff <= 500):
        raise ValueError("cutoff must be None or an integer in [0, 500]")
    if any((source / name).exists() for name in ("reproduction.py", "endgame_config.py")):
        raise ValueError("baseline already contains endgame module names")
    population.make_variant(source, destination, 64)
    (destination / "brain.py").rename(destination / "reproduction.py")
    shutil.copy2(TEMPLATE, destination / "brain.py")
    (destination / "endgame_config.py").write_text(f"STOP_ROUND = {cutoff!r}\n", encoding="utf8")
    return destination


def select_candidate(games, candidates):
    # None/control is evaluated but not eligible as an experimental challenger.
    # Exact ties prefer the smaller behavioral change: stopping later.
    return min(candidates[1:], key=lambda p: (-population.tally(games, p.name).score,
                                            -int(p.name.removeprefix("stop_"))))


def diagnostics(games, candidate):
    """Descriptive counts; conditional endgame lengths are not a causal metric."""
    counts = Counter()
    longest = []
    for g in games:
        if candidate not in (g["bot_a"], g["bot_b"]):
            continue
        if arena.is_error(g):
            counts["errors"] += 1
            continue
        counts["games"] += 1
        side = "a" if g["bot_a"] == candidate else "b"
        score = arena.score_for(g, candidate)
        counts["wins" if score == 1 else "draws" if score == .5 else "losses"] += 1
        if g["reason"] == "length":
            counts["length_decisions"] += 1
            counts["length_wins" if score == 1 else "length_draws" if score == .5 else "length_losses"] += 1
            longest.append(g[f"{side}_longest"])
        elif score == 0:
            counts["elimination_losses"] += 1
    return {**counts, "mean_longest_in_length_decisions":
            sum(longest) / len(longest) if longest else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("workers must be positive")
    screen, holdout = population.reserve_maps(resolve_maps("all"))
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-endgame-" + uuid.uuid4().hex[:6])
    out.mkdir(parents=True, exist_ok=False)
    candidates = [make_variant(ROOT / "mybot", out / "bots" /
                              ("perpetual" if c is None else f"stop_{c}"), c) for c in CUTOFFS]
    opponents = [population.snapshot(ROOT / rel, out / "bots" / name)
                 for rel, name in (("versions/v1", "v1"), ("opponents/splitter", "splitter"),
                                   ("opponents/hunter", "hunter"))]
    (out / "maps").mkdir()
    copies = {}
    for m in screen + holdout:
        dest = out / "maps" / f"{m.stem}_{map_signature(m)}.map"
        shutil.copy2(m, dest)
        copies[m] = dest
    # Capture experiment implementation too, so a later edit does not obscure
    # exactly what selected the challenger or computed these results.
    (out / "implementation").mkdir()
    for source in (pathlib.Path(__file__), ROOT / "bcsim" / "population.py",
                   ROOT / "bcsim" / "arena.py", ROOT / "bcsim" / "match.py",
                   ROOT / "bcsim" / "paths.py", ROOT / "bcsim" / "replay.py"):
        shutil.copy2(source, out / "implementation" / source.name)
    plan = {
        "question": "Does a fixed late-game split cutoff outperform perpetual splitting?",
        "cutoffs": CUTOFFS, "semantics": "split only while observed round < cutoff; None = perpetual",
        "population_cap": 64, "split_threshold": 8, "movement": "unchanged mybot snapshot",
        "baseline_hash": bot_hash(ROOT / "mybot"),
        "screen_maps": [str(copies[m]) for m in screen], "screen_seeds": [2000, 2001],
        "holdout_maps": [str(copies[m]) for m in holdout], "holdout_seeds": list(range(3000, 3004)),
        "selection": "highest screen score among finite cutoffs; exact ties prefer later cutoff",
        "success_gate": "held-out paired map-cluster delta lower bound > 0 AND splitter score CI lower bound > 0.5",
        "control": "perpetual", "opponents": [p.name for p in opponents],
        "runner_hash": file_hash(pathlib.Path(__file__)), "template_hash": file_hash(TEMPLATE),
        "map_identity_hash": file_hash(ROOT / "bcsim" / "paths.py"),
        "limits": "five validation maps, familiar from previous experiment; only cutoff selection is held out; "
                  "scripted opponents, bot-RNG seeds, in-process without judge CPU metering",
    }
    population.write_json(out / "plan.json", plan)
    print(f"Experiment: {out}", flush=True)
    screening = population.stage(out, "screen", candidates, opponents, [copies[m] for m in screen],
                                plan["screen_seeds"], args.workers)
    chosen = select_candidate(screening, candidates)
    selection = {"selected": chosen.name,
                 "scores": {p.name: population.tally(screening, p.name).score for p in candidates}}
    population.write_json(out / "selection.json", selection)
    print(json.dumps(selection, indent=2), flush=True)
    games = population.stage(out, "holdout", [candidates[0], chosen], opponents,
                             [copies[m] for m in holdout], plan["holdout_seeds"], args.workers, True)
    delta = population.paired_delta(games, chosen.name, "perpetual")
    versus_splitter = [g for g in games if "splitter" in (g["bot_a"], g["bot_b"])]
    direct = population.tally(versus_splitter, chosen.name)
    success = delta["map_cluster_ci95"][0] > 0 and direct.ci()[0] > .5
    result = {**delta, "selected": chosen.name, "success_gate_passed": success,
              "splitter_score": direct.score, "splitter_score_ci95": direct.ci(),
              "diagnostics": {p.name: diagnostics(games, p.name) for p in (candidates[0], chosen)}}
    population.write_json(out / "comparison.json", result)
    lines = ["# Split-cutoff experiment", "", f"Selected using screen only: {chosen.name}.", "",
             "| Policy | Screen score | Held-out score |", "|---|---:|---:|"]
    for p in candidates:
        t = population.tally(games, p.name)
        held = f"{t.score:.1%}" if t.n else "not tested"
        lines.append(f"| {p.name} | {selection['scores'][p.name]:.1%} | {held} |")
    lo, hi = delta["map_cluster_ci95"]
    lines += ["", f"Paired delta: {100 * delta['difference']:+.2f} percentage points; "
              f"95% map-cluster interval [{100 * lo:+.2f}, {100 * hi:+.2f}].", "",
              f"Selected candidate vs splitter: {direct.w}-{direct.d}-{direct.l} W-D-L, "
              f"{direct.score:.1%} score. Success gate passed: {success}.", "",
              "No live bot changed or submitted. Only five validation maps and a scripted pool; "
              "not an online-strength claim. Negative/inconclusive results are retained."]
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf8")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
