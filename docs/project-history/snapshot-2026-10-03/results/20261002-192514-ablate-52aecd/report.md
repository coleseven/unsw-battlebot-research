# Ablation report: 20261002-192514-ablate-52aecd

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 11 official + 11 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.219, wins 563/924; by opponent: cpp_nicked_v92 -0.136, cpp_nicked_v75 -0.030, cpp_leviathan3 +0.591, v7-base-bot +0.485, nicked_v44 +0.545, nicked_lab +0.076, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| travel_w | -0.052 [-0.138, +0.024] | neutral | +0.000 | -0.024 [-0.074, +0.022] | neutral | -0.182 | -0.091 | +0.061 | +0.000 | +0.030 | +0.045 | -0.030 | -0.043 | -0.004 | 552/924 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.880 over 308 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.880^2 / (308 * K)): K=2: 0.098, K=3: 0.080, K=4: 0.070, K=6: 0.057, K=8: 0.049
