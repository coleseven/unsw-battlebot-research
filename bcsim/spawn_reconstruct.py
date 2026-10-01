"""Reconstruct hidden pearl spawners of a server map from its replays.

Server replays of map variants zero the TILE spawn parameters. Pearls still
appear in the events: a pearl that appears in a round phase with no death is
a spawn (corpse pearls appear only in the turn of a death). For each spawner
cell the gaps between a pearl being taken and the next spawn there give the
respawn-delay range, written back as TILE x y lo hi.

    python -m bcsim.spawn_reconstruct --map-name "Tower Defense" --games data/sprint1_games.json --out maps/sprint/Tower_Defense.map

The result approximates the real spawners (rare slow spawners seen once give
a wide range); it is a test map for generalisation, not the server's file.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from . import replay as rp, scrape


def scan(blob_paths):
    """Per cell: clean spawn count, delay samples; plus the map text and game count."""
    spawns = defaultdict(int)
    delays = defaultdict(list)
    initial = defaultdict(int)
    text = None
    games = 0
    for path in blob_paths:
        r = rp.load(path)
        text = text or r.map_text
        games += 1
        rnd = 0
        phase = []                 # TILE_CHANGE events of the current turn / round-start phase
        death_in_phase = False
        taken = {}                 # cell -> round the pearl there was removed
        has = set()

        def flush():
            nonlocal phase, death_in_phase
            for x, y, pearl in phase:
                c = (x, y)
                if pearl:
                    if not death_in_phase:
                        spawns[c] += 1
                        if rnd == 0:
                            initial[c] += 1
                        if c in taken:
                            delays[c].append(rnd - taken.pop(c))
                    has.add(c)
                else:
                    if c in has:
                        taken[c] = rnd
                    has.discard(c)
            phase, death_in_phase = [], False

        for ev in r.events:
            k = ev[0]
            if k == rp.ROUND_START:
                flush(); rnd = ev[1]
            elif k == rp.TURN_START:
                flush()
            elif k == rp.DRAGON_DEATH:
                death_in_phase = True
            elif k == rp.TILE_CHANGE:
                phase.append((ev[1], ev[2], bool(ev[3])))
        flush()
    return text, games, spawns, delays, initial


def mirror_fn(lines):
    """Cell -> its mirror under the map's SYMMETRY line (the engine requires
    spawners to match their mirror): x, y, or xy (point reflection)."""
    w, h = (int(v) for v in next(l for l in lines if l.startswith("MAP ")).split()[1:3])
    sym = next((l.split()[1] for l in lines if l.startswith("SYMMETRY")), "xy")
    # the engine's convention: "y" reflects across the vertical axis (x flips),
    # "x" across the horizontal one (y flips); checked on Islands (2,1)<->(53,1)
    if sym == "y":
        return lambda c: (w - 1 - c[0], c[1])
    if sym == "x":
        return lambda c: (c[0], h - 1 - c[1])
    return lambda c: (w - 1 - c[0], h - 1 - c[1])


def symmetrise(lines, spawns, delays):
    """Pool each cell's evidence with its mirror's, so both get identical spawners."""
    m = mirror_fn(lines)
    s2, d2 = defaultdict(int), defaultdict(list)
    cells = set(spawns) | set(m(c) for c in spawns)
    for c in cells:
        mc = m(c)
        pair = {c, mc}
        s2[c] = sum(spawns.get(k, 0) for k in pair) / len(pair)
        d2[c] = [v for k in pair for v in delays.get(k, [])]
    return s2, d2


def rebuild(text: str, games: int, spawns, delays, min_per_game: float = 0.3):
    lines = text.replace("\r\n", "\n").strip().split("\n")
    spawns, delays = symmetrise(lines, spawns, delays)
    out, kept = [], {}
    for line in lines:
        if line.startswith("TILE "):
            p = line.split()
            c = (int(p[1]), int(p[2]))
            if spawns.get(c, 0) / games >= min_per_game:
                ds = sorted(delays.get(c, []))
                if ds:
                    lo = ds[int(0.1 * (len(ds) - 1))]; hi = ds[int(0.9 * (len(ds) - 1))]
                else:              # seen but never respawned within a game: slow
                    lo, hi = 400, 500
                lo, hi = max(1, lo), max(max(1, lo), hi)
                kept[c] = (lo, hi)
                line = f"TILE {p[1]} {p[2]} {lo} {hi}"
        out.append(line)
    return "\n".join(out) + "\n", kept


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--map-name", required=True)
    ap.add_argument("--games", type=Path, default=Path("data/sprint1_games.json"))
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--min-per-game", type=float, default=0.3)
    a = ap.parse_args()
    rows = json.loads(a.games.read_text())
    paths = [scrape.REPLAYS / f"{gid}.replay" for _, gid, m, _ in rows if m == a.map_name]
    text, games, spawns, delays, initial = scan(paths)
    mapped, kept = rebuild(text, games, spawns, delays, a.min_per_game)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(mapped, encoding="utf8", newline="\n")
    fast = sum(1 for lo, hi in kept.values() if hi <= 20)
    print(f"{a.map_name}: {games} games, {len(kept)} spawners ({fast} fast), "
          f"{sum(1 for c in kept if initial.get(c))} with a round-0 pearl -> {a.out}")


if __name__ == "__main__":
    main()
