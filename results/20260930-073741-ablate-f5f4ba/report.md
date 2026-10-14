# Ablation report: 20260930-073741-ablate-f5f4ba

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.169, wins 339/540; by opponent: cpp_nicked_v92 -0.315, cpp_nicked_v75 -0.104, cpp_leviathan3 +0.441, v7-base-bot +0.505, nicked_v44 +0.395, nicked_lab +0.093

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hubsep | +0.011 [-0.016, +0.040] | neutral | +0.000 | +0.008 [-0.012, +0.027] | neutral | +0.001 | +0.032 | -0.020 | +0.006 | +0.044 | -0.016 | +0.000 | +0.029 | 342/540 |
| v3portal | -0.043 [-0.095, +0.006] | neutral | +0.036 | -0.017 [-0.059, +0.024] | neutral | -0.036 | -0.045 | -0.018 | -0.070 | +0.028 | +0.041 | -0.019 | -0.010 | 330/540 |
| both | -0.033 [-0.093, +0.030] | neutral | +0.036 | -0.010 [-0.059, +0.037] | neutral | -0.019 | -0.010 | -0.041 | -0.072 | +0.047 | +0.037 | -0.019 | +0.016 | 332/540 |
| v12tune | -0.091 [-0.192, +0.002] | neutral | -0.007 | -0.063 [-0.147, +0.020] | neutral | -0.185 | +0.061 | -0.024 | -0.157 | -0.004 | -0.069 | -0.110 | +0.067 | 317/540 |
| v12gen5 | -0.087 [-0.175, +0.001] | neutral | +0.069 | -0.035 [-0.108, +0.042] | neutral | -0.100 | -0.032 | +0.097 | -0.062 | +0.034 | -0.149 | -0.071 | +0.062 | 324/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.618 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.618^2 / (180 * K)): K=2: 0.090, K=3: 0.074, K=4: 0.064, K=6: 0.052, K=8: 0.045
