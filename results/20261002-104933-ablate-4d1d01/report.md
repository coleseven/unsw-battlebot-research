# Ablation report: 20261002-104933-ablate-4d1d01

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 11 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.242, wins 492/792; by opponent: cpp_nicked_v92 -0.424, cpp_nicked_v75 +0.000, cpp_leviathan3 +0.636, v7-base-bot +0.530, nicked_v44 +0.530, nicked_lab +0.182

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ql_qt | +0.039 [-0.072, +0.144] | neutral | -0.042 | -0.005 [-0.076, +0.063] | neutral | +0.106 | +0.030 | -0.030 | -0.015 | -0.091 | -0.030 | +0.000 | -0.010 | 490/792 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.765 over 264 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.765^2 / (264 * K)): K=2: 0.092, K=3: 0.075, K=4: 0.065, K=6: 0.053, K=8: 0.046
