# Ablation report: 20260929-134853-ablate-5617dc

3 seeds, opponents cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v6; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.170, wins 335/540; by opponent: cpp_nicked_v75 -0.344, cpp_leviathan3 +0.466, v7-base-bot +0.237, nicked_v44 +0.308, nicked_lab -0.147, v6 +0.500

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v6 | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| book | +0.150 [+0.073, +0.236] | harmful (drop) | +0.065 | +0.122 [+0.054, +0.191] | harmful (drop) | +0.259 | +0.035 | +0.116 | +0.146 | +0.113 | +0.061 | +0.166 | +0.000 | 378/540 |
| bookgrad15 | -0.156 [-0.312, +0.005] | neutral | +0.050 | -0.087 [-0.206, +0.022] | neutral | +0.059 | -0.261 | -0.114 | -0.159 | +0.091 | -0.141 | -0.155 | +0.099 | 309/540 |
| bookgrad8 | +0.010 [-0.126, +0.141] | neutral | +0.057 | +0.026 [-0.074, +0.121] | neutral | +0.154 | -0.132 | +0.033 | +0.004 | +0.164 | -0.068 | -0.013 | +0.134 | 347/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.568 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.568^2 / (180 * K)): K=2: 0.083, K=3: 0.068, K=4: 0.059, K=6: 0.048, K=8: 0.041
