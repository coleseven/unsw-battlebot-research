"""Verify complete fission validation replays and exact candidate decisions."""

import argparse
import json
import os
from collections import Counter
from pathlib import Path

from . import arena, audit_jobs, guarded_audit, population, reconstruct, replay
from .match import InProcessBot, _seed_for
from .paths import ROOT, bot_hash


def one_game(args, observer=None):
    game, botpath, mapfile = args
    r = replay.load(game["replay"])
    audit_jobs.verify_map(mapfile, r.map_text)
    assert r.result["winner"] == game["winner"]
    for side in ("a", "b"):
        assert r.result[side]["longest"] == game[f"{side}_longest"]
        assert r.result[side]["total"] == game[f"{side}_length"]
    counts = Counter(games=1)
    for ev in r.events:
        if ev[0] == replay.DRAGON_ACTION:
            assert not ev[4] and not ev[5]
        elif ev[0] == replay.DRAGON_DEATH:
            assert ev[2] != "A"
    if not botpath:
        return dict(counts), {}
    name = Path(botpath).name
    team = "A" if game["bot_a"] == name else "B"
    board = reconstruct.Board(r.map_text)
    loader = InProcessBot(Path(botpath))
    brains, samples = {}, {}
    for t in reconstruct.turns(r):
        if t.team != team:
            continue
        init = f"ID {t.id}\nTEAM {team}\nMAP {board.w} {board.h}\nUNIT_LIMIT 64\n"
        if t.id not in brains:
            brains[t.id] = loader.new_brain(init, _seed_for(game["seed"], team, t.id))
        brain = brains[t.id]
        obs = brain.turn.__func__.__globals__["bc"].Obs(t.block)
        actual = brain.turn(obs)  # deliberately bypass exception fallback
        kind, value = actual.split()
        assert (kind.lower(), int(value) if kind == "SPLIT" else value) == t.action
        counts["verified_candidate_turns"] += 1
        counts["splits"] += kind == "SPLIT"
        counts["late_splits"] += kind == "SPLIT" and obs.round >= 450
        if observer is not None:
            observer(brain, obs, actual, t, counts)
        metrics = {"long": obs.length, "dense": sum(p is not None for p in obs.occ),
                   "enemy_heads": len(obs.enemy_heads(team)), "population": obs.unit_count}
        for category, score in metrics.items():
            if category not in samples or score > samples[category]["score"]:
                samples[category] = {"score": score, "init": init, "id": t.id, "round": t.round,
                                     "block": t.block, "source": game["replay"]}
    return dict(counts), samples


def audit(out, workers):
    os.environ["RAYON_NUM_THREADS"] = "1"
    plan = json.loads((out / "plan.json").read_text())
    selection = json.loads((out / "selection.json").read_text())
    botpath = out / "bots" / selection["selected"]
    assert bot_hash(botpath) == selection["hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    maps = {Path(p).stem: p for p in plan["maps"]}
    games = [json.loads(s) for s in (out / "validation/games.jsonl").read_text().splitlines()]
    prov = json.loads((out / "validation/run.json").read_text())
    assert not arena.check_hashes(games, prov)
    assert len(games) == 864 and not any(arena.is_error(g) for g in games)
    assert len({(g["map"], g["seed"], g["bot_a"], g["bot_b"]) for g in games}) == 864
    tasks = [(g, str(botpath) if botpath.name in (g["bot_a"], g["bot_b"]) else None,
              maps[g["map"]]) for g in games]
    counts, samples = audit_jobs.run(tasks, workers, out, one_game, "fission audit")
    assert counts["late_splits"] == 0
    population.write_json(out / "replay-audit.json", {"counts": dict(counts), "hash": bot_hash(botpath),
                                                    "samples": samples})
    print(json.dumps(dict(counts), indent=2), flush=True)


def audit_transfer(out, workers):
    os.environ["RAYON_NUM_THREADS"] = "1"
    plan = json.loads((out / "plan.json").read_text())
    botpath = out / "bots" / Path(plan["source"]).name
    assert bot_hash(botpath) == plan["source_hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    maps = {Path(p).stem: p for p in plan["maps"]}
    games = [json.loads(s) for s in (out / "transfer/games.jsonl").read_text().splitlines()]
    prov = json.loads((out / "transfer/run.json").read_text())
    assert not arena.check_hashes(games, prov)
    expected = len(maps) * len(plan["seeds"]) * 2
    assert len(games) == expected and not any(arena.is_error(g) for g in games)
    assert len({(g["map"], g["seed"], g["bot_a"], g["bot_b"]) for g in games}) == expected
    tasks = [(g, str(botpath), maps[g["map"]]) for g in games]
    counts, samples = audit_jobs.run(tasks, workers, out, one_game, "transfer audit")
    assert counts["late_splits"] == 0
    population.write_json(out / "replay-audit.json", {"counts": dict(counts), "hash": bot_hash(botpath),
                                                    "samples": samples})
    print(json.dumps(dict(counts), indent=2), flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("experiment", type=Path)
    p.add_argument("--workers", type=int, default=6)
    p.add_argument("--budget", action="store_true")
    p.add_argument("--transfer", action="store_true")
    args = p.parse_args()
    if args.budget:
        guarded_audit.budget(args.experiment)
    elif args.transfer:
        audit_transfer(args.experiment, args.workers)
    else:
        audit(args.experiment, args.workers)
