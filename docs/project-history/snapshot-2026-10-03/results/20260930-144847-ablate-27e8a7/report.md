# Ablation report: 20260930-144847-ablate-27e8a7

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.215, wins 348/540; by opponent: cpp_nicked_v92 -0.299, cpp_nicked_v75 -0.073, cpp_leviathan3 +0.563, v7-base-bot +0.415, nicked_v44 +0.509, nicked_lab +0.178

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sum64 | +0.014 [-0.019, +0.044] | neutral | +0.011 | +0.013 [-0.016, +0.043] | neutral | +0.047 | +0.028 | +0.024 | +0.025 | -0.053 | +0.008 | +0.007 | +0.029 | 355/540 |
| sum12 | +0.034 [-0.003, +0.070] | neutral | +0.017 | +0.028 [+0.001, +0.056] | harmful (drop) | +0.027 | +0.071 | +0.060 | +0.014 | -0.035 | +0.035 | +0.021 | +0.048 | 362/540 |
| sum64early | -0.002 [-0.064, +0.053] | neutral | -0.005 | -0.003 [-0.045, +0.032] | neutral | +0.058 | +0.067 | -0.030 | -0.014 | -0.107 | +0.007 | -0.013 | +0.025 | 349/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.587 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.587^2 / (180 * K)): K=2: 0.086, K=3: 0.070, K=4: 0.061, K=6: 0.050, K=8: 0.043
