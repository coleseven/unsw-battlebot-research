"""Rebuild full game state from a replay and regenerate, for every turn, the
exact round block the engine sent that dragon.

    for turn in turns(replay.load(path)):
        turn.id, turn.team, turn.round, turn.block, turn.action

The regenerated block parses with bc.Obs like a live one, so the training
pipeline and the bot share one featurizer. `python -m bcsim.reconstruct`
checks the reconstruction against real blocks captured from local games.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import replay as rp

DXY = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}


class Board:
    """Static map: size, edges (kelp / portals), initial dragons."""

    def __init__(self, text: str) -> None:
        self.w = self.h = 0
        self.hedge: dict[tuple[int, int], int] = {}   # north edge of (x, y): -2 kelp, >=0 portal
        self.vedge: dict[tuple[int, int], int] = {}   # west edge of (x, y)
        self.spawns: set[tuple[int, int]] = set()     # tiles with max_gap > 0
        self.dragons: list[tuple[str, list[tuple[int, int]]]] = []
        for line in text.splitlines():
            p = line.split()
            if not p:
                continue
            if p[0] == "MAP":
                self.w, self.h = int(p[1]), int(p[2])
            elif p[0] == "TILE":
                if int(p[4]) > 0:
                    self.spawns.add((int(p[1]), int(p[2])))
            elif p[0] == "EDGE":
                idx, kind, pid = int(p[1]), int(p[2]), int(p[3])
                if kind == 0:
                    continue
                row, c = divmod(idx, self.w + 1)
                r, vertical = divmod(row, 2)
                val = -2 if kind == 1 else pid
                if vertical:
                    self.vedge[(c % self.w, r % self.h)] = val
                else:
                    self.hedge[(c % self.w, r % self.h)] = val
            elif p[0] == "DRAGON":
                team = "AB"[int(p[1])]
                n = int(p[2])
                coords = [(int(p[3 + 2 * i]), int(p[4 + 2 * i])) for i in range(n)]
                self.dragons.append((team, coords))
        self.portals: dict[int, list[tuple[str, tuple[int, int]]]] = {}
        for key, v in self.hedge.items():
            if v >= 0:
                self.portals.setdefault(v, []).append(("h", key))
        for key, v in self.vedge.items():
            if v >= 0:
                self.portals.setdefault(v, []).append(("v", key))

    def edge(self, x: int, y: int, d: str) -> int:
        """-1 open, -2 kelp, >= 0 portal id, for leaving (x, y) toward d."""
        if d == "N":
            return self.hedge.get((x, y), -1)
        if d == "S":
            return self.hedge.get((x, (y + 1) % self.h), -1)
        if d == "W":
            return self.vedge.get((x, y), -1)
        return self.vedge.get(((x + 1) % self.w, y), -1)

    def token(self, v: int) -> str:
        return "." if v == -1 else "w" if v == -2 else str(v)

    def dest(self, x: int, y: int, d: str) -> tuple[int, int] | None:
        """Tile reached by stepping d from (x, y); None for kelp."""
        e = self.edge(x, y, d)
        if e == -2:
            return None
        if e >= 0:
            here = ("h", (x, y)) if d == "N" else ("h", (x, (y + 1) % self.h)) if d == "S" \
                else ("v", (x, y)) if d == "W" else ("v", ((x + 1) % self.w, y))
            ends = self.portals.get(e, [])
            other = [p for p in ends if p != here]
            if other:
                _, (px, py) = other[0]
                if d == "E" or d == "S":
                    return px, py
                if d == "W":
                    return (px - 1) % self.w, py
                return px, (py - 1) % self.h
        dx, dy = DXY[d]
        return (x + dx) % self.w, (y + dy) % self.h


@dataclass
class Turn:
    game: str
    round: int
    id: int
    team: str
    block: str            # the round block this dragon received
    action: tuple | None  # ("move", "NNE") | ("split", n) | ("suicide",) | None
    points: int | None    # CPU points used (server replays), if recorded


class Dragon:
    """body[0] is the head. seg[k] is body segment k's facing (the way to the
    next segment toward the head), recorded as the head moves so it stays
    right across portals; seg[0] is unused (the head's facing is `facing`)."""

    __slots__ = ("id", "team", "body", "seg", "facing")

    def __init__(self, did: int, team: str, body: list, facing: str, w: int, h: int) -> None:
        self.id, self.team, self.body, self.facing = did, team, body, facing
        self.seg = [facing] + [_facing(body[k - 1], body[k], w, h) for k in range(1, len(body))]


def _facing(a: tuple[int, int], b: tuple[int, int], w: int, h: int) -> str:
    """Direction from b to a (neighbouring tiles, with wrap)."""
    dx = (a[0] - b[0]) % w
    dy = (a[1] - b[1]) % h
    if dx == 1:
        return "E"
    if dx == w - 1:
        return "W"
    if dy == 1:
        return "S"
    return "N"


def turns(r: rp.Replay, game: str = ""):
    """Yield a Turn for every dragon turn in the replay."""
    board = Board(r.map_text)
    w, h = board.w, board.h
    dragons: dict[int, Dragon] = {}
    for i, (team, coords) in enumerate(board.dragons):
        f = _facing(coords[0], coords[1], w, h) if len(coords) > 1 else "N"
        dragons[i] = Dragon(i, team, list(coords), f, w, h)
    pearls: set[tuple[int, int]] = set()
    countdown: dict[tuple[int, int], int] = {}
    inbox: dict[int, list[int]] = {}
    rnd = 0
    pending: Turn | None = None

    def block_for(d: Dragon) -> str:
        hx, hy = d.body[0]
        occ = {}
        for o in dragons.values():
            for k, (x, y) in enumerate(o.body):
                occ[(x, y)] = (o, k)
        lines = [f"ROUND {rnd}", f"DIR {d.facing}", f"LENGTH {len(d.body)}",
                 f"UNIT_COUNT {sum(1 for o in dragons.values() if o.team == d.team)}"]
        msgs = inbox.pop(d.id, [])
        lines.append(f"NUM_MSGS {len(msgs)}")
        lines += [str(m) for m in msgs]
        cells = [((hx + dc) % w, (hy + dr) % h) for dr in range(-3, 4) for dc in range(-3, 4)]
        for (x, y) in cells:
            cd = countdown.get((x, y), -1) if (x, y) in board.spawns else -1
            lines.append(f"{x} {y} {1 if (x, y) in pearls else 0} {cd}")
        parts = []
        for (x, y) in cells:
            if (x, y) in occ:
                o, k = occ[(x, y)]
                f = o.facing if k == 0 else o.seg[k]
                parts.append(f"{o.team} {o.id} {x} {y} {f} {1 if k == 0 else 0}")
        lines.append(f"DRAGON_BODIES {len(parts)}")
        lines += parts
        for r_ in range(8):
            y = (hy - 3 + r_) % h
            lines.append(" ".join(board.token(board.hedge.get(((hx + dc) % w, y), -1)) for dc in range(-3, 4)))
        for r_ in range(7):
            y = (hy - 3 + r_) % h
            lines.append(" ".join(board.token(board.vedge.get(((hx + dc) % w, y), -1)) for dc in range(-3, 5)))
        return "\n".join(lines) + "\n"

    for ev in r.events:
        k = ev[0]
        if k == rp.ROUND_START:
            rnd = ev[1]
            for t in board.spawns:
                if t in countdown:
                    countdown[t] -= 1
        elif k == rp.PEARL_COUNTDOWN:
            countdown[(ev[1], ev[2])] = ev[3]
        elif k == rp.TILE_CHANGE:
            if ev[3]:
                pearls.add((ev[1], ev[2]))
            else:
                pearls.discard((ev[1], ev[2]))
        elif k == rp.TURN_START:
            if pending is not None:
                yield pending
            d = dragons.get(ev[1])
            pending = Turn(game, rnd, ev[1], d.team, block_for(d), None, None) if d else None
        elif k == rp.DRAGON_ACTION:
            if pending is not None and pending.id == ev[1]:
                pending.action, pending.points = ev[2], ev[3]
        elif k == rp.DRAGON_UPDATE:
            # one update per step of a move (so a sprint emits several), with
            # the engine's own head position: portals are already resolved
            d = dragons.get(ev[1])
            if d is None:
                continue
            d.facing = ev[2]
            head, tail = ev[3], ev[4]
            if d.body[0] != head:
                d.body.insert(0, head)
                d.seg.insert(0, ev[2])
                d.seg[1] = ev[2]
            # trim the tail back to the reported one (handles growth + sprint cost)
            if tail in d.body:
                cut = len(d.body) - d.body[::-1].index(tail)
                del d.body[cut:]
                del d.seg[cut:]
        elif k == rp.DRAGON_SPLIT:
            _, parent, child, team, cf, pbody, cbody = ev
            if parent in dragons:
                par = dragons[parent]
                n = len(pbody)
                if par.body[:n] == list(pbody):
                    del par.body[n:]
                    del par.seg[n:]
                else:
                    par.body = list(pbody)
                    par.seg = [par.facing] + [_facing(pbody[k - 1], pbody[k], w, h) for k in range(1, n)]
            dragons[child] = Dragon(child, team, list(cbody), cf, w, h)
        elif k == rp.DRAGON_DEATH:
            dragons.pop(ev[1], None)
        elif k == rp.SONAR_PING:
            hit = ev[6]
            if hit is not None:
                inbox.setdefault(hit, []).append(ev[3])
    if pending is not None:
        yield pending


# -- self check -------------------------------------------------------------------


def _check(n_maps: int = 99) -> None:
    """Play local games capturing real blocks, then compare reconstruction."""
    import pathlib
    import sys

    from .match import InProcessBot, engine
    from .paths import FRAMEWORK, MAPS, ROOT
    sys.path.insert(0, str(FRAMEWORK))
    import bc  # noqa: E402

    def canon(text: str):
        o = bc.Obs(text)
        return (o.round, o.facing, o.length, o.unit_count, tuple(o.msgs), tuple(o.x), tuple(o.y),
                tuple(o.pearl), tuple(o.pearl_in), frozenset(o.bodies),
                tuple(map(tuple, o.hedge)), tuple(map(tuple, o.vedge)))

    bots = [InProcessBot((ROOT / "opponents" / n).resolve()) for n in ("splitter", "hunter")]
    total = bad = 0
    fields = ["round", "facing", "length", "unit_count", "msgs", "x", "y", "pearl",
              "pearl_in", "bodies", "hedge", "vedge"]
    diff_count = {f: 0 for f in fields}
    for m in sorted(MAPS.rglob("*.map"))[:n_maps]:
        real: dict[tuple[int, int], str] = {}
        brains = {}
        teams = {}

        def spawn(i, init):
            t = "B" if b"TEAM B" in init else "A"
            teams[i] = t
            brains[i] = bots[t == "B"].new_brain(init.decode(), i)

        def reply(i, block):
            text = block.decode()
            real[(i, int(text.split("\n", 1)[0].split()[1]))] = text
            return brains[i].step(text).encode()

        eng = engine()
        eng.run(m.read_bytes(), reply, None, spawn, lambda l: None, 0)
        rep = rp.decode(eng.replay("a", "b"))
        for t in turns(rep):
            want = real.get((t.id, t.round))
            if want is None:
                continue
            total += 1
            a, b = canon(t.block), canon(want)
            if a != b:
                bad += 1
                for f, x, y in zip(fields, a, b):
                    if x != y:
                        diff_count[f] += 1
    print(f"reconstructed {total} turns, {bad} differ; by field: "
          + ", ".join(f"{k}={v}" for k, v in diff_count.items() if v))


if __name__ == "__main__":
    _check()
