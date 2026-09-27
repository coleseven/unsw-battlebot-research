"""Spawn-perturbed copies of ranked maps, for robustness tests.

Since 27 Sep the ranked server plays hash-suffixed variants of its maps
(e.g. Prisoners_Dilemma_12862686): same walls and portals, pearl spawner rates
changed and hidden from the replay. A Prisoners Dilemma variant moved the rich
spawners from one pair of columns to the other; a Trauma variant left its big
hub nearly dead. A bot tuned on the originals can learn their exact pearl
layout (and the hub book encodes it), so tests should also use maps whose
spawners are perturbed the same way.

    python -m bcsim.perturb_maps [--pool current|ranked] [--variants 1] [--seed 7]

Writes maps/perturbed/<stem>_p<k>.map. Each spawner's (min, max) respawn
interval is scaled by one log-uniform factor in [1/3, 4] (and with
probability 0.15 by 12, a near-dead hub), the same factor for a tile and its
mirror image under the map's symmetry, so both teams face the same map. Walls,
portals and starting dragons are unchanged.
"""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

from . import official_suite
from .paths import ROOT

OUT = ROOT / "maps" / "perturbed"


def _parse(text):
    w = h = None
    tiles = {}
    for line in text.splitlines():
        p = line.split()
        if p and p[0] == "MAP":
            w, h = int(p[1]), int(p[2])
        elif p and p[0] == "TILE":
            tiles[(int(p[1]), int(p[2]))] = (int(p[3]), int(p[4]))
    return w, h, tiles


def _symmetry(w, h, tiles):
    """The transform that maps the spawner layout onto itself."""
    spawners = {c: v for c, v in tiles.items() if v != (0, 0)}
    for name, f in (("rot180", lambda x, y: (w - 1 - x, h - 1 - y)),
                    ("mirror_x", lambda x, y: (w - 1 - x, y)),
                    ("mirror_y", lambda x, y: (x, h - 1 - y))):
        if all(tiles.get(f(x, y)) == v for (x, y), v in spawners.items()):
            return name, f
    raise ValueError("no symmetry maps the spawners onto themselves")


def perturb(text: str, rng: random.Random) -> str:
    w, h, tiles = _parse(text)
    _, f = _symmetry(w, h, tiles)
    factor = {}
    for c, v in sorted(tiles.items()):
        if v == (0, 0) or c in factor:
            continue
        k = 12.0 if rng.random() < 0.15 else math.exp(rng.uniform(math.log(1 / 3), math.log(4)))
        factor[c] = factor[f(*c)] = k
    out = []
    for line in text.splitlines():
        p = line.split()
        if p and p[0] == "TILE" and (int(p[1]), int(p[2])) in factor:
            k = factor[(int(p[1]), int(p[2]))]
            lo, hi = max(1, round(int(p[3]) * k)), max(1, round(int(p[4]) * k))
            line = f"TILE {p[1]} {p[2]} {lo} {max(lo, hi)}"
        out.append(line)
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--pool", choices=["current", "ranked"], default="current")
    ap.add_argument("--variants", type=int, default=1)
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    maps = official_suite.current_pool_maps() if a.pool == "current" else official_suite.ranked_maps()
    OUT.mkdir(parents=True, exist_ok=True)
    rng = random.Random(a.seed)
    for m in maps:
        text = m.read_text(encoding="utf8")
        for k in range(1, a.variants + 1):
            dest = OUT / f"{m.stem}_p{k}.map"
            dest.write_bytes(perturb(text, rng).encode("utf8"))
            print(dest.relative_to(ROOT))


if __name__ == "__main__":
    main()
