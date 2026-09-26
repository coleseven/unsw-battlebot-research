"""Descriptive screen ablation; never substitutes for held-out validation."""

import argparse
import json
from pathlib import Path

from . import endgame, population, reconstruct


def report(out):
    plan = json.loads((out / "plan.json").read_text())
    games = [json.loads(l) for l in (out / "screen/games.jsonl").read_text().splitlines()]
    assert len(games) == 216 and (out / "screen/summary.md").exists()
    no_portal = {Path(p).stem for p in plan["maps"] if not reconstruct.Board(Path(p).read_text()).portals}
    def key(g, name):
        return (*g["block"], "A" if g["bot_a"] == name else "B")
    reference = {key(g, "terrain_memory"): g for g in games
                 if "terrain_memory" in (g["bot_a"], g["bot_b"]) and g["map"] in no_portal}
    checked = 0
    fields = ("winner", "reason", "rounds", "a_dragons", "b_dragons", "a_length", "b_length",
              "a_longest", "b_longest", "deaths", "error")
    for g in games:
        if "portal_memory" not in (g["bot_a"], g["bot_b"]) or g["map"] not in no_portal:
            continue
        control = reference[key(g, "portal_memory")]
        assert all(g.get(f) == control.get(f) for f in fields), "ablation differs on a no-portal map"
        checked += 1
    result = {"no_portal_ablation_pairs_identical": checked,
              "portal_addition_paired_gain": population.paired_delta(games, "portal_memory", "terrain_memory"),
              "diagnostics": {n: endgame.diagnostics(games, n) for n in ("control_450", *plan["modes"])},
              "limits": "Screening data only; selection and descriptive ablation, not independent confirmation."}
    population.write_json(out / "screen/ablation-report.json", result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("experiment", type=Path)
    report(p.parse_args().experiment)
