# Ablation report: 20261002-003855-ablate-58e7c5

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.150, wins 207/360; by opponent: cpp_nicked_v92 -0.433, cpp_nicked_v75 -0.167, cpp_leviathan3 +0.567, v7-base-bot +0.433, nicked_v44 +0.433, nicked_lab +0.067

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qx2 | -0.008 [-0.158, +0.150] | neutral | -0.617 | -0.211 [-0.394, -0.028] | essential | -0.333 | -0.167 | -0.100 | -0.133 | -0.300 | -0.233 | -0.318 | +0.083 | 169/360 |
| qx3 | +0.042 [-0.125, +0.200] | neutral | -0.700 | -0.206 [-0.417, +0.006] | neutral | -0.233 | -0.033 | -0.267 | -0.233 | -0.167 | -0.300 | -0.333 | +0.146 | 170/360 |
| qx2_nosplit | +0.000 [-0.150, +0.167] | neutral | -0.667 | -0.222 [-0.406, -0.022] | essential | -0.233 | -0.167 | -0.167 | -0.200 | -0.333 | -0.233 | -0.341 | +0.104 | 167/360 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.888 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.888^2 / (180 * K)): K=2: 0.130, K=3: 0.106, K=4: 0.092, K=6: 0.075, K=8: 0.065
