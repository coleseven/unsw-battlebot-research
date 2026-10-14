# Ablation report: 20260930-210927-ablate-9aaef8

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.161, wins 333/540; by opponent: cpp_nicked_v92 -0.514, cpp_nicked_v75 -0.016, cpp_leviathan3 +0.517, v7-base-bot +0.417, nicked_v44 +0.420, nicked_lab +0.140

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sh_age15 | -0.014 [-0.052, +0.021] | neutral | +0.000 | -0.009 [-0.034, +0.013] | neutral | -0.000 | -0.070 | +0.046 | -0.001 | +0.019 | -0.048 | +0.000 | -0.034 | 331/540 |
| sh_age30 | +0.026 [+0.001, +0.054] | harmful (drop) | +0.000 | +0.017 [+0.001, +0.036] | harmful (drop) | +0.036 | -0.007 | +0.049 | +0.030 | -0.013 | +0.008 | +0.000 | +0.064 | 340/540 |
| sh_age60 | +0.028 [-0.001, +0.066] | neutral | +0.000 | +0.019 [-0.001, +0.041] | neutral | -0.008 | +0.022 | +0.039 | +0.015 | +0.022 | +0.022 | +0.000 | +0.070 | 342/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.611 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.611^2 / (180 * K)): K=2: 0.089, K=3: 0.073, K=4: 0.063, K=6: 0.052, K=8: 0.045
