# Independent movement experiments

Baseline: the frozen round-450 cutoff candidate from
`results/20260922-171805-endgame-b67e3b/bots/stop_450/`.
Its split behavior, threshold, population cap, and ordinary pearl/exploration
policy are retained. Neither experiment trains a network or modifies live bots.

## Loss audit

The baseline's 12 saved validation losses contained 36,287 team turns and
297 deaths during the dying dragon's own turn: 136 other-body collisions,
50 head collisions, 17 self collisions, and 94 kelp collisions. In every
case, the old helper returned no admissible ordinary move. This helper is
conservative: it excludes portals, so this is not proof that no legal game
action existed. Deaths during other dragons' turns are outside this count.
These counts are descriptive, not exposure-normalized policy comparisons.

This suggests anticipating confinement rather than trying to rescue a fully
boxed-in dragon. Even a sprint needs a usable first step.

## Two fixed variants

**Trap avoidance (`trap`):** compute available local room up to the current
length (capped at 24), and seek a three-step continuation that does not revisit
new path cells. Penalize insufficient room, short continuations, and the
existing heuristic's enemy-head danger cells. Override the original single
step only for a score improvement of at least 15; ties retain the original.

**Emergency sprint (`sprint`):** leave normal movement unchanged. Only when
all admissible single steps score -15 or worse, evaluate two-step paths.
Require a nonnegative endpoint safety score and enough length to pay the
extra segment without relying on pearls. Prefer more endpoint exits, then
pearls, then initially continuing forward. Otherwise retain the original.
This variant does not enable the trap variant's single-step overrides.

Both leave split actions unchanged. They use the same bounded assessment:
30-point penalties per missing continuation step, up to 30 points for room
deficit, and 60 points for an endpoint in the old enemy danger set. Those
weights are fixed hypotheses, not optimized values. There is no combined
trap-plus-sprint variant in this experiment.

### Safety boundaries

Every proposed sprint step must cross an open non-portal edge into a
currently empty visible tile; paths cannot revisit cells. All old bodies
remain blocked, even when a full moving-tail simulation could permit a path.
Reachable open vision boundaries count as potential room, not verified safety.
The enemy danger model remains one-step adjacency, not enemy sprint search.
Future enemy moves, friendly movement, and unseen geometry remain uncertain.

These restrictions respect the official [step-by-step movement rules](https://game.battlecode.au/docs/execution-order),
including collision checks before tail advancement and the inability of a
length-2 dragon to pay for an extra step. They deliberately omit legal paths
that require portals or precise tail-release reasoning.

## Evaluation design

- Freeze the exact earlier candidate and all dependencies. Keep a separate,
  identical `reference_450` opponent for direct head-to-head testing.
- Opponents: `reference_450`, splitter, and hunter. This is a harder pool than
  the earlier endgame experiment, which included the weaker v1 instead.
  Absolute scores are not directly comparable between those experiments.
- Four screening maps, seeds 4000-4001, both sides: 144 games across the
  control and two candidates.
- Five semantically distinct validation maps, seeds 5000-5003, both sides:
  360 games, 120 per policy, including 40 against the reference.
- Neither variant is selected, changed, or discarded based on the screen;
  both fixed policies receive the full validation test.
- Success requires a positive lower confidence bound for the paired overall
  score gain AND a direct-reference score lower bound above 50%.
- Use 97.5% intervals per candidate to account for the two experiments
  (Bonferroni adjustment). The overall difference resamples whole maps;
  the direct matchup interval resamples side-paired map/seed blocks.

Both stages use maps familiar from previous research, but validation is
separated from this run's screening. This is local scripted-pool evidence,
not a ladder rating or an untouched project-wide final test. Only five
validation maps limit uncertainty estimates. Any match error or bot-hash
mismatch invalidates a stage.

## Runtime and reproduction

```powershell
.venv\Scripts\python.exe -B -m unittest discover -s tests -q
.venv\Scripts\python.exe -B -m bcsim.movement_audit results/20260922-171805-endgame-b67e3b
.venv\Scripts\python.exe -B -m bcsim.movement --workers 4
```

The run is saved under `results/20260922-173739-movement-659d1f/`, with frozen
bots/maps, predeclared plan, raw games, stage summaries, comparisons, and all
validation replays. `bcsim/movement_budget.py` can probe a run using the
installed unswbc judge sandbox. Its inputs and results are saved separately
as `budget-inputs.json` and `budget.json`.

The initial runtime probe used eight real observations (long bodies, dense
occupancy, many enemy heads, an emergency-sprint opportunity, and four round
positions), each tested cold and warm for all three policies: 48 turns.

| Policy | Maximum observed CPU points | Maximum memory | Failures |
|---|---:|---:|---:|
| Control | 32.92 million | 20.56 MiB | 0 |
| Trap | 45.18 million | 20.56 MiB | 0 |
| Sprint | 45.16 million | 20.56 MiB | 0 |

These are sampled interpreter-metered turns, not full sandbox matches or a
worst-case guarantee. The published limits are 100 million points per turn
and 48 MiB memory. [Official runtime documentation](https://game.battlecode.au/docs/timeouts)

61 tests pass, including exact split-cutoff preservation, frozen dependencies,
stepwise sprint collision/cost guards, emergency-only activation, trap routing,
and accepted two-step paths checked against the real engine.

## Results

All 504 scheduled games completed without match errors or bot-code hash
mismatches. No policy was changed after inspecting screening results.

| Policy | Screen score (48 games) | Validation score (120 games) | W-L against round-450 reference |
|---|---:|---:|---:|
| Control | 72.9% | 74.2% | 20-20 |
| Trap avoidance | 77.1% | 79.2% | 23-17 |
| Emergency sprint | 75.0% | 73.3% | 21-19 |

The primary paired **97.5%** map-cluster intervals, adjusted for testing two
variants, are:

- Trap: **+5.00 percentage points**, interval **-2.50 to +15.83**.
- Sprint: **-0.83 points**, interval **-2.50 to 0.00**.

The direct-reference 97.5% score intervals also include 50%: trap **40-75%**,
sprint **42.5-62.5%**. **Neither passes the predeclared success gate.**
The stage summaries additionally show unadjusted 95% intervals; use the
adjusted intervals in `comparison.json` for the decision above.

### What the results suggest

Trap avoidance cut elimination losses from **16 to 8**, but round-limit
losses rose from **15 to 17**. Its net six additional wins all came from
Arena (22/24 versus 16/24); Default gained one, Schooltime lost one, and the
other two maps tied in aggregate. The overall point estimate is promising,
but that concentration is exactly why map-level uncertainty matters. It is
not a proven broad improvement.

Sprint elimination losses barely changed (**16 to 15**), while round-limit
losses rose to **17**. Direct wins against the reference rose by one but
wins against splitter fell by two. This configuration did not improve the
actual match objective; legal escapes alone are insufficient evidence.

Keep the previous round-450 candidate as the experimental reference. The
next useful follow-up is to diagnose why trap avoidance helps Arena and
test that hypothesis on additional distinct layouts, retaining the negative
maps. Do not combine these two variants or tune their thresholds on this
validation set and call it a fresh confirmation. Park the current sprint
policy unless a more selective trigger has independent evidence behind it.
No live bot or training corpus was modified and nothing was submitted.

### Final replay audit

Verified all **360 validation replays**, including winners, final longest
dragons and total lengths; frozen bot hashes; complete game counts; disjoint
map identities; and unchanged original/live bots. No candidate had an
invalid-action death or reported turn timeout/budget flag in these in-process
games (the independent sandbox probe supplies the sampled CPU measurements).

The sprint candidate actually issued **1,885 two-step sprints** in **418,254
actions** (about 0.45%). None died during its own sprint execution. Thus the
negative result is not explained by an inactive feature or an observed
stepwise-collision bug. It still could lose later, waste length, or make a
strategically inferior move. Control/trap emitted no multi-step moves.

Raw audit counts are saved in `replay-audit.json`. Repeat the verification
in a fresh audit destination or preserve/rename its existing output first;
the writer intentionally refuses to overwrite an existing report:

```powershell
.venv\Scripts\python.exe -B -m bcsim.movement_audit results/20260922-173739-movement-659d1f --verify
```
