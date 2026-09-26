"""Descriptive newborn survival from recorded games; not a policy comparison."""

import argparse
import json
from collections import Counter
from pathlib import Path

from . import arena, audit_jobs, population, replay


def count_births(events, team):
    counts, children = Counter(), {}
    rnd, current = 0, None
    for ev in events:
        if ev[0] == replay.ROUND_START:
            rnd, current = ev[1], None
        elif ev[0] == replay.TURN_START:
            current = ev[1]
            if current in children:
                children[current]["turns"] += 1
                counts["newborn_first_turns"] += children[current]["turns"] == 1
        elif ev[0] == replay.DRAGON_SPLIT and ev[3] == team:
            assert ev[2] not in children
            children[ev[2]] = {"round": rnd, "turns": 0, "dead": False}
            counts["births"] += 1
            counts[f"child_length_{len(ev[6])}"] += 1
        elif ev[0] == replay.DRAGON_DEATH and ev[1] in children:
            child = children[ev[1]]
            assert not child["dead"]
            child["dead"] = True
            counts["child_deaths"] += 1
            if child["turns"] == 0:
                counts["deaths_before_first_turn"] += 1
            if child["turns"] == 1 and current == ev[1]:
                counts["first_own_turn_deaths"] += 1
                counts[f"first_own_turn_death_{ev[2]}"] += 1
            if rnd == child["round"]:
                counts["birth_round_deaths"] += 1
            if rnd - child["round"] < 5:
                counts["deaths_before_age5"] += 1
    counts["children_alive_at_end"] = sum(not c["dead"] for c in children.values())
    counts["children_without_first_turn_at_end"] = sum(not c["dead"] and not c["turns"] for c in children.values())
    return counts


def one_game(args):
    game, botpath, mapfile = args
    name = Path(botpath).name
    team = "A" if game["bot_a"] == name else "B"
    r = replay.load(game["replay"])
    audit_jobs.verify_map(mapfile, r.map_text)
    assert r.result["winner"] == game["winner"]
    counts = count_births(r.events, team)
    counts["games"] = 1
    return dict(counts), {}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("experiment", type=Path)
    p.add_argument("--candidate", default="control_450")
    p.add_argument("--opponent", default="reference_v2")
    p.add_argument("--workers", type=int, default=4, choices=range(1, 9))
    args = p.parse_args()
    out = args.experiment
    games = [json.loads(l) for l in (out / "validation/games.jsonl").read_text().splitlines()]
    games = [g for g in games if args.candidate in (g["bot_a"], g["bot_b"])
             and args.opponent in (g["bot_a"], g["bot_b"])]
    assert games and not any(arena.is_error(g) for g in games)
    assert not arena.check_hashes(games, json.loads((out / "validation/run.json").read_text()))
    maps = {p.stem: p for p in (out / "maps").glob("*.map")}
    folder = out / ("split-mortality-" + args.candidate)
    folder.mkdir(exist_ok=True)
    tasks = [(g, str(out / "bots" / args.candidate), str(maps[g["map"]])) for g in games]
    counts, _ = audit_jobs.run(tasks, args.workers, folder, one_game, "split mortality")
    result = {"candidate": args.candidate, "opponent": args.opponent, "counts": dict(counts),
              "first_own_turn_death_rate": counts["first_own_turn_deaths"] / counts["newborn_first_turns"]
              if counts["newborn_first_turns"] else None,
              "limits": "Descriptive survival, not causal evidence that postponing splits helps. "
                        "Deaths before age 5 are a count, not a survival-rate estimate: end-of-game censoring applies."}
    population.write_json(folder / "summary.json", result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
