# Ablation report: 20260930-095351-ablate-907fbc

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.107, wins 314/540; by opponent: cpp_nicked_v92 -0.406, cpp_nicked_v75 -0.166, cpp_leviathan3 +0.456, v7-base-bot +0.458, nicked_v44 +0.355, nicked_lab -0.054

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| kb2 | +0.033 [+0.009, +0.060] | harmful (drop) | -0.012 | +0.018 [-0.008, +0.045] | neutral | -0.034 | +0.012 | +0.087 | +0.011 | -0.001 | +0.035 | +0.013 | +0.032 | 323/540 |
| kb2hub | +0.041 [+0.003, +0.085] | harmful (drop) | -0.012 | +0.023 [-0.009, +0.058] | neutral | -0.017 | +0.028 | +0.078 | +0.062 | +0.020 | -0.032 | +0.013 | +0.050 | 324/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.605 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.605^2 / (180 * K)): K=2: 0.088, K=3: 0.072, K=4: 0.062, K=6: 0.051, K=8: 0.044
