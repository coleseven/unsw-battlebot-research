# Ablation report: 20261001-203651-ablate-9c6006

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.111, wins 200/360; by opponent: cpp_nicked_v92 -0.667, cpp_nicked_v75 -0.067, cpp_leviathan3 +0.700, v7-base-bot +0.233, nicked_v44 +0.367, nicked_lab +0.100

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| q_on | -0.058 [-0.233, +0.108] | neutral | -0.750 | -0.289 [-0.489, -0.094] | essential | -0.200 | -0.433 | -0.433 | -0.033 | -0.300 | -0.333 | -0.333 | -0.167 | 148/360 |
| q_nosplit | -0.067 [-0.217, +0.083] | neutral | -0.750 | -0.294 [-0.489, -0.111] | essential | -0.100 | -0.533 | -0.367 | -0.100 | -0.400 | -0.267 | -0.356 | -0.125 | 147/360 |
| q_late | -0.058 [-0.267, +0.150] | neutral | -0.583 | -0.233 [-0.411, -0.044] | essential | +0.067 | -0.400 | -0.367 | +0.000 | -0.267 | -0.433 | -0.197 | -0.333 | 158/360 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.894 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.894^2 / (180 * K)): K=2: 0.131, K=3: 0.107, K=4: 0.092, K=6: 0.075, K=8: 0.065
