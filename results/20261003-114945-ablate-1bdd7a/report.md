# Ablation report: 20261003-114945-ablate-1bdd7a

2 seeds [651001, 651002], opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab (families: cpp_leviathan3 1, nicked 4, ours 1); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.186, wins 242/408; by opponent: cpp_nicked_v92 -0.294, cpp_nicked_v75 -0.294, cpp_leviathan3 +0.588, v7-base-bot +0.529, nicked_v44 +0.500, nicked_lab +0.088

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| nobookmap | -0.064 [-0.176, +0.039] | unclear | -3.2 [-8.8, +2.0] | -0.064 | -0.039 | -0.029 | -0.088 | +0.029 | -0.059 | -0.059 | -0.176 | 229/408 |
| nobooks | -0.127 [-0.275, +0.005] | unclear | -6.4 [-13.7, +0.2] | -0.127 | -0.086 | -0.206 | -0.029 | +0.029 | -0.118 | -0.088 | -0.353 | 216/408 |

Per map (wins/games; delta vs base):

| map | base | nobookmap | nobooks |
|---|---|---|---|
| around_unsw | 19/24 | 18/24 (-0.083) | 18/24 (-0.083) |
| australia | 17/24 | 13/24 (-0.333) | 13/24 (-0.333) |
| autarky | 15/24 | 15/24 (+0.000) | 15/24 (+0.000) |
| default | 19/24 | 12/24 (-0.583) | 12/24 (-0.583) |
| devil | 13/24 | 18/24 (+0.417) | 14/24 (+0.083) |
| islands | 11/24 | 11/24 (+0.000) | 11/24 (+0.000) |
| maze | 19/24 | 19/24 (+0.000) | 16/24 (-0.250) |
| portals | 12/24 | 12/24 (+0.000) | 14/24 (+0.167) |
| prisoners_dilemma | 9/24 | 9/24 (+0.000) | 13/24 (+0.333) |
| queen_of_spades | 18/24 | 14/24 (-0.333) | 5/24 (-1.083) |
| schooltime | 19/24 | 18/24 (-0.083) | 16/24 (-0.250) |
| slithery_fight | 13/24 | 13/24 (+0.000) | 14/24 (+0.083) |
| stripes | 13/24 | 13/24 (+0.000) | 13/24 (+0.000) |
| tower_defense | 18/24 | 18/24 (+0.000) | 18/24 (+0.000) |
| trauma | 12/24 | 12/24 (+0.000) | 10/24 (-0.167) |
| trophy | 10/24 | 9/24 (-0.083) | 9/24 (-0.083) |
| weakhold | 5/24 | 5/24 (+0.000) | 5/24 (+0.000) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.804 over 204 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.804^2 / (204 * K)): K=2: 0.110, K=3: 0.090, K=4: 0.078, K=6: 0.064, K=8: 0.055
