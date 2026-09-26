"""Attribute eaten pearls to replay-visible spawns or a specific corpse.

This is observational: a corpse pearl reaching a long dragon does not prove
that the dead dragon intended to feed it. Run only on saved replay files.
"""

import argparse
import json
from collections import Counter
from pathlib import Path

from . import reconstruct, replay


def trace(r):
    board = reconstruct.Board(r.map_text)
    bodies = {i: list(coords) for i, (_, coords) in enumerate(board.dragons)}
    teams = {i: team for i, (team, _) in enumerate(board.dragons)}
    origins = {}
    consumed = []
    snapshots = {}
    counts = Counter()
    deaths = []
    round_num, actor, action, recent_death = 0, None, None, None

    for ev in r.events:
        kind = ev[0]
        if kind == replay.ROUND_START:
            round_num, recent_death = ev[1], None
            if round_num in (400, 450, 499):
                snapshots[round_num] = {did: len(body) for did, body in bodies.items()}
        elif kind == replay.TURN_START:
            actor, action, recent_death = ev[1], None, None
        elif kind == replay.DRAGON_ACTION:
            action = ev[2]
        elif kind == replay.DRAGON_DEATH:
            did = ev[1]
            body = bodies.pop(did, [])
            recent_death = (did, teams.get(did), set(body))
            deaths.append((round_num, did, teams.get(did), ev[2], len(body)))
        elif kind == replay.TILE_CHANGE:
            cell = (ev[1], ev[2])
            if ev[3]:
                if cell in origins:
                    counts["origin_overwrites"] += 1
                if recent_death and cell in recent_death[2]:
                    origins[cell] = ("corpse", recent_death[1], recent_death[0], round_num)
                    counts["corpse_pearls_created"] += 1
                else:
                    origins[cell] = ("spawn", None, None, round_num)
                    counts["spawn_pearls_created"] += 1
                    if recent_death:
                        counts["true_after_death_not_in_body"] += 1
            else:
                origin = origins.pop(cell, ("unknown", None, None, None))
                if actor not in bodies or not action or action[0] != "move":
                    counts["consumption_without_moving_actor"] += 1
                consumed.append((round_num, actor, teams.get(actor), cell, *origin))
                counts["pearls_eaten"] += 1
                counts["eaten_" + origin[0]] += 1
        elif kind == replay.DRAGON_UPDATE:
            did, head, tail = ev[1], ev[3], ev[4]
            body = bodies.get(did)
            if body is None:
                continue
            if body[0] != head:
                body.insert(0, head)
            if tail in body:
                del body[len(body) - body[::-1].index(tail):]
            recent_death = None
        elif kind == replay.DRAGON_SPLIT:
            _, parent, child, team, _, pbody, cbody = ev
            bodies[parent], bodies[child] = list(pbody), list(cbody)
            teams[child] = team
            recent_death = None

    death_reason = {did: why for _, did, _, why, _ in deaths}
    result = {"map": r.map_name, "winner": r.result.get("winner"),
              "round_limit": r.result.get("end_reason") == "round_limit",
              "teams": {}, "checks": dict(counts)}
    for team in "AB":
        alive = [(len(body), did) for did, body in bodies.items() if teams[did] == team]
        if not alive:
            result["teams"][team] = {"final_king": None, "final_longest": 0}
            continue
        length, king = max(alive, key=lambda row: (row[0], -row[1]))
        late = [x for x in consumed if x[0] >= 400 and x[1] == king]
        source_counts = Counter("own_corpse" if x[4] == "corpse" and x[5] == team else
                                "enemy_corpse" if x[4] == "corpse" else x[4] for x in late)
        team_late = [x for x in consumed if x[0] >= 400 and x[2] == team]
        team_own_corpse = sum(x[4] == "corpse" and x[5] == team for x in team_late)
        result["teams"][team] = {
            "final_king": king, "final_longest": length,
            "king_length_r400_r450_r499": [snapshots.get(t, {}).get(king, 0) for t in (400, 450, 499)],
            "king_late_pearls": dict(source_counts),
            "king_late_total": len(late),
            "king_late_own_corpse_fraction": (source_counts["own_corpse"] / len(late) if late else None),
            "king_late_own_no_action_corpse": sum(
                x[4] == "corpse" and x[5] == team and death_reason.get(x[6]) == "A"
                for x in late),
            "team_late_own_corpse_eaten": team_own_corpse,
            "team_late_total_eaten": len(team_late),
            "late_self_or_no_action_deaths": sum(d[0] >= 400 and d[2] == team and d[3] in ("S", "A")
                                                 for d in deaths),
        }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("replays", nargs="+", type=Path)
    args = parser.parse_args()
    for path in args.replays:
        result = trace(replay.load(path))
        print(json.dumps({"replay": str(path), **result}, ensure_ascii=False))


if __name__ == "__main__":
    main()
