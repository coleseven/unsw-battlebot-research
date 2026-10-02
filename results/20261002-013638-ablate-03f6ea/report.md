# Ablation report: 20261002-013638-ablate-03f6ea

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 11 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.130, wins 447/792; by opponent: cpp_nicked_v92 -0.470, cpp_nicked_v75 -0.242, cpp_leviathan3 +0.553, v7-base-bot +0.500, nicked_v44 +0.485, nicked_lab -0.045

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ms | +0.061 [-0.017, +0.150] | neutral | +0.074 | +0.068 [+0.013, +0.124] | harmful (drop) | +0.000 | +0.152 | +0.152 | +0.015 | +0.000 | +0.091 | +0.121 | +0.015 | 474/792 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.854 over 264 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.854^2 / (264 * K)): K=2: 0.103, K=3: 0.084, K=4: 0.073, K=6: 0.059, K=8: 0.051
