# Feature-efficiency experiment (v8 plan, drafted 2026-09-26)

**Status (26 Sep 21:45):** stage 1 running, `results/20260926-214429-ablate-346278`
(18 groups + base, vs v7-base and nicked, 15 maps, both sides, 4 seeds, 4,560
games, aligned objective, in-process C++, 12 workers).

**Question:** which of the bot's features earn their place, and what is the
smallest feature set that, once tuned, beats v6.1 (`versions/v7-base`, the
C++ port with v6.1 parameters) and nicked v44?

**Starts after** the cloud's in-process C++ build (`CLOUD_TASK_3.md`) is merged
and passes parity locally. Runs locally. The user uploads bots.

## 0. Why (evidence so far)

- The 14-generation CMA-ES run (`20260926-001535-tune-79f3f9`, 21 parameters,
  old engine, 1 seed) learned almost no structure: covariance condition number
  2.0, every principal direction 3-7% of variance. A linear model on all 21
  parameters predicts F worse than the mean (cross-validated R^2 -0.04); only
  W_SPAWN (-0.32), W_PEARL (+0.26) and DEPTH_MAX (-0.25) correlate with F.
- Its best candidate's gain vanished on 3 seeds (V7_EXPERIMENT.md, "unswbc
  1.1.0 re-check"): too many dimensions for the signal.
- Parameter counts elsewhere: ctmes CMA-tuned 25 of about 40 parameters and
  still loses to us about 20/22. nicked (strongest) has 55 (v34) / 98 (v44)
  hand-set constants and no sign of automated tuning. Kraken varies 3 of 17
  per map. We have 93 constants and tuned 21-25. Tuning improves a design;
  it does not replace one.

## 1. Evaluation protocol (used by every stage)

**What the site rewards (docs re-read 27 Sep):** a game is won by elimination,
else at round 500 by the longest living dragon, then total length, else a draw.
Elo moves once per ranked battle (5 games on random maps) by the **fraction of
games won** (draw = half); the size of a win never counts. So the target is
expected games won on the maps being drawn. The aligned score below is a lower-
noise stand-in for that; the win column is the ground truth.

**Current ranked rotation** (sampled from public ranked battles):
since about 26 Sep 14:00-16:00 UTC, 10 maps: Trophy, Queen Of Spades,
Default, Devil, Trauma, Schooltime, Autarky, Prisoners Dilemma, Slithery
Fight, Portals (`official_suite.CURRENT_POOL`). Default Small, Stronghold and
Big Empty left then; Arena and Colosseum have not appeared since at least
25 Sep 12:00. **Decisions use the current pool; the other 5 maps are a
regression guard** (the pool changed twice in two days). Reports show both.

- **Maps:** the 11 official maps (required by CLAUDE.md) plus the 4 ladder-only
  maps (Autarky, Prisoners Dilemma, Slithery Fight, Portals) = 15. Report
  official-11 and ladder-4 separately as well as combined.
- **Both sides, K engine seeds** (unswbc 1.1.0 seeds pearl spawns). Every
  variant in a comparison plays **the same (map, side, seed) set**, so results
  are paired.
- **Opponents:**
  - training/screening: `B0` (= v7-base) and nicked v34;
  - held out (final stage only): nicked v44, ctmes, Python v6, leviathan3.
- **Metric:** the win-aligned per-game score (`bcsim.margin` "aligned"):
  0.5 x result (+1/0/-1) + 0.25 x final longest-dragon share + 0.25 x the
  time-averaged total-length margin; eliminations score +/-1. The round-500
  tiebreak is the longest living dragon, and the length-only margin disagreed
  with the result in 36 of 180 v7-base vs nicked games (26 wins with less
  total length, 10 losses with more) and in ranked play (a Slithery Fight loss
  with 277 vs 52 total length, 27 vs 30 longest). Wins reported alongside.
- **Statistics:** paired difference vs B0 on identical (map, side, seed)
  blocks; 95% bootstrap CI resampling (map, seed) blocks. With 18 variants
  screened at once, a result counts only if it **replicates on a fresh seed
  set** (screen, then confirm).
- **CPU:** any variant that raises search effort gets a judge-sandbox check
  (`unswbc run --sandbox`, max < 60M points per turn).

Noise measured 26 Sep (length margin, v7-base vs nicked, 6 seeds): seed-to-seed SD
0.33 per (map, side) cell, so K = 4 seeds with 2 opponents gives a paired CI
half-width of about 0.06 (worst case, ignoring the positive correlation of paired
games). Stage 1 therefore uses K = 4. Original plan text: B0 vs nicked v34, 15 maps x 2 sides x 6
seeds (180 games). From the per-block SD, pick K so the CI half-width on a
paired margin difference is about 0.03 (expected K = 3-4).

## 2. Stage 1: leave-one-group-out ablation

Group the scoring terms into features and remove one group at a time (weights
set to 0 in `params.hpp`, booleans off). Each ablated bot plays B0 and nicked
v34 on the protocol set.

| # | group | parameters set to 0 / off |
|---|---|---|
| 1 | food | W_PEARL, W_MEM_PEARL |
| 2 | spawn anticipation | W_SPAWN |
| 3 | unseen/stale exploration | W_UNSEEN, W_STALE |
| 4 | room/trap | W_TRAP, W_LETHAL |
| 5 | dead end / corridor | W_DEADEND, W_CORRIDOR |
| 6 | head safety | W_HEAD_ENEMY, W_HEAD_TEAM, W_AHEAD |
| 7 | revisit | W_REVISIT |
| 8 | fan-out | W_FAN_EARLY, W_FAN_LATE |
| 9 | straight bias | W_STRAIGHT |
| 10 | portals | W_PORTAL, W_PORTAL_UNSEEN, W_PORTAL_SCOUT (+ PORTAL_BOOK off) |
| 11 | v3 learned action model | W_V3 |
| 12 | attack/trade | W_ATTACK, W_TRADE |
| 13 | hunt | W_HUNT |
| 14 | defend | W_DEFEND |
| 15 | hubs | W_HUB (+ HUB_BOOK, LEARN_HUBS off) |
| 16 | exploration goal | W_GOAL (+ GOAL off) |
| 17 | king feeding | W_CASH, FEED_ROUND past 500 |
| 18 | king protection | PROTECT_MULT = 1, PROTECT_FOOD_MULT = 1 |

The split economy (SPLIT_AT, CHILD, CAP, FLOOR, timings) and search size are
structural, not removable; they stay in the tuned set.

Sonar is not in this table: it is inert in v6 and absent from the C++ bot
(see stage 4).

Tooling: `python -m bcsim.ablate` with `experiments/features/groups_v7.json`.

Cost: 18 variants x 2 opponents x 15 maps x 2 sides x K=3 = 3,420 games.
Output per group: paired delta-margin vs B0 with CI, by map group. Classify:
- **essential:** removing it hurts (CI below 0);
- **neutral:** CI spans 0: candidate to drop;
- **harmful:** removing it helps (CI above 0): drop.

**Stage 1b (optional, cheap, explains the ablation):** log every term's value
per decision for ~20 games (the Python core matches the C++ core exactly)
and report (a) the correlation matrix / PCA of term values, to find redundant
pairs, and (b) the **decision-flip rate**, meaning how often removing a term
changes the chosen move. A term that almost never flips a decision is dead
weight whatever its weight.

### Stage 1 result (27 Sep 02:10, `results/20260926-214429-ablate-346278`)

Aligned objective, delta from removing the group (negative = the group helps),
current 10-map pool with 95% CI; guard = the other 5 maps.

| group | pool delta [CI] | pool verdict | guard | all 15 |
|---|---|---|---|---|
| v3 learned action model (W_V3) | -0.355 [-0.463, -0.252] | essential | -0.271 | essential |
| food | -0.255 [-0.376, -0.137] | essential | -0.235 | essential |
| spawn anticipation | -0.123 [-0.218, -0.014] | essential | -0.099 | essential |
| hubs | -0.115 [-0.200, -0.033] | essential | +0.051 | neutral |
| room/trap | +0.131 [+0.024, +0.231] | **harmful** | -0.066 | neutral (ladder maps +0.315) |
| defend | +0.025 [-0.020, +0.068] | neutral | +0.118 | **harmful** (+0.056 [+0.016, +0.098]) |
| attack | -0.029 [-0.130, +0.066] | neutral | -0.195 | essential |
| feed | -0.038 | neutral | -0.086 | neutral (-0.054, CI to +0.001) |
| dead end | -0.029 | neutral | -0.052 | neutral |
| exploration, revisit, fan, hunt, goal, protect | +0.008 to +0.055 | neutral | | neutral |
| head safety, straight, portals | -0.017 to -0.004 | neutral | | neutral |

Base (v7-base) won 141/240 (vs itself 50%, vs nicked +0.267 aligned). The
aligned score is noisier than the length margin (per-cell SD 0.65 vs 0.33),
so CIs are about +/-0.10 at K = 4 with two opponents.

## 3. Stage 2: simplify

`B1` = B0 with every harmful group removed and neutral groups removed
together. Confirm on a **fresh** seed set that B1 >= B0 (paired CI not below
0). If the joint removal hurts, restore neutral groups one at a time (largest
single-group delta first) until it does not.

## 4. Stage 3: tune the compact set with group multipliers

Tune **one multiplier per kept group** (scaling that group's weights from
their v6.1 values), plus the structural knobs that showed signal: at most
about 10 dimensions instead of 25.
- Tooling: add group multipliers to the tuning space file (`bcsim.tune` maps
  each multiplier onto its member weights), and teach `write_params` booleans.
- CMA-ES: popsize 10, sigma 0.25, 3 fresh seeds per generation, 15 maps,
  opponents B0 and nicked v34.
- Stop when the CMA mean's F has not improved for 4 generations.
- Candidates: the mean of the last 5 generations' means (ctmes found this beat
  single best points) plus the top 3 single candidates.

## 5. Stage 4: forward selection of new features

Add candidate features one at a time to the tuned compact bot, each behind
its switch, each on the protocol set with confirmation seeds:
- dead-end corridor check that respects the no-reverse rule (ladder
  analysis: 43 kelp deaths per game vs 26 for opponents, 513 on Slithery
  Fight);
- larger search (N_SEARCH, DEPTH_MAX) with the CPU meter (`CPP_BUDGET`);
- path distances (`CPP_PATH_DIST`), beam (`CPP_BEAM`);
- Queen of Spades / Portals handling (negative for every candidate so far);
- **sonar**, which cannot be ablated because it does nothing today. v6 only
  broadcasts a public king beacon (fixed magic `0xBC`, unencrypted, rounds
  400+, length >= 6) that our own dragons decode and discard
  (`framework/v4_sonar.py`), and the C++ port omits it. Candidates, each
  behind its own switch in the C++ bot (cloud):
  - **S1 king beacon routing:** the king broadcasts its position; feeding
    dragons route toward it before it is in view (today the feed pull only
    starts once the king is visible);
  - **S2 hub / pearl-cluster sharing:** a dragon that sees a rich cluster
    broadcasts it and far dragons get a pull (nicked broadcasts pearl
    clusters of 3+ with an encrypted scheme);
  - **S3 enemy-head warnings:** broadcast the nearest large enemy head and
    steer away (ctmes tried this: no measurable edge over 1,056 games, so
    lowest priority);
  - encode with a keyed checksum so opponents cannot read or spoof it, and
    count the judge's per-write CPU cost in the sandbox check.
Keep a feature only if it replicates; re-tune its own weight only.

## 6. Stage 5: final validation and success criteria

Held-out opponents (nicked v44, ctmes, Python v6, leviathan3) and B0, 15 maps,
both sides, 6 fresh seeds; judge-sandbox CPU on the largest maps.

**Success:** vs B0 (v6.1) paired margin CI above 0 and wins >= 55%; vs nicked
v44 wins >= 50% (B0 today: 32/66 = 48%); no official map worse than B0 by more
than 0.10 margin. A candidate that meets this with fewer features than B0
wins ties.

## 7. Budget (per game about 4 s wall at 8 workers today; the cloud change should roughly halve it)

| stage | games | now | after speedup |
|---|---|---|---|
| noise measurement | 180 | 12 min | 6 min |
| stage 1 ablation | 3,420 | 4 h | 2 h |
| stage 1b logging | ~20 (Python) | 30 min | 30 min |
| stage 2 confirm | ~360 | 25 min | 12 min |
| stage 3 CMA (<=15 gens) | ~13,500 | 15 h | 7-8 h |
| stage 4 (per feature) | ~360 + confirm | 25 min | 12 min |
| stage 5 | ~1,800 | 2 h | 1 h |

Stage 1 is the overnight-friendly first run; stage 3 is the next night.
