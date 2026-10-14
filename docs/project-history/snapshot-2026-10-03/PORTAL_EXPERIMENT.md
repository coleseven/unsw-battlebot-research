# Last-resort portal experiment

Frozen baseline: `versions/v2`, hash `9f29ab4138b51d26`.
Run: `results/20260923-085446-portal-9297e0/`.

## Fixed policy

The normal greedy movement helper treats portals as non-passable. This small
wrapper considers them only when there is no known-empty ordinary adjacent
step. It leaves reproduction, sprint behavior, normal movement, and movement
RNG unchanged. It also preserves the baseline's direct enemy-head collision
when that is its fallback action.

When a portal's partner is visible, its exit is calculated using the actual
directional edge rules. Known occupied exits, including our own tail, are
rejected. Visible empty exits rank above unknown exits. Ties retain the
original direction, then use stable NESW order. An unseen exit is uncertain,
not safe. This is not a global portal planner or persistent map memory.

## Evaluation fixed before play

One unchanged candidate directly against v2 on all five official portal maps:
Colosseum, Default, Queen of Spades, Schooltime, and Trophy. Twenty-four fresh
seeds (17000-17023), both sides, give 240 games. There is no policy screen or
combination with the grower experiment. The performance gate is a direct score
95% map-cluster lower bound above 50%, followed by replay and sandbox checks.
Five familiar map clusters are limited evidence; this is not ladder testing.

Tests cover all four portal exit orientations, blocked exits, unchanged splits
and normal moves, enemy-head trades, an actual engine escape, and unchanged
outcomes on two no-portal maps. The audit reconstructs every candidate turn
and calls the policy directly, bypassing exception fallbacks. It also counts
portal attempts and survival of the immediate turn. That survival statistic
does not establish whether the portal improves the full game.

```powershell
.venv\Scripts\python.exe -B -m bcsim.portal_experiment --workers 2
.venv\Scripts\python.exe -B -m bcsim.portal_experiment --audit results/20260923-085446-portal-9297e0 --workers 8
.venv\Scripts\python.exe -B -m bcsim.portal_experiment --budget results/20260923-085446-portal-9297e0
```

Results and checks are saved in the run directory. The active bot and frozen
v2 remain unchanged; neither this experiment nor its tooling submits a bot.

## Result: encouraging, but not promoted

Candidate hash: `f972d364f8744605`. Direct v2 results: **131 wins, 109 losses**
(54.58%). The 95% map-cluster interval is **49.58-59.58%**; the paired-seed
interval is **49.17-60.00%**. The predeclared performance gate did not pass.

| Map | Wins-losses | Score |
|---|---:|---:|
| Colosseum | 30-18 | 62.50% |
| Default | 27-21 | 56.25% |
| Queen of Spades | 28-20 | 58.33% |
| Schooltime | 24-24 | 50.00% |
| Trophy | 22-26 | 45.83% |

A complete 500-round Default game in the actual judge sandbox passed with
8,330 candidate decisions, no errors, peak **32,611,470 CPU points**, and
**21,561,344 bytes** memory. This is a runtime test, not additional paired
strength evidence. Replay checks and targeted budget samples are saved in
the run directory.

All **240** validation replays passed. **2,201,606** candidate actions matched
exactly with exception fallback disabled; there were no invalid-action deaths,
recorded timeout flags, or splits from round 450 onward. There were 1,826
portal moves, of which 1,222 redirected the baseline fallback. **889 of those
1,222 redirects survived their immediate turn**. None of the chosen portal
exits was visible, and none redirected an already-selected portal. These are
mechanism diagnostics, not counterfactual game wins.

All 26 additional cold/warm candidate probes passed, including a real portal
override observation. Their maximum was **33,185,559 CPU points** with
**21,561,344 bytes** memory and zero failures. The complete **84-test**
regression suite and `git diff --check` passed. Both candidate hashes and the
unchanged active/frozen baseline hashes were checked; no unsupported judge
imports were found. These measurements are not a worst-case runtime proof.

The unchanged portal policy is a reasonable replication candidate, but these
results do not establish an improvement. Any follow-up should fix its sample
size and new seeds in advance, include frozen opponents and new portal
layouts, and avoid repeatedly adding games until an interval crosses 50%.
