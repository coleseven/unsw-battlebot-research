# Unchanged portal policy: fixed replication and transfer

The first portal test scored 131-109 against v2, but failed its confidence
gate. This follow-up does not tune the policy or pool results with that test.
Candidate hash stays `f972d364f8744605`; baseline v2 stays `9f29ab4138b51d26`.

## Plan fixed before matches

- Official maps: all nine layouts, 16 fresh seeds (18000-18015), both sides.
  Candidate and v2 control each play frozen v2, splitter, and hunter:
  **1,728 games**.
- New layouts: eight generated portal maps, 16 fresh seeds (19000-19015),
  both sides, candidate directly against v2: **256 games**.
- No additional batches based on a near-significant result, no retuning,
  and no combination with the unsuccessful grower policy.

The generated maps use four related families (open, baffles, dense, scarce),
with two sizes per family and four/eight portal pairs. Generation seeds are
23001-23008, distinct from earlier transfer layouts. Portal placement is
reflection-symmetric, avoids initial bodies, and retains full connectivity.
Rejecting a proposed placement depends only on geometry, never bot results.
Tests verify paired same-orientation edges, reflected destinations in every
direction, deterministic generation, distinct map signatures, connectivity,
and engine acceptance without repairs. These procedural families are not a
sample from the competition's actual map distribution.

## Acceptance criteria (all required)

1. Official portal-map direct-v2 score: 95% map-cluster lower bound >50%.
2. Paired score gain across the full official opponent pool: 95% map-cluster
   lower bound >0.
3. New-map score: 95% family-cluster lower bound >50%, and every map >=37.5%.
4. All paired no-portal official games have identical outcomes, duration,
   lengths, and death counts to control.
5. Replay/action fidelity and judge-runtime checks pass.

No-portal maps serve as regression controls, not independent wins for the
portal feature. Both sides and shared map families stay grouped in reported
intervals. Opponents are familiar scripts, so passing would still not establish
ranked-ladder strength. A failed gate leaves v2 as the best verified candidate.

```powershell
.venv\Scripts\python.exe -B -m bcsim.portal_followup --workers 8
.venv\Scripts\python.exe -B -m bcsim.portal_followup --audit results/20260923-091759-portal-followup-206dc9 --workers 8
.venv\Scripts\python.exe -B -m bcsim.portal_experiment --budget results/20260923-091759-portal-followup-206dc9
.venv\Scripts\python.exe -B -m bcsim.portal_report results/20260923-091759-portal-followup-206dc9
```

The runner records its plan, frozen code, map files, provenance, all replays,
and results in a fresh directory. No active-bot mutation or submission.

## Completed performance result: no promotion

Run: `results/20260923-091759-portal-followup-206dc9/`.
All **1,984** planned matches completed; no additional match batches were added.

| Test | Result | 95% clustered interval | Gate |
|---|---|---|---|
| Official portal maps, direct v2 | 85-0-75; 53.13% score | 46.88-59.38% | Fail |
| Paired full official pool | +0.87 percentage points | -0.35 to +2.37 pp | Fail |
| New portal maps, direct v2 | 172-1-83; 67.38% score | 63.48-70.70% | Pass |
| No-portal regression | All 384 paired games identical | Exact outcome check | Pass |

Pool totals: candidate 692 wins / 2 draws / 170 losses, versus v2 control
684 / 3 / 177 (864 games each). The candidate gained against splitter but
lost three net games against hunter. New-map scores ranged from 53.13% to
75%; the worst was open_large. No generated-map score breached the 37.5%
floor. The synthetic-family interval groups the two layouts of each family;
with only four related families it should not be read as universal coverage.

The strong procedural-map result does not override either failed official
criterion. This policy remains a frozen experimental artifact, not v3 and not
the active bot. The earlier 240-game test is not pooled into these intervals.

## Runtime and regression checks

A complete 500-round judge-sandbox game on `new_dense_large` passed with
7,989 candidate decisions, zero errors, peak **30,234,024 CPU points**, and
**21,561,344 bytes** memory. It is a runtime integration test, not an additional
paired strength result. The final 87-test regression suite passed after
resumption, including a test of mechanism-report aggregation and its refusal
to accept an incomplete replay audit.
Full replay audit and sampled runtime artifacts are recorded in the run folder.

Verification is complete:

- All **1,984** replay results and recorded action flags passed checks.
- **10,531,661** candidate decisions reproduced exactly, with exception
  fallback bypassed; zero late splits and no invalid-action deaths.
- All 26 additional cold/warm candidate probes passed. Maximum
  **33,185,559 CPU points**, **21,561,344 bytes** memory, zero failures.
- `mybot` remains `ffe736af6c14ea33`; frozen v2 remains `9f29ab4138b51d26`.
  No bot was activated, submitted, or committed.

## Mechanism findings

`mechanism-report.json` contains per-map geometry, portal-use counts, and
endgame diagnostics. On official portal maps, fallback redirects occurred
**0.501 times per 1,000 candidate decisions**; on generated maps, **6.489**
times per 1,000 (about 13 times as often). Chosen visible-empty exits appeared
30 times on official maps versus 7,313 on generated maps. This is a substantial
difference in the situations being tested, consistent with different feature
value; it is descriptive, not proof that geometry alone caused the score gap.

The official pool's elimination losses were unchanged at 17; length losses
fell from 160 to 153. These mechanism and phase counts do not replace the
failed predeclared performance gates.

Interpretation: emergency portal use has demonstrated value on this generated
map set, but not a sufficiently reliable official-map gain. A next navigation
experiment should isolate persistent terrain memory and deliberate portal
routing; repeatedly extending this fallback's sample until it passes is not
the plan. Frozen v2 remains the benchmark.
