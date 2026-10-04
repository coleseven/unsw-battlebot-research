# Ablation report: 20261004-160858-ablate-b4a68d

2 seeds [821001, 821002], opponents cpp_nicked_v92, cpp_leviathan3, nicked_lab, opp-careful-queen, opp-raider, opp-economy (families: cpp_leviathan3 1, nicked 2, ours 3); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.039, wins 212/408; by opponent: cpp_nicked_v92 -0.294, cpp_leviathan3 +0.588, nicked_lab +0.029, opp-careful-queen -0.029, opp-raider -0.294, opp-economy +0.235

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_leviathan3 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-economy | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pt | -0.025 [-0.093, +0.025] | unclear | -1.2 [-4.7, +1.2] | -0.025 | -0.015 | -0.059 | +0.029 | -0.029 | -0.029 | -0.029 | -0.029 | 207/408 |
| pt2 | +0.029 [-0.108, +0.162] | unclear | +1.5 [-5.4, +8.1] | +0.029 | +0.059 | +0.000 | +0.176 | +0.000 | +0.088 | +0.118 | -0.206 | 218/408 |
| pt1 | +0.032 [-0.113, +0.172] | unclear | +1.6 [-5.6, +8.6] | +0.032 | +0.026 | +0.059 | +0.015 | -0.029 | +0.029 | +0.265 | -0.147 | 216/408 |

Per map (wins/games; delta vs base):

| map | base | pt | pt2 | pt1 |
|---|---|---|---|---|
| around_unsw | 10/24 | 10/24 (+0.000) | 14/24 (+0.333) | 17/24 (+0.583) |
| australia | 10/24 | 10/24 (+0.000) | 13/24 (+0.250) | 13/24 (+0.250) |
| autarky | 11/24 | 11/24 (+0.000) | 17/24 (+0.500) | 9/24 (-0.167) |
| default | 16/24 | 15/24 (-0.083) | 13/24 (-0.250) | 9/24 (-0.583) |
| devil | 12/24 | 12/24 (+0.000) | 10/24 (-0.167) | 13/24 (+0.083) |
| islands | 12/24 | 12/24 (+0.000) | 10/24 (-0.167) | 7/24 (-0.417) |
| maze | 15/24 | 15/24 (+0.000) | 15/24 (+0.000) | 15/24 (+0.000) |
| portals | 16/24 | 15/24 (-0.083) | 11/24 (-0.417) | 15/24 (-0.083) |
| prisoners_dilemma | 6/24 | 6/24 (+0.000) | 4/24 (-0.167) | 4/24 (-0.167) |
| queen_of_spades | 17/24 | 17/24 (+0.000) | 18/24 (+0.083) | 17/24 (+0.000) |
| schooltime | 17/24 | 17/24 (+0.000) | 17/24 (+0.000) | 17/24 (+0.000) |
| slithery_fight | 17/24 | 17/24 (+0.000) | 13/24 (-0.333) | 15/24 (-0.167) |
| stripes | 4/24 | 6/24 (+0.167) | 16/24 (+1.000) | 16/24 (+1.000) |
| tower_defense | 9/24 | 9/24 (+0.000) | 13/24 (+0.333) | 10/24 (+0.083) |
| trauma | 14/24 | 9/24 (-0.417) | 13/24 (-0.083) | 15/24 (+0.083) |
| trophy | 14/24 | 14/24 (+0.000) | 14/24 (+0.000) | 15/24 (+0.083) |
| weakhold | 12/24 | 12/24 (+0.000) | 7/24 (-0.417) | 9/24 (-0.042) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.863 over 204 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.863^2 / (204 * K)): K=2: 0.118, K=3: 0.097, K=4: 0.084, K=6: 0.068, K=8: 0.059
