# Ablation report: 20260930-182348-ablate-81c0bb

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.198, wins 347/540; by opponent: cpp_nicked_v92 -0.314, cpp_nicked_v75 +0.045, cpp_leviathan3 +0.525, v7-base-bot +0.471, nicked_v44 +0.423, nicked_lab +0.040

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r4 | -0.044 [-0.149, +0.060] | neutral | +0.021 | -0.022 [-0.113, +0.069] | neutral | -0.043 | -0.041 | -0.006 | -0.102 | -0.032 | +0.091 | -0.006 | -0.067 | 333/540 |
| r4eq | -0.053 [-0.148, +0.036] | neutral | -0.068 | -0.058 [-0.156, +0.037] | neutral | -0.038 | -0.141 | -0.087 | -0.092 | -0.072 | +0.080 | -0.050 | -0.083 | 326/540 |
| r4lo | -0.175 [-0.283, -0.078] | essential | -0.173 | -0.174 [-0.287, -0.076] | essential | -0.160 | -0.326 | -0.131 | -0.227 | -0.134 | -0.069 | -0.188 | -0.136 | 291/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.606 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.606^2 / (180 * K)): K=2: 0.089, K=3: 0.072, K=4: 0.063, K=6: 0.051, K=8: 0.044
