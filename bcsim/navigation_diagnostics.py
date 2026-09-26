"""Post-hoc, matched case study of the strongest and weakest navigation maps."""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from . import audit_jobs, population, reconstruct, replay
from .match import InProcessBot, _seed_for
from .paths import bot_hash


def one_game(args):
    game, botpath, mapfile = args
    r = replay.load(game["replay"])
    audit_jobs.verify_map(mapfile, r.map_text)
    board = reconstruct.Board(r.map_text)
    name = Path(botpath).name
    team = "A" if game["bot_a"] == name else "B"
    loader, brains, counts = InProcessBot(Path(botpath)), {}, Counter(games=1)
    rnd, current, immediate_deaths = 0, None, set()
    for ev in r.events:
        if ev[0] == replay.ROUND_START:
            rnd, current = ev[1], None
        elif ev[0] == replay.TURN_START:
            current = ev[1]
        elif ev[0] == replay.DRAGON_DEATH and current == ev[1]:
            immediate_deaths.add((rnd, current))
    for t in reconstruct.turns(r):
        if t.team != team:
            continue
        init = f"ID {t.id}\nTEAM {team}\nMAP {board.w} {board.h}\nUNIT_LIMIT 64\n"
        if t.id not in brains:
            brains[t.id] = loader.new_brain(init, _seed_for(game["seed"], team, t.id))
        brain = brains[t.id]
        globs = brain.turn.__func__.__globals__
        obs = globs["bc"].Obs(t.block)
        # The frozen wrapper's exact three operations, exposing its baseline
        # action without a second RNG draw or a counterfactual full game.
        brain.memory.update(obs)
        original = globs["baseline_brain"].Brain.turn(brain, obs)
        actual = brain.memory.choose(obs, team, original)
        kind, value = actual.split()
        assert (kind.lower(), int(value) if kind == "SPLIT" else value) == t.action
        counts["verified_candidate_turns"] += 1
        if actual == original:
            continue
        assert kind == "MOVE" and len(value) == 1
        counts["overrides"] += 1
        counts["late_overrides"] += obs.round >= 450
        counts["override_own_turn_deaths"] += (t.round, t.id) in immediate_deaths
        nav = globs["navigation"]
        good = {d for d, score in nav.tactics.safe_moves(obs, team).items() if score > -10}
        paths = obs.bfs()
        food = any(paths[k][1] in good for _, k in nav.tactics.pearl_targets(obs, paths))
        counts["overrides_with_baseline_food_route"] += food
        counts["overrides_without_baseline_food_route"] += not food
        portal = obs.edge(24, value) >= 0
        counts["immediate_portal_overrides"] += portal
        if portal:
            dest = brain.memory.destination(obs.y[24]*board.w+obs.x[24], value)
            counts["hidden_immediate_portal_exits"] += dest not in brain.memory.visible
    return dict(counts), {}


def main(out, workers):
    plan = json.loads((out / "plan.json").read_text())
    candidate = out / "bots/portal_memory"
    assert bot_hash(candidate) == plan["candidate_hashes"][candidate.name]
    maps = {Path(p).stem: p for p in plan["maps"]}
    games = [json.loads(l) for l in (out / "validation/games.jsonl").read_text().splitlines()]
    games = [g for g in games if candidate.name in (g["bot_a"], g["bot_b"])
             and any(n in (g["bot_a"], g["bot_b"]) for n in ("reference_v2", "hunter"))
             and (g["map"].startswith("queen_of_spades_") or g["map"].startswith("default_"))
             and not g["map"].startswith("default_small_") and g["seed"] == plan["validation_seeds"][0]]
    assert len(games) == 8
    folder = out / "case-study"
    folder.mkdir(exist_ok=True)
    population.write_json(folder / "plan.json", {"games": games,
                          "limits": "Post-hoc eight-game case study, chosen from best/worst maps; not representative or causal, not tuning data."})
    tasks = [(g, str(candidate), maps[g["map"]]) for g in games]
    audit_jobs.run(tasks, workers, folder, one_game, "navigation case study")
    lookup = {str(Path(g["replay"]).resolve()): g["map"] for g in games}
    by_map = defaultdict(Counter)
    for line in (folder / "audit-progress.jsonl").read_text().splitlines():
        row = json.loads(line)
        by_map[lookup[row["key"]]].update(row["counts"])
    result = {"maps": {m: dict(c) for m, c in by_map.items()},
              "limits": "Baseline action on visited states is not a counterfactual game outcome. No strategy changes from these validation cases."}
    population.write_json(folder / "summary.json", result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("experiment", type=Path)
    p.add_argument("--workers", type=int, choices=range(1, 9), default=2)
    args = p.parse_args()
    main(args.experiment, args.workers)
