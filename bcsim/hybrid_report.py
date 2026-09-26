"""Post-evaluation outcome and fixed-subset collision diagnostics; no tuning."""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from . import arena, population, reconstruct, replay


def collision_counts(game, name):
    r = replay.load(game["replay"])
    b = reconstruct.Board(r.map_text)
    teams = {i: t for i, (t, _) in enumerate(b.dragons)}
    side = "A" if game["bot_a"] == name else "B"
    counts = Counter(games=1)
    heads = []
    def finish():
        if heads:
            kinds = {teams[i] for i in heads}
            for did in heads:
                if teams[did] == side:
                    counts["friendly_head_deaths" if kinds == {side} else "enemy_head_deaths"] += 1
    for e in r.events:
        if e[0] in (replay.ROUND_START, replay.TURN_START):
            finish(); heads = []
        elif e[0] == replay.DRAGON_SPLIT:
            teams[e[2]] = e[3]
            if e[3] == side:
                counts["splits"] += 1
        elif e[0] == replay.DRAGON_ACTION and teams[e[1]] == side:
            counts["actions"] += 1
        elif e[0] == replay.DRAGON_DEATH:
            if e[2] == "H":
                heads.append(e[1])
            if teams[e[1]] == side:
                counts["deaths_" + e[2]] += 1
    finish()
    assert counts["friendly_head_deaths"] + counts["enemy_head_deaths"] == counts["deaths_H"]
    return counts


def run(out):
    plan = json.loads((out / "plan.json").read_text())
    comparison = json.loads((out / "comparison.json").read_text())
    games = [json.loads(l) for l in (out / "validation/games.jsonl").read_text().splitlines()]
    names = ["control_450"] + list(comparison)
    assert not arena.check_hashes(games, json.loads((out / "validation/run.json").read_text()))
    folder = out / "diagnostics"
    folder.mkdir()
    population.write_json(folder / "plan.json", {
        "subset": "All validation maps, first predeclared validation seed, both sides against reference_v2, "
                  "all finalists and their paired control. No outcome filtering.",
        "seed": plan["validation_seeds"][0], "candidates": names,
        "limits": "Posthoc descriptive mechanisms; deaths per action and absolute deaths are not causal effects."})
    summaries, sampled = {}, {}
    for name in names:
        own = [g for g in games if name in (g["bot_a"], g["bot_b"])]
        breakdown = {}
        for label, selected in [("overall", own)] + [(m, [g for g in own if g["map"] == m]) for m in sorted({g["map"] for g in own})]:
            counts = Counter()
            for g in selected:
                score = arena.score_for(g, name)
                counts["wins" if score == 1 else "draws" if score == .5 else "losses"] += 1
                if score == 0:
                    counts["loss_" + g["reason"]] += 1
            breakdown[label] = dict(counts)
        summaries[name] = breakdown
        sample = [g for g in own if "reference_v2" in (g["bot_a"], g["bot_b"]) and
                  g["seed"] == plan["validation_seeds"][0]]
        assert len(sample) == len(plan["maps"]) * 2
        counts = Counter()
        for g in sample:
            counts.update(collision_counts(g, name))
        sampled[name] = {**dict(counts), "friendly_head_deaths_per_1000_actions":
                         1000 * counts["friendly_head_deaths"] / counts["actions"]}
        print(name, json.dumps(sampled[name]), flush=True)
    population.write_json(folder / "summary.json", {"outcomes": summaries, "collision_sample": sampled})


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("experiment", type=Path)
    run(p.parse_args().experiment)
