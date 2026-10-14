# Ablation report: 20260929-152611-ablate-5cb6f9

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.010, wins 280/540; by opponent: cpp_nicked_v92 -0.525, cpp_nicked_v75 -0.366, cpp_leviathan3 +0.472, v7-base-bot +0.365, nicked_v44 +0.258, nicked_lab -0.144

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| book | +0.118 [+0.033, +0.203] | harmful (drop) | +0.034 | +0.090 [+0.019, +0.164] | harmful (drop) | +0.027 | +0.164 | +0.089 | +0.066 | +0.071 | +0.124 | +0.123 | +0.000 | 316/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.575 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.575^2 / (180 * K)): K=2: 0.084, K=3: 0.069, K=4: 0.059, K=6: 0.049, K=8: 0.042
