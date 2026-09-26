"""Reproduce observed games to audit trap overrides; not additional evidence."""

import json
from collections import Counter, defaultdict

from . import arena, bounded, population, reconstruct, replay
from .match import InProcessBot, _seed_for
from .paths import RESULTS

PRIOR = RESULTS / "20260922-175423-trap-followup-a1e642"


def inspect_game(game, root):
    r = replay.load(game["replay"])
    board = reconstruct.Board(r.map_text)
    team = "A" if game["bot_a"] == "trap" else "B"
    loader = InProcessBot(root / "bots/trap")
    brains = {}
    counts, examples = Counter(), []
    for turn in reconstruct.turns(r):
        if turn.team != team:
            continue
        if turn.id not in brains:
            init = f"ID {turn.id}\nTEAM {team}\nMAP {board.w} {board.h}\nUNIT_LIMIT 64\n"
            brains[turn.id] = loader.new_brain(init, _seed_for(game["seed"], team, turn.id))
        brain = brains[turn.id]
        globs = brain.turn.__func__.__globals__
        helper = globs["local_safety"]
        obs = helper.bc.Obs(turn.block)
        # Call the underlying baseline once, exactly as the wrapper did live.
        original = globs["baseline_brain"].Brain.turn(brain, obs)
        actual = helper.choose(obs, team, original, "trap")
        kind, value = actual.split()
        assert (kind.lower(), int(value) if kind == "SPLIT" else value) == turn.action
        counts["turns"] += 1
        if kind != "MOVE":
            counts["splits"] += 1
            continue
        counts["moves"] += 1
        counts["pearl_moves"] += bool(obs.pearl[obs.step(24, value)])
        if actual == original:
            continue
        counts["overrides"] += 1
        view = helper.View(obs, team)
        old, new = view.profile(original.split()[1]), view.profile(value)
        counts["old_illegal"] += old is None
        if old is not None:
            counts["depth_changed"] += old["depth"] != new["depth"]
            counts["room_only"] += old["depth"] == new["depth"] and (
                (obs.step(24, original.split()[1]) in view.danger) ==
                (obs.step(24, value) in view.danger))
            counts["avoided_head_threat"] += (obs.step(24, original.split()[1]) in view.danger and
                                              obs.step(24, value) not in view.danger)
            counts["new_head_threat"] += (obs.step(24, original.split()[1]) not in view.danger and
                                         obs.step(24, value) in view.danger)
            counts["both_shallow"] += old["depth"] < 3 and new["depth"] < 3
            counts["old_depth_full"] += old["depth"] == 3
            counts["gave_up_immediate_pearl"] += old["pearls"] > new["pearls"]
        counts["late_overrides"] += obs.round >= 450
        if len(examples) < 8:
            examples.append({"round": turn.round, "id": turn.id, "length": obs.length,
                             "original": original, "actual": actual, "old": old, "new": new,
                             "block": turn.block})
    return {"map": game["map"], "seed": game["seed"], "team": team,
            "score": arena.score_for(game, "trap"), "counts": dict(counts), "examples": examples}


def main():
    out = PRIOR / "diagnostics"
    maps = [PRIOR / "maps" / f"{m}.map" for m in ("arena", "arena_pockets", "arena_slow_food")]
    jobs = population.jobs_for([PRIOR / "bots/trap"], [PRIOR / "bots/control_450"],
                              maps, range(6000, 6003), out / "replays")
    games = bounded.run(jobs, 6, out, "diagnostic replay")
    prior_games = [json.loads(l) for l in (PRIOR / "games.jsonl").read_text().splitlines()]
    identity = lambda g: (g["map"], g["seed"], g["bot_a"], g["bot_b"])
    previous = {identity(g): g for g in prior_games}
    for g in games:
        for key in ("winner", "rounds", "a_longest", "b_longest", "a_length", "b_length", "hash_a", "hash_b"):
            assert g[key] == previous[identity(g)][key], key
    rows, totals = [], defaultdict(Counter)
    for i, g in enumerate(games):
        row = inspect_game(g, PRIOR)
        rows.append(row)
        totals[g["map"]].update(row["counts"])
        print(f"audited {i + 1}/{len(games)} replays", flush=True)
    result = {"totals": {m: dict(c) for m, c in totals.items()}, "games": rows,
              "limits": "First three previously used seeds per map, same games reproduced. "
                        "Descriptive action audit only; no causal attribution to individual overrides."}
    population.write_json(out / "audit.json", result)
    print(json.dumps(result["totals"], indent=2), flush=True)


if __name__ == "__main__":
    main()
