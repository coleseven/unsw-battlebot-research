# Ablation report: 20260929-005706-ablate-39e66c

3 seeds, opponents cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44; 11 official + 14 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.209, wins 386/600; by opponent: cpp_nicked_v75 -0.238, cpp_leviathan3 +0.462, v7-base-bot +0.409, nicked_v44 +0.202

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hub_observe | -0.104 [-0.175, -0.041] | essential | +0.007 | -0.038 [-0.093, +0.019] | neutral | -0.081 | -0.087 | -0.050 | +0.068 | -0.088 | +0.002 | 367/600 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.552 over 200 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.552^2 / (200 * K)): K=2: 0.076, K=3: 0.062, K=4: 0.054, K=6: 0.044, K=8: 0.038
