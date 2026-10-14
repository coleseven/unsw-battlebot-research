"""One-shot transfer test on new, connected, symmetric synthetic maps.

This generator is NOT the competition's map distribution. It tests a declared
range of unfamiliar sizes, kelp densities, and food scarcity without tuning
the selected bot on their results.
"""

import argparse
import json
import random
import shutil
import uuid
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from . import arena, guarded, population, reconstruct, trap_followup
from .paths import ROOT, RESULTS, bot_hash, map_signature

SPECS = (
    ("open_small", "open", 12, 12, 0., 1., 8, 20, 15001),
    ("open_large", "open", 24, 24, 0., .7, 16, 35, 15002),
    ("baffles_small", "baffles", 12, 16, .12, 1., 5, 15, 15003),
    ("baffles_large", "baffles", 20, 16, .18, .6, 10, 25, 15004),
    ("dense_small", "dense", 14, 14, .30, 1., 8, 20, 15005),
    ("dense_large", "dense", 20, 20, .38, .65, 10, 30, 15006),
    ("scarce_small", "scarce", 16, 12, .20, .3, 20, 40, 15007),
    ("scarce_large", "scarce", 18, 18, .34, .3, 20, 40, 15008),
)


def generate(spec):
    name, _, w, h, density, food, low, high, seed = spec
    rng = random.Random(seed)
    walls = set()

    def orbit(axis, x, y):
        if axis == "v":
            return {(axis, a, b) for a in (x, (-x) % w) for b in (y, h - 1 - y)}
        return {(axis, a, b) for a in (x, w - 1 - x) for b in (y, (-y) % h)}

    protected = set()
    for x, y in ((2, 3), (2, 4), (w - 3, h - 3), (w - 3, h - 4)):
        protected.update(orbit("h", x, y))

    def connected():
        seen, todo = {(0, 0)}, [(0, 0)]
        while todo:
            x, y = todo.pop()
            for edge, dest in ((('h', x, y), (x, (y - 1) % h)),
                               (('h', x, (y + 1) % h), (x, (y + 1) % h)),
                               (('v', x, y), ((x - 1) % w, y)),
                               (('v', (x + 1) % w, y), ((x + 1) % w, y))):
                if edge not in walls and dest not in seen:
                    seen.add(dest)
                    todo.append(dest)
        return len(seen) == w * h

    choices = [(a, x, y) for a in "hv" for x in range(w) for y in range(h)]
    rng.shuffle(choices)
    target = int(2 * w * h * density)
    for edge in choices:
        if len(walls) >= target:
            break
        group = orbit(*edge)
        if group & protected:
            continue
        added = group - walls
        walls.update(added)
        if not connected():
            walls.difference_update(added)
    tiles, visited = set(), set()
    for y in range(h):
        for x in range(w):
            if (x, y) in visited:
                continue
            group = {(a, b) for a in (x, w - 1 - x) for b in (y, h - 1 - y)}
            visited.update(group)
            if rng.random() < food:
                tiles.update(group)
    lines = [f"MAP {w} {h}", "SYMMETRY xy", f"MAP_NAME Novel_{name}", f"TILE_COUNT {len(tiles)}"]
    lines += [f"TILE {x} {y} {low} {high}" for x, y in sorted(tiles)]
    lines += [f"EDGE_COUNT {len(walls)}"]
    lines += [f"EDGE {(2 * y + (axis == 'v')) * (w + 1) + x} 1 -1" for axis, x, y in sorted(walls)]
    lines += ["DRAGON_COUNT 2", "DRAGON 0 3 2 2 2 3 2 4",
              f"DRAGON 1 3 {w-3} {h-3} {w-3} {h-4} {w-3} {h-5}"]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--source", type=Path, default=RESULTS / "20260922-232921-fission-5df835")
    args = parser.parse_args()
    selection = json.loads((args.source / "selection.json").read_text())
    source = args.source / "bots" / selection["selected"]
    assert bot_hash(source) == selection["hash"]
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-novel-maps-" + uuid.uuid4().hex[:6])
    out.mkdir()
    candidate = population.snapshot(source, out / "bots" / source.name)
    reference = population.snapshot(args.source / "bots/reference_450", out / "bots/reference_450")
    (out / "maps").mkdir()
    maps, families = [], {}
    for spec in SPECS:
        path = out / "maps" / (spec[0] + ".map")
        path.write_text(generate(spec), encoding="utf8")
        trap_followup.validate_map(path)
        maps.append(path)
        families[path.stem] = spec[1]
    assert len({map_signature(p) for p in maps}) == len(maps)
    plan = {"question": "Does the selected, unchanged reproduction policy transfer to new generated layouts?",
            "source": str(source), "source_hash": bot_hash(source), "live_hash": bot_hash(ROOT / "mybot"),
            "specs": SPECS, "maps": [str(p) for p in maps], "families": families,
            "seeds": list(range(14000, 14008)), "workers": args.workers,
            "selection": "none; fixed fission-screen winner, no use of transfer results for tuning",
            "gate": "Family-cluster 95% lower bound above .5, and no per-map score below .375",
            "limits": "Four related procedural families, not the competition's map distribution. "
                      "No portals. Bot/map RNG seeds differ from previous performance experiments."}
    population.write_json(out / "plan.json", plan)
    shutil.copy2(Path(__file__), out / "generator.py")
    print(f"Experiment: {out}", flush=True)
    games = guarded.stage(out, "transfer", [candidate], [reference], maps, plan["seeds"], args.workers, True)
    tally = population.tally(games, candidate.name)
    groups = defaultdict(list)
    for g in games:
        groups[families[g["map"]]].append(arena.score_for(g, candidate.name))
    ci = arena.block_bootstrap(list(groups.values()), iters=8000)
    by_map = {m.stem: population.tally([g for g in games if g["map"] == m.stem], candidate.name).score for m in maps}
    result = {"wins": tally.w, "draws": tally.d, "losses": tally.l, "score": tally.score,
              "family_ci95": ci, "pair_ci95": tally.ci(), "map_scores": by_map,
              "transfer_gate": ci[0] > .5 and min(by_map.values()) >= .375}
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    population.write_json(out / "comparison.json", result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
