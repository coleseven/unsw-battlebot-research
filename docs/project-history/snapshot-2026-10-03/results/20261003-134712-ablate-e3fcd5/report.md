# Ablation report: 20261003-134712-ablate-e3fcd5

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy; 17 official + 0 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.050, wins 534/1020; by opponent: cpp_nicked_v92 -0.667, cpp_nicked_v75 -0.314, cpp_leviathan3 +0.569, v7-base-bot +0.588, nicked_v44 +0.392, nicked_lab -0.157, opp-careful-queen +0.000, opp-raider -0.098, opp-growth-queen +0.137, opp-economy +0.049

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t2 | -0.003 [-0.067, +0.070] | neutral | +0.100 | +0.070 [-0.003, +0.141] | neutral | +0.294 | +0.039 | +0.098 | -0.176 | +0.020 | +0.118 | +0.157 | -0.078 | -0.059 | +0.284 | +0.070 | - | 571/1020 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.831 over 340 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.831^2 / (340 * K)): K=2: 0.088, K=3: 0.072, K=4: 0.062, K=6: 0.051, K=8: 0.044
