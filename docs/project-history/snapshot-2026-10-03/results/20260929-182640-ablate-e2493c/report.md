# Ablation report: 20260929-182640-ablate-e2493c

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.167, wins 329/540; by opponent: cpp_nicked_v92 -0.417, cpp_nicked_v75 -0.089, cpp_leviathan3 +0.590, v7-base-bot +0.447, nicked_v44 +0.478, nicked_lab -0.005

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| shift40 | +0.004 [-0.027, +0.036] | neutral | +0.079 | +0.029 [-0.000, +0.061] | neutral | +0.024 | +0.053 | -0.024 | +0.039 | +0.032 | +0.049 | +0.031 | +0.022 | 344/540 |
| plen4 | -0.185 [-0.269, -0.106] | essential | -0.030 | -0.133 [-0.197, -0.077] | essential | -0.133 | -0.199 | -0.082 | -0.101 | -0.160 | -0.124 | -0.147 | -0.095 | 285/540 |
| plen4pf16r5 | -0.302 [-0.403, -0.201] | essential | -0.138 | -0.248 [-0.335, -0.164] | essential | -0.228 | -0.236 | -0.269 | -0.292 | -0.357 | -0.103 | -0.276 | -0.170 | 250/540 |
| plen4pf16r5s40 | -0.324 [-0.430, -0.226] | essential | -0.120 | -0.256 [-0.349, -0.167] | essential | -0.212 | -0.251 | -0.283 | -0.313 | -0.344 | -0.134 | -0.280 | -0.191 | 247/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.547 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.547^2 / (180 * K)): K=2: 0.080, K=3: 0.065, K=4: 0.057, K=6: 0.046, K=8: 0.040
