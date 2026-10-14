# Ablation report: 20261002-180409-ablate-3db476

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 11 official + 11 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.212, wins 560/924; by opponent: cpp_nicked_v92 -0.303, cpp_nicked_v75 +0.015, cpp_leviathan3 +0.636, v7-base-bot +0.576, nicked_v44 +0.470, nicked_lab +0.091, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| travel | +0.000 [-0.071, +0.071] | neutral | -0.012 | -0.006 [-0.056, +0.043] | neutral | -0.030 | -0.076 | +0.061 | +0.015 | +0.030 | -0.076 | +0.030 | -0.048 | +0.035 | 557/924 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.837 over 308 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.837^2 / (308 * K)): K=2: 0.094, K=3: 0.076, K=4: 0.066, K=6: 0.054, K=8: 0.047
