# Ablation report: 20261003-115234-ablate-b8901c

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 17 official + 0 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.071, wins 255/476; by opponent: cpp_nicked_v92 -0.529, cpp_nicked_v75 -0.294, cpp_leviathan3 +0.529, v7-base-bot +0.441, nicked_v44 +0.412, nicked_lab -0.059, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| y150 | +0.000 [+0.000, +0.000] | neutral | +0.018 | +0.013 [+0.000, +0.029] | neutral | +0.000 | +0.000 | +0.000 | +0.000 | +0.029 | +0.029 | +0.029 | +0.013 | - | 258/476 |
| y300 | +0.000 [+0.000, +0.000] | neutral | +0.018 | +0.013 [+0.000, +0.029] | neutral | +0.000 | +0.000 | +0.000 | +0.000 | +0.029 | +0.029 | +0.029 | +0.013 | - | 258/476 |
| y150_t2 | +0.100 [-0.029, +0.257] | neutral | +0.137 | +0.126 [+0.025, +0.218] | harmful (drop) | +0.265 | +0.206 | +0.088 | +0.147 | -0.029 | +0.176 | +0.029 | +0.126 | - | 285/476 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.815 over 238 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.815^2 / (238 * K)): K=2: 0.104, K=3: 0.085, K=4: 0.073, K=6: 0.060, K=8: 0.052
