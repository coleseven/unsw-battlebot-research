# Ablation report: 20260930-224324-ablate-a110d4

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 14 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.142, wins 542/900; by opponent: cpp_nicked_v92 -0.481, cpp_nicked_v75 -0.123, cpp_leviathan3 +0.553, v7-base-bot +0.415, nicked_v44 +0.413, nicked_lab +0.075

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sh_age30 | +0.038 [-0.004, +0.085] | neutral | +0.037 | +0.038 [+0.010, +0.065] | harmful (drop) | +0.060 | +0.033 | -0.019 | +0.089 | +0.055 | +0.008 | +0.000 | +0.067 | 563/900 |
| sh_age60 | +0.026 [-0.013, +0.069] | neutral | +0.015 | +0.020 [-0.002, +0.044] | neutral | +0.006 | +0.029 | -0.009 | +0.093 | +0.038 | -0.038 | +0.000 | +0.035 | 552/900 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.574 over 300 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.574^2 / (300 * K)): K=2: 0.065, K=3: 0.053, K=4: 0.046, K=6: 0.038, K=8: 0.033
