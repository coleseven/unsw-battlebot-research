"""Lean bot framework for UNSW Battlecode.

A bot is a `Brain` subclass: one instance per dragon, fed one parsed `Obs`
per turn, returning an action string. The same class runs two ways:

  * submitted / `unswbc run`: main.py calls `bc.run(Brain)`, a stdin loop;
  * the local arena: the harness builds Brains in-process and calls `step`
    directly, which is orders of magnitude faster than one OS process per
    dragon.

Keep all state on `self` (never module globals): on the judge every dragon
is its own process, and the arena gives every dragon a fresh module copy.

This file is the single source of truth; `python -m bcsim.sync` copies it
into every bot directory.
"""

from __future__ import annotations

import random
import sys

R = 3                  # vision radius
W = 7                  # vision width
CENTER = R * W + R     # index of the head tile in 7x7 row-major order

DIRS = "NESW"
DX = {"N": 0, "E": 1, "S": 0, "W": -1}
DY = {"N": -1, "E": 0, "S": 1, "W": 0}
OPPOSITE = {"N": "S", "E": "W", "S": "N", "W": "E"}
LEFT = {"N": "W", "E": "N", "S": "E", "W": "S"}
RIGHT = {"N": "E", "E": "S", "S": "W", "W": "N"}

OPEN, KELP = -1, -2    # edge encoding; >= 0 is a portal id


class Init:
    __slots__ = ("id", "team", "width", "height", "unit_limit")

    def __init__(self, text: str) -> None:
        self.id = 0
        self.team = "A"
        self.width = self.height = 0
        self.unit_limit = 64
        for line in text.splitlines():
            p = line.split()
            if not p:
                continue
            if p[0] == "ID":
                self.id = int(p[1])
            elif p[0] == "TEAM":
                self.team = p[1]
            elif p[0] == "MAP":
                self.width, self.height = int(p[1]), int(p[2])
            elif p[0] == "UNIT_LIMIT":
                self.unit_limit = int(p[1])


def _edge(tok: str) -> int:
    if tok == ".":
        return OPEN
    if tok == "w":
        return KELP
    return int(tok)


class Obs:
    """One turn's view. Local cells are indexed k = row * 7 + col, with the
    head at k = CENTER (row 0 is three tiles north of the head)."""

    __slots__ = ("round", "facing", "length", "unit_count", "msgs",
                 "x", "y", "pearl", "pearl_in",
                 "occ", "bodies", "hedge", "vedge")

    def __init__(self, text: str) -> None:
        lines = text.split("\n")
        i = 0
        while not lines[i].startswith("ROUND"):
            i += 1
        self.round = int(lines[i].split()[1])
        self.facing = lines[i + 1].split()[1]
        self.length = int(lines[i + 2].split()[1])
        self.unit_count = int(lines[i + 3].split()[1])
        n = int(lines[i + 4].split()[1])
        i += 5
        self.msgs = [int(lines[i + j]) for j in range(n)]
        i += n

        xs, ys, pearl, pearl_in = [], [], [], []
        for j in range(49):
            a, b, c, d = lines[i + j].split()
            xs.append(int(a))
            ys.append(int(b))
            pearl.append(c == "1")
            pearl_in.append(int(d))
        i += 49
        self.x, self.y = xs, ys          # absolute coordinates per local cell
        self.pearl, self.pearl_in = pearl, pearl_in

        # occ[k] = (team, id, is_head, facing) or None
        occ: list = [None] * 49
        bodies = []
        count = int(lines[i].split()[1])
        i += 1
        hx, hy = xs[CENTER], ys[CENTER]
        index = {(xs[k], ys[k]): k for k in range(49)}
        for j in range(count):
            team, did, x, y, f, head = lines[i + j].split()
            part = (team, int(did), head == "1", f)
            bodies.append((team, int(did), int(x), int(y), f, head == "1"))
            k = index.get((int(x), int(y)))
            if k is not None:
                occ[k] = part
        i += count
        self.occ, self.bodies = occ, bodies

        # hedge[r][c]: north edge of row r (r = 7 is the south edge of row 6)
        # vedge[r][c]: west edge of column c (c = 7 is the east edge of col 6)
        self.hedge = [[_edge(t) for t in lines[i + r].split()] for r in range(8)]
        i += 8
        self.vedge = [[_edge(t) for t in lines[i + r].split()] for r in range(7)]

    # -- geometry -------------------------------------------------------------

    @property
    def head(self) -> tuple[int, int]:
        return self.x[CENTER], self.y[CENTER]

    @staticmethod
    def step(k: int, d: str) -> int:
        """Local neighbour of cell k, or -1 when it leaves the window."""
        r, c = divmod(k, W)
        r += DY[d]
        c += DX[d]
        if 0 <= r < W and 0 <= c < W:
            return r * W + c
        return -1

    def edge(self, k: int, d: str) -> int:
        r, c = divmod(k, W)
        if d == "N":
            return self.hedge[r][c]
        if d == "S":
            return self.hedge[r + 1][c]
        if d == "W":
            return self.vedge[r][c]
        return self.vedge[r][c + 1]

    def passable(self, k: int, d: str) -> bool:
        """True if a head at k can step d onto a known-empty tile with no
        kelp, no portal (destination unknown) and no dragon part there."""
        e = self.edge(k, d)
        if e != OPEN:
            return False
        n = self.step(k, d)
        return n >= 0 and self.occ[n] is None

    def enemy_heads(self, team: str) -> list[int]:
        return [k for k in range(49)
                if self.occ[k] is not None and self.occ[k][2] and self.occ[k][0] != team]

    def bfs(self, start: int = CENTER, blocked=None) -> dict[int, tuple[int, str]]:
        """Shortest paths inside the window over passable cells.
        Returns {cell: (distance, first move)}."""
        out = {start: (0, "")}
        frontier = [start]
        while frontier:
            nxt = []
            for k in frontier:
                dist, first = out[k]
                for d in DIRS:
                    if not self.passable(k, d):
                        continue
                    n = self.step(k, d)
                    if n in out or (blocked is not None and n in blocked):
                        continue
                    out[n] = (dist + 1, first or d)
                    nxt.append(n)
            frontier = nxt
        return out


class Brain:
    """Subclass and override `turn`. Return an action string such as
    "MOVE N", "MOVE NNE" or "SPLIT 3"; extra lines (SONAR, INDICATOR,
    LOG, DOT, LINE) go in `self.extra`."""

    def __init__(self, init: Init, seed: int | None = None) -> None:
        self.init = init
        self.team = init.team
        self.id = init.id
        self.rng = random.Random(seed if seed is not None else random.getrandbits(64))
        self.extra: list[str] = []

    def turn(self, obs: Obs) -> str:
        raise NotImplementedError

    def step(self, block: str) -> str:
        obs = Obs(block)
        self.extra = []
        try:
            action = self.turn(obs)
        except Exception as exc:  # a crash would kill the dragon; fall back
            action = self.fallback(obs)
            self.extra.append(f"LOG crash {type(exc).__name__}: {exc}")
        return "\n".join([action, *self.extra, "ENDTURN", ""])

    def fallback(self, obs: Obs) -> str:
        for d in (obs.facing, LEFT[obs.facing], RIGHT[obs.facing]):
            if obs.passable(CENTER, d):
                return "MOVE " + d
        return "MOVE " + obs.facing


def run(brain_cls) -> None:
    """stdin/stdout loop used by main.py on the judge and in `unswbc run`."""
    read = sys.stdin.readline
    out = sys.stdout
    header = []
    while True:
        line = read()
        if not line:
            return
        if line.strip() == "":
            if header:
                break
            continue
        header.append(line)
        if line.startswith("UNIT_LIMIT"):
            break
    brain = brain_cls(Init("".join(header)))
    while True:
        lines = []
        line = read()
        while line and not line.startswith("ROUND"):
            line = read()
        if not line:
            return
        lines.append(line)
        # header (4 more) + msgs + 49 tiles + bodies header
        for _ in range(4):
            lines.append(read())
        n = int(lines[-1].split()[1])
        for _ in range(n + 49):
            lines.append(read())
        bodies = read()
        lines.append(bodies)
        for _ in range(int(bodies.split()[1]) + 15):
            lines.append(read())
        out.write(brain.step("".join(lines)))
        out.flush()
