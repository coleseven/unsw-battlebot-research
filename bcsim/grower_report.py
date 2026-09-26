"""Verify unchanged early games and summarize completed grower experiments."""

import argparse
import json
from pathlib import Path

from . import endgame, population

FIELDS = ("winner", "reason", "rounds", "a_dragons", "b_dragons", "a_length", "b_length",
          "a_longest", "b_longest", "deaths", "error")


def early_equivalence(games, candidate, cutoff):
    def key(g, name):
        return (*g["block"], "A" if g["bot_a"] == name else "B")

    control = {key(g, "control_450"): g for g in games if "control_450" in (g["bot_a"], g["bot_b"])}
    checked = 0
    for g in games:
        if candidate not in (g["bot_a"], g["bot_b"]):
            continue
        reference = control[key(g, candidate)]
        # rounds is a COUNT: cutoff=350 first changes zero-based round 350,
        # so a game lasting exactly 350 rounds must still be identical.
        if reference["rounds"] > cutoff:
            continue
        for field in FIELDS:
            if g.get(field) != reference.get(field):
                raise ValueError(f"Early divergence in {field}: {g['map']} seed {g['seed']}")
        checked += 1
    return checked


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("experiment", type=Path)
    args = p.parse_args()
    out = args.experiment
    plan = json.loads((out / "plan.json").read_text())
    result = {}
    for stage in ("screen", "validation"):
        path = out / stage / "games.jsonl"
        if not (out / stage / "summary.md").exists():
            continue
        games = [json.loads(line) for line in path.read_text().splitlines()]
        names = ["control_450"] + [n for n in plan["modes"] if any(n in (g["bot_a"], g["bot_b"]) for g in games)]
        result[stage] = {"diagnostics": {n: endgame.diagnostics(games, n) for n in names},
                         "early_equivalence": {n: early_equivalence(games, n, min(c for c in plan["modes"][n] if c is not None))
                                               for n in names[1:]}}
    population.write_json(out / "phase-diagnostics.json", result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
