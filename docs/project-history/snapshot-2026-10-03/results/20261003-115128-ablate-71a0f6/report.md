# Ablation report: 20261003-115128-ablate-71a0f6

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 17 official + 0 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.147, wins 273/476; by opponent: cpp_nicked_v92 -0.588, cpp_nicked_v75 -0.235, cpp_leviathan3 +0.676, v7-base-bot +0.559, nicked_v44 +0.471, nicked_lab +0.147, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t2 | -0.014 [-0.100, +0.071] | neutral | +0.113 | +0.076 [-0.008, +0.160] | neutral | +0.324 | +0.000 | +0.235 | -0.147 | +0.029 | -0.382 | +0.471 | +0.076 | - | 291/476 |
| t2_d4 | +0.071 [+0.000, +0.157] | neutral | +0.030 | +0.042 [-0.042, +0.130] | neutral | +0.206 | +0.088 | +0.088 | +0.059 | -0.059 | -0.206 | +0.118 | +0.042 | - | 283/476 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.739 over 238 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.739^2 / (238 * K)): K=2: 0.094, K=3: 0.077, K=4: 0.066, K=6: 0.054, K=8: 0.047
