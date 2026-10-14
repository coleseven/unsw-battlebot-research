# Ablation report: 20260927-021008-ablate-5c0197

4 seeds, opponents v7-base-bot, nicked; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.165, wins 147/240; by opponent: v7-base-bot +0.000, nicked +0.331

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs v7-base-bot | vs nicked | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|
| drop_harmful | +0.131 [+0.051, +0.210] | harmful (drop) | -0.022 | +0.080 [+0.018, +0.148] | harmful (drop) | +0.104 | +0.057 | +0.018 | +0.250 | 161/240 |
| lean | +0.098 [-0.057, +0.248] | neutral | +0.007 | +0.068 [-0.050, +0.177] | neutral | +0.122 | +0.013 | -0.000 | +0.254 | 159/240 |
| simplified | +0.005 [-0.143, +0.148] | neutral | +0.109 | +0.040 [-0.085, +0.149] | neutral | +0.097 | -0.018 | -0.048 | +0.280 | 156/240 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.645 over 60 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.645^2 / (60 * K)): K=2: 0.163, K=3: 0.133, K=4: 0.115, K=6: 0.094, K=8: 0.082
