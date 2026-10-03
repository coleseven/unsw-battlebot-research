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

### 29 Sep afternoon: Trophy opening, nicked v92, king growth

- Trophy trace (founders' per-move term breakdown, results/make_dbg_bot.py):
  the v3 local ranker decides moves (85-205 points, 10-30 between moves);
  the hub term changes by about 1 point between moves, and walls block the
  straight-line pull, so founders drift along the edges.
- CPP_BOOK_MAP (fill the identified book map's open edges, so paths to hubs
  are known from turn one) vs v10, 6 opponents, 15 maps, 3 seeds (540 games):
  +0.150 [+0.073, +0.236] current pool, +0.122 [+0.054, +0.191] all 15, wins
  378 vs 335, positive against every opponent (+0.259 vs nicked v75); ladder
  maps +0.000 (no book to fill). With CPP_HUB_GRAD 15: -0.156; 8: +0.010
  (the per-step pull hurts). Fresh-seed confirmation (seeds 153001-3, nicked
  v92 added, leviathan3 kept, v6 dropped): +0.118 [+0.033, +0.203] current
  pool, +0.090 [+0.019, +0.164] all 15, wins 316 vs 280, positive against
  all six (v92 +0.027, v75 +0.164). Adopted: base for further tests is
  results/v10g-bot (v10 + CPP_BOOK_MAP 1).
- New public bots (GitHub check): nicked v92 (arch4) and abyss's live
  submission (wall-clock search, validation only). v10 vs nicked v92: 8/40
  on the current pool (v75: 14/40); 0/4 on Portals, PD, Slithery, Trauma,
  Schooltime, Trophy.
- King growth (strategy from nicked, our own code): our protected long dragons
  keep splitting while the team has fewer than FLOOR (24) units; nicked's stop
  at a quarter of the cap and then only split a 2-child every 5 rounds.
  Switches CPP_PROTECT_FLOOR, CPP_RESCUE_EVERY, and CPP_FEED_SHIFT_LARGE
  (cash-in schedule earlier on big maps, as nicked's BIG_CASH_SHIFT).
  Round 1 on v10g (seeds 161001-3, 540 games each): floor 16, floor 16 +
  rescue 5, floor 10 + rescue 5 all within +/-0.013 (they barely trigger:
  SPLIT_AT 4 splits a dragon at length 4, before PROTECT_LEN 5 makes it
  protected). shift40 +0.026 [-0.007, +0.064] pool, +0.036 [+0.011, +0.064]
  all 15, wins 344 vs 325. Round 2 (seeds 171001-3): shift40 again, and
  PROTECT_LEN 4 alone / with floor 16 + rescue 5 / plus shift40.
  Round 2: PROTECT_LEN 4 -0.185 [-0.269, -0.106] pool (285 vs 329 wins);
  with floor 16 + rescue 5 -0.302 (250); plus shift40 -0.324 (247). Growing
  kings early is badly worse for us, against every opponent: our strength is
  many small dragons. shift40 +0.004 pool, +0.029 [-0.000, +0.061] all 15
  (344 vs 329); both rounds together 688 vs 654 wins and positive vs both
  nicked versions each time: adopted (v10h = v10 + book map + shift40).
- v12 retune (results/v12-tune-dir.txt): warm from the v11 run's covariance,
  centred on v10h, space_v12 (17 dims: v11 minus CPP_DEADEND_PEN plus
  CPP_FEED_SHIFT_LARGE), strong opponents only (nicked v92, v75, v44, lab,
  v7-base; leviathan3 held out after it overfit v11), current pool + perturbed
  copies (pair sampling), seed 181001, popsize 12, sigma 0.2.
  Result: distribution-mean F +0.086 (gen 1), +0.080 (gen 5), then down to
  -0.280 (gen 11); the final mean drifted far from v10h (food x2.9, attack
  x2.2, feed x2.1). Per-generation scores are confounded by seed and map
  sampling, so the final and gen-5 means are judged in the paired ablate below.
- Review defects (TOP_100_RESEARCH.md, checked in source): CPP_HUB_SEP_FIX
  (learned hubs' 5-cell spacing used max of the wrapped distances, so it
  never applied) and CPP_V3_PORTAL (v3 scores a portal move by the cells
  beside the head, not the far end). Ablate on v10i (= v10h behaviour), seeds
  191001-3: hubsep, v3portal, both, v12tune (final mean), v12gen5 (gen-5 mean).
  Result (540 games each; base 339 wins): hubsep +0.011 [-0.016, +0.040]
  pool, 342 wins (Portals up, Autarky down, v92 +0.001); v3portal -0.043
  [-0.095, +0.006], 330; both -0.033, 332; v12tune -0.091 [-0.192, +0.002],
  317, v92 -0.185; v12gen5 -0.087 [-0.175, +0.001], 324, v92 -0.100. None
  adopted; the broad retune made the bot worse against the strongest
  opponent. v10h stays the incumbent.
- CPP_KB_V2 (king beacon v2, same 32 bits): tag 5 | x 6 | y 6 | length/4 (4)
  | origin round mod 8 | king token = id mod 16 | checksum 4. Relays keep the
  origin round (a dead king expires after the TTL, capped at 7); ties go to
  the lower token; a stored king is dropped when the cell it must be near is
  in view without its head; feeders bind to the head carrying the token.
  Smoke test (4 games vs v75) runs; ablate on v10j (= v10h), seeds 211001-3:
  kb2, kb2 + hubsep.
  Result (540 games each; base 314 wins): kb2 +0.033 [+0.009, +0.060] pool,
  +0.018 all 15, 323 wins; kb2hub +0.041 [+0.003, +0.085], 324. Mostly from
  easy opponents (leviathan3 +0.087; v92 -0.034): current-pool wins vs the
  strong three (v92, v75, lab) 65/180 vs base 62/180, vs the easy three 140 vs
  132. Not established; fresh-seed confirmation of kb2 alone (seeds 221001-3).
- CPP_FEED_REACH (F1): feed only if the king's head can walk (in view, through
  free cells and our own body) to our body within this many steps; the old
- kb2 confirmation (seeds 221001-3; base 303 wins): +0.017 [-0.020, +0.060]
  pool, 308 wins; strong three on the pool 55/180 vs 56/180, easy three
  143 vs 136. Same pattern as the first run: gains only against easy
  opponents. Not adopted alone; kept as an option under feeding changes.
  check was a 2-4 geometric distance that ignores kelp and bodies between.
  Ablate on v10k (= v10h), seeds 231001-3: reach4, reach6, kb2 + reach4.
  Result (base 329 wins): reach4 +0.030 [-0.014, +0.078] pool, 333 wins
  (strong three on the pool 82 vs 76/180, guard 31 vs 35/90); reach6 +0.004,
  325; kb2reach4 +0.022, 326; all slightly negative vs v92. Not adopted.
- v92 loss anatomy (630 base games vs v92 from the 29-30 Sep runs): wins by
  map Autarky 8/42, Colosseum 21, Devil 16, Portals 1, PD 0, Slithery 2,
  Trauma 7, Arena 10, Big Empty 7, Default 15, Default Small 7, QoS 18,
  Schooltime 6, Stronghold 19, Trophy 11. Round-limit losses are lost on the
  longest dragon with similar or more total length (medians, ours/theirs:
  Autarky 12/26 longest, 86/52 total; Big Empty 55/77, 588/556; Slithery
  36/54, 184/204; Schooltime 36/60). Eliminations dominate PD (41 of 42,
  median round 221), Default Small, Arena, Trophy.
- CPP_KING_GRAD: per-step pull (walking distance, PathDist) toward the
  feeding target. Ablate on v10l (= v10h), seeds 241001-3: kgrad10, kgrad25,
  kgrad25 + kb2.
  Result (base 327 wins): kgrad10 -0.011, 318; kgrad25 -0.022, 319;
  kgrad25kb2 -0.013, 316; mean longest dragon vs v92 19.1 (base) vs 19.2-19.7:
  the pull is not the bottleneck. Not adopted.
- Feed trace of 6 new replays vs v92 (results/v92-diag, v10h behaviour):
  late sacrifices per game ours 0-19 vs v92's 22-100 (Big Empty 19/9 vs
  36/100, Schooltime 9/6 vs 60/84, Autarky 0 vs 22); v92's team eats 3-4x more
  of its own corpses late. Our king gets its share when feeding happens; the
  volume is missing: only length <= FEED_MAXLEN (5) dragons feed, and only
  near a visible king twice their length. Ablate on v10l, seeds 261001-3:
  sum64 (FEED_MAXLEN 64, KING_GRAD 10), sum12 (12), sum64early (+ FEED_ROUND
  380).
  Result (base 348 wins): sum12 +0.034 [-0.003, +0.070] pool, +0.028
  [+0.001, +0.056] all 15, 362 wins; strong three on the pool 80 vs 69/180;
  positive vs v92 (+0.027), v75 (+0.071), lab (+0.035); mean longest vs v92
  21.3 vs 18.5. sum64 +0.013, 355 (strong 75); sum64early -0.003, 349 (strong
  80, easy pool 139 vs 148). First change that moves the mechanism and helps
  against the strong opponents. Confirmation of sum12 and sum64, seeds
  271001-3.
  Confirmation (base 323 wins): sum12 -0.017 [-0.050, +0.024] pool, 322
  wins, strong three on the pool 66 vs 67/180; sum64 -0.030, 316. Did not
  replicate. Both runs together sum12 684 vs 671 wins of 1080; vs v92
  consistently positive (+0.027, +0.049; longest dragon +2.5 both times, v92
  wins 30 vs 28 and 20 vs 16 of 90), vs v75 +0.071 then -0.051. Small real
  mechanism effect, no established win gain. Not adopted.

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

### 30 Sep evening: v10h uploaded; move ranker refit (R4)

- v10h frozen (versions/v10h, bot hash f9d00cd150ff2c53, battlebot-v10h.zip),
  judge sandbox max 7.9M points/turn; active on the ladder by 21:59 UTC.
- Prisoners Dilemma vs v92 (4 games): both sides stay small (~20 total), but
  v92 eats 221-399 pearls per game to our 29-82 and splits 83-146 times to our
  14-33; we lose ~7 dragons to kelp in rounds 0-50. Food finding, not fights.
- Move ranker refit (bcsim/ranker_v4.py): 300 local games of nicked v92 vs our
  five strongest bots on all 15 maps (2 seeds, both sides), v92's single-step
  moves with at least two candidates, 25% sample, the same 24 features;
  split by (map, seed). ~650k examples. Linear softmax (LBFGS, l2 by dev nll):
  test accuracy on v92's moves 60.7% vs 57.9% for the old v3 weights (nll
  0.820 vs 0.835). Largest changes: friendly_near -2.3 -> -6.3 (avoid
  teammates), space_x_length +0.1 -> +6.4 (long dragons seek room), food_count
  -0.7 -> -6.1 (nearest pearl over clusters). Weight norm 1.76x the old.
  Stored in framework/ranker_r4.json, emitted as model::WEIGHT_R4 behind
  CPP_V3_R4. Ablate on v10m (= v10h), seeds 301001-3: r4 (W_V3 24.7), r4eq
  (W_V3 14.06, the old norm), r4lo (W_V3 9).
  Result (base 347 wins): r4 -0.044 [-0.149, +0.060] pool, 333 wins; r4eq
  -0.053, 326; r4lo -0.175 [-0.283, -0.078], 291. Strong three on the pool
  71/71/53 vs 76. Better imitation of v92 (60.7% vs 57.9%) made our bot
  worse: v92's moves fit v92's own search, splitting and feeding, not ours.
  A weaker ranker (W_V3 9) hurts a lot, consistent with the stage-1 finding
  that v3 is our most important term. Not adopted. Next ranker step, if any:
  labels from our own bot's outcomes (search/rollout teacher on states our bot
  visits), not imitation of another bot.

### 30 Sep night: Prisoners Dilemma food

- PD's food is 12 cells that respawn every round (x=14 and 17, y=0-2 and
  13-15, two 6-cell blocks across the vertical wrap); the middle diamond
  respawns every 150-250 rounds, x=15/16 every 480. Before round 150 v92 eats
  94-116 pearls from the fast cells, we eat 16-38, though our founders start
  beside them.
- Hub log (results/make_hubdbg_bot.py, 1 game): founders starting on the left
  edge never see a spawner timer and have no hubs all game; dragons that know
  the hub wander away from it (the hub pull is drowned again); learned hubs
  bunch on one patch (the spacing bug).
- PD-only probe vs v92 (diagnostic, 6 games per variant): base 0/6, 50
  pearls/game; CPP_SONAR_HUB 2/6, 161; + CPP_HUB_SEP_FIX 0/6, 36 (spreading
  hubs sends dragons to slow cells); + sep + W_HUB x3 1/6, 123; + sep + goal
  off 2/6, 225. Fresh seeds: sonarhub 3/6, 226; + goal off 1/6, 168; + W_HUB
  x3 2/6, 274; + every 2 rounds 1/6, 158. CPP_SONAR_HUB alone 5/12 vs v92 on
  PD (base 0/42 earlier today). It hurt on PD on 27 Sep (v7-era bot vs v75),
  so the full suite decides: ablate on v10m, seeds 311001-3: sonarhub,
  sonarhub + W_HUB x3.
  Full suite (base 343 wins): sonarhub -0.011 [-0.065, +0.042] pool, 337
  wins: PD 15 -> 20 of 36, but Slithery 24 -> 16 and Portals 21 -> 17 (book
  maps identical: sharing only matters without a book). sonarhub + W_HUB x3
  -0.193, 293. Not adopted as is.
- Absolute learned-hub richness (5x5 respawn-rate sum, logged per dragon vs
  v92): PD median 2.0-2.5 (max 5.0), Slithery 1.5 (max 7.1), Portals 0.8-1.9,
  Autarky 1.2-2.3: a richness threshold (CPP_SONAR_HUB_MIN, added) cannot
  separate PD from Slithery. Likely difference: on PD the hub-less dragons are
  founders that never see a spawner; on Slithery they are newborns that would
  find food themselves and get crowded onto one hub. CPP_SONAR_ADOPT_AGE: adopt
  a shared hub only after this many rounds alive without one. Ablate on v10n
  (= v10h), seeds 331001-3: adopt age 15, 30, 60.
  Result (base 333 wins): age15 -0.014, 331 (strong pool 55 vs 63); age30
  +0.026 [+0.001, +0.054] pool, +0.017 [+0.001, +0.036] all 15, 340 (strong
  65); age60 +0.028 [-0.001, +0.066], +0.019, 342 (strong 66). PD 17/16/14 vs
  15 of 36, Slithery 19/20/25 vs 16, Portals 18/20/20 vs 19: the Slithery and
  Portals losses are gone but so is the PD gain (per-map counts of 36 vary a
  lot between runs: base Slithery 24 in the previous run, 16 here). Mildly
  positive overall; confirmation of age30/age60 on fresh seeds 341001-3 with
  the 10 perturbed layouts added (25 layouts).
  Confirmation (seeds 341001-3, 15 maps + 10 perturbed = 25 layouts, 900
  games each; base 542 wins): age30 +0.038 [-0.004, +0.085] pool, +0.038
  [+0.010, +0.065] all layouts, 563 wins; strong three pool 66 vs 63,
  perturbed 74 vs 68; vs v92 +0.060. age60 +0.020, 552. **age30 replicated**
  (+0.026, then +0.038 pool). Not the PD-specific fix (PD gain not kept) but a
  small robust overall gain: candidate **v10o** = v10h + CPP_SONAR_HUB 1 +
  CPP_SONAR_ADOPT_AGE 30 (versions/v10o, bot hash 7623b9aa5ef6172b); judge
  sandbox check pending.

### 1 Oct: Sprint, unseen maps, R5 mover

- Sprint 1 (591 teams, best of 7, 7 unseen maps; v10h played): seed 131, bye,
  beat Split and Stack 6-1, lost to Citadel Insecurities 1-6 (won Stripes, drew
  weakhold; longest 62/64 on Maze, 29/43 on Around UNSW with more total, Tower
  Defense 62 vs 771 pearls). Maps extracted to maps/server; panel
  `official_suite.sprint_maps()`. The ladder still drew the 10 known maps
  afterwards (14:51 UTC sample).
- Unseen-map baseline (results/sprint-baseline, 2 seeds, 6 opponents, both
  sides): v10h 58/168 (35%), v10o 52/168; v10h loses even to v7-base 4/28 and
  leviathan3 6/28 there (it beats them easily on known maps). Tower Defense
  0/24, Australia 2/24, Stripes 4/24, Around UNSW 6/24.
- R5 mover (NEW_MOVER_RESULTS.md): counterfactual teacher sound, labels
  chaos-dominated; the trained residual lost games (tau 0.5: 184 vs 270 of
  528). Stopped; incumbent kept.
- Unseen-maps diagnosis: v10h differs from v7-base mainly in CMA-tuned weights
  tuned on known maps (food x2.2, W_V3 x2.5, attack x2.8, weaker trap/lethal
  and fan) plus king beacon/big feed. Grouped ablate on v10q (= v10h), 11
  official + 7 Sprint maps, 2 seeds 421001-2: all v7 weights, then v3, food,
  safety, fight, explore groups at v7 values, and king beacon + big feed off.
- **Correction (1 Oct evening): the unseen-map results above are invalid.**
  All 7 Sprint map extracts have zero pearl spawners (the server hides them in
  replays); `bcsim/scrape.py` filed them as normal maps because its spawner
  check matched the `TILE_COUNT` header line (fixed: "TILE " with a space; the
  7 extracts moved to maps/server/hidden/). Local games on them had almost no
  food (Tower Defense: 24/24 draws with 0 pearls eaten; Stripes 18/24 draws),
  so the "35% on unseen maps / loses to v7" finding and the grouped unseen-map
  ablate (no group differed: 50-64/168) measured spawner-less maps, not
  generalisation. Books probe on them: map fill off identical, all books off
  48 vs 58. All 15 ranked maps do have spawners (checked), so earlier
  evaluations stand. Next: reconstruct the Sprint spawners from the real
  replays' pearl appearances.
- Sprint spawners reconstructed (`bcsim/spawn_reconstruct.py`): a pearl that
  appears in a phase with no death is a spawn; take-to-respawn gaps give the
  delay range (10th-90th percentile); evidence pooled with the mirror cell
  (engine convention: SYMMETRY y flips x, x flips y, xy is a point
  reflection). Validated on PD (true spawners known): 56 found, 0 false; 8 of
  12 every-round cells found fast; slow delays rough. Built from 57 real games
  per map into maps/sprint/ (70-350 spawners each); all 7 play.
- **Corrected unseen-map baseline** (results/sprint-baseline, 2 seeds 361001-2,
  6 opponents, both sides): v10h 82/168 (49%), v10o 83/168. v10h vs v92 4/28,
  v75 9/28, lab 9/28, v44 14/28, leviathan3 26/28, v7-base 20/28. Weakest maps:
  Tower Defense 4/24, weakhold 7/24, Islands 10/24; strongest Stripes 23/24.
  Against this panel v10h wins ~62% on the known maps: a moderate
  generalisation gap, concentrated against the strong opponents. v10o is no
  worse on unseen maps than v10h.

### 1-2 Oct night: queen rules (Slay Queen, unswbc 1.2.3)

- Rules changed 1 Oct (official /updates): queens (ids 0/1) score first, then
  longest dragon, then total length; ceil(len/4) free steps per move; ratings
  reset and all submissions idled; unswbc 1.2.3 (its 15 bundled maps equal our
  ranked suite). Astra's Q0 groundwork verified: isolated 1.2.3 runtime
  (`bcsim.queen_runtime`), 6 engine rules tests pass, queen diagnostics, wins
  objective. v10o legal under 1.2.3 (sandbox max 8.0M); uploaded ~00:48 UTC 2 Oct.
- Q1 baseline (v11a = v10o settings, 1.2.3, 15 maps, 6 opponents, both sides,
  2 seeds 431001-2): 200/360 wins; **our queen alive at round 500 in 10/360**
  (median death round 84-87), theirs 43; of 234 round-limit games only 23 were
  decided by queen length. Queen deaths in 12 diagnostic games: 5 walls/kelp
  (often length 2-3, as early as round 10), 4 enemy head-ons, 3 our own dragons.
- Q1 CPP_QUEEN (Astra's mode: queen protected, no late splits, feeding only to
  the queen by id, king beacon off): q_on 148/360 (queen alive 28), q_nosplit
  147 (31), q_late 158 (33); strong three 42-48 vs 71/180. Worse overall; the
  opponent's queen also survives more (50-66 vs 43).
- Q2 CPP_MULTISTEP (extra free steps only to grab a visible pearl): legal,
  rarely triggers (dragons split at 4 = one free step).
- Q3 (seeds 441001-2; base 216/360): q_ms 175; q_ms_s7 100; q_ms_s11 83; q_s7
  86; ms_s7 126. Splitting later (bigger, faster dragons) is a large loss: the
  small-dragon economy dominates. Pending: multistep alone (Q3b) and queen
  safety switches (Q1b: multi-step enemy reach, queen dead-end look-ahead,
  worker guard, safety multiplier, king beacon kept).
- Tooling: ablate now takes the guard lock before deleting a partial variant
  (a waiting resume deleted 33 replays of a running variant; that run was
  redone). Overnight jobs run as detached chains (results/overnight_chain*.sh).
- Queen death diagnosis (debug bot logging the queen each turn, 12 games, full
  queen-safety settings): 11/12 queens died; 7 enemy head-ons at length 12-20
  with 1-2 legal moves and enemy heads in view; 4 boxed in early (Portals,
  Autarky, rounds 10-50, zero legal moves; the queen splits a 2-child and still
  dies). Scoring-level safety terms cannot fix positions already short of moves.
- Q1b (seeds 461001-2; base 210): q_kb (queen mode, king beacon kept) 181,
  queen alive 27; qs_reach 178 (27); qs_dead 182 (29); qs_full 174 (29);
  qs_full_nosplit 166 (28). The king beacon explains part of the queen-mode
  loss (q_on 148 vs 200 in Q1); none of the safety terms moves queen survival.
- Q1c (seeds 491001-2; base 207, queen alive 9): wider enemy-reach margin +2
  qx2 169 (queen alive 32), +3 qx3 170 (32), qx2_nosplit 167 (33). Queen
  safety triples survival but costs 30-40 wins against this old-rules panel.
  Caveat: the panel's opponents do not protect their own queens, so most local
  games still end with both queens dead and are decided by longest dragon; on
  the reset ladder, opponents adapting to queen scoring will make a dead queen
  far more costly. A queen-aware sparring opponent is needed before judging.
- **Q3b (seeds 471001-2; base 209): CPP_MULTISTEP alone 236 wins (+27),
  strong three 95 vs 76, pool 144 vs 130**; ms + full queen safety 201 (queen
  alive 34). Confirmation queued: 3 fresh seeds 501001-3, 15 ranked + 7 Sprint
  maps (results/q3c-ms-confirm-dir.txt).
- **Multistep confirmed** (seeds 501001-3, 15 ranked + 7 Sprint maps, 792
  games each): 474 vs 447; wins delta +0.068 [+0.013, +0.124]; known maps 335
  vs 308/540, Sprint 139 vs 139/252; vs v75 +0.15, leviathan3 +0.15, lab +0.09,
  v92 0. Frozen **v11ms** (versions/v11ms, hash d8a1433a6097d63c,
  battlebot-v11ms.zip), 1.2.3 sandbox max 8.0M points/turn.
- Head-to-heads under 1.2.3 (15 maps, both sides, 4 seeds, 120 games):
  v11ms vs v10o (live) 62/120; v11ms + queen safety vs v11ms 48/120 (queens
  alive 17 vs 12). Queen safety as scoring penalties loses even against our own
  queen-careless bot; queen survival needs tactics (Q4), not weights.

### 2 Oct: Q4 queen tactics

- Queen deaths with queen mode off (v11e = v11ms, 12 logged games): 5 killed
  by our own dragons (head-ons, own bodies), 4 walls/kelp at length 2-3, 2
  enemy head-ons, 1 fed itself to a worker (feeding rule picked the queen).
- CPP_QUEEN_TACTICS: exact 3-step escape search for the queen in the view
  (own body simulated, tail blocks; threat heads at ceil(visible len/4) steps
  per turn, own workers included); keeps the incumbent's move unless another
  survives longer. CPP_QUEEN_LIGHT: the queen never feeds; workers within
  CPP_QUEEN_GUARD_R of the queen's head pay CPP_QUEEN_GUARD_PEN. Probe (24
  games): queen median death round 105 -> 175.
- Q4 ablate (1.2.3, seeds 531001-2, base v11e 223/360, queen alive 13): qt 218
  (queen alive 19, median death 139); ql 226 (22); **ql_qt 228, pool 152 vs
  142, queen alive 37 vs 13 (theirs 33), median death 137**; ql_qt_r2 217
  (51; strong 71 vs 85: a wider guard crowds workers out); ql_qt_m1 204 (14:
  assuming faster threats makes every cell deadly). First queen change that
  keeps or adds wins against this old-rules panel while nearly tripling queen
  survival. Confirmation queued: 3 seeds 541001-3, 15 ranked + 7 Sprint maps.
- **Q4 confirmation** (seeds 541001-3, 15 ranked + 7 Sprint maps, 792 games):
  ql_qt 490 vs 492 wins (neutral vs this old-rules panel), pool 233 vs 226/360,
  strong three 189 vs 182/396; **our queen alive at round 500: 79 vs 24**
  (theirs 56 vs 57); known maps 353 vs 353, Sprint 137 vs 139. Frozen **v11q**
  (versions/v11q, hash 1c547e93cdff8382, battlebot-v11q.zip; 1.2.3 sandbox max
  8.0M). Head-to-heads (15 maps, both sides, 4 seeds, 120 games): **v11q vs
  v10o 80/120 (queens alive 20 vs 2), v11q vs v11ms 73/120 (20 vs 1)**. Against
  opponents that, like ours, lose their queens, a surviving queen decides the
  game; the old-rules panel understates this. Recommended upload: v11q.
- **Live ladder evidence (2 Oct ~18:40 UTC, v10o, 10 ranked battles / 50
  games after the reset):** rating ~1445 (rank 100 at 1533), 7/10 battles won.
  Queens at round 500: both dead 38 games (we won 25), only theirs alive 10
  (we won 0), only ours 1 (won), both alive 1 (won). Our queen survived 2/50,
  theirs 11/50. Ladder teams already protect queens; queen survival decided 10
  of our 23 losses. Strong case for v11q (queen alive 3.3x in testing, 80/120 vs
  v10o head-to-head).
- Q5 queen growth (v11f = v11q behaviour, 7 opponents incl. v11q, seeds
  561001-2; base 268/420, queen alive 65 at median length 3): split cutoff 250/
  350 no effect (the queen is already below split length); qfeed (late feeders
  target the queen by id) 269, pool 174 vs 168, queen length 4, but vs v92 17 vs
  25; qs350feed 270, length 5, v92 17. Mixed; not adopted.
- Q6 (v11g, seeds 571001-2; base 254/420): queen flight 251 (queen length 3-4
  = one free step, nothing to flee with); queen food x3 246.
- Q6 complete: qkeep6 226 (queen length 15 when alive, but alive 27 vs 56);
  qfood3_keep6 235 (26); all3 230 (27). A big queen is a target; with current
  tactics a small careful queen survives best. Not adopted.
- **Q7 queen hunt** (v11h = v11q behaviour, 7 opponents incl. v11q, seeds
  581001-2; base 262/420, their queen alive 40): CPP_QUEEN_HUNT (bonus 300 for a
  head-on into the enemy queen at any length gap, pull 150/(1+d) for workers
  <= ATTACK_MAXLEN) 265, their queen alive 25, vs v92 22 vs 15, vs v11q 35 vs
  30, vs v75 29 vs 35; hunt_strong (600/400) 261 (27); hunt_nopull 260 (31; no
  gain vs v92). Confirmation queued (3 seeds 591001-3, 15 + 7 Sprint maps).
- Q7 hunt confirmation (seeds 591001-3, 15 + 7 Sprint maps, 7 opponents, 924
  games): hunt 549 vs 563, their queen alive 65 vs 72, vs v92 40 vs 36, vs v11q
  65 vs 66; known 390 vs 405, Sprint 159 vs 158. Did not replicate; not adopted.
- v11q uploaded 2 Oct ~21:04 UTC (ladder ~1445, rank 100 ~1533).
- v11q live, first 4 battles / 20 games after upload: 3 battles won (vs 1638
  CookAgent, 1597 Kerwin, 1534 DIET CODE), 12/20 games; rating 1455 -> 1519.
  Our queen alive 7/20 (v10o 2/50); only ours alive 4 games, won 4; only theirs
  2, lost 2; both alive 3, won 1; both dead 11, won 7.
- Q8 CPP_MULTISTEP_TRAVEL (extra free steps toward the best hub when no pearl;
  seeds 601001-3, 15 + 7 Sprint maps, 7 opponents, 924 games): 557 vs 560,
  queen alive 75 vs 94 (the light-mode queen travelled into danger). Rerun with
  workers only (the queen never travels).
- v11q live after ~3 h (14 battles, 82 games): 34/82 games won; queens at round
  500: only ours alive 7 (won 7), only theirs 15 (won 0), both alive 8 (won 3),
  both dead 52 (won 24). Our queen alive 18% (v10o 4%), theirs 28%: opponents at
  1500-1600 protect queens better. Leaderboard ~00:00 UTC 3 Oct: **rank 108 /
  973 at 1529; rank 100 at 1560** (gap was ~88 before v11q).
- Q8b travel for workers only (seeds 611001-3, 924 games): 552 vs 563, vs v92
  45 vs 57/132, queen alive 101 vs 102. Not adopted: spending spare free steps
  on hub travel does not help; pearl-only multistep (v11ms) stays.
- Ladder queen deaths with v11q (20 battles, 83 queen deaths): walls/kelp 36
  (boxed in, no legal move), enemy head-on 18, own dragons 18 (14 head-on, 4
  body), self 6, enemy body 3, no action 2; median death round 146, length 3. We
  killed their queen 14 times. A boxed-in small queen is the main loss.
- Q9 (v11j, seeds 621001-2; base 256/420, queen alive 50): d4 251 (57); d5 249
  (44); keep300 (light queen reach penalty) 257 (55); keep300x1 pending.
- CPP_QUEEN_LIGHT_SAFE: room/lethal multiplier for the light queen (in light
  mode the queen had no extra trap safety). Q10 queued: safe3, safe6, safe3 +
  guard radius 2, safe3 + depth 4.
- Q9 complete: keep300x1 (light queen reach penalty 300, +1 margin) 256 vs 256,
  **queen alive 63 vs 50** at equal wins; d4_keep300 253 (57).
- Q10 (v11k, seeds 631001-2; base 258/420, queen alive 55): CPP_QUEEN_LIGHT_SAFE
  x3 255 (56), x6 254 (56): room safety does nothing for a length-3 queen
  (boxing-in is dynamic); safe3 + guard radius 2: 255, **queen alive 69,
  theirs 37 vs 48**. Confirmation queued: kx1, kx1 + guard 2 (seeds 641001-3,
  15 + 7 Sprint maps, 7 opponents).
- Q11 confirmation (seeds 641001-3, 15 + 7 Sprint maps, 7 opponents, 924
  games; base v11k = v11q behaviour 572, queen alive 94): kx1 563 (104; vs v92
  61 vs 53, vs v11q 61 vs 66); kx1_g2 545 (107). Queen survival +10-14% but
  9-27 fewer wins: not adopted. v11q stays the incumbent. Local queen tweaks are
  at diminishing returns; next: learn from the top ladder teams' queen play.

### 3 Oct: ladder anatomy

- Top-ladder games (37 battles, 185 games, both teams >= 1580, since 2 Oct):
  decided by elimination 31%, longest dragon with both queens dead 31%, queen
  survival 23%, queen length with both alive 15%. Queens alive 31%; surviving
  queens median length 3 (quartiles 3, 16): top teams also keep small queens.
- v11q on the ladder (30 battles, 162 games since upload): wins by reason
  elimination 27, longest 33, queen length 10, queen survival 4; losses
  elimination 16, longest 33, queen length 8, **queen survival 31** (net -27,
  the largest loss source). The local panel rarely protects queens, so local
  tests underweight queen survival.
- **Ranked pool changed**: 12 recent ranked battles drew the old 10 maps plus
  all 7 Sprint maps (~40% of games). `official_suite.CURRENT_POOL` now has 17
  maps; `current_pool_maps()` includes the reconstructed Sprint maps.
