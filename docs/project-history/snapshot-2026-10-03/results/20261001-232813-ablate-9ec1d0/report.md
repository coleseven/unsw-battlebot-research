# Ablation report: 20261001-232813-ablate-9ec1d0

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.161, wins 209/360; by opponent: cpp_nicked_v92 -0.467, cpp_nicked_v75 -0.067, cpp_leviathan3 +0.667, v7-base-bot +0.367, nicked_v44 +0.400, nicked_lab +0.067

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ms | +0.117 [+0.025, +0.217] | harmful (drop) | +0.217 | +0.150 [+0.050, +0.261] | harmful (drop) | +0.300 | +0.100 | +0.100 | -0.133 | +0.300 | +0.233 | +0.129 | +0.208 | 236/360 |
| ms_qsafe | +0.125 [-0.025, +0.283] | neutral | -0.383 | -0.044 [-0.267, +0.167] | neutral | -0.233 | +0.000 | -0.167 | +0.033 | +0.133 | -0.033 | -0.136 | +0.208 | 201/360 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.837 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.837^2 / (180 * K)): K=2: 0.122, K=3: 0.100, K=4: 0.086, K=6: 0.071, K=8: 0.061
