"""Per-map, per-opponent paired outcomes for a full bot-change screen."""

import argparse
import json
from pathlib import Path


def render(games, candidate, opponents, maps):
    lines = [f"# {candidate}: every official map, both sides", "",
             "Each cell is candidate W-D-L across its two sides. A 1-0-1 cell",
             "may reflect side advantage rather than a policy improvement.", "",
             "| map | " + " | ".join(opponents) + " |",
             "|---|" + "---|" * len(opponents)]
    for name in maps:
        cells = []
        for opponent in opponents:
            rows = [g for g in games if g["map"] == name and
                    candidate in (g["bot_a"], g["bot_b"]) and
                    opponent in (g["bot_a"], g["bot_b"])]
            if len(rows) != 2 or {g["bot_a"] == candidate for g in rows} != {True, False}:
                raise ValueError(f"missing map/side pair: {name} vs {opponent}")
            w = l = d = 0
            for game in rows:
                side = "A" if game["bot_a"] == candidate else "B"
                w += game["winner"] == side
                l += game["winner"] not in (side, None)
                d += game["winner"] is None
            cells.append(f"{w}-{d}-{l}")
        lines.append("| " + name + " | " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", type=Path)
    args = parser.parse_args()
    plan = json.loads((args.experiment / "plan.json").read_text())
    games = [json.loads(line) for line in
             (args.experiment / "full/games.jsonl").read_text().splitlines()]
    text = render(games, "candidate", list(plan["opponent_sources"]),
                  [Path(p).stem for p in plan["maps"]])
    target = args.experiment / "map_matrix.md"
    with target.open("x", encoding="utf8") as f:
        f.write(text)
    print(target)


if __name__ == "__main__":
    main()
