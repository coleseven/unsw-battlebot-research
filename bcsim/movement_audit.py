"""Diagnose the saved baseline's losses without replaying/tuning matches."""

import argparse
import json
from collections import Counter
from pathlib import Path

from . import arena, replay, reconstruct
from .match import InProcessBot
from .paths import ROOT, bot_hash, map_signature, file_hash


def audit(prior, bot="stop_450"):
    games = [json.loads(s) for s in (prior / "holdout/games.jsonl").read_text().splitlines()]
    losses = [g for g in games if bot in (g["bot_a"], g["bot_b"]) and arena.score_for(g, bot) == 0]
    loader = InProcessBot(prior / "bots" / bot)
    brain = loader.new_brain("ID 0\nTEAM A\nMAP 16 16\nUNIT_LIMIT 64\n", 0)
    bc = brain.turn.__func__.__globals__["movement"].bc
    tactics = brain.turn.__func__.__globals__["movement"].tactics
    counts = Counter()
    examples = []
    for g in losses:
        r = replay.load(g["replay"])
        team = "A" if g["bot_a"] == bot else "B"
        current, rnd, direct = None, 0, {}
        for ev in r.events:
            if ev[0] == replay.ROUND_START:
                rnd = ev[1]
            elif ev[0] == replay.TURN_START:
                current = ev[1]
            elif ev[0] == replay.DRAGON_DEATH and ev[1] == current:
                direct[rnd, current] = ev[2]
        for t in reconstruct.turns(r):
            if t.team != team:
                continue
            counts["team_turns_in_lost_games"] += 1
            cause = direct.get((t.round, t.id))
            if cause is None:
                continue
            obs = bc.Obs(t.block)
            safe = tactics.safe_moves(obs, team)
            counts["own_turn_deaths"] += 1
            counts[f"cause_{cause}"] += 1
            group = "no_static_legal_move" if not safe else "only_risky_moves" if max(safe.values()) <= -10 else "has_heuristically_safe_move"
            counts[group] += 1
            if len(examples) < 12:
                examples.append({"map": g["map"], "round": t.round, "id": t.id,
                                 "action": t.action, "length": obs.length, "cause": cause,
                                 "single_step_scores": safe})
    return {"lost_matches": len(losses), "counts": dict(counts), "examples": examples,
            "limits": "only own-turn deaths in losing matches; no population exposure normalization; "
                      "static safety is a heuristic, not proof of avoidability"}


def verify(experiment):
    """Audit frozen identities, replay standings, action mix and sprint deaths."""
    plan = json.loads((experiment / "plan.json").read_text())
    assert bot_hash(Path(plan["baseline_path"])) == plan["baseline_hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_bot_hash"]
    assert file_hash(ROOT / "bcsim/paths.py") == plan["map_identity_hash"]
    a = {map_signature(Path(p)) for p in plan["screen_maps"]}
    b = {map_signature(Path(p)) for p in plan["holdout_maps"]}
    assert len(a) == 4 and len(b) == 5 and not a & b
    for stage, expected in (("screen", 144), ("holdout", 360)):
        games = [json.loads(s) for s in (experiment / stage / "games.jsonl").read_text().splitlines()]
        prov = json.loads((experiment / stage / "run.json").read_text())
        assert len(games) == expected and not arena.check_hashes(games, prov)
        assert not any(arena.is_error(g) for g in games)
        assert len({(g["bot_a"], g["bot_b"], g["map"], g["seed"]) for g in games}) == expected
    totals = {p: Counter() for p in plan["variants"]}
    for index, g in enumerate(games):
        r = replay.load(g["replay"])
        assert r.result["winner"] == g["winner"]
        for side in ("a", "b"):
            assert r.result[side]["longest"] == g[f"{side}_longest"]
            assert r.result[side]["total"] == g[f"{side}_length"]
        focus = next(p for p in totals if p in (g["bot_a"], g["bot_b"]))
        target = "A" if g["bot_a"] == focus else "B"
        teams = {i: t for i, (t, _) in enumerate(reconstruct.Board(r.map_text).dragons)}
        counts = totals[focus]
        counts["games"] += 1
        active, sprinting = None, False
        for ev in r.events:
            if ev[0] == replay.TURN_START:
                active, sprinting = ev[1], False
            elif ev[0] == replay.DRAGON_SPLIT:
                teams[ev[2]] = ev[3]
            elif ev[0] == replay.DRAGON_ACTION and teams.get(ev[1]) == target:
                counts["actions"] += 1
                assert not ev[4] and not ev[5]
                action = ev[2]
                if action and action[0] == "move":
                    n = len(action[1])
                    assert n <= (2 if focus == "sprint" else 1)
                    counts["sprints" if n > 1 else "single_moves"] += 1
                    counts["requested_sprint_cost"] += n - 1
                    sprinting = n > 1
                elif action and action[0] == "split":
                    counts["splits"] += 1
            elif ev[0] == replay.DRAGON_DEATH and teams.get(ev[1]) == target:
                counts["dragon_deaths"] += 1
                counts[f"deaths_{ev[2]}"] += 1
                if ev[1] == active and sprinting:
                    counts["own_turn_sprint_deaths"] += 1
        if (index + 1) % 60 == 0:
            print(f"verified {index + 1}/{len(games)} replays", flush=True)
    assert totals["sprint"]["own_turn_sprint_deaths"] == 0
    assert all(c["deaths_A"] == 0 for c in totals.values())
    result = {"verified_replays": len(games), "maps_disjoint": True, "originals_unchanged": True,
              "counts": {p: dict(c) for p, c in totals.items()}}
    from .population import write_json
    write_json(experiment / "replay-audit.json", result)
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("prior", type=Path)
    p.add_argument("--verify", action="store_true")
    args = p.parse_args()
    print(json.dumps(verify(args.prior) if args.verify else audit(args.prior), indent=2))
