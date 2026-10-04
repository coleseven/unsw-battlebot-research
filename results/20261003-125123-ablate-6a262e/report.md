# Ablation report: 20261003-125123-ablate-6a262e

2 seeds [681001, 681002], opponents cpp_nicked_v92, cpp_nicked_v75, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy (families: nicked 3, ours 4); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin -0.063, wins 222/476; by opponent: cpp_nicked_v92 -0.412, cpp_nicked_v75 -0.324, nicked_lab -0.029, opp-careful-queen +0.000, opp-raider -0.206, opp-growth-queen +0.353, opp-economy +0.176

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ref100 | +0.042 [-0.074, +0.162] | unclear | +2.1 [-3.7, +8.1] | +0.042 | +0.056 | +0.059 | +0.176 | +0.235 | +0.029 | +0.000 | -0.147 | -0.059 | 233/476 |
| ref250 | +0.042 [-0.067, +0.155] | unclear | +2.1 [-3.4, +7.8] | +0.042 | +0.047 | +0.118 | +0.029 | +0.088 | -0.088 | +0.176 | -0.029 | +0.000 | 233/476 |

Per map (wins/games; delta vs base):

| map | base | ref100 | ref250 |
|---|---|---|---|
| around_unsw | 18/28 | 11/28 (-0.500) | 14/28 (-0.286) |
| australia | 9/28 | 15/28 (+0.429) | 17/28 (+0.571) |
| autarky | 14/28 | 17/28 (+0.214) | 16/28 (+0.143) |
| default | 16/28 | 19/28 (+0.214) | 17/28 (+0.071) |
| devil | 20/28 | 17/28 (-0.214) | 18/28 (-0.143) |
| islands | 7/28 | 8/28 (+0.071) | 9/28 (+0.143) |
| maze | 16/28 | 17/28 (+0.071) | 15/28 (-0.071) |
| portals | 11/28 | 17/28 (+0.429) | 12/28 (+0.071) |
| prisoners_dilemma | 8/28 | 9/28 (+0.071) | 12/28 (+0.286) |
| queen_of_spades | 10/28 | 8/28 (-0.143) | 14/28 (+0.286) |
| schooltime | 17/28 | 17/28 (+0.000) | 17/28 (+0.000) |
| slithery_fight | 12/28 | 15/28 (+0.214) | 14/28 (+0.143) |
| stripes | 19/28 | 19/28 (+0.000) | 14/28 (-0.357) |
| tower_defense | 12/28 | 6/28 (-0.429) | 7/28 (-0.357) |
| trauma | 14/28 | 18/28 (+0.286) | 16/28 (+0.143) |
| trophy | 11/28 | 11/28 (+0.000) | 12/28 (+0.071) |
| weakhold | 8/28 | 9/28 (+0.000) | 9/28 (+0.000) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.830 over 238 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.830^2 / (238 * K)): K=2: 0.105, K=3: 0.086, K=4: 0.075, K=6: 0.061, K=8: 0.053
