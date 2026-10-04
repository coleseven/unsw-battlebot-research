# Ablation report: 20261002-091849-ablate-0b2d16

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.239, wins 223/360; by opponent: cpp_nicked_v92 -0.333, cpp_nicked_v75 -0.100, cpp_leviathan3 +0.533, v7-base-bot +0.500, nicked_v44 +0.567, nicked_lab +0.267

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qt | +0.008 [-0.092, +0.100] | neutral | -0.100 | -0.028 [-0.106, +0.050] | neutral | -0.033 | +0.100 | +0.000 | -0.033 | -0.100 | -0.100 | -0.053 | +0.042 | 218/360 |
| ql | +0.042 [-0.025, +0.108] | neutral | -0.033 | +0.017 [-0.044, +0.078] | neutral | +0.067 | -0.067 | -0.133 | +0.067 | +0.033 | +0.133 | +0.008 | +0.042 | 226/360 |
| ql_qt | +0.083 [-0.025, +0.183] | neutral | -0.083 | +0.028 [-0.050, +0.117] | neutral | -0.067 | +0.200 | +0.067 | +0.033 | +0.033 | -0.100 | +0.015 | +0.062 | 228/360 |
| ql_qt_r2 | +0.025 [-0.083, +0.133] | neutral | -0.150 | -0.033 [-0.128, +0.056] | neutral | -0.167 | -0.100 | +0.100 | +0.000 | +0.167 | -0.200 | -0.061 | +0.042 | 217/360 |
| ql_qt_m1 | -0.017 [-0.100, +0.083] | neutral | -0.283 | -0.106 [-0.217, +0.006] | neutral | -0.167 | +0.000 | -0.033 | -0.267 | -0.033 | -0.133 | -0.144 | +0.000 | 204/360 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.767 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.767^2 / (180 * K)): K=2: 0.112, K=3: 0.092, K=4: 0.079, K=6: 0.065, K=8: 0.056
