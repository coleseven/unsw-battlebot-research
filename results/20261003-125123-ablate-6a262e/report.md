# Ablation report: 20261003-125123-ablate-6a262e

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy; 17 official + 0 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin -0.063, wins 222/476; by opponent: cpp_nicked_v92 -0.412, cpp_nicked_v75 -0.324, nicked_lab -0.029, opp-careful-queen +0.000, opp-raider -0.206, opp-growth-queen +0.353, opp-economy +0.176

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ref100 | +0.014 [-0.093, +0.164] | neutral | +0.054 | +0.042 [-0.074, +0.162] | neutral | +0.059 | +0.176 | +0.235 | +0.029 | +0.000 | -0.147 | -0.059 | +0.042 | - | 233/476 |
| ref250 | +0.086 [-0.007, +0.193] | neutral | +0.024 | +0.042 [-0.067, +0.155] | neutral | +0.118 | +0.029 | +0.088 | -0.088 | +0.176 | -0.029 | +0.000 | +0.042 | - | 233/476 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.830 over 238 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.830^2 / (238 * K)): K=2: 0.105, K=3: 0.086, K=4: 0.075, K=6: 0.061, K=8: 0.053
