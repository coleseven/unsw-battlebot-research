# Ablation report: 20261002-221412-ablate-3a1e25

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.229, wins 258/420; by opponent: cpp_nicked_v92 -0.167, cpp_nicked_v75 -0.233, cpp_leviathan3 +0.533, v7-base-bot +0.667, nicked_v44 +0.633, nicked_lab +0.167, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| safe3 | +0.014 [-0.029, +0.050] | neutral | -0.071 | -0.014 [-0.052, +0.024] | neutral | -0.033 | -0.067 | -0.067 | -0.067 | +0.033 | +0.000 | +0.100 | -0.019 | +0.000 | 255/420 |
| safe6 | +0.014 [-0.036, +0.064] | neutral | -0.086 | -0.019 [-0.062, +0.019] | neutral | -0.033 | -0.067 | -0.100 | -0.067 | +0.033 | +0.033 | +0.067 | -0.026 | +0.000 | 254/420 |
| safe3_g2 | +0.021 [-0.114, +0.157] | neutral | -0.086 | -0.014 [-0.114, +0.086] | neutral | -0.167 | +0.267 | +0.167 | -0.233 | +0.000 | -0.100 | -0.033 | +0.006 | -0.071 | 255/420 |
| safe3_d4 | +0.114 [+0.014, +0.221] | harmful (drop) | -0.014 | +0.071 [-0.005, +0.157] | neutral | -0.100 | +0.100 | +0.267 | -0.133 | +0.067 | +0.067 | +0.233 | +0.091 | +0.018 | 273/420 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.851 over 210 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.851^2 / (210 * K)): K=2: 0.115, K=3: 0.094, K=4: 0.081, K=6: 0.066, K=8: 0.058
