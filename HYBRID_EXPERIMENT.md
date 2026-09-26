# Hybrid experiment

Started after reviewing 36 uploaded v2 games and 26 other-team games. Those
observations motivate the hypotheses; they are not independent confirmation.
No uploads, live-bot changes, or changes to frozen v2 are authorized by this run.

## Predeclared comparisons

1. **Adaptive roles, unchanged movement.** `mature` retains promising length-8+
   dragons after round 200 when population is at least 16. `opportunity` retains
   length-4+ dragons after round 250 when population is at least 16 and at least
   three unoccupied visible cells have food. Both retain their role until
   population falls below 8 or own length below 4. Roles are local, not a global
   champion election. All other split decisions and movement are frozen v2.
2. **Matched action rankers, unchanged reproduction.** Fixed heuristic, learned
   linear score, and a 16-hidden-unit tanh MLP receive the same 24 features and
   same visible-empty ordinary-move candidates. No portal/sprint/sonar learning.
   Static area and three-step empty-cell paths are heuristic features, not
   exact moving-body search or a safety proof. Unknown space is not traversed.
3. **Imitation training.** Reuse the previously audited 12 high-rated archived
   battles (60 games), deterministically split 8/2/2 complete battles into
   train/dev/test. Sample one eighth of turns, then retain eligible teacher
   single-step moves with at least two candidates; reservoir cap 4,000/game.
   All filtering and candidate exclusions are reported. This estimates
   conditional teacher imitation, not unconditional action accuracy.
4. Train a linear model once and the MLP with three initializations for 20
   epochs each. Select epochs and the MLP initialization by dev cross-entropy
   before exposing test metrics or match results. Check portable pure-Python
   inference against PyTorch. The server does not run PyTorch.
5. Screen each family independently on all previous maps plus distinct maps
   embedded in the new uploads, four fresh bot seeds, both sides. Select the
   highest-scoring new candidate in each family only if it exceeds 50% against
   v2. Confirm each selected candidate unchanged on eight fresh seeds against
   v2, splitter, and hunter, with a paired v2 control.

The exact map set, code hashes, input replay hashes, battle partition, seeds,
selection rule and gate are written to a new `results/*-hybrid-*/plan.json`
before any training or strength evaluation. All replay-based training uses
only reconstructed acting-dragon observations; no hidden board or win labels.

## Interpretation and safeguards

Battle separation does **not** establish unseen-team or unseen-map transfer.
Our scripted league is not a substitute for live opponents. Imitation does not
provide counterfactual action values and cannot recreate private opponent
memory. Training is per decision, not equal-weighted per team or map; the
per-game cap only limits dominance by very long games. A better imitation score
alone is not evidence of a stronger bot. Multiple families are exploratory;
positive finalists require independent follow-up before broad claims.

Promotion is not automatic. Require positive map-cluster lower confidence
bounds for both direct v2 score above 50% and paired pool gain above zero,
exact replay audits, and actual judge-sandbox resource checks. Below-normal
worker priority, maximum eight workers, and existing RAM guards remain active.
Frozen v2, the submitted ZIP, original datasets and live mybot are preserved.

## Initial run: `20260923-231438-hybrid-b0801d`

The map set contains 11 unique configurations (the previous nine plus
Stronghold and Trauma). Extraction examined 1,209,469 dragon turns across 60
games. Of 152,160 sampled turns, 3,474 were not single moves, 17,397 had only one
candidate, and 3,126 teacher actions were outside the conservative candidate
set. After per-game reservoir caps: 68,099 training examples, 19,311 dev,
16,591 test. All examples have at least two candidate actions.

| Model | Dev accuracy | Test accuracy | Test cross-entropy |
| --- | ---: | ---: | ---: |
| Linear | 60.22% | 58.09% | 0.8310 |
| MLP seed 0 | 60.74% | 59.37% | 0.8140 |
| MLP seed 1, selected by dev loss | 60.98% | 59.27% | 0.8187 |
| MLP seed 2 | 60.65% | 59.17% | 0.8171 |

The MLP has 417 parameters, the linear model 25. Portable Python scores agree
with PyTorch to less than 0.0000013 absolute error on the export probes. These
are conditional imitation metrics, not win rates; test results did not change
the dev-selected model. Seed 0's slightly better test result is not a reason
to substitute it after looking at the test set.

All 48 preflight judge probes passed (eight recorded observations and eight
synthetic round-499 variants per evaluator). Maxima: heuristic 62,645,351 CPU
points, linear 62,645,222, neural 68,950,993; peak memory 21,626,880 bytes.
Sampled budget checks are not a worst-case guarantee. Full regression suite:
103 tests passed at this stage.

Simple held-out imitation references: uniformly choosing among candidates has
40.53% expected accuracy; straight-if-available, otherwise NESW order, reaches
50.48%. These references use the same filtered test rows.

Role screen (264 games, 88 per candidate including control): `mature` 45-43
(51.14%), `opportunity` 35-1-52 (40.34%). Only `mature` advances. Its net extra
win was confined to Big Empty; every other map remained 4-4. This is weak
screening evidence, not a verified gain. No policies were retuned after it.

The neural candidate also completed a full actual-sandbox Default game:
11,538 metered decisions, peak 81,341,728 points and 22,020,096 bytes, no
exceptions, timeout reports or invalid-action deaths. That single runtime game
was a loss; it is not part of the paired in-process strength estimates.

To use available compute while the evaluator screen finishes, the unchanged
validation design is scheduled in two chunks by `bcsim.hybrid_confirm`: shared
control plus selected role first, selected evaluator second. Merge verifies
the exact full job-key set against the original plan. No extra control games,
candidate reselection, changed seeds, or changed promotion thresholds.

The complete role-screen audit reproduced 1,549,615 candidate decisions across
264 replays, with zero mismatches, invalid-action deaths or splits at/after
round 450. The mature role suppressed 896 otherwise length/population-eligible
split opportunities; opportunity suppressed 14,453 (descriptive counts omit
the enemy-head split guard, so they are not exact counterfactual split counts).

The linear candidate completed a full actual-sandbox Big Empty game:
28,942 metered decisions, peak 77,626,712 points and 21,954,560 bytes, no errors.
This runtime game was a win, but is not included in paired strength estimates.

An additional **no-fit diagnostic** evaluated the frozen models on all 26
supplied top-team games. These newer games were excluded from fitting and
selection but previously inspected to motivate the research, so are not a
pristine unseen benchmark. Of 491,663 turns, 30,704 were sampled and 25,016
qualified as multi-choice ordinary moves. Accuracy: uniform expected 39.24%,
straight 55.70%, linear 65.53%, selected MLP 65.87%. Cross-entropy: linear
0.7963, MLP 0.7695. The neural advantage remains small in action agreement;
no model was refitted or reselected using these results.

Both role policies passed eight sampled history-restoring sandbox probes:
631 total decisions, peak 34,757,051 points and 21,561,344 bytes. These restore
each sampled dragon from birth rather than pretending its late-game role state
can be tested from a single isolated observation.

## Screening results and confirmation status

Evaluator screen completed: 352 games, 88 per policy including control.

| Movement policy | W-D-L versus frozen v2 | Score |
| --- | --- | ---: |
| Control | 44-0-44 | 50.00% |
| Fixed heuristic | 63-0-25 | 71.59% |
| Learned linear | 67-0-21 | 76.14% |
| Selected MLP | 63-0-25 | 71.59% |

The linear model advances under the predeclared selection rule. Its four-win
lead over the MLP is not established statistical superiority. The fixed
heuristic's equal score to the MLP also indicates that this screen alone cannot
attribute the movement improvement specifically to neural learning.
Linear weaknesses: Default 2-6, Stronghold 3-5. Neural was 4-4 and 6-2 on
those maps respectively, but regressed elsewhere. Do not construct a map-name
switch from these eight-game cells and call it a validated improvement.

Control plus mature-role confirmation completed (1,056 games). Mature scored
92-84 directly against v2 (52.27%) and 400-128 over the opponent pool versus
control 393-135. All net extra wins remain on Big Empty; no broad improvement
has been established. Its map-clustered direct interval is 50.00–56.82%;
paired pool gain is +1.33 percentage points, interval 0.00–3.98. It fails
the predeclared strict-positive confirmation gates.

Linear confirmation completed: **126-50 versus v2 (71.59%)**, with a
map-clustered 95% interval of **57.39–83.52%**. Across all three opponents,
linear scored 445-83 (84.28%), versus control 393-135 (74.43%). The paired
pool gain is **+9.85 percentage points**, map-clustered interval **+4.36–14.20**.
Both performance gates pass. By opponent: v2 126-50, splitter 161-15,
hunter 158-18. This is fresh-seed confirmation on familiar layouts and
scripted opponents, not evidence of a ranked-ladder Elo gain.

The evaluator-screen audit passed all 352 games and 3,782,827 exact candidate
actions, with no late splits or invalid-action deaths. Together with the role
screen: 616 games and 5,332,442 verified candidate actions. Twelve additional
history-restoring evaluator sandbox probes passed (peak 81,365,065 points,
21,954,560 bytes). The combined confirmation replay audit passed all **1,584
games and 10,383,046 exact candidate actions** (6,061,638 linear finalist
actions), 165,805 splits, zero late splits, and no invalid-action deaths.
Eight final confirmation history-restoring judge probes passed. The selected
linear bot peaked at 65,604,977 points and 21,954,560 bytes; the mature
candidate also passed but failed the performance gate. These are sampled
histories, not a worst-case runtime guarantee. No upload.

An additional full neural sandbox Big Empty game passed: 29,376 decisions,
peak 85,070,845 points and 22,020,096 bytes, no errors. It was a win, excluded
from paired strength estimates like the other integration/runtime games.

## Conditional new-layout follow-up

Before observing the linear confirmation result, froze 16 generated layouts:
four geometry/food families, two sizes each, both with and without portals.
Sizes, food parameters and layout seeds differ from prior transfer suites.
Eight new bot seeds per map/side against v2; unchanged linear and unchanged
neural models. Direct linear-neural games use one seed per map/side because
both policies are deterministic and the harness seed only changes bot RNG.
The original 768-game plan is preserved alongside a pre-test amendment to
544 nonredundant games. No transfer outcomes existed when amended.

This follow-up runs only if linear passes the original confirmation gate.
Additional linear transfer gate: four-family clustered 95% lower score bound
above 50%, with every map score at least 37.5%. Neural comparisons are
diagnostic, not a second chance to select a winner on the transfer set.

The original confirmation gate passed, so the unchanged 544-game transfer
suite ran on September 24. Linear versus v2: **210-32-14** across 256 games,
score **88.28%**, with the four-family clustered 95% interval **78.13–95.31%**.
The worst per-map score was 50% on the two large dense maps; the predeclared
transfer gate passes. Neural versus v2: **206-32-18**, score **86.72%**.
In the 32 nonredundant direct games, linear versus neural was **10-4-18**,
score 37.5%, family interval 25.00–53.13%; that small diagnostic does not
establish which ranker is stronger across future maps. Both use familiar v2
as opponent, and these four generated families are not a ladder sample.
The transfer replay audit passed all **544 games** and **6,985,884 exact
learned-bot actions** (3,508,188 linear and 3,477,696 neural), with 487,687
splits, zero late splits, and no invalid-action deaths. Eight history-restoring
judge-budget probes passed, peak 48,380,009 points and 21,757,952 bytes.
These sampled observations do not prove a worst-case runtime bound.

## Local release and next decision

All predeclared performance, replay and sampled judge-budget gates for the
linear evaluator have passed. `versions/v3` freezes that exact bot with hash
`69382825b699723d`. The upload-ready `battlebot-v3.zip` contains the bot
files at the archive root, with SHA-256
`1105b2431e317164aee40950f6527489eae621541ad8b30925339233103677b7`.
Its extracted contents have the same bot hash and no foreign imports.
`mybot`, `versions/v2`, and the previously uploaded v2 ZIP were not changed.
The user must decide whether to submit v3 for ranked games; this experiment
does not itself measure ranked Elo or play against the current top teams.

The next useful learning experiment is a new frozen comparison of linear,
neural and a simple score ensemble on additional maps, followed by ranked
replays if v3 is submitted. The neural ranker matched the fixed heuristic on
the official-map screen yet led 18-10 with four draws in the small direct
transfer diagnostic. That evidence supports further tests, not a posthoc
substitution of the current selected model.

Regression suite rerun on September 24: all 104 tests passed, including
rotation-equivalent evaluator features and unchanged RNG state for learned
decisions. Frozen v2 and the submitted ZIP remain untouched.

## Confirmation diagnostics (descriptive, no tuning)

Across the complete 528-game confirmation per policy, elimination losses fell
from 10 for control to 3 for linear; round-limit length losses fell from 125
to 80. Default remains a regression (pooled 40-8 control versus 35-13 linear),
Stronghold is unchanged at 36-12, and Trauma remains difficult at 15-33 despite
improving from 9-39. Gains are not uniform across maps.

A fixed, outcome-unfiltered subset takes the first predeclared validation
seed, both sides, all 11 maps against v2: 22 games per policy, 66 total.

| Policy | Dragon actions | Friendly head deaths | Per 1,000 actions |
| --- | ---: | ---: | ---: |
| Control | 200,254 | 1,452 | 7.25 |
| Mature role | 200,113 | 1,436 | 7.18 |
| Linear | 313,083 | 1,644 | 5.25 |

Linear produces 56.34% more actions and a 27.58% lower friendly-head-death
rate per action, but **more absolute friendly deaths**. This is compatible
with greater survival/activity, not proof of causally safer coordination;
population, match length, and opponent interactions all change. Crowding
remains unresolved. Artifacts: `diagnostics/plan.json` and `summary.json`.
