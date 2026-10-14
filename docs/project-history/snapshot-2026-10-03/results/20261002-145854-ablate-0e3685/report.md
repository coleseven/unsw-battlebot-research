# Ablation report: 20261002-145854-ablate-0e3685

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.248, wins 262/420; by opponent: cpp_nicked_v92 -0.500, cpp_nicked_v75 +0.167, cpp_leviathan3 +0.767, v7-base-bot +0.567, nicked_v44 +0.600, nicked_lab +0.133, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hunt | +0.021 [-0.114, +0.157] | neutral | +0.000 | +0.014 [-0.090, +0.105] | neutral | +0.233 | -0.200 | -0.033 | -0.067 | -0.067 | +0.067 | +0.167 | -0.006 | +0.071 | 265/420 |
| hunt_strong | +0.043 [-0.029, +0.121] | neutral | -0.100 | -0.005 [-0.071, +0.062] | neutral | +0.267 | -0.133 | -0.033 | +0.000 | -0.067 | -0.067 | +0.000 | -0.032 | +0.071 | 261/420 |
| hunt_nopull | -0.021 [-0.064, +0.014] | neutral | +0.014 | -0.010 [-0.048, +0.024] | neutral | -0.033 | -0.100 | +0.067 | +0.067 | -0.033 | +0.000 | -0.033 | -0.013 | +0.000 | 260/420 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.828 over 210 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.828^2 / (210 * K)): K=2: 0.112, K=3: 0.091, K=4: 0.079, K=6: 0.065, K=8: 0.056
