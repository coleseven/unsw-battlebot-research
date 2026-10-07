# Ablation report: 20261007-084959-ablate-ca9d33

2 seeds [1001001, 1001002], opponents cpp_nicked_v92, cpp_leviathan3, nicked_lab, opp-careful-queen, opp-raider, opp-hunter, opp-sprinter, opp-economy (families: cpp_leviathan3 1, nicked 2, ours 5); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.018, wins 277/544; by opponent: cpp_nicked_v92 -0.353, cpp_leviathan3 +0.706, nicked_lab -0.118, opp-careful-queen -0.029, opp-raider +0.029, opp-hunter -0.206, opp-sprinter -0.206, opp-economy +0.324

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_leviathan3 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-hunter | vs opp-sprinter | vs opp-economy | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| es3 | +0.000 [-0.048, +0.044] | unclear | +0.0 [-2.4, +2.2] | +0.000 | -0.028 | +0.059 | -0.118 | -0.029 | +0.029 | -0.088 | +0.029 | +0.118 | +0.000 | 277/544 |
| es4 | -0.040 [-0.114, +0.033] | unclear | -2.0 [-5.7, +1.7] | -0.040 | -0.023 | +0.147 | -0.059 | +0.000 | +0.029 | -0.176 | -0.059 | -0.029 | -0.176 | 266/544 |

Per map (wins/games; delta vs base):

| map | base | es3 | es4 |
|---|---|---|---|
| around_unsw | 19/32 | 20/32 (+0.062) | 15/32 (-0.250) |
| australia | 17/32 | 16/32 (-0.062) | 14/32 (-0.188) |
| autarky | 13/32 | 13/32 (+0.000) | 14/32 (+0.062) |
| default | 17/32 | 13/32 (-0.250) | 14/32 (-0.188) |
| devil | 19/32 | 19/32 (+0.000) | 19/32 (+0.000) |
| islands | 9/32 | 10/32 (+0.062) | 14/32 (+0.312) |
| maze | 15/32 | 16/32 (+0.062) | 15/32 (+0.000) |
| portals | 14/32 | 14/32 (+0.000) | 14/32 (+0.000) |
| prisoners_dilemma | 7/32 | 9/32 (+0.125) | 8/32 (+0.062) |
| queen_of_spades | 16/32 | 17/32 (+0.062) | 15/32 (-0.062) |
| schooltime | 21/32 | 19/32 (-0.125) | 17/32 (-0.250) |
| slithery_fight | 24/32 | 23/32 (-0.062) | 21/32 (-0.188) |
| stripes | 8/32 | 8/32 (+0.000) | 7/32 (-0.062) |
| tower_defense | 24/32 | 25/32 (+0.062) | 25/32 (+0.062) |
| trauma | 19/32 | 18/32 (-0.062) | 18/32 (-0.062) |
| trophy | 13/32 | 15/32 (+0.125) | 15/32 (+0.125) |
| weakhold | 22/32 | 22/32 (+0.000) | 21/32 (-0.062) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.870 over 272 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.870^2 / (272 * K)): K=2: 0.103, K=3: 0.084, K=4: 0.073, K=6: 0.060, K=8: 0.052
