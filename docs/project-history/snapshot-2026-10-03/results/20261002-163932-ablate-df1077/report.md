# Ablation report: 20261002-163932-ablate-df1077

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 11 official + 11 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.219, wins 563/924; by opponent: cpp_nicked_v92 -0.455, cpp_nicked_v75 -0.015, cpp_leviathan3 +0.773, v7-base-bot +0.500, nicked_v44 +0.591, nicked_lab +0.136, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hunt | -0.036 [-0.112, +0.038] | neutral | -0.022 | -0.028 [-0.081, +0.024] | neutral | +0.061 | -0.030 | -0.076 | -0.076 | +0.000 | -0.076 | +0.000 | -0.039 | -0.017 | 549/924 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.819 over 308 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.819^2 / (308 * K)): K=2: 0.091, K=3: 0.075, K=4: 0.065, K=6: 0.053, K=8: 0.046
