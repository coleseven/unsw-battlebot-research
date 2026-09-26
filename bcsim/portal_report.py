"""Descriptive mechanisms after the fixed portal follow-up, not a new gate."""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from . import endgame, population, reconstruct


def report(out):
    plan = json.loads((out / "plan.json").read_text())
    audits = [json.loads(l) for l in (out / "audit-progress.jsonl").read_text().splitlines()]
    # Require the completed final audit, not a live partial checkpoint.
    final = json.loads((out / "replay-audit.json").read_text())
    assert final["counts"]["games"] == sum(plan["expected_games"].values())
    lookup, phases, mechanisms = {}, {}, defaultdict(Counter)
    for stage in ("validation", "transfer"):
        games = [json.loads(l) for l in (out / stage / "games.jsonl").read_text().splitlines()]
        assert len(games) == plan["expected_games"][stage]
        names = ("control_450", "portal_escape") if stage == "validation" else ("portal_escape",)
        phases[stage] = {n: endgame.diagnostics(games, n) for n in names}
        for g in games:
            lookup[str(Path(g["replay"]).resolve())] = (stage, g["map"])
    for row in audits:
        stage, name = lookup[row["key"]]
        mechanisms[stage, name].update(row["counts"])
    rows = []
    for stage, field in (("validation", "official_maps"), ("transfer", "transfer_maps")):
        for value in plan[field]:
            path = Path(value)
            b = reconstruct.Board(path.read_text())
            c = mechanisms[stage, path.stem]
            turns = c["verified_candidate_turns"]
            row = {"stage": stage, "map": path.stem, "width": b.w, "height": b.h,
                   "portal_pairs": len(b.portals),
                   "portal_edge_fraction": sum(len(v) for v in b.portals.values()) / (2*b.w*b.h),
                   "spawn_tile_fraction": len(b.spawns) / (b.w*b.h),
                   "kelp_edge_fraction": sum(v == -2 for edges in (b.hedge, b.vedge) for v in edges.values()) / (2*b.w*b.h),
                   "counts": dict(c),
                   "overrides_per_1000_turns": 1000*c["portal_overrides"]/turns if turns else None,
                   "immediate_override_survival": c["override_survived_own_turn"]/c["portal_overrides"]
                   if c["portal_overrides"] else None}
            rows.append(row)
    result = {"phase_diagnostics": phases, "maps": rows,
              "limits": "Post-test descriptive geometry and mechanism counts, not a causal explanation or new acceptance gate."}
    population.write_json(out / "mechanism-report.json", result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("experiment", type=Path)
    report(p.parse_args().experiment)
