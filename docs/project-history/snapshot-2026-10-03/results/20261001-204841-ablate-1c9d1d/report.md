# Ablation report: 20261001-204841-ablate-1c9d1d

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.200, wins 216/360; by opponent: cpp_nicked_v92 -0.467, cpp_nicked_v75 +0.033, cpp_leviathan3 +0.667, v7-base-bot +0.533, nicked_v44 +0.433, nicked_lab +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| q_ms | -0.075 [-0.267, +0.133] | neutral | -0.533 | -0.228 [-0.422, -0.022] | essential | -0.167 | -0.367 | -0.167 | -0.367 | -0.167 | -0.133 | -0.227 | -0.229 | 175/360 |
| q_ms_s7 | -0.625 [-0.850, -0.400] | essential | -0.683 | -0.644 [-0.844, -0.417] | essential | -0.333 | -0.800 | -0.733 | -0.767 | -0.567 | -0.667 | -0.667 | -0.583 | 100/360 |
| q_ms_s11 | -0.692 [-0.933, -0.433] | essential | -0.833 | -0.739 [-0.967, -0.494] | essential | -0.467 | -0.933 | -0.467 | -1.000 | -0.833 | -0.733 | -0.795 | -0.583 | 83/360 |
| q_s7 | -0.633 [-0.875, -0.375] | essential | -0.900 | -0.722 [-0.922, -0.517] | essential | -0.433 | -0.800 | -0.700 | -0.967 | -0.733 | -0.700 | -0.788 | -0.542 | 86/360 |
| ms_s7 | -0.517 [-0.758, -0.275] | essential | -0.467 | -0.500 [-0.744, -0.239] | essential | -0.167 | -0.767 | -0.367 | -0.667 | -0.400 | -0.633 | -0.576 | -0.292 | 126/360 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.803 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.803^2 / (180 * K)): K=2: 0.117, K=3: 0.096, K=4: 0.083, K=6: 0.068, K=8: 0.059
