# Ablation report: 20260930-114529-ablate-214862

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.151, wins 329/540; by opponent: cpp_nicked_v92 -0.306, cpp_nicked_v75 -0.140, cpp_leviathan3 +0.538, v7-base-bot +0.522, nicked_v44 +0.350, nicked_lab -0.058

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| reach4 | +0.030 [-0.014, +0.078] | neutral | -0.032 | +0.009 [-0.024, +0.045] | neutral | -0.029 | +0.049 | +0.002 | +0.015 | +0.016 | +0.003 | -0.005 | +0.050 | 333/540 |
| reach6 | +0.004 [-0.039, +0.051] | neutral | -0.032 | -0.008 [-0.043, +0.026] | neutral | -0.048 | -0.012 | +0.008 | +0.018 | +0.001 | -0.011 | -0.025 | +0.041 | 325/540 |
| kb2reach4 | +0.022 [-0.017, +0.064] | neutral | -0.057 | -0.005 [-0.037, +0.030] | neutral | -0.058 | +0.014 | +0.003 | +0.005 | +0.016 | -0.007 | -0.021 | +0.041 | 326/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.620 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.620^2 / (180 * K)): K=2: 0.091, K=3: 0.074, K=4: 0.064, K=6: 0.052, K=8: 0.045
