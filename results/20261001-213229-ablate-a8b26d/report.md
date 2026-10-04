# Ablation report: 20261001-213229-ablate-a8b26d

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.167, wins 210/360; by opponent: cpp_nicked_v92 -0.433, cpp_nicked_v75 -0.167, cpp_leviathan3 +0.567, v7-base-bot +0.467, nicked_v44 +0.533, nicked_lab +0.033

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| q_kb | -0.017 [-0.158, +0.108] | neutral | -0.450 | -0.161 [-0.333, +0.000] | neutral | -0.100 | -0.267 | -0.067 | -0.067 | -0.200 | -0.267 | -0.220 | +0.000 | 181/360 |
| qs_reach | -0.008 [-0.150, +0.125] | neutral | -0.517 | -0.178 [-0.356, -0.006] | essential | -0.133 | -0.200 | -0.033 | -0.133 | -0.233 | -0.333 | -0.250 | +0.021 | 178/360 |
| qs_dead | -0.008 [-0.150, +0.117] | neutral | -0.450 | -0.156 [-0.328, +0.000] | neutral | -0.100 | -0.300 | -0.067 | -0.067 | -0.133 | -0.267 | -0.212 | +0.000 | 182/360 |
| qs_full | -0.033 [-0.192, +0.133] | neutral | -0.533 | -0.200 [-0.378, -0.028] | essential | -0.267 | -0.100 | -0.033 | -0.200 | -0.267 | -0.333 | -0.273 | +0.000 | 174/360 |
| qs_full_nosplit | -0.067 [-0.225, +0.100] | neutral | -0.600 | -0.244 [-0.433, -0.061] | essential | -0.233 | -0.167 | -0.133 | -0.200 | -0.333 | -0.400 | -0.311 | -0.062 | 166/360 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.803 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.803^2 / (180 * K)): K=2: 0.117, K=3: 0.096, K=4: 0.083, K=6: 0.068, K=8: 0.059
