# Ablation report: 20260929-074209-ablate-87a257

3 seeds, opponents cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.131, wins 212/360; by opponent: cpp_nicked_v75 -0.338, cpp_leviathan3 +0.311, v7-base-bot +0.325, nicked_v44 +0.226

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v11 | +0.105 [+0.008, +0.191] | harmful (drop) | -0.065 | +0.048 [-0.025, +0.123] | neutral | -0.059 | +0.152 | +0.032 | +0.067 | -0.004 | +0.192 | 232/360 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.628 over 120 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.628^2 / (120 * K)): K=2: 0.112, K=3: 0.092, K=4: 0.079, K=6: 0.065, K=8: 0.056
