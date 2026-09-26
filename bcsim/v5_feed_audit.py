"""Count deliberate local-feed activations and final king sizes in replay pairs."""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from . import feed_trace, reconstruct, replay
from .paths import ROOT

sys.path.insert(0, str(ROOT / "framework"))
import bc  # noqa: E402
import v5_feeding  # noqa: E402


def audit_game(game):
    path = Path(game["replay"])
    if not path.is_absolute():
        path = ROOT / path
    rep = replay.load(path)
    counts = Counter()
    candidate_team = "A" if game["bot_a"] == "feed_king" else "B"
    for turn in reconstruct.turns(rep):
        if turn.team != candidate_team or turn.round < 400:
            continue
        obs = bc.Obs(turn.block)
        predicted = v5_feeding.should_feed(obs, turn.team, turn.id)
        if predicted:
            counts["feed_predicate_true"] += 1
            if turn.action is None:
                counts["feed_no_action"] += 1
            elif turn.action == ("suicide",):
                counts["feed_suicide"] += 1
        if turn.action is None:
            counts["all_no_action"] += 1
    stats = feed_trace.trace(rep)["teams"][candidate_team]
    return {"map": game["map"], "candidate_team": candidate_team,
            "winner": game["winner"], "counts": dict(counts),
            "final_longest": stats["final_longest"],
            "final_king_late_own_corpse": stats["king_late_pearls"].get("own_corpse", 0),
            "team_late_own_corpse_eaten": stats["team_late_own_corpse_eaten"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", type=Path)
    parser.add_argument("--stage", default="vs-king")
    args = parser.parse_args()
    games = [json.loads(line) for line in
             (args.experiment / args.stage / "games.jsonl").read_text().splitlines()]
    rows = [audit_game(game) for game in games]
    print(json.dumps({"rows": rows,
                      "totals": dict(sum((Counter(row["counts"]) for row in rows), Counter()))},
                     indent=2))


if __name__ == "__main__":
    main()
