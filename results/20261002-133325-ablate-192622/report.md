# Ablation report: 20261002-133325-ablate-192622

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.210, wins 254/420; by opponent: cpp_nicked_v92 -0.433, cpp_nicked_v75 -0.067, cpp_leviathan3 +0.667, v7-base-bot +0.433, nicked_v44 +0.667, nicked_lab +0.200, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| flight | -0.029 [-0.071, +0.007] | neutral | +0.014 | -0.014 [-0.048, +0.014] | neutral | +0.000 | -0.033 | +0.033 | +0.000 | -0.100 | -0.067 | +0.067 | -0.019 | +0.000 | 251/420 |
| qfood3 | -0.021 [-0.136, +0.079] | neutral | -0.071 | -0.038 [-0.133, +0.067] | neutral | -0.033 | -0.067 | -0.100 | +0.033 | +0.033 | -0.133 | +0.000 | -0.052 | +0.000 | 246/420 |
| qkeep6 | -0.043 [-0.150, +0.057] | neutral | -0.314 | -0.133 [-0.233, -0.038] | essential | -0.133 | -0.167 | -0.067 | -0.200 | -0.133 | -0.200 | -0.033 | -0.195 | +0.036 | 226/420 |
| qfood3_keep6 | -0.036 [-0.157, +0.079] | neutral | -0.200 | -0.090 [-0.205, +0.019] | neutral | -0.033 | -0.100 | -0.033 | -0.167 | +0.033 | -0.267 | -0.067 | -0.130 | +0.018 | 235/420 |
| all3 | -0.029 [-0.143, +0.100] | neutral | -0.286 | -0.114 [-0.224, -0.010] | essential | +0.000 | -0.133 | -0.167 | -0.067 | -0.067 | -0.233 | -0.133 | -0.175 | +0.054 | 230/420 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.816 over 210 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.816^2 / (210 * K)): K=2: 0.110, K=3: 0.090, K=4: 0.078, K=6: 0.064, K=8: 0.055
