"""Audit hotspot presence and survival in a frozen v5 experiment directory."""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from . import analyze, reconstruct, replay
from .paths import ROOT

sys.path.insert(0, str(ROOT / "framework"))
import bc  # noqa: E402

HOT = {"A": {(11, y) for y in range(10, 15)} | {(12, 14)},
       "B": {(36, y) for y in range(9, 14)} | {(35, 9)}}


def near(point, group):
    x, y = point
    return min(abs(x - px) + abs(y - py) for px, py in group) <= 2


def one(game):
    path = Path(game["replay"])
    if not path.is_absolute():
        path = ROOT / path
    blob = path.read_bytes()
    rep = replay.decode(blob)
    g = analyze.game_stats(blob)
    rounds = defaultdict(set)
    visitors = defaultdict(set)
    exact_turns = defaultdict(int)
    first = {}
    first_exact = {}
    hotspot_splits = defaultdict(int)
    for turn in reconstruct.turns(rep):
        if g["size"] != [48, 24]:
            break
        obs = bc.Obs(turn.block)
        if near(obs.head, HOT[turn.team]):
            rounds[turn.team].add(turn.round)
            visitors[turn.team].add(turn.id)
            first[turn.team] = min(first.get(turn.team, turn.round), turn.round)
        if obs.head in HOT[turn.team]:
            exact_turns[turn.team] += 1
            first_exact[turn.team] = min(first_exact.get(turn.team, turn.round),
                                         turn.round)
            hotspot_splits[turn.team] += bool(turn.action and turn.action[0] == "split")
    return {
        "map": game["map"], "bots": [game["bot_a"], game["bot_b"]],
        "winner": game["winner"],
        "teams": {side: {
            "first_near_hotspot": first.get(side),
            "rounds_near_hotspot": len(rounds[side]),
            "distinct_visitors": len(visitors[side]),
            "head_turns_on_fast_tiles": exact_turns[side],
            "first_on_fast_tile": first_exact.get(side),
            "splits_on_fast_tiles": hotspot_splits[side],
            "pearls": g["teams"][side]["pearls"],
            "portal_steps": g["teams"][side]["portal_steps"],
            "deaths": g["teams"][side]["deaths"],
            "final": g["teams"][side]["final"],
        } for side in "AB"},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", type=Path)
    args = parser.parse_args()
    games = [json.loads(line) for line in
             (args.experiment / "vs-additive/games.jsonl").read_text().splitlines()]
    selected = [g for g in games if g["map"] in ("Trauma", "stronghold")]
    print(json.dumps([one(g) for g in selected], indent=2), flush=True)


if __name__ == "__main__":
    main()
