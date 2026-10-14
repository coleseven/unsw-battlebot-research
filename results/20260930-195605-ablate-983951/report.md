# Ablation report: 20260930-195605-ablate-983951

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.178, wins 343/540; by opponent: cpp_nicked_v92 -0.382, cpp_nicked_v75 -0.097, cpp_leviathan3 +0.636, v7-base-bot +0.394, nicked_v44 +0.466, nicked_lab +0.052

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sonarhub | -0.011 [-0.065, +0.042] | neutral | +0.000 | -0.007 [-0.040, +0.028] | neutral | +0.027 | +0.005 | -0.014 | +0.014 | -0.038 | -0.038 | +0.000 | -0.027 | 337/540 |
| sonarhub_whub3 | -0.193 [-0.318, -0.069] | essential | -0.043 | -0.143 [-0.228, -0.061] | essential | -0.033 | -0.148 | -0.148 | -0.151 | -0.219 | -0.159 | -0.171 | -0.066 | 293/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.594 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.594^2 / (180 * K)): K=2: 0.087, K=3: 0.071, K=4: 0.061, K=6: 0.050, K=8: 0.043
