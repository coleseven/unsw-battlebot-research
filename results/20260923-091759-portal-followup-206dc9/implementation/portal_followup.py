"""Fixed-size, unchanged-policy portal replication and generated-map transfer."""

import argparse
import json
import os
import random
import shutil
import uuid
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from . import arena, audit_jobs, fission_audit, guarded, novel_maps, population, portal_experiment, reconstruct, trap_followup
from .paths import ROOT, RESULTS, bot_hash, map_signature, resolve_maps

SOURCE = RESULTS / "20260923-085446-portal-9297e0"
SPECS = tuple((*s[:-1], 23001 + i, 4 if i % 2 == 0 else 8)
              for i, s in enumerate(novel_maps.SPECS))


def connected(board):
    seen, todo = {(0, 0)}, [(0, 0)]
    while todo:
        x, y = todo.pop()
        for d in "NESW":
            dest = board.dest(x, y, d)
            if dest is not None and dest not in seen:
                seen.add(dest)
                todo.append(dest)
    return len(seen) == board.w * board.h


def generate(spec):
    """Add reflection-symmetric portal pairs, retaining full connectivity.

    Candidate locations are shuffled before any games. Reject only invalid
    geometry, not layouts based on either bot's performance.
    """
    base = novel_maps.generate(spec[:-1])
    b = reconstruct.Board(base)
    w, h = b.w, b.h
    edges = {(axis, x, y): (1, -1) for axis, source in (("h", b.hedge), ("v", b.vedge))
             for x, y in source}
    protected = set()
    for _, body in b.dragons:
        for x, y in body:
            protected.update((("h", x, y), ("h", x, (y+1) % h),
                              ("v", x, y), ("v", (x+1) % w, y)))

    def render(current):
        lines = []
        for line in base.splitlines():
            if line.startswith("EDGE_COUNT "):
                lines.append(f"EDGE_COUNT {len(current)}")
                lines.extend(f"EDGE {(2*y+(axis=='v'))*(w+1)+x} {kind} {pid}"
                             for (axis, x, y), (kind, pid) in sorted(current.items()))
            elif line.startswith("EDGE "):
                continue
            elif line.startswith("MAP_NAME "):
                lines.append("MAP_NAME Portal_" + spec[0])
            else:
                lines.append(line)
        return "\n".join(lines) + "\n"

    choices = [(a, x, y) for a in "hv" for x in range(w) for y in range(h)]
    random.Random(spec[-2] ^ 0xABC123).shuffle(choices)
    pid = 0
    for axis, x, y in choices:
        if axis == "h":
            pairs = (((x, y), (w-1-x, y)), ((x, (-y) % h), (w-1-x, (-y) % h)))
        else:
            pairs = (((x, y), (x, h-1-y)), (((-x) % w, y), ((-x) % w, h-1-y)))
        keys = {(axis, a, c) for pair in pairs for a, c in pair}
        if len(keys) != 4 or keys & protected or any(edges.get(k, (0, -1))[0] == 2 for k in keys):
            continue
        trial = dict(edges)
        for i, pair in enumerate(pairs):
            for a, c in pair:
                trial[axis, a, c] = (2, pid+i)
        if not connected(reconstruct.Board(render(trial))):
            continue
        edges, pid = trial, pid+2
        if pid == spec[-1]:
            return render(edges)
    raise ValueError("Could not place the declared portal pairs")


def direct_summary(games, groups):
    tally = population.tally(games, "portal_escape")
    clusters = defaultdict(list)
    by_map = defaultdict(list)
    for g in games:
        score = arena.score_for(g, "portal_escape")
        clusters[groups[g["map"]]].append(score)
        by_map[g["map"]].append(score)
    return {"wins": tally.w, "draws": tally.d, "losses": tally.l, "score": tally.score,
            "cluster_ci95": arena.block_bootstrap(list(clusters.values()), iters=8000),
            "pair_ci95": tally.ci(), "map_scores": {m: sum(v)/len(v) for m, v in by_map.items()}}


def unchanged_no_portal(games, names):
    fields = ("winner", "reason", "rounds", "a_dragons", "b_dragons", "a_length", "b_length",
              "a_longest", "b_longest", "deaths", "error")
    def key(g, name):
        return (*g["block"], "A" if g["bot_a"] == name else "B")
    controls = {key(g, "control_450"): g for g in games
                if "control_450" in (g["bot_a"], g["bot_b"]) and g["map"] in names}
    checked = 0
    for g in games:
        if "portal_escape" not in (g["bot_a"], g["bot_b"]) or g["map"] not in names:
            continue
        control = controls[key(g, "portal_escape")]
        assert all(g.get(k) == control.get(k) for k in fields), "no-portal regression"
        checked += 1
    return checked


def run(workers):
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-portal-followup-" + uuid.uuid4().hex[:6])
    out.mkdir()
    original = json.loads((SOURCE / "plan.json").read_text())
    candidate = population.snapshot(SOURCE / "bots/portal_escape", out / "bots/portal_escape")
    reference = population.snapshot(ROOT / "versions/v2", out / "bots/reference_v2")
    control = population.snapshot(reference, out / "bots/control_450")
    assert bot_hash(candidate) == original["candidate_hash"]
    assert bot_hash(reference) == original["baseline_hash"]
    opponents = [reference] + [population.snapshot(guarded.MOVEMENT / "bots" / n, out / "bots" / n)
                               for n in ("splitter", "hunter")]
    (out / "maps").mkdir()
    official, transfer, portal_maps, no_portal, families = [], [], [], [], {}
    for source in resolve_maps("all"):
        dest = out / "maps" / f"official_{source.stem}_{map_signature(source)}.map"
        shutil.copy2(source, dest)
        official.append(dest)
        (portal_maps if reconstruct.Board(dest.read_text()).portals else no_portal).append(dest.stem)
    for spec in SPECS:
        dest = out / "maps" / ("new_" + spec[0] + ".map")
        dest.write_text(generate(spec), encoding="utf8")
        trap_followup.validate_map(dest)
        transfer.append(dest)
        families[dest.stem] = spec[1]
    assert len({map_signature(p) for p in official + transfer}) == len(official + transfer)
    plan = {"question": "Does unchanged emergency portal use replicate and transfer?",
            "source": str(SOURCE), "candidate_hash": bot_hash(candidate), "baseline_hash": bot_hash(reference),
            "live_hash": bot_hash(ROOT / "mybot"), "specs": SPECS, "families": families,
            "official_maps": [str(p) for p in official], "transfer_maps": [str(p) for p in transfer],
            "portal_maps": portal_maps, "no_portal_maps": no_portal,
            "official_seeds": list(range(18000, 18016)), "transfer_seeds": list(range(19000, 19016)),
            "expected_games": {"validation": len(official)*16*2*2*3, "transfer": len(transfer)*16*2},
            "gate": "ALL: official portal-only direct map-cluster CI lower > .5; "
                    "paired all-official opponent-pool gain map-cluster CI lower > 0; "
                    "transfer family-cluster CI lower > .5 with every transfer map score >= .375; "
                    "no-portal paired outcomes identical; replay and judge checks pass.",
            "selection": "none; fixed policy and sample sizes; no pooling with prior test, retuning, or optional stopping",
            "limits": "Familiar scripted opponents. Four related procedural families, not official distribution. "
                      "Fresh layout and bot seeds. Full local verification is not ranked evidence.", "workers": workers}
    population.write_json(out / "plan.json", plan)
    (out / "implementation").mkdir()
    for name in ("portal_followup.py", "portal_experiment.py", "novel_maps.py", "guarded.py", "bounded.py",
                 "arena.py", "match.py", "population.py", "paths.py", "fission_audit.py", "audit_jobs.py"):
        shutil.copy2(ROOT / "bcsim" / name, out / "implementation" / name)
    print(f"Experiment: {out}\nFixed games: {plan['expected_games']}", flush=True)
    games = guarded.stage(out, "validation", [control, candidate], opponents, official,
                          plan["official_seeds"], workers, True)
    newer = guarded.stage(out, "transfer", [candidate], [reference], transfer,
                          plan["transfer_seeds"], workers, True)
    direct = [g for g in games if "portal_escape" in (g["bot_a"], g["bot_b"])
              and "reference_v2" in (g["bot_a"], g["bot_b"]) and g["map"] in portal_maps]
    result = {"official_direct_portal": direct_summary(direct, {m: m for m in portal_maps}),
              "paired_pool": population.paired_delta(games, candidate.name, control.name),
              "transfer": direct_summary(newer, families),
              "no_portal_matched_games": unchanged_no_portal(games, no_portal)}
    result["performance_gate"] = (result["official_direct_portal"]["cluster_ci95"][0] > .5 and
        result["paired_pool"]["map_cluster_ci95"][0] > 0 and result["transfer"]["cluster_ci95"][0] > .5 and
        min(result["transfer"]["map_scores"].values()) >= .375)
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    assert bot_hash(ROOT / "versions/v2") == plan["baseline_hash"]
    population.write_json(out / "comparison.json", result)
    print(json.dumps(result, indent=2), flush=True)


def audit_game(args):
    return portal_experiment.audit_game(args) if args[1] else fission_audit.one_game(args)


def audit(out, workers):
    os.environ["RAYON_NUM_THREADS"] = "1"
    plan = json.loads((out / "plan.json").read_text())
    candidate = out / "bots/portal_escape"
    assert bot_hash(candidate) == plan["candidate_hash"]
    maps = {Path(p).stem: p for p in plan["official_maps"] + plan["transfer_maps"]}
    tasks = []
    for stage in ("validation", "transfer"):
        games = [json.loads(l) for l in (out / stage / "games.jsonl").read_text().splitlines()]
        assert len(games) == plan["expected_games"][stage]
        assert len({(g["map"], g["seed"], g["bot_a"], g["bot_b"]) for g in games}) == len(games)
        assert not any(arena.is_error(g) for g in games)
        assert not arena.check_hashes(games, json.loads((out / stage / "run.json").read_text()))
        tasks.extend((g, str(candidate) if candidate.name in (g["bot_a"], g["bot_b"]) else None,
                      maps[g["map"]]) for g in games)
    counts, samples = audit_jobs.run(tasks, workers, out, audit_game, "portal follow-up audit")
    assert counts["late_splits"] == 0
    population.write_json(out / "replay-audit.json", {"counts": dict(counts), "samples": samples,
                                                    "hash": bot_hash(candidate)})
    print(json.dumps(dict(counts), indent=2), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workers", type=int, choices=range(1, 9), default=8)
    p.add_argument("--audit", type=Path)
    args = p.parse_args()
    audit(args.audit, args.workers) if args.audit else run(args.workers)
