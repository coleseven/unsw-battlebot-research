# Ablation report: 20261003-171037-ablate-052b88

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy; 17 official + 0 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.053, wins 358/680; by opponent: cpp_nicked_v92 -0.500, cpp_nicked_v75 -0.118, cpp_leviathan3 +0.559, v7-base-bot +0.559, nicked_v44 +0.324, nicked_lab -0.147, opp-careful-queen -0.029, opp-raider -0.088, opp-growth-queen +0.029, opp-economy -0.059

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ref100 | +0.040 [+0.010, +0.070] | harmful (drop) | +0.125 | +0.100 [+0.029, +0.176] | harmful (drop) | +0.235 | -0.059 | +0.000 | +0.088 | +0.059 | +0.147 | +0.000 | -0.029 | +0.324 | +0.235 | +0.100 | - | 392/680 |
| ref250 | +0.050 [-0.050, +0.140] | neutral | +0.092 | +0.079 [+0.003, +0.156] | harmful (drop) | +0.265 | -0.088 | +0.088 | +0.088 | -0.029 | -0.029 | +0.088 | +0.059 | +0.059 | +0.294 | +0.079 | - | 385/680 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.840 over 340 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.840^2 / (340 * K)): K=2: 0.089, K=3: 0.073, K=4: 0.063, K=6: 0.052, K=8: 0.045
