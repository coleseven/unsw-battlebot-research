# Ablation report: 20260930-131507-ablate-bfe34e

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.132, wins 327/540; by opponent: cpp_nicked_v92 -0.349, cpp_nicked_v75 -0.167, cpp_leviathan3 +0.526, v7-base-bot +0.418, nicked_v44 +0.333, nicked_lab +0.030

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| kgrad10 | -0.011 [-0.038, +0.020] | neutral | -0.028 | -0.016 [-0.048, +0.015] | neutral | -0.034 | -0.051 | -0.000 | -0.005 | -0.008 | -0.000 | -0.023 | +0.003 | 318/540 |
| kgrad25 | -0.022 [-0.058, +0.014] | neutral | -0.012 | -0.018 [-0.047, +0.010] | neutral | -0.005 | -0.052 | -0.007 | -0.010 | -0.011 | -0.026 | -0.028 | +0.007 | 319/540 |
| kgrad25kb2 | -0.013 [-0.046, +0.018] | neutral | -0.037 | -0.021 [-0.050, +0.004] | neutral | -0.030 | -0.025 | -0.002 | +0.001 | -0.002 | -0.070 | -0.031 | +0.005 | 316/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.610 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.610^2 / (180 * K)): K=2: 0.089, K=3: 0.073, K=4: 0.063, K=6: 0.051, K=8: 0.045
