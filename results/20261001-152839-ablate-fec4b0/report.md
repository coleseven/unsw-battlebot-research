# Ablation report: 20261001-152839-ablate-fec4b0

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 7 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.124, wins 226/432; by opponent: cpp_nicked_v92 -0.148, cpp_nicked_v75 -0.016, cpp_leviathan3 +0.345, v7-base-bot +0.167, nicked_v44 +0.370, nicked_lab +0.023

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v7_weights | +0.011 [-0.202, +0.206] | neutral | -0.065 | -0.040 [-0.131, +0.054] | neutral | -0.031 | -0.095 | -0.098 | -0.002 | +0.055 | -0.068 | -0.073 | +0.013 | 214/432 |
| v7_v3 | -0.115 [-0.299, +0.077] | neutral | -0.005 | -0.042 [-0.125, +0.037] | neutral | -0.115 | -0.025 | +0.010 | +0.037 | -0.110 | -0.047 | -0.077 | +0.013 | 199/432 |
| v7_food | -0.017 [-0.143, +0.096] | neutral | -0.005 | -0.009 [-0.061, +0.045] | neutral | +0.058 | -0.016 | -0.024 | +0.114 | -0.077 | -0.107 | -0.038 | +0.038 | 222/432 |
| v7_safety | +0.120 [+0.039, +0.194] | harmful (drop) | +0.000 | +0.040 [-0.004, +0.084] | neutral | -0.037 | +0.004 | +0.074 | +0.059 | +0.084 | +0.057 | +0.058 | +0.013 | 237/432 |
| v7_fight | +0.018 [-0.070, +0.115] | neutral | +0.013 | +0.015 [-0.027, +0.055] | neutral | -0.024 | -0.015 | -0.031 | +0.038 | +0.032 | +0.089 | +0.013 | +0.017 | 229/432 |
| v7_explore | +0.011 [-0.126, +0.166] | neutral | +0.023 | +0.019 [-0.038, +0.080] | neutral | -0.015 | -0.055 | +0.077 | +0.043 | +0.055 | +0.008 | +0.027 | +0.006 | 223/432 |
| no_kb_feed | -0.083 [-0.170, -0.012] | essential | -0.056 | -0.065 [-0.114, -0.024] | essential | -0.099 | -0.146 | -0.004 | -0.050 | -0.059 | -0.033 | -0.107 | +0.000 | 200/432 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.491 over 216 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.491^2 / (216 * K)): K=2: 0.066, K=3: 0.053, K=4: 0.046, K=6: 0.038, K=8: 0.033
