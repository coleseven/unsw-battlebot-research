"""Compare actual action streams, not replay CPU-point metadata, to control."""

import argparse
import json
from pathlib import Path

from . import analyze, replay
from .paths import ROOT

OLD = ROOT / "results/20260924-233609-full-change-bb86e5/full/replays"


def actions(rep):
    return [(ev[1], ev[2]) for ev in rep.events if ev[0] == replay.DRAGON_ACTION]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("probe", type=Path)
    args = parser.parse_args()
    games = [json.loads(line) for line in
             (args.probe / "diagnostic/games.jsonl").read_text().splitlines()]
    rows = []
    for game in games:
        side_a = game["bot_a"] == "portal_push"
        old = OLD / (("candidate-vs-nicked" if side_a else "nicked-vs-candidate") +
                     f"-{game['map']}-s53001.replay")
        new = ROOT / game["replay"]
        original_actions = actions(replay.load(old))
        candidate_actions = actions(replay.load(new))
        first = next((i for i, pair in enumerate(zip(original_actions, candidate_actions))
                      if pair[0] != pair[1]), None)
        old_stats = analyze.game_stats(old.read_bytes())
        new_stats = analyze.game_stats(new.read_bytes())
        side = "A" if side_a else "B"
        rows.append({"map": game["map"], "side": side,
                     "changed_actions": first is not None or
                     len(original_actions) != len(candidate_actions),
                     "first_changed_action_index": first,
                     "old_portal_steps": old_stats["teams"][side]["portal_steps"],
                     "new_portal_steps": new_stats["teams"][side]["portal_steps"],
                     "old_pearls": old_stats["teams"][side]["pearls"],
                     "new_pearls": new_stats["teams"][side]["pearls"],
                     "winner": game["winner"]})
    result = {"games": rows,
              "changed_action_games": sum(r["changed_actions"] for r in rows)}
    target = args.probe / "behavior.json"
    with target.open("x", encoding="utf8") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
