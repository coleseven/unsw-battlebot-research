# Ablation report: 20260929-092956-ablate-1fdc1e

3 seeds, opponents cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.119, wins 258/450; by opponent: cpp_nicked_v75 -0.210, cpp_leviathan3 +0.408, v7-base-bot +0.335, nicked_v44 +0.229, nicked_lab -0.169

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fpr80 | -0.008 [-0.063, +0.046] | neutral | +0.010 | -0.002 [-0.045, +0.039] | neutral | +0.014 | +0.065 | -0.009 | +0.032 | -0.112 | -0.008 | +0.013 | 260/450 |
| anchor80 | -0.008 [-0.068, +0.053] | neutral | +0.029 | +0.004 [-0.040, +0.050] | neutral | -0.029 | +0.052 | +0.013 | +0.096 | -0.112 | +0.011 | -0.014 | 262/450 |
| anchor150 | +0.015 [-0.046, +0.068] | neutral | +0.010 | +0.014 [-0.028, +0.052] | neutral | -0.046 | +0.025 | +0.049 | +0.012 | +0.028 | -0.012 | +0.086 | 265/450 |
| anchor80_r20 | -0.020 [-0.084, +0.042] | neutral | +0.026 | -0.005 [-0.051, +0.040] | neutral | +0.006 | +0.003 | +0.033 | +0.026 | -0.090 | -0.009 | +0.007 | 258/450 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.587 over 150 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.587^2 / (150 * K)): K=2: 0.094, K=3: 0.077, K=4: 0.066, K=6: 0.054, K=8: 0.047
