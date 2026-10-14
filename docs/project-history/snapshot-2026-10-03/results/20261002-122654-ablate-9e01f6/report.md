# Ablation report: 20261002-122654-ablate-9e01f6

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.276, wins 268/420; by opponent: cpp_nicked_v92 -0.167, cpp_nicked_v75 -0.033, cpp_leviathan3 +0.733, v7-base-bot +0.600, nicked_v44 +0.567, nicked_lab +0.233, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qs250 | +0.000 [-0.021, +0.021] | neutral | +0.000 | +0.000 [-0.014, +0.014] | neutral | -0.067 | +0.000 | +0.033 | +0.000 | +0.033 | +0.000 | +0.000 | +0.000 | +0.000 | 268/420 |
| qs350 | +0.000 [+0.000, +0.000] | neutral | +0.000 | +0.000 [+0.000, +0.000] | neutral | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | 268/420 |
| qfeed | +0.043 [-0.043, +0.136] | neutral | -0.071 | +0.005 [-0.062, +0.071] | neutral | -0.267 | +0.133 | +0.100 | +0.000 | +0.100 | +0.067 | -0.100 | +0.019 | -0.036 | 269/420 |
| qs350feed | +0.050 [-0.043, +0.143] | neutral | -0.071 | +0.010 [-0.057, +0.081] | neutral | -0.267 | +0.133 | +0.133 | +0.000 | +0.100 | +0.067 | -0.100 | +0.026 | -0.036 | 270/420 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.884 over 210 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.884^2 / (210 * K)): K=2: 0.120, K=3: 0.098, K=4: 0.085, K=6: 0.069, K=8: 0.060
