# Ablation report: 20261006-164930-ablate-c1a05d

2 seeds [941001, 941002], opponents cpp_nicked_v92, cpp_leviathan3, nicked_lab, opp-careful-queen, opp-raider, opp-hunter, opp-economy (families: cpp_leviathan3 1, nicked 2, ours 4); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.063, wins 253/476; by opponent: cpp_nicked_v92 -0.382, cpp_leviathan3 +0.706, nicked_lab +0.059, opp-careful-queen +0.029, opp-raider +0.000, opp-hunter -0.059, opp-economy +0.088

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_leviathan3 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-hunter | vs opp-economy | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v3half | +0.025 [-0.088, +0.139] | unclear | +1.3 [-4.4, +6.9] | +0.025 | +0.012 | +0.088 | +0.000 | -0.118 | +0.088 | -0.029 | -0.059 | +0.206 | 259/476 |
| v3quarter | -0.063 [-0.189, +0.063] | unclear | -3.2 [-9.5, +3.2] | -0.063 | -0.066 | -0.029 | -0.029 | -0.235 | +0.176 | -0.059 | -0.206 | -0.059 | 238/476 |

Per map (wins/games; delta vs base):

| map | base | v3half | v3quarter |
|---|---|---|---|
| around_unsw | 12/28 | 15/28 (+0.214) | 15/28 (+0.214) |
| australia | 16/28 | 15/28 (-0.071) | 11/28 (-0.357) |
| autarky | 16/28 | 14/28 (-0.143) | 13/28 (-0.214) |
| default | 12/28 | 15/28 (+0.214) | 10/28 (-0.143) |
| devil | 14/28 | 12/28 (-0.143) | 9/28 (-0.357) |
| islands | 18/28 | 15/28 (-0.214) | 13/28 (-0.357) |
| maze | 15/28 | 17/28 (+0.143) | 14/28 (-0.071) |
| portals | 13/28 | 18/28 (+0.357) | 15/28 (+0.143) |
| prisoners_dilemma | 8/28 | 4/28 (-0.286) | 9/28 (+0.071) |
| queen_of_spades | 13/28 | 14/28 (+0.071) | 10/28 (-0.214) |
| schooltime | 19/28 | 17/28 (-0.143) | 18/28 (-0.071) |
| slithery_fight | 21/28 | 18/28 (-0.214) | 19/28 (-0.143) |
| stripes | 10/28 | 11/28 (+0.071) | 9/28 (-0.071) |
| tower_defense | 21/28 | 21/28 (+0.000) | 18/28 (-0.214) |
| trauma | 16/28 | 20/28 (+0.286) | 18/28 (+0.143) |
| trophy | 10/28 | 13/28 (+0.214) | 17/28 (+0.500) |
| weakhold | 19/28 | 20/28 (+0.071) | 20/28 (+0.071) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.845 over 238 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.845^2 / (238 * K)): K=2: 0.107, K=3: 0.088, K=4: 0.076, K=6: 0.062, K=8: 0.054
