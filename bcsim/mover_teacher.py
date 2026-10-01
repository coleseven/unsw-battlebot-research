"""Counterfactual-move teacher for the new mover (R5, NEW_MOVER_PLAN.md).

A decision is (map, seed, sides, dragon id, round). The game is replayed from
the start with the same seed; at that decision the dragon's own reply is
produced as usual (its private state updates normally), then only its MOVE
line is rewritten to the forced direction. Every later decision of every bot
is recomputed from the changed observations.

    python -m bcsim.mover_teacher --identity      # M1 gate: no-op / same-move replay

The identity gate requires: no hook, a pass-through hook, and forcing the
move the bot chose anyway all reproduce the reference event stream (actions,
tile changes, moves, splits, deaths, sonar), ignoring CPU-point fields.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from . import guard, match, official_suite, replay as rp

STABLE = {rp.TILE_CHANGE, rp.DRAGON_ACTION, rp.DRAGON_UPDATE, rp.DRAGON_SPLIT,
          rp.DRAGON_DEATH, rp.SONAR_PING, rp.ROUND_START, rp.TURN_START}


def block_round(block: bytes) -> int:
    first = block.split(b"\n", 1)[0]
    return int(first.split()[1]) if first.startswith(b"ROUND") else -1


def move_of(reply: bytes) -> str | None:
    """The single-step direction of an ordinary MOVE reply, else None."""
    for line in reply.split(b"\n"):
        if line.startswith(b"MOVE "):
            d = line[5:].strip().decode()
            return d if len(d) == 1 else None
        if line.strip() and not line.startswith(b"SONAR") and not line.startswith(b"LOG"):
            return None
    return None


class Force:
    """Hook that forces `direction` for dragon `did` at `rnd` (a no-op when
    direction is None) and records what the bot originally chose."""

    def __init__(self, did: int | None = None, rnd: int | None = None, direction: str | None = None):
        self.did, self.rnd, self.direction = did, rnd, direction
        self.original: str | None = None
        self.applied = False

    def __call__(self, dragon_id, team, block, reply):
        if dragon_id != self.did or block_round(block) != self.rnd:
            return reply
        self.original = move_of(reply)
        if self.direction is None or self.original is None:
            return reply
        lines = reply.split(b"\n")
        for i, line in enumerate(lines):
            if line.startswith(b"MOVE "):
                lines[i] = b"MOVE " + self.direction.encode()
                self.applied = True
                break
        return b"\n".join(lines)


def events(blob: bytes):
    out = []
    for ev in rp.decode(blob).events:
        if ev[0] not in STABLE:
            continue
        if ev[0] == rp.DRAGON_ACTION:
            ev = ev[:3]                      # drop CPU points / exceeded / tle
        out.append(ev)
    return out


def play_blob(map_path, a, b, seed, hook=None):
    tmp = Path(os.environ.get("TEMP", ".")) / f"mover-{os.getpid()}.replay"
    r = match.play(Path(map_path), Path(a), Path(b), seed=seed, replay_to=tmp, hook=hook)
    blob = tmp.read_bytes()
    tmp.unlink(missing_ok=True)
    return r, blob


def first_moves(blob: bytes, team: str, start_round: int, limit: int = 5):
    """A few (dragon id, round, direction) ordinary moves by `team` from start_round on."""
    r = rp.decode(blob)
    teams, rnd, out = {}, 0, []
    from . import reconstruct
    board = reconstruct.Board(r.map_text)
    for i, (t, _) in enumerate(board.dragons):
        teams[i] = t
    for ev in r.events:
        if ev[0] == rp.ROUND_START:
            rnd = ev[1]
        elif ev[0] == rp.DRAGON_SPLIT:
            teams[ev[2]] = ev[3]
        elif ev[0] == rp.DRAGON_ACTION and rnd >= start_round and teams.get(ev[1]) == team:
            act = ev[2]
            if act and act[0] == "move" and len(act[1]) == 1:
                out.append((ev[1], rnd, act[1]))
                if len(out) >= limit:
                    break
    return out


def identity(cases) -> dict:
    report = []
    for map_path, a, b, seed, team in cases:
        _, ref = play_blob(map_path, a, b, seed)
        ref_ev = events(ref)
        _, again = play_blob(map_path, a, b, seed, hook=Force())
        same_noop = events(again) == ref_ev
        rows = []
        for did, rnd, d in first_moves(ref, team, 40, 3) + first_moves(ref, team, 300, 2):
            f = Force(did, rnd, d)
            _, blob = play_blob(map_path, a, b, seed, hook=f)
            same = events(blob) == ref_ev
            others = [x for x in "NESW" if x != d]
            g = Force(did, rnd, others[0])
            _, blob2 = play_blob(map_path, a, b, seed, hook=g)
            rows.append({"dragon": did, "round": rnd, "move": d, "seen": f.original,
                         "same_move_identical": same, "other_move": others[0],
                         "other_applied": g.applied, "other_diverges": events(blob2) != ref_ev})
        report.append({"map": Path(map_path).stem, "a": Path(a).name, "b": Path(b).name, "seed": seed,
                       "team": team, "noop_identical": same_noop, "forced": rows})
        print(json.dumps(report[-1]), flush=True)
    return {"cases": report, "pass": all(c["noop_identical"] and all(r["same_move_identical"] for r in c["forced"])
                                         for c in report)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--identity", action="store_true")
    ap.add_argument("--base", default="versions/v10h")
    ap.add_argument("--out", type=Path, default=Path("results/mover-m1-identity.json"))
    a = ap.parse_args()
    os.environ.setdefault("BCSIM_DETERMINISTIC_V6", "1")
    os.environ.setdefault("BCSIM_CPP_INPROC", "1")
    if a.identity:
        maps = {p.stem: p for p in official_suite.ranked_maps()}
        cases = [(maps["Portals"], a.base, "sparring/cpp_nicked_v92", 351001, "A"),
                 (maps["schooltime"], "sparring/nicked_lab", a.base, 351002, "B"),
                 (maps["trophy"], a.base, "results/v7-base-bot", 351003, "A")]
        with guard.slot("mover-identity"):
            rep = identity(cases)
        a.out.write_text(json.dumps(rep, indent=1), encoding="utf8")
        print("PASS" if rep["pass"] else "FAIL", a.out)


if __name__ == "__main__":
    main()
