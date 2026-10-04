# Ablation report: 20261003-171037-ablate-052b88

2 seeds [721001, 721002], opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy (families: cpp_leviathan3 1, nicked 4, ours 5); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.053, wins 358/680; by opponent: cpp_nicked_v92 -0.500, cpp_nicked_v75 -0.118, cpp_leviathan3 +0.559, v7-base-bot +0.559, nicked_v44 +0.324, nicked_lab -0.147, opp-careful-queen -0.029, opp-raider -0.088, opp-growth-queen +0.029, opp-economy -0.059

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ref100 | +0.100 [+0.029, +0.176] | variant better | +5.0 [+1.5, +8.8] | +0.100 | +0.073 | +0.235 | -0.059 | +0.000 | +0.088 | +0.059 | +0.147 | +0.000 | -0.029 | +0.324 | +0.235 | 392/680 |
| ref250 | +0.079 [+0.003, +0.156] | variant better | +4.0 [+0.1, +7.8] | +0.079 | +0.078 | +0.265 | -0.088 | +0.088 | +0.088 | -0.029 | -0.029 | +0.088 | +0.059 | +0.059 | +0.294 | 385/680 |

Per map (wins/games; delta vs base):

| map | base | ref100 | ref250 |
|---|---|---|---|
| around_unsw | 27/40 | 28/40 (+0.050) | 26/40 (-0.050) |
| australia | 18/40 | 25/40 (+0.350) | 22/40 (+0.200) |
| autarky | 26/40 | 28/40 (+0.100) | 25/40 (-0.050) |
| default | 25/40 | 26/40 (+0.050) | 29/40 (+0.200) |
| devil | 24/40 | 28/40 (+0.200) | 26/40 (+0.100) |
| islands | 25/40 | 22/40 (-0.150) | 19/40 (-0.300) |
| maze | 20/40 | 26/40 (+0.300) | 25/40 (+0.250) |
| portals | 18/40 | 23/40 (+0.250) | 26/40 (+0.400) |
| prisoners_dilemma | 18/40 | 19/40 (+0.050) | 19/40 (+0.050) |
| queen_of_spades | 26/40 | 28/40 (+0.100) | 27/40 (+0.050) |
| schooltime | 28/40 | 28/40 (+0.000) | 28/40 (+0.000) |
| slithery_fight | 26/40 | 27/40 (+0.050) | 28/40 (+0.100) |
| stripes | 8/40 | 11/40 (+0.150) | 12/40 (+0.200) |
| tower_defense | 17/40 | 12/40 (-0.250) | 12/40 (-0.250) |
| trauma | 23/40 | 31/40 (+0.400) | 32/40 (+0.450) |
| trophy | 15/40 | 16/40 (+0.050) | 12/40 (-0.150) |
| weakhold | 14/40 | 14/40 (+0.000) | 17/40 (+0.150) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.840 over 340 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.840^2 / (340 * K)): K=2: 0.089, K=3: 0.073, K=4: 0.063, K=6: 0.052, K=8: 0.045
