# First gameplay experiment: population policy

This is the first controlled gameplay experiment after the evaluation/data
infrastructure work (the population ablation from E3 in the research plan).
It asks whether reproduction helps the existing movement policy before we
spend time training a neural network or tuning many interacting parameters.

## Design

- Five variants: no splitting, or live population caps of 2, 4, 8, and 64.
- Split at length 8 or greater, into two approximately equal pieces, subject
  to the existing splitter's enemy-head danger heuristic and engine unit limit.
- A population cap limits simultaneously living dragons, not lifetime births.
  Dragons may replenish losses. The experiment does not test a stop-splitting
  endgame, specialized growers, tail safety, or a new movement algorithm.
- Every variant carries an unchanged copy of the current `mybot` movement
  implementation and dependencies. The 64-cap variant reproduces the existing
  splitter's policy; it is a reference, not a novel algorithm.
- Opponents: frozen v1, splitter, and hunter. Each matchup uses both sides.
- Deduplicate maps by semantic signature. Sort by signature, use the first
  four for screening (seeds 0 and 1), and reserve the rest for confirmation
  (seeds 1000 through 1003). Seeds vary bot randomness, not engine map setup.
- Select the highest-screen-score splitting variant, breaking exact ties in
  favor of the smaller cap. Compare that candidate and the no-split control
  on the same reserved matchups. The rule is saved before any games run;
  selection is saved before confirmation starts.

With nine unique maps this is 240 screening games and 240 held-out
games. Each confirmed policy has 20 side-paired blocks per opponent. The maps
have disjoint exact configurations, but related map families can cross stages.

## Interpretation

Score means `(wins + 0.5 * draws) / games`. Report the paired improvement over
the no-split control; resample whole maps for the main bootstrap interval so
seeds and opponents on the same map stay together. Also retain the arena's
opponent/map/seed block intervals for each matchup.

Five reserved maps and three scripted opponents are a limited test. The
screen's highest-scoring cap is not proven optimal, and confirmation only
compares the selected cap to no splitting, not to every other cap. These maps
were reserved from this run's selection, not necessarily unseen in all prior
project work. The in-process runner does not meter judge CPU costs or establish
online ladder strength. Any match errors or bot-hash mismatches invalidate a
stage rather than being counted as draws.

## Reproduce

```powershell
.venv\Scripts\python.exe -B -m unittest discover -s tests -v
.venv\Scripts\python.exe -B -m bcsim.population --workers 4
```

The runner creates a fresh `results/*-population-*/` directory containing the
predeclared plan, frozen self-contained bots and maps, selection, code/engine
hashes, raw game results, summaries, paired comparison, and all held-out
replays. It never edits `mybot`, opponents, versions, or the training corpus,
and never submits. Repeating identical inputs is a reproducibility check,
not additional independent evidence. New maps/code can change a future run;
use the original saved inputs to audit the original result.

Implementation: `bcsim/population.py`, `experiments/population/brain.py`, and
`tests/test_population.py`. Tests include cap/length/danger guards, preserved
movement and source hashes, map separation, side pairing, paired-comparison
validation, and real-engine equivalence to the no-split and splitter references.

## First run: 2026-09-22

Artifacts: `results/20260922-161702-population-94dab2/`.
Use **`map-audit/summary.md`** and **`map-audit/comparison.json`** for the
corrected result, not the original top-level summary.

Final verification: all 49 regression tests passed after the map-identity
fix and audit changes; `git diff --check` passed.

All 576 initially scheduled games completed without match errors or bot-code
hash mismatches. A post-run audit found a map-signature bug: explicit open
edges fell through into the signature's miscellaneous fields, so identical
maps could hash differently. The server Big Empty was a screening-map copy,
and Default occurred twice in validation. Fixed `bcsim/paths.py`, added a
regression test, and excluded 96 games based solely on map identity. Screening
contained four unique maps, so the predeclared selection remains unchanged.
All original results and 336 replays are retained; the corrected experiment
uses 240 screen games and 240 validation games on five distinct held-out maps.

| Live population cap | Screen score (48 games each) | Reserved-map score (120 games each) |
|---|---:|---:|
| No splitting | 37.5% | 34.2% |
| 2 | 64.6% | Not tested |
| 4 | 68.8% | Not tested |
| 8 | 72.9% | Not tested |
| 64 | 83.3% | 78.3% |

The selected 64-cap candidate improved held-out score by **44.2 percentage
points**, with a 95% map-cluster bootstrap interval of **+35.0 to +52.5 points**.
It improved aggregate score on each of the five reserved configurations.
There were no draws in this run, so match score and win rate coincide.

| Held-out opponent | No-split W-L | 64-cap W-L |
|---|---:|---:|
| Frozen v1 | 20-20 | 37-3 |
| Hunter | 18-22 | 37-3 |
| Splitter | 3-37 | 20-20 |

Conclusion: reproduction is a valuable missing capability in the current
greedy bot, and the permissive splitter is a sensible experimental baseline.
This is **not** an improvement over the existing splitter: the selected
policy implements that same behavior, and its mirror matchup scores 50%.
It also does not prove that cap 64 is optimal; other caps only received a
small screen. Do not infer competitive ladder strength from this opponent set.

Replay audit: all 336 saved held-out outcomes and final longest lengths
match the result records, and the original `mybot` hash is unchanged.
Of the selected candidate's six retained losses to v1/hunter, five reached round
500 and lost on length: its longest survivors were only 4-7 segments,
versus 14-46 for the opponent. This suggests that perpetual splitting can
conflict with the longest-dragon endgame; it does not yet establish a fix.

Next experiment: keep movement fixed and compare perpetual splitting with
predeclared late-game split cutoffs or a protected grower. Test collision/trap
avoidance and a small legal-sprint escape variant independently afterward,
against the frozen splitter. Do not bundle population and movement changes.
Neither NN training nor genetic optimization is needed to establish this
first result. No bot has been promoted or submitted.
