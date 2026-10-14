# Ablation report: 20260930-161837-ablate-05467d

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.127, wins 323/540; by opponent: cpp_nicked_v92 -0.506, cpp_nicked_v75 -0.105, cpp_leviathan3 +0.535, v7-base-bot +0.472, nicked_v44 +0.441, nicked_lab -0.075

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sum12 | -0.017 [-0.050, +0.024] | neutral | +0.009 | -0.008 [-0.035, +0.019] | neutral | +0.049 | -0.051 | +0.027 | -0.036 | -0.031 | -0.007 | -0.017 | +0.016 | 322/540 |
| sum64 | -0.030 [-0.064, +0.008] | neutral | -0.003 | -0.021 [-0.049, +0.007] | neutral | +0.038 | -0.054 | +0.030 | -0.049 | -0.068 | -0.024 | -0.038 | +0.026 | 316/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.589 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.589^2 / (180 * K)): K=2: 0.086, K=3: 0.070, K=4: 0.061, K=6: 0.050, K=8: 0.043
