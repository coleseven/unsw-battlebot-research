# Ablation report: 20260928-140413-ablate-2970a3

3 seeds, opponents cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.152, wins 210/360; by opponent: cpp_nicked_v75 -0.363, cpp_leviathan3 +0.449, v7-base-bot +0.281, nicked_v44 +0.241

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| kb | +0.027 [-0.022, +0.075] | neutral | +0.008 | +0.021 [-0.012, +0.052] | neutral | +0.001 | +0.038 | +0.060 | -0.016 | -0.007 | +0.098 | 218/360 |
| kbbig | +0.059 [-0.004, +0.126] | neutral | +0.136 | +0.085 [+0.032, +0.138] | harmful (drop) | +0.035 | +0.105 | +0.104 | +0.095 | +0.052 | +0.173 | 237/360 |
| dead | -0.008 [-0.086, +0.068] | neutral | +0.008 | -0.003 [-0.054, +0.048] | neutral | -0.014 | -0.027 | -0.042 | +0.073 | +0.043 | -0.127 | 213/360 |
| all | +0.002 [-0.082, +0.087] | neutral | +0.136 | +0.047 [-0.024, +0.110] | neutral | +0.029 | -0.010 | +0.048 | +0.121 | +0.093 | -0.079 | 228/360 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.581 over 120 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.581^2 / (120 * K)): K=2: 0.104, K=3: 0.085, K=4: 0.073, K=6: 0.060, K=8: 0.052
