# Ablation report: 20260930-110033-ablate-a99756

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.076, wins 303/540; by opponent: cpp_nicked_v92 -0.532, cpp_nicked_v75 -0.287, cpp_leviathan3 +0.451, v7-base-bot +0.472, nicked_v44 +0.333, nicked_lab +0.020

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| kb2 | +0.017 [-0.020, +0.060] | neutral | -0.008 | +0.009 [-0.021, +0.040] | neutral | -0.026 | +0.022 | +0.053 | +0.015 | +0.049 | -0.059 | -0.001 | +0.036 | 308/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.556 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.556^2 / (180 * K)): K=2: 0.081, K=3: 0.066, K=4: 0.057, K=6: 0.047, K=8: 0.041
