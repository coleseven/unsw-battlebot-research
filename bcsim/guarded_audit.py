"""Replay/action fidelity and sampled judge-budget checks for guarded policies."""

import argparse
import json
import os
from collections import Counter
from pathlib import Path

from . import arena, audit_jobs, population, reconstruct, replay
from .match import InProcessBot, _seed_for
from .paths import ROOT, bot_hash


def one_game(args):
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
        globs = brain.turn.__func__.__globals__
        helper = globs["guarded_safety"]
        obs = helper.bc.Obs(t.block)
        # The exact wrapper sequence, without Brain.step's exception fallback.
        # Any hidden strategy exception therefore invalidates this audit.
        original = globs["baseline_brain"].Brain.turn(brain, obs)
        actual = helper.choose(obs, team, original, name)
        kind, value = actual.split()
        assert (kind.lower(), int(value) if kind == "SPLIT" else value) == t.action
        counts["verified_candidate_turns"] += 1
        counts["overrides"] += original != actual
        counts["splits"] += kind == "SPLIT"
        metrics = {"long": obs.length, "dense": sum(p is not None for p in obs.occ),
                   "enemy_heads": len(obs.enemy_heads(team)),
                   "override": int(actual != original) * 100 + obs.length if actual != original else -1,
                   "complete_body": obs.length if helper.own_body(obs) is not None else -1}
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
    tasks = []
    maps = {Path(p).stem: p for p in plan["official_maps"] + plan["stress_maps"]}
    for stage in ("validation", "stress"):
        games = [json.loads(s) for s in (out / stage / "games.jsonl").read_text().splitlines()]
        prov = json.loads((out / stage / "run.json").read_text())
        assert not arena.check_hashes(games, prov)
        expected = 864 if stage == "validation" else 48
        assert len(games) == expected and not any(arena.is_error(g) for g in games)
        assert len({(g["map"], g["seed"], g["bot_a"], g["bot_b"]) for g in games}) == expected
        tasks += [(g, str(botpath) if botpath.name in (g["bot_a"], g["bot_b"]) else None,
                   maps[g["map"]]) for g in games]
    counts, samples = audit_jobs.run(tasks, workers, out, one_game, "movement audit")
    population.write_json(out / "replay-audit.json", {"counts": dict(counts), "hash": bot_hash(botpath),
                                                    "samples": samples})
    print(json.dumps(dict(counts), indent=2), flush=True)


def budget(out, names=None):
    if names is None:
        selection = json.loads((out / "selection.json").read_text())
        names = ("control_450", selection["selected"])
    audit_result = json.loads((out / "replay-audit.json").read_text())
    previous = ROOT / "results/20260922-173739-movement-659d1f/budget-inputs.json"
    inputs = json.loads(previous.read_text()) + [{"category": k, **v} for k, v in audit_result["samples"].items()]
    os.environ["UNSWBC_WARM"] = "1"
    from unswbc.sandbox import SandboxPool, SandboxBot
    rows = []
    for name in names:
        path = out / "bots" / name
        print(f"sandbox: {name}, {len(inputs)} cold/warm observations", flush=True)
        pool = SandboxPool(["python", "main.py"], cwd=str(path.resolve()), team="a")
        try:
            for sample in inputs:
                bot = SandboxBot(pool, init=sample["init"].encode(), name=str(sample["id"]))
                try:
                    for phase in ("cold", "warm"):
                        output = bot.ask(sample["block"].encode()).decode()
                        points, memory = bot.live
                        row = {"bot": name, "category": sample["category"], "phase": phase,
                               "points": points, "memory_bytes": memory, "error": bot.error, "output": output}
                        rows.append(row)
                        print(f"{name} {sample['category']} {phase}: {points} points, {memory} bytes", flush=True)
                finally:
                    bot.stop()
        finally:
            pool.close()
    summary = {}
    for name in names:
        r = [row for row in rows if row["bot"] == name]
        summary[name] = {"turns": len(r), "max_points": max(x["points"] for x in r),
                         "max_memory_bytes": max(x["memory_bytes"] for x in r),
                         "failures": sum(bool(x["error"]) or "crash" in x["output"] or
                                         not x["output"].startswith(("MOVE ", "SPLIT ")) for x in r)}
    population.write_json(out / "budget-inputs.json", inputs)
    population.write_json(out / "budget.json", {"summary": summary, "turns": rows,
                           "limits": "Sampled cold/warm turns, not a full-game or worst-case guarantee."})
    print(json.dumps(summary, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", type=Path)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--budget", action="store_true")
    args = parser.parse_args()
    if args.budget:
        budget(args.experiment)
    else:
        audit(args.experiment, args.workers)


if __name__ == "__main__":
    main()
