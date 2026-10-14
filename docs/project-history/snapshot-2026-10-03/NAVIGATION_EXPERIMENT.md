# Persistent terrain memory and deliberate portal routing

Baseline: frozen v2 (`9f29ab4138b51d26`). Active experiment:
`results/20260923-140427-navigation-6e47f4/`.

## Two fixed ablations

1. `terrain_memory`: each dragon remembers observed static edges and recent
   food sightings. Routes can leave the current window through known terrain.
2. `portal_memory`: identical memory and search, with discovered paired portal
   edges admitted to the route graph. Unknown partners are never guessed.

Both preserve v2's split-at-4 / round-450 cutoff and call its original policy
once per turn. They do not incorporate the earlier emergency-portal fallback.
Known-empty ordinary first moves retain v2's danger/space filter. Portal first
moves reject currently visible occupied or threatened exits. Hidden occupancy
is uncertain, not certified empty; entering unseen cells costs extra.

Search expands at most 96 nodes and considers at most 12 moves. It chooses
visible or recently seen food, requiring a margin over an existing local food
route; if no food target is available, it can head toward a known frontier.
Portal traversal costs two additional units; unseen cells one additional
unit; remembered out-of-view food three additional units. Non-pearl countdown
targets have the original two-unit penalty. Food sightings expire after eight
rounds; static edges persist for the dragon's lifetime. This is bounded weighted
search, not a dynamic-body planner or an optimal-path/survival guarantee.

All memory lives on the dragon instance. Newborns start empty; there is no
shared state, inherited map, sonar, map-name special case, or omniscient input.
The helper source is in `framework/navigation.py`; only experimental bundles
receive it, so syncing does not silently alter the active bot or benchmarks.

## Tests and preflight

Tests cover canonical wrapped coordinates, every portal direction against the
reference board, known occupied exits, unknown partners, food expiry, bounded
search, unchanged splitting, newborn isolation, and no-portal equivalence
between the two modes in a real game.

An initial preflight-only snapshot (`20260923-140214-navigation-e8864d`) is
retained but superseded. Review caught an off-window local threat index (-1)
being interpreted as the last visible cell in the new global-coordinate
conversion. The correction has a targeted regression test. No strength games
were run on that superseded snapshot. Both corrected snapshots must complete
their own judge-sandbox games before screening; old runtime results do not
substitute for those checks.

Both corrected preflights passed full 500-round Default games without errors:
terrain-only, 6,515 decisions and peak 74,477,893 CPU points; portal-routing,
9,546 decisions and peak 74,384,735 points. Both used at most 21,626,880 bytes.
These are runtime tests, not paired strength evidence. The 95-test suite passed.
An additional integration check reproduced both real-game navigation fixtures
exactly through the stateful replay auditor.

The stateful budget check (`bcsim.navigation_audit --budget`) replays each
sampled dragon's own observation history from birth. That restores its terrain
and food memory before probing the high-memory/high-search state. Judge RNG
may differ from arena RNG; these are runtime probes, not counterfactual games.

## Fixed evaluation

- Screen: control and both candidates against v2, all nine official maps,
  four fresh seeds (20000-20003), both sides: **216 games**, all replayed.
- Select only the highest new-policy score if >50%; ties prefer terrain-only.
  If neither exceeds 50%, stop. Screening is not confirmation.
- If selected, validate unchanged on seeds 21000-21007: candidate and control
  each face v2, splitter, and hunter on nine maps/both sides: **864 games**.
- Require direct-v2 map-cluster 95% lower bound >50% and paired-pool gain
  map-cluster lower bound >0, plus strict replay and judge-runtime checks.
- A passing candidate would still need fresh generated-map confirmation before
  promotion. No tuning against either validation or prior portal-transfer maps.

The conditional confirmation design is fixed while official validation runs:
eight new no-portal layouts (generation seeds 24001-24008) and eight new portal
layouts (25001-25008), using the existing four-family generators. Eight fresh
bot seeds (22000-22007), both sides, directly against v2 yield 256 games. Group
all four related layouts of each family together in the bootstrap; require
the family-cluster lower bound >50% and every map >=37.5%. This is fresh-layout
transfer, not unseen-family or competition-distribution evidence. Run it only
if the unchanged candidate first passes official validation.

## Screen completed

Terrain memory (`1b01ff4654b23d84`): **39 wins, 1 draw, 32 losses**, 54.86%.
Portal memory (`8ae8a538410a4be2`): **40 wins, 0 draws, 32 losses**, 55.56%.
The declared rule selects portal memory unchanged. Its half-win advantage over
terrain-only is not evidence that portals independently help: the paired
map-cluster interval for that difference is -13.19 to +15.28 percentage points.
All 32 matched no-portal pairs between the two variants are identical.

The v2 mirror control was 36-0-36. Elimination losses in this small screen were
4 for control, 6 for terrain-only, and 8 for portal-memory; these are descriptive
warning signs, not reasons to alter the policy during held-out validation.

## Validation failed: no promotion or transfer batch

All 864 predeclared validation games completed. The unchanged portal-memory
candidate scored **70 wins, 2 draws, 72 losses** directly against v2: **49.31%**,
95% map-cluster interval **33.33-65.63%**. The paired pool gain was exactly
**0.00 percentage points**, interval **-9.38 to +9.03 pp**. Both gates failed;
the conditional generated-map test is therefore not run. V2 stays frozen and
the active bot remains unchanged.

| Opponent | V2 control W-D-L | Portal-memory W-D-L |
|---|---:|---:|
| V2 | 72-0-72 | 70-2-72 |
| Splitter | 131-0-13 | 140-0-4 |
| Hunter | 140-0-4 | 132-0-12 |
| Total | 343-0-89 | 342-2-88 |

The equal aggregate score hides substantial map variation. Default improved
from 36-0-12 to **48-0-0**, but Queen of Spades regressed from 33-0-15 to
**18-1-29**. Across the pool, length losses fell from 81 to 71 while elimination
losses rose from 8 to 17. This is not a robust replacement for v2.

## Verification and diagnostic evidence

The screen audit passed all 216 replays and reproduced **1,347,021** candidate
decisions exactly, bypassing exception fallback. Search reached its 96-node
cap on 363,268 terrain-memory turns and 365,501 portal-memory turns; these
counts are descriptive, not a reason to increase the budget after seeing results.

Sixteen stateful judge probes replayed **2,544** observation-history turns.
Every probe passed; peak **85,002,202 CPU points**, below the 100M limit. These
prefix probes and full-game preflights are observed runtime checks, not a
worst-case proof.

The validation audit is also complete: all **864** replays passed, with
**3,838,621** candidate decisions matching exactly and zero late splits or
invalid-action deaths. Combined with screening, that is **1,080** audited games
and **5,185,642** exact candidate decisions. Eight validation-history probes
added **1,445** measured turns and passed, with peak **82,013,213 CPU points**.
Across both stages, all **24 probes / 3,989 history turns** passed; maximum
memory was **21,692,416 bytes**. Validation stress samples include 1,828 mapped
cells, 12 discovered portal pairs, 96 expanded search nodes, length 59, and
the 64-dragon population cap. Artifacts are under each stage's `audit/` folder.

The final **96-test** suite and `git diff --check` passed. Candidate hashes
match the frozen plan, imports are judge-compatible, and `mybot` / v2 hashes
remain unchanged. The conditional transfer batch was not started.

A post-hoc case study inspected four Default and four Queen of Spades games
(first validation seed, v2/hunter opponents, both sides). It reproduced all
**56,480** candidate actions before comparing the frozen wrapper's internal
baseline action to its final choice, without drawing RNG twice.

| Case-study map | Overrides | With baseline food route | Without baseline food route | Immediate portal overrides |
|---|---:|---:|---:|---:|
| Default | 2,103 | 6 | 2,097 | 81 |
| Queen of Spades | 649 | 3 | 646 | 64 |

Thus these sampled changes primarily occur when the baseline would explore.
The sample does not identify which exploration component caused the regression
or establish counterfactual game wins. No map-specific tuning was applied.

No activation, submission, or commit is part of this experiment.

```powershell
.venv\Scripts\python.exe -B -m bcsim.navigation_experiment --screen results/20260923-140427-navigation-6e47f4 --workers 8
.venv\Scripts\python.exe -B -m bcsim.navigation_experiment --validate results/20260923-140427-navigation-6e47f4 --workers 8
.venv\Scripts\python.exe -B -m bcsim.navigation_audit results/20260923-140427-navigation-6e47f4 --stage screen --workers 8
.venv\Scripts\python.exe -B -m bcsim.navigation_audit results/20260923-140427-navigation-6e47f4 --stage screen --budget
.venv\Scripts\python.exe -B -m bcsim.navigation_audit results/20260923-140427-navigation-6e47f4 --stage validation --workers 8
.venv\Scripts\python.exe -B -m bcsim.navigation_audit results/20260923-140427-navigation-6e47f4 --stage validation --budget
```
