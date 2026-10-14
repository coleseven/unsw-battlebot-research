# Ablation report: 20260929-121639-ablate-d99145

3 seeds, opponents cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v6; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.237, wins 359/540; by opponent: cpp_nicked_v75 -0.202, cpp_leviathan3 +0.507, v7-base-bot +0.407, nicked_v44 +0.306, nicked_lab -0.097, v6 +0.500

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v6 | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hubfar | -0.048 [-0.137, +0.040] | neutral | -0.071 | -0.056 [-0.136, +0.017] | neutral | -0.127 | -0.075 | -0.146 | -0.070 | +0.024 | +0.058 | -0.040 | -0.099 | 338/540 |
| hubfar_strong | -0.041 [-0.117, +0.039] | neutral | -0.091 | -0.058 [-0.136, +0.014] | neutral | -0.127 | -0.068 | -0.081 | -0.093 | -0.007 | +0.030 | -0.059 | -0.053 | 336/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.579 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.579^2 / (180 * K)): K=2: 0.085, K=3: 0.069, K=4: 0.060, K=6: 0.049, K=8: 0.042
