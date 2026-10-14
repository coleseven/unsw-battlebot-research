# Ablation report: 20260928-180616-ablate-22301c

3 seeds, opponents cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.273, wins 247/360; by opponent: cpp_nicked_v75 -0.155, cpp_leviathan3 +0.566, v7-base-bot +0.331, nicked_v44 +0.349

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| brief | -0.012 [-0.043, +0.017] | neutral | +0.010 | -0.005 [-0.027, +0.015] | neutral | +0.018 | -0.012 | -0.011 | -0.013 | -0.007 | +0.002 | 247/360 |
| brief_room8 | -0.127 [-0.204, -0.053] | essential | -0.023 | -0.092 [-0.149, -0.041] | essential | -0.001 | -0.167 | -0.059 | -0.142 | -0.097 | -0.078 | 221/360 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.559 over 120 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.559^2 / (120 * K)): K=2: 0.100, K=3: 0.082, K=4: 0.071, K=6: 0.058, K=8: 0.050
