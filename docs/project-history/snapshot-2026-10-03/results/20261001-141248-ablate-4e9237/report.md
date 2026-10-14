# Ablation report: 20261001-141248-ablate-4e9237

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 11 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.090, wins 270/528; by opponent: cpp_nicked_v92 -0.277, cpp_nicked_v75 -0.079, cpp_leviathan3 +0.298, v7-base-bot +0.305, nicked_v44 +0.334, nicked_lab -0.039

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| mv_t05 | -0.352 [-0.557, -0.161] | essential | -0.179 | -0.258 [-0.367, -0.156] | essential | -0.246 | -0.251 | -0.213 | -0.194 | -0.361 | -0.282 | -0.415 | -0.100 | 184/528 |
| mv_t1 | -0.163 [-0.314, -0.016] | essential | -0.036 | -0.094 [-0.177, -0.015] | essential | -0.066 | -0.138 | -0.011 | -0.139 | -0.029 | -0.181 | -0.191 | +0.003 | 234/528 |
| mv_t2 | -0.014 [-0.104, +0.080] | neutral | +0.009 | -0.001 [-0.049, +0.052] | neutral | +0.028 | -0.037 | +0.098 | -0.042 | -0.007 | -0.048 | +0.009 | -0.011 | 263/528 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.440 over 264 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.440^2 / (264 * K)): K=2: 0.053, K=3: 0.043, K=4: 0.038, K=6: 0.031, K=8: 0.027
