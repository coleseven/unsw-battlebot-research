# Guarded movement experiments

## Motivation and diagnostic evidence

The unchanged trap policy repeated its Arena win but scored only 25% on a
related pocket layout. An exact action audit reproduced 18 already-played
games (three maps, three seeds, both sides). These are diagnostics, NOT new
evaluation evidence. Every audited action matched its original replay.

In the six pocket games, the trap wrapper made 111 overrides in 6,343 moves:

- All 111 changed the estimated three-step continuation depth.
- None was a room-only change.
- 27 moved into a new one-step enemy-head threat.
- 44 gave up an immediate pearl.

These observations identify possible tradeoffs, not the cause of each loss.
Other dragons move between turns, and the original static depth model freezes
our own tail as well as other bodies. A potential enemy move is not a certain
enemy move; avoiding every threat may itself be strategically harmful.

Audit: `results/20260922-175423-trap-followup-a1e642/diagnostics/audit.json`.

## Fixed candidates

All start from the frozen round-450 baseline. Splitting, baseline movement,
RNG consumption, and the final-growth cutoff are unchanged. Single-step moves
only; no new sprint or portal behavior.

1. `head_guard`: old trap scoring, but do not override an unthreatened first
   step with a threatened one.
2. `tail_guard`: head guard plus three-step moving-own-body continuation when
   the complete body can be reconstructed from visible segment-facing links.
   Partly visible/portal-linked bodies fall back to static occupancy. Collision
   is checked before tail release. Pearl growth is conservatively assumed for
   visible and potentially matured pearls. Other dragons remain static; unknown
   boundary exits are still optimistic, not proved safe.
3. `food_guard`: head guard plus retention of an immediate pearl unless the
   baseline step has no continuation at all.

Shared source lives in `framework/guarded_safety.py`; the wrapper lives in
`experiments/guarded/brain.py`. Live bot copies are not synchronized during
isolated experiments. A real-engine four-step body loop tests tail release,
including the important growth case where the tail does NOT vacate.

## Selection and validation

Experiment: `results/20260922-232135-guarded-0cb56c/`.

The 192-game screen uses nine official maps and three related Arena stress
maps, seeds 7000-7001, both sides, versus the frozen baseline. The original
trap is a diagnostic comparator, not a candidate for promotion. Select the
best new policy using official maps only; ties use the declared mode order.

Official-map scores: head guard 47.2%, tail guard 66.7% (24-12), food guard
47.2%. Tail guard was selected unchanged, hash `1f7db5f7f15de29c`.

Validation reserves seeds 8000-8007: selected candidate and baseline, each
against baseline/splitter/hunter, nine official maps, both sides: 864 games.
A further 48 games use seeds 8100-8107 on the three stress maps.

Predeclared performance gate:

- Direct baseline score: 95% map-cluster lower bound above 50%.
- Paired opponent-pool improvement: 95% map-cluster lower bound above zero.
- Stress-family aggregate at least 50%; no individual stress map below 37.5%.
- Replay/action fidelity and actual judge-runtime checks are also required.

All official maps have been seen in earlier experiments. This reserves RNG
seeds, not unknown map families or opponents. Do not present the results as
ladder strength or generalization to unseen maps.

## Completed performance result: not promoted

Tail guard scored 75-69 (52.1%) directly against the baseline. Its 95%
map-cluster interval was 42.4-61.8%. Across the matched opponent pool the gain
was only +0.69 percentage points, interval [-3.01, +4.40]. The performance
gate failed; the screening lead did not replicate as a convincing improvement.

Stress results: baffles 14-2, pockets 8-8, slow food 9-7. This repairs the
earlier pocket regression in this sample but does not establish a broad gain.

A full real-engine Arena game with the candidate in the actual judge Python
sandbox completed without runtime errors: 1,779 metered candidate turns,
48,710,730 maximum points, 41,961,929 p99 points, 21,954,560 maximum bytes.
The opponent ran in-process; that game is runtime evidence, not an additional
paired win or a worst-case guarantee. Artifact: `sandbox-full-arena.json`.

Final audit verified all 912 validation/stress replay results and reproduced
2,318,083 candidate actions exactly, with no hidden strategy exception.
An initial raw-text map comparison rejected engine-reordered synthetic records;
the semantic comparison fix and a regression test resolved it. The complete
audit was rerun successfully with per-game, input-hashed resume checkpoints.

## Compute controls and reproduction

`bcsim/bounded.py` checkpoints every game and creates a fresh process pool
after each batch of at most 12*workers jobs. Each completed game records worker
PID/RSS; workers stop on less than 4 GiB available memory or over 1 GiB sampled
RSS. These are between-game checks, not hard memory quotas. No GPU work.
The runner's regression test verifies identical game outcomes across process
recycling. Installed engine/runtime libraries are not modified.

```powershell
.venv\Scripts\python.exe -B -m bcsim.guarded --workers 6
.venv\Scripts\python.exe -B -m bcsim.guarded --validate results/20260922-232135-guarded-0cb56c --workers 6
.venv\Scripts\python.exe -B -m bcsim.guarded_audit results/20260922-232135-guarded-0cb56c
.venv\Scripts\python.exe -B -m bcsim.guarded_audit results/20260922-232135-guarded-0cb56c --budget
```

Completed stages refuse to overwrite their result files. Repeating a fixed
match is useful for verification but supplies no new statistical evidence.
