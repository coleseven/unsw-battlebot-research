"""Time-averaged team-length margins from decoded Battlecode replays.

Usage:
    python -m bcsim.margin RESULT_DIR --opponent nicked --out PATH

The sampled trajectory is rounds 10, 20, ..., 500. After an elimination,
remaining samples have margin +1/-1; round-limit games carry their final
round-499 position to sample 500.
"""

import argparse
import json
import statistics
from pathlib import Path

from . import analyze
from .paths import ROOT


SAMPLES = range(10, 501, 10)


def share(ours, theirs):
    return (ours - theirs) / max(1, ours + theirs)


def game_margin(stats, side):
    """Return the v6 objective and diagnostics for one replay and one side."""
    if side not in ("A", "B"):
        raise ValueError(side)
    other = "B" if side == "A" else "A"
    timeline = {row["round"]: row for row in stats["timeline"]}
    final = stats["timeline"][-1]
    end_round = final["round"]
    margins = []
    for round_no in SAMPLES:
        if round_no in timeline:
            row = timeline[round_no]
            value = share(row[side][1], row[other][1])
        elif round_no > end_round and stats["end"] == "eliminated" and stats["winner"] in ("A", "B"):
            value = 1.0 if stats["winner"] == side else -1.0
        elif round_no > end_round:
            value = share(final[side][1], final[other][1])
        else:
            raise ValueError(f"missing timeline sample {round_no}")
        margins.append(value)
    outcome = 1.0 if stats["winner"] == side else 0.0 if stats["winner"] not in ("A", "B") else -1.0
    if stats["end"] == "eliminated" and stats["winner"] in ("A", "B"):
        longest_share = outcome
    else:
        longest_share = share(final[side][2], final[other][2])
    margin = statistics.fmean(margins)
    return {
        "margin": margin,
        # Win-aligned objective. A round-500 game is decided by the longest
        # living dragon, then total length, so the total-length margin alone
        # disagreed with the result in 36 of 180 v7-base vs nicked games (26
        # wins with less total length, 10 losses with more). Half the result,
        # a quarter the final longest-dragon share, a quarter the (smoother)
        # time-averaged total-length margin.
        "aligned": 0.5 * outcome + 0.25 * longest_share + 0.25 * margin,
        "longest_share": longest_share,
        "final_share": share(final[side][1], final[other][1]),
        "final_longest_gap": final[side][2] - final[other][2],
        "elimination_round": end_round if stats["end"] == "eliminated" else None,
        "outcome": "win" if stats["winner"] == side else
                   "draw" if stats["winner"] not in ("A", "B") else "loss",
        "samples": len(margins),
    }


def result_dir(path, bot="candidate", opponent="nicked"):
    """Score every distinct map/side game from a frozen full-change result."""
    path = Path(path)
    games_path = path / "completed/games.jsonl"
    if not games_path.is_file():
        games_path = path / "full/games.jsonl"
    if not games_path.is_file():
        raise FileNotFoundError(games_path)
    games = [json.loads(line) for line in games_path.read_text(encoding="utf8").splitlines()]
    rows = []
    for game in games:
        if {game["bot_a"], game["bot_b"]} != {bot, opponent}:
            continue
        side = "A" if game["bot_a"] == bot else "B"
        replay_path = ROOT / game["replay"]
        stats = analyze.load_stats(("file", str(replay_path), None))
        row = {"map": game["map"], "side": side,
               **game_margin(stats, side)}
        rows.append(row)
    if not rows:
        raise ValueError(f"no {bot} versus {opponent} games in {games_path}")
    keys = [(row["map"].lower(), row["side"]) for row in rows]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate deterministic map/side pairing")
    by_map = {}
    for name in sorted(set(row["map"] for row in rows), key=str.lower):
        selected = [row for row in rows if row["map"] == name]
        if len(selected) != 2 or {row["side"] for row in selected} != {"A", "B"}:
            raise ValueError(f"missing side for {name}")
        by_map[name] = statistics.fmean(row["margin"] for row in selected)
    map_values = list(by_map.values())
    return {"bot": bot, "opponent": opponent, "games": len(rows),
            "mean_margin": statistics.fmean(map_values),
            "worst_map_margin": min(map_values),
            "F": statistics.fmean(map_values) + 0.25 * min(map_values),
            "map_margin": by_map,
            "games_detail": sorted(rows, key=lambda x: (x["map"].lower(), x["side"]))}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", type=Path)
    parser.add_argument("--bot", default="candidate")
    parser.add_argument("--opponent", default="nicked")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = result_dir(args.result, args.bot, args.opponent)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf8")
    print(json.dumps({k: v for k, v in report.items() if k != "games_detail"}, indent=2))
