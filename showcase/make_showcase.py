"""Showcase matches for the project writeup (PROJECT_WRITEUP.md).

Plays each frozen version against its predecessor on a few maps, both sides, one seed,
under the rules of its era, and keeps every replay in showcase/replays/<era>/.
These are illustrations for the writeup and for video capture, NOT strength evidence:
the evidence is the multi-seed, multi-opponent experiments in FEATURE_EXPERIMENT.md.

    # old rules (unswbc 1.1.0, longest dragon wins at round 500)
    .venv/Scripts/python showcase/make_showcase.py old
    # queen rules (unswbc 1.2.9, official current maps)
    .venv/Scripts/python showcase/make_showcase.py queen

Same seed + same bots = the same game, so any match here can be re-recorded.
"""
import json, sys
from pathlib import Path

SEED = 20261012
OLD_MAPS = ["maps/default.map", "maps/trophy.map", "maps/schooltime.map", "maps/server/Prisoners_Dilemma.map"]
OLD_PAIRS = [("versions/v1", "opponents/splitter"), ("versions/v2", "versions/v1"), ("versions/v3", "versions/v2"),
             ("versions/v6", "versions/v3"), ("versions/v7-base", "versions/v6"), ("versions/v9", "versions/v7-base"),
             ("versions/v10", "versions/v9"), ("versions/v10h", "versions/v10"), ("versions/v10o", "versions/v10h")]
QUEEN_MAPS = ["maps/v129/schooltime.map", "maps/v129/weakhold.map", "maps/v129/stripes.map", "maps/v129/autarky.map",
              "maps/v129/australia.map", "maps/v129/tower_defense.map"]
QUEEN_PAIRS = [("versions/v11ms", "versions/v10o"), ("versions/v11q", "versions/v11ms"), ("versions/v11t", "versions/v11q"),
               ("versions/v12x", "versions/v11t"), ("versions/v12z", "versions/v12x")]

if __name__ == "__main__":
    era = sys.argv[1]
    if era == "queen":
        from bcsim import queen_runtime
        queen_runtime.activate()
    from bcsim import bounded
    maps, pairs = (OLD_MAPS, OLD_PAIRS) if era == "old" else (QUEEN_MAPS, QUEEN_PAIRS)
    out = Path("showcase/replays") / era
    jobs = []
    for new, old in pairs:
        for m in maps:
            for a, b in ((new, old), (old, new)):
                jobs.append((m, a, b, SEED, str(out), [Path(old).name, Path(m).stem, SEED]))
    games = bounded.run(jobs, 12, Path("showcase/run-" + era), f"showcase {era}")
    Path(f"showcase/games-{era}.json").write_text(json.dumps(games, indent=0, default=str))
    for new, old in pairs:
        n, o = Path(new).name, Path(old).name
        gg = [g for g in games if {g["bot_a"], g["bot_b"]} == {n, o}]
        w = sum(g["winner"] == ("A" if g["bot_a"] == n else "B") for g in gg)
        d = sum(g["winner"] is None for g in gg)
        print(f"{n} vs {o}: {w} wins, {d} draws, {len(gg) - w - d} losses of {len(gg)}", flush=True)
