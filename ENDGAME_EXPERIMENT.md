# Second gameplay experiment: when to stop splitting

The first experiment established a strong advantage for reproduction over
the original greedy bot. Its remaining non-mirror losses often came at the
500-round length decision. This experiment tests whether a fixed split
cutoff helps, without changing movement or adding a learned model.

## Predeclared design

- Control: split perpetually at length 8, up to 64 living teammates, with the
  same danger heuristic as the existing splitter.
- Candidates: stop splitting when the observed round reaches 200, 300, 400,
  or 450. At and after the cutoff, run the unchanged greedy movement policy.
- No new sprint logic, pathfinding, role assignment, or safety heuristic.
  Descendants follow the same cutoff using the globally observed round.
- Freeze all candidate/opponent dependencies and map files in a new result
  directory. Opponents are frozen v1, hunter, and splitter.
- Nine semantic map identities, deduplicated with the corrected map code:
  four screening maps and five distinct validation maps, sorted by signature.
- Screening: seeds 2000-2001, both sides, 48 games per policy, 240 total.
- Selection: highest screening match score among finite cutoffs; ties choose
  the later cutoff. Record the choice before playing validation.
- Validation: selected cutoff and perpetual control on identical matchups;
  seeds 3000-3003, both sides, 120 games per policy, 240 total.
- Success requires BOTH a positive lower bound for the paired, map-cluster
  95% interval on overall score improvement AND a lower bound above 50% for
  the selected candidate's side-paired score interval against splitter.

Score is wins plus half draws, divided by games. The actual game result is
the objective; longer survivors alone are not success. Endgame length and
elimination counts are descriptive, because policies also change which games
reach the round limit. Errors or bot-hash changes invalidate a stage.

These maps were seen in the previous experiment. Validation is held apart
from this run's cutoff selection, not untouched across the entire research
project. Bot seeds do not randomize engine map setup. Five maps and a small
scripted opponent pool cannot establish ladder strength. The in-process
experiment also does not verify the judge's CPU allowance.

## Run and inspect

```powershell
.venv\Scripts\python.exe -B -m unittest discover -s tests -q
.venv\Scripts\python.exe -B -m bcsim.endgame --workers 4
```

Implementation: `bcsim/endgame.py`, `experiments/endgame/brain.py`, and
`tests/test_endgame.py`. Tests check exact cutoff boundaries, unchanged
movement, invalid inputs, selection ties, and real-engine equivalence of
perpetual/zero-cutoff wrappers to splitter/the original bot.

Each `results/*-endgame-*/` directory contains the plan, frozen bots/maps,
runner implementation copies, screening selection, raw games, comparison,
diagnostics, summaries, and all validation replays. No live bot or dataset is
modified, and no submission is made. Preserve negative results as well as
positive ones; do not adjust the cutoff after inspecting validation.

## Result: 2026-09-22

Run: `results/20260922-171805-endgame-b67e3b/`.
All 480 games completed without match errors or bot-code hash mismatches.
All 54 regression tests passed; `git diff --check` passed.
Replay audit verified all 240 validation outcomes and final longest lengths,
four/five disjoint screen/validation map identities, and the unchanged live
bot hash. All 81 control games ending before the cutoff had identical
candidate outcomes, final statistics, and death counts.

| Policy | Screen score (48 games) | Validation score (120 games) |
|---|---:|---:|
| Perpetual splitting | 79.2% | 79.2% |
| Stop at 200 | 81.2% | Not tested |
| Stop at 300 | 83.3% | Not tested |
| Stop at 400 | 83.3% | Not tested |
| Stop at 450 | 87.5% | 90.0% |

The screen selected round 450. On the five validation maps, its paired gain
was **+10.83 percentage points**, with a 95% map-cluster bootstrap interval
of **+4.17 to +16.67 points**. It beat the splitter **33-7 (82.5%)**; the
side-paired score interval was **70.0-92.5%**. Both predeclared gates passed.
Aggregate score improved on four validation maps and tied on arena.

| Validation opponent | Perpetual W-L | Stop at 450 W-L |
|---|---:|---:|
| v1 | 38-2 | 39-1 |
| Hunter | 37-3 | 36-4 |
| Splitter | 20-20 | 33-7 |

This is an improvement against the local splitter benchmark, unlike the
first experiment's behaviorally identical reference. It is not uniformly
better: hunter performance fell by one win in 40 games. Round 450 is the
best screened cutoff in this run, not a proven global optimum.

### Mechanism and next step

Across 120 validation games per policy, round-limit losses fell from **19 to
6**, while elimination losses stayed at **6**. Mean longest surviving dragon
among round-limit games rose from **7.0 to 13.15**, but that conditional mean
is descriptive rather than an independent causal measure (35 control games
and 34 candidate games reached the limit). The win/loss change is the useful
evidence supporting the endgame hypothesis.

Keep the frozen `bots/stop_450/` candidate as the next experiment's reference.
Next, isolate improved trap avoidance or short-sprint escape while keeping
this reproduction policy fixed. Wider opponents/maps and a judge-sandbox
budget check remain necessary before treating it as a competition-ready bot.
No live bot was promoted or submitted, and the training corpus was untouched.
