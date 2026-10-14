# Ablation report: 20261002-200810-ablate-394220

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.219, wins 256/420; by opponent: cpp_nicked_v92 -0.467, cpp_nicked_v75 +0.067, cpp_leviathan3 +0.533, v7-base-bot +0.500, nicked_v44 +0.700, nicked_lab +0.200, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| d4 | -0.036 [-0.143, +0.064] | neutral | +0.000 | -0.024 [-0.090, +0.043] | neutral | +0.133 | -0.067 | -0.067 | +0.033 | -0.133 | -0.033 | -0.033 | -0.026 | -0.018 | 251/420 |
| d5 | -0.036 [-0.100, +0.021] | neutral | -0.029 | -0.033 [-0.090, +0.029] | neutral | +0.133 | -0.200 | +0.067 | -0.033 | -0.100 | +0.033 | -0.133 | -0.045 | +0.000 | 249/420 |
| keep300 | -0.014 [-0.036, +0.000] | neutral | +0.043 | +0.005 [-0.019, +0.033] | neutral | +0.000 | -0.067 | +0.067 | +0.033 | +0.000 | +0.000 | +0.000 | +0.006 | +0.000 | 257/420 |
| keep300x1 | -0.014 [-0.093, +0.057] | neutral | +0.029 | +0.000 [-0.067, +0.062] | neutral | +0.100 | +0.000 | +0.100 | -0.067 | +0.067 | -0.067 | -0.133 | -0.013 | +0.036 | 256/420 |
| d4_keep300 | -0.043 [-0.143, +0.057] | neutral | +0.043 | -0.014 [-0.090, +0.062] | neutral | +0.100 | -0.033 | -0.067 | +0.100 | -0.100 | -0.033 | -0.067 | -0.013 | -0.018 | 253/420 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.884 over 210 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.884^2 / (210 * K)): K=2: 0.120, K=3: 0.098, K=4: 0.085, K=6: 0.069, K=8: 0.060
