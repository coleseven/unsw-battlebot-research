# Ablation report: 20261004-233200-ablate-bc4e4e

2 seeds [861001, 861002], opponents cpp_nicked_v92, cpp_leviathan3, nicked_lab, opp-careful-queen, opp-raider, opp-economy (families: cpp_leviathan3 1, nicked 2, ours 3); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.083, wins 221/408; by opponent: cpp_nicked_v92 -0.471, cpp_leviathan3 +0.647, nicked_lab +0.000, opp-careful-queen +0.235, opp-raider -0.088, opp-economy +0.176

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_leviathan3 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-economy | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| e40 | +0.044 [-0.074, +0.172] | unclear | +2.2 [-3.7, +8.6] | +0.044 | +0.059 | +0.088 | +0.088 | +0.088 | -0.235 | +0.088 | +0.147 | 230/408 |
| e80 | +0.010 [-0.103, +0.135] | unclear | +0.5 [-5.1, +6.7] | +0.010 | +0.023 | +0.147 | +0.029 | +0.029 | -0.176 | -0.059 | +0.088 | 222/408 |

Per map (wins/games; delta vs base):

| map | base | e40 | e80 |
|---|---|---|---|
| around_unsw | 15/24 | 18/24 (+0.250) | 14/24 (-0.083) |
| australia | 10/24 | 12/24 (+0.167) | 11/24 (+0.083) |
| autarky | 15/24 | 11/24 (-0.333) | 16/24 (+0.083) |
| default | 15/24 | 13/24 (-0.167) | 16/24 (+0.083) |
| devil | 14/24 | 14/24 (+0.000) | 11/24 (-0.250) |
| islands | 10/24 | 13/24 (+0.250) | 10/24 (+0.000) |
| maze | 19/24 | 14/24 (-0.417) | 15/24 (-0.333) |
| portals | 14/24 | 14/24 (+0.000) | 14/24 (+0.000) |
| prisoners_dilemma | 8/24 | 10/24 (+0.167) | 8/24 (+0.000) |
| queen_of_spades | 15/24 | 11/24 (-0.333) | 15/24 (+0.000) |
| schooltime | 17/24 | 17/24 (+0.000) | 17/24 (+0.000) |
| slithery_fight | 14/24 | 23/24 (+0.750) | 20/24 (+0.500) |
| stripes | 8/24 | 8/24 (+0.000) | 11/24 (+0.250) |
| tower_defense | 8/24 | 15/24 (+0.583) | 14/24 (+0.500) |
| trauma | 17/24 | 15/24 (-0.167) | 14/24 (-0.250) |
| trophy | 10/24 | 10/24 (+0.000) | 10/24 (+0.000) |
| weakhold | 12/24 | 12/24 (+0.000) | 6/24 (-0.417) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.798 over 204 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.798^2 / (204 * K)): K=2: 0.110, K=3: 0.089, K=4: 0.077, K=6: 0.063, K=8: 0.055
