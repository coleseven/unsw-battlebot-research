# Ablation report: 20261004-172323-ablate-961460

2 seeds [841001, 841002], opponents cpp_nicked_v92, cpp_leviathan3, nicked_lab, opp-careful-queen, opp-raider, opp-economy (families: cpp_leviathan3 1, nicked 2, ours 3); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.127, wins 230/408; by opponent: cpp_nicked_v92 -0.235, cpp_leviathan3 +0.706, nicked_lab -0.147, opp-careful-queen +0.235, opp-raider -0.088, opp-economy +0.294

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_leviathan3 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-economy | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| calm1 | -0.147 [-0.255, -0.034] | variant worse | -7.4 [-12.7, -1.7] | -0.147 | -0.126 | -0.294 | -0.029 | -0.088 | -0.265 | +0.029 | -0.235 | 199/408 |
| calm2 | -0.054 [-0.191, +0.078] | unclear | -2.7 [-9.6, +3.9] | -0.054 | -0.031 | -0.265 | +0.088 | +0.000 | -0.294 | +0.294 | -0.147 | 219/408 |

Per map (wins/games; delta vs base):

| map | base | calm1 | calm2 |
|---|---|---|---|
| around_unsw | 13/24 | 17/24 (+0.333) | 19/24 (+0.500) |
| australia | 15/24 | 10/24 (-0.417) | 13/24 (-0.167) |
| autarky | 15/24 | 12/24 (-0.250) | 10/24 (-0.417) |
| default | 15/24 | 10/24 (-0.417) | 12/24 (-0.250) |
| devil | 16/24 | 14/24 (-0.167) | 10/24 (-0.500) |
| islands | 13/24 | 14/24 (+0.083) | 14/24 (+0.083) |
| maze | 12/24 | 14/24 (+0.167) | 15/24 (+0.250) |
| portals | 14/24 | 11/24 (-0.250) | 10/24 (-0.333) |
| prisoners_dilemma | 8/24 | 8/24 (+0.000) | 14/24 (+0.500) |
| queen_of_spades | 15/24 | 10/24 (-0.417) | 10/24 (-0.417) |
| schooltime | 14/24 | 14/24 (+0.000) | 14/24 (+0.000) |
| slithery_fight | 21/24 | 10/24 (-0.917) | 16/24 (-0.417) |
| stripes | 10/24 | 11/24 (+0.083) | 13/24 (+0.250) |
| tower_defense | 9/24 | 10/24 (+0.083) | 15/24 (+0.500) |
| trauma | 17/24 | 17/24 (+0.000) | 15/24 (-0.167) |
| trophy | 11/24 | 9/24 (-0.167) | 10/24 (-0.083) |
| weakhold | 12/24 | 8/24 (-0.250) | 9/24 (-0.250) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.852 over 204 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.852^2 / (204 * K)): K=2: 0.117, K=3: 0.095, K=4: 0.083, K=6: 0.067, K=8: 0.058
