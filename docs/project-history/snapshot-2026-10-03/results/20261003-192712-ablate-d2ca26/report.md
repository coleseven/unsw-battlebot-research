# Ablation report: 20261003-192712-ablate-d2ca26

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy; 17 official + 0 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.182, wins 402/680; by opponent: cpp_nicked_v92 -0.382, cpp_nicked_v75 -0.294, cpp_leviathan3 +0.794, v7-base-bot +0.500, nicked_v44 +0.588, nicked_lab +0.147, opp-careful-queen +0.206, opp-raider -0.059, opp-growth-queen +0.265, opp-economy +0.059

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sx2 | -0.040 [-0.130, +0.020] | neutral | -0.087 | -0.074 [-0.153, -0.009] | essential | -0.088 | -0.059 | -0.088 | -0.118 | -0.059 | -0.088 | -0.147 | -0.059 | -0.088 | +0.059 | -0.074 | - | 377/680 |
| sx3 | -0.090 [-0.180, -0.010] | essential | -0.046 | -0.059 [-0.144, +0.009] | neutral | +0.000 | +0.029 | -0.059 | -0.088 | -0.059 | -0.235 | -0.206 | -0.029 | -0.118 | +0.176 | -0.059 | - | 382/680 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.854 over 340 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.854^2 / (340 * K)): K=2: 0.091, K=3: 0.074, K=4: 0.064, K=6: 0.052, K=8: 0.045
