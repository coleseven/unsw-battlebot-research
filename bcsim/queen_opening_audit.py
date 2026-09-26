"""Read-only first-50-round founder audit for local Queen replays."""

import argparse
from collections import defaultdict
from pathlib import Path

from . import reconstruct, replay


def audit(path):
    r = replay.load(path)
    board = reconstruct.Board(r.map_text)
    own = "A" if path.name.startswith(("candidate-vs-", "queen_opening-vs-")) else "B"
    founders = {i: list(body)[0] for i, (team, body) in enumerate(board.dragons)
                if team == own}
    positions = defaultdict(list)
    actions = defaultdict(list)
    splits = defaultdict(list)
    round_no = -1
    for ev in r.events:
        if ev[0] == replay.ROUND_START:
            round_no = ev[1]
        if round_no > 50:
            break
        if ev[0] == replay.DRAGON_ACTION and ev[1] in founders:
            actions[ev[1]].append((round_no, ev[2]))
        elif ev[0] == replay.DRAGON_UPDATE and ev[1] in founders:
            positions[ev[1]].append((round_no, ev[3]))
        elif ev[0] == replay.DRAGON_SPLIT and ev[1] in founders:
            splits[ev[1]].append((round_no, ev[2]))
    print(path.name, "own", own)
    for did, initial in founders.items():
        locs = positions[did]
        print("founder", did, "initial", initial, "unique", len(set(p for _, p in locs)),
              "splits", splits[did])
        print(" positions", [(r, p) for r, p in locs if r % 5 == 0][:11])
        print(" actions", actions[did][:18])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("replays", nargs="+", type=Path)
    args = parser.parse_args()
    for path in args.replays:
        audit(path)
