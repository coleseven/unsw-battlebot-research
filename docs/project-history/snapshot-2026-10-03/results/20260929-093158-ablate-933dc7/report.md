# Ablation report: 20260929-093158-ablate-933dc7

3 seeds, opponents cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.119, wins 258/450; by opponent: cpp_nicked_v75 -0.210, cpp_leviathan3 +0.408, v7-base-bot +0.335, nicked_v44 +0.229, nicked_lab -0.169

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hubfar | +0.047 [-0.024, +0.130] | neutral | +0.039 | +0.044 [-0.011, +0.101] | neutral | +0.093 | +0.003 | -0.049 | +0.070 | +0.105 | +0.032 | +0.078 | 275/450 |
| hubfar2 | +0.040 [-0.026, +0.104] | neutral | +0.026 | +0.035 [-0.010, +0.079] | neutral | +0.071 | +0.023 | +0.010 | +0.055 | +0.016 | +0.018 | +0.081 | 270/450 |
| goal0 | +0.023 [-0.062, +0.110] | neutral | -0.017 | +0.010 [-0.059, +0.075] | neutral | -0.061 | -0.026 | +0.016 | +0.086 | +0.034 | -0.031 | +0.122 | 268/450 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.587 over 150 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.587^2 / (150 * K)): K=2: 0.094, K=3: 0.077, K=4: 0.066, K=6: 0.054, K=8: 0.047
