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

### Stage 2 result (27 Sep 03:06, `results/20260927-021008-ablate-5c0197`, fresh seeds 71001-71004)

| variant | pool delta [95% CI] | guard | all 15 | wins /240 |
|---|---|---|---|---|
| drop_harmful (no trap, no defend) | **+0.131 [+0.051, +0.210]** | -0.022 | +0.080 [+0.018, +0.148] | 161 (base 147) |
| lean (+ no explore, revisit, fan, hunt, goal, protect) | +0.098 [-0.057, +0.248] | +0.007 | +0.068 | 159 |
| simplified (+ no headsafe, straight, portal) | +0.005 [-0.143, +0.148] | +0.109 | +0.040 | 156 |

The trap/defend removal replicated exactly (+0.131 in both stages; +0.10 vs
v7-base, +0.06 vs nicked). Removing the neutral groups together gives the gain
back, so they stay. **B1 = v7-base with W_TRAP, W_LETHAL, W_DEFEND = 0**
(`results/v7-b1-bot`, hash b98a09bab93b8c7c).

Stage 3 launched 27 Sep 03:07: `results/20260927-030709-tune-4efc96`, space
`experiments/tuning/space_v7_b1_groups.json` (9 group multipliers 0.25-3x +
FEED_ROUND, SPLIT_UNTIL_LARGE, SPLIT_UNTIL_SMALL = 12 dims), current 10-map
pool, vs v7-base and nicked, 2 fresh seeds per generation, aligned objective,
F = plain mean over maps (`--worst-weight 0`), popsize 12, 12 workers.

### B1 held-out check (27 Sep 08:24, `results/20260927-061647-full-change-fc188d` vs `...-061649-full-change-db2585`)

Paired, same seeds 53001-53003, 15 maps, both sides, vs nicked v44, ctmes,
Python v6, leviathan3 (none used in stages 1-2):

| | B1 wins | v7-base wins | aligned delta [95% CI] |
|---|---|---|---|
| all 15 maps | 252/360 | 244/360 | +0.040 [-0.026, +0.106] |
| current pool | 161/240 | 157/240 | +0.032 [-0.065, +0.126] |
| pool vs nicked v44 | 25/60 | 28/60 | -0.035 |
| pool vs v6 | 41/60 | 37/60 | +0.104 |

Per pool map (B1 vs v7-base wins of 24): Trauma 18-11, Portals 16-11,
Default 12-8, Autarky 23-21, Prisoners Dilemma 18-17, Trophy 19-21, Devil
21-23, Schooltime 17-19, Slithery 9-11, **Queen Of Spades 8-15**.

So the stage 1-2 gain (+0.13) was mostly against the training opponents;
held out it is small and not significant. Dropping the trap penalty helps the
open ladder maps and hurts Queen Of Spades (a tight map where the room check
matters). Not upload-worthy on its own. Follow-ups: a map-dependent trap
weight (off or low on open maps, on in tight ones), and training against more
than two opponents (add nicked v44 / ctmes to the training set, keep others
held out).

### 27 Sep morning: new opponents and ladder findings (before re-tuning)

- **New sparring bots** (GitHub, triaged, in git-ignored `sparring/`), vs
  v7-base on the current pool, both sides, 2 seeds (40 games):
  cpp_nicked_v75 33/40, nicked_v75py 33/40 (same logic), nicked_lab 32/40,
  cpp_abyss 14/40, cpp_danielhe 2/40, patrick 1/40, kgts 0/40, ryuken 0/40.
  nicked v75 (27 Sep, "changed to cpp, upgrade king cashin and portal
  traversal") sweeps Prisoners Dilemma, Portals, Trauma, Slithery and
  Schooltime 4/4.
- **v7-base on the ladder** (sub 7946, 90 games): 53-37, Elo 1500 -> 1575.
  Losses are decided early: total length flat from round 30 to 100 (7 alive,
  16 total) while the opponent triples. The stall is a portal-map problem:
  Prisoners Dilemma 10/10 games, Portals 6/8, Trauma 4/9, QoS 3/8, others ~0.
  Cause: unknown portals score -60 (W_PORTAL_UNSEEN) with only +40 scouting
  bonus before game round 100, so dragons never cross; nicked values an unseen
  portal at +0.7 pearl before round 50 and ramps its penalty by the dragon's
  own age, and spreads teammates across portals.
- **Map variants:** since 27 Sep the server plays hash-suffixed variants
  (Prisoners_Dilemma_12862686, Devil_c5844559, Default_9c45bfb7, Trauma_...,
  Slithery_..., Autarky_..., Portals_...): same walls (Default: 66 edges
  differ), pearl spawn data hidden in the replay (spawners exist: pearls are
  eaten). Our hub book identifies maps by walls, so it may pull to hubs that
  moved. Local testing needs spawn-perturbed maps.

### 27 Sep afternoon: v8 code changes (C++ switches, all default off)

- Portal book regenerated from all 15 ranked maps (the 4 ladder maps had no
  entries). Changed nothing on Prisoners Dilemma: 0 portal crossings, 0/4 vs
  nicked v75. The PD stall is not portals: its fast spawners sit next to each
  team's start; in rounds 0-100 nicked ate 59 pearls (48 camping six fast
  tiles), we ate 8 while our children fanned out and explored.
- CPP_PORTAL_AGE / CPP_PORTAL_SPREAD, CPP_TRAP_OPEN, CPP_VOR: in the v8 tuning
  space (`results/20260927-132201-tune-a63e89`).
- CPP_SONAR_HUB (hub sharing over sonar, protocol-2 32-bit messages, team tag
  + checksum, rotates through known hubs, receivers keep up to 4): judge
  sandbox accepts it (no invalid actions, max 7.1M points). **It hurts on
  Prisoners Dilemma vs nicked v75**: our team is down to 1 dragon of length 3
  by round 100 in all 4 seeds (without it 5-7 dragons), 24 vs 180 pearls over
  4 games; neutral on Trauma/Portals, 2/4 vs 1/4 on Autarky. Sharing sends our
  dragons to the hub, where nicked wins the fight. The underlying deficiency is
  **losing hub contests** (nicked: paired head-on trades and walling decide
  them). Left off.
- With every switch off the build still plays 88/88 official-map games
  identically to v7-base. Hidden-spawn map extracts moved to
  `maps/server/hidden/` (a case-insensitive `trophy.map` lookup had picked one up).

### 27 Sep evening: CMA-ES upgrades and v9 run

- Research + measurement: the tuner's signal-to-noise ratio is about 1 per
  generation (candidate F spread vs 0.059 expected noise), so about half of each
  ranking is noise. Changes in `bcsim/tune.py`: `--backend cmaes-lra`
  (learning-rate adaptation, Nomura et al. GECCO 2023), `--eval-mean` (the
  distribution mean is played every generation on the same seeds: an honest
  progress curve and the final pick), `--map-sample pair` (one of each
  map/perturbed pair per generation), `--warm-from` (start from a previous
  run's CMA mean and covariance, rescaled to new bounds), `--fixed`.
- Switches taken out of CMA (poor fit for binary variables) and decided by a
  2x2 paired A/B at the gen-4 CMA mean (`results/20260927-190107-ablate-6028c1`,
  1,080 games, 3 training opponents, 15 maps, 3 seeds): portal-by-age +0.068
  [-0.011, +0.148] on the pool (and +0.07 within every tuning generation) ->
  **on**; Voronoi +0.016 [-0.080, +0.109] -> off. The gen-4 mean itself won
  156/270 (+0.29 vs v7-base, +0.32 vs leviathan3, -0.19 vs nicked v75).
- v9 run `results/20260927-194503-tune-ccc4cd`: warm start from the v8 run's
  gen-4 state, 16 dims (`space_v9.json`, bounds widened where the mean sat on
  them: food, attack, action model, goal), cmaes-lra, popsize 12 + mean,
  pair map sampling, vs nicked v75 / leviathan3 / v7-base.

### 28 Sep: v9 gen-5 mean validated -> `versions/v9`

v9 run distribution mean F by generation: +0.185, +0.278, +0.140, +0.119,
+0.208, +0.092, +0.177, +0.155 (60 games each, per-gen noise about +/-0.08:
a plateau near +0.17). Held-out paired check of the gen-5 mean vs v7-base
(`results/20260927-231030-full-change-1f35bb` vs `...-231031-full-change-51b4d9`,
nicked v44 / nicked_lab / Python v6, 15 maps, both sides, seeds 53001-53003):

| | v9-g5 wins | v7-base wins | aligned delta [95% CI] |
|---|---|---|---|
| all 15 maps | 153/270 | 124/270 | +0.174 [+0.083, +0.265] |
| current pool | 99/180 | 77/180 | +0.187 [+0.088, +0.290] |
| guard maps | 54/90 | 47/90 | +0.147 [-0.044, +0.346] |
| pool vs nicked_lab | 23/60 | 12/60 | +0.284 |
| pool vs v6 | 51/60 | 37/60 | +0.307 |
| pool vs nicked v44 | 25/60 | 28/60 | -0.030 |

Pool maps (wins of 18): Default 12-5, Autarky 18-13, Prisoners Dilemma
14-11, Portals 9-5, Slithery 5-2, QoS 8-6, Schooltime 9-7, Trauma 4-4,
Devil 13-15, Trophy 7-9. Judge sandbox (vs splitter): max 7.3M points;
"no valid action" deaths are the late king feeding (all after round 400).
Frozen as `versions/v9`, `battlebot-v9.zip` (SHA-256
940e78c139b1c7e06e7dcf19c4b17d6b483c480384cf5611646a31e8023a1d0e), verified
by extracting and playing a sandbox game.

### 28 Sep 05:20: tuning has converged; v9 stays

v9 run distribution means, gens 8-14: +0.104, +0.206, +0.069, +0.086,
+0.203, +0.247, +0.023 (average +0.134 vs +0.169 over gens 0-7), while the
mean kept drifting (food x3.4, action model x2.8, attack x3.2). The run was
stopped after gen 14 (state saved; resumable). The average of the gen 8-14
means played v9 paired on the held-out set (nicked v44, nicked_lab, v6; 15
maps, both sides, 3 seeds): 153 vs 153 wins, -0.001 [-0.070, +0.068]; pool
+0.011 [-0.069, +0.091]. No gain: the weights have converged, and v9 (earlier,
less drift) stays the candidate. Further gains need new behaviour, above all
winning hub contests against nicked-style play (nicked v75 still beats the
tuned mean, -0.19).

### 28 Sep: king beacon, big-dragon feeding, dead-end check (on top of v9)

Ladder (v9, first 30 games, Elo 1579 -> 1626): 4-5 of 13 losses were on the
longest-dragon tiebreak with more total length (e.g. QoS 11/69 vs 14/14): long
non-kings never fed the king. Kelp deaths vs nicked v75: 320/game vs their
117; 90% are length-2 children, about 70% within 3-5 rounds of birth, 91% on
Slithery Fight (children born onto a crowded two-wide fast-spawner patch).
Head-on trades with nicked are even (lost shorter 125, longer 122).

Paired test vs v9 (`results/20260928-140413-ablate-2970a3`; nicked v75,
leviathan3, v7-base, nicked v44; 15 maps, both sides, 3 seeds, 360 games each):

| variant | all 15 [95% CI] | pool | ladder 4 | wins (v9 210) |
|---|---|---|---|---|
| king beacon | +0.021 [-0.012, +0.052] | +0.027 | +0.098 | 218 |
| **beacon + big feeding** | **+0.085 [+0.032, +0.138]** | +0.059 | +0.173 | **237** |
| dead-end check (pen 400) | -0.003 | -0.008 | -0.127 | 213 |
| all three | +0.047 | +0.002 | -0.079 | 228 |

Beacon + big feeding is the v10 candidate (`results/v10-cand-bot`): positive
vs all four opponents. The dead-end check cut kelp deaths in diagnostics but
does not win games (it hurts the ladder maps), so it stays off. Next: split
safety by room (CPP_SPLIT_ROOM 8/16) and a gentle dead-end penalty (60) on
top of the candidate (`results/20260928-174742-ablate-8cf646`).

Ops note: two BSODs and three GCC segfaults this day came from stacked jobs
plus a build-cache bug (every worker recompiled every C++ bot per batch);
both fixed (`bcsim/guard.py`, `match.build_cpp_lib`).

### 28 Sep evening: kelp fixes and sonar briefing (on top of beacon + big feeding)

Paired vs the v10 candidate (247/360 wins; nicked v75, leviathan3, v7-base,
nicked v44; 15 maps, both sides, 3 seeds; `results/20260928-174742-ablate-8cf646`
and `results/20260928-180616-ablate-22301c`):

| variant | all 15 [95% CI] | wins |
|---|---|---|
| split only with >= 8 free tiles (CPP_SPLIT_ROOM 8) | -0.069 [-0.130, -0.012] | 229 |
| split only with >= 16 free tiles | -0.017 [-0.058, +0.023] | 242 |
| dead-end penalty 60 | -0.046 [-0.100, +0.005] | 234 |
| parent->child sonar brief (dead-end mask) | -0.005 [-0.027, +0.015] | 247 |
| brief + room 8 | -0.092 [-0.149, -0.041] | 221 |

None helps: the kelp deaths are cheap length-2 children, a price of fast
splitting; fewer splits or detours cost more than they save. Own-team body
deaths (18/game) are crowding (60% with no free neighbour), not
coordination. v10 = v9 + CPP_KING_BEACON + CPP_BIG_FEED only.

### 28 Sep 23:10: v10 frozen

Held out vs v9 (`results/20260928-224114-full-change-f05cec` vs
`...-224115-full-change-345748`; nicked_lab, Python v6, ctmes; 15 maps, both
sides, 3 seeds): 207 vs 198 of 270, +0.036 [+0.003, +0.073]; pool +0.028;
nicked_lab +0.053, v6 +0.029, ctmes +0.003 (59/60 both). Judge sandbox max
7.6M points (Slithery); "no valid action" deaths only from round 403 (king
feeding). `versions/v10`, `battlebot-v10.zip` (SHA-256
5927847622bf570f28cb40524f406397d03d0a9ce696194411336a3ae30393b6), verified by
extracting and playing a sandbox game.

### 29 Sep night: v9 ladder analysis, hub book tests, v11 retune

v9 ladder (128 games, 31 battles, opponents 1560-1650): 66 wins (52%).
Worst maps Default 3/14, Trauma 2/8, Slithery 5/14, PD 5/14, QoS 5/11; best
Autarky 13/13, Trophy 11/14. Losses: 25 round-500 with shorter king and less
total, 15 tiebreak with shorter king but more total, 18 eliminations.
Opponents' deliberate feeding deaths 47.6/game vs our 23.7 (plus 36 self-hits):
they feed kings about twice as hard.

Hub book A/B (25 maps = 15 + 10 perturbed; 4 opponents; 3 seeds; 600 each):
book off vs on: book maps original spawns -0.103 [-0.199, -0.006], perturbed
+0.048 [-0.083, +0.187]. CPP_HUB_OBSERVE (switch to learned hubs once observed):
current pool originals -0.104 [-0.172, -0.037], perturbed +0.003. The book is
a good prior even with shuffled spawns: kept on, observe off.

v11 retune `results/20260929-013847-tune-c7cd3d`: base v10 (current code),
warm start centred on v10 with the v9 run's covariance (`--warm-mean base`),
17 dims (`space_v11.json`: king-feeding ranges widened, economy settings
added, dead-end penalty 0-150 with look 12), 4 opponents, current + perturbed
maps (pair sampling), cmaes-lra, mean played each generation.

### 29 Sep: v11 retune and follow-up research (none beats v10 robustly)

- v11 retune (gens 0-8, mean of gen 5-8 means) vs v10: held out (nicked_lab,
  v6, ctmes) 205 vs 207, -0.029 [-0.117, +0.048]; training opponents on fresh
  seeds 232 vs 212, +0.048 [-0.025, +0.123], but -0.059 vs nicked v75 and
  +0.152 vs leviathan3: overfits the easy opponent. Not adopted.
- v10 vs nicked v75 (40 recorded games, 15/40 won): we eat more pearls (604 vs
  454/game) and reach the same total, but nicked's longest dragon is 11 at
  round 300 (ours 4) and 23 at 490 (ours 17); it feeds more (29 vs 12.5
  deliberate feeding deaths/game) and sprints a little (4/game, we 0).
  Trophy 0/4 (by round 100 nicked has 103-111 total vs our 15-16: our
  dragons wander to nicked's side while it takes the centre hub), Schooltime
  0/4 (their feeding deaths 72-147 vs ours 6-22), Slithery 0/4 (our kelp
  deaths 940-1340 vs 340-470), PD 0/4 (early eliminations).
- CPP_ANCHOR (founders stop splitting from round 80/150, as nicked's anchors):
  neutral (-0.005..+0.014 over 450 games); anchored founders get killed.
- Stronger far hub pull (HUB_FAR_MULT/HUB_SCALE): +0.044 [-0.011, +0.101]
  first, then -0.056 [-0.136, +0.017] and -0.058 on fresh seeds with v6 added:
  the first result was noise. Exploration goal off: +0.010.

Lesson: first-pass effects of +0.04 are within noise (paired CI about +/-0.05
at 450-540 games); only fresh-seed confirmation counts. v10 stays the best.

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
