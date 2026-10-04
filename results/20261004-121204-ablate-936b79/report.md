# Ablation report: 20261004-121204-ablate-936b79

2 seeds [801001, 801002], opponents cpp_nicked_v92, cpp_leviathan3, nicked_lab, opp-careful-queen, opp-raider, opp-economy (families: cpp_leviathan3 1, nicked 2, ours 3); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.083, wins 221/408; by opponent: cpp_nicked_v92 -0.324, cpp_leviathan3 +0.676, nicked_lab -0.235, opp-careful-queen +0.088, opp-raider +0.118, opp-economy +0.176

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_leviathan3 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-economy | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gp | +0.074 [-0.054, +0.206] | unclear | +3.7 [-2.7, +10.3] | +0.074 | +0.082 | +0.059 | +0.118 | +0.059 | +0.147 | -0.029 | +0.088 | 236/408 |
| hp3 | -0.005 [-0.118, +0.108] | unclear | -0.2 [-5.9, +5.4] | -0.005 | +0.015 | -0.176 | +0.088 | +0.147 | -0.088 | -0.059 | +0.059 | 220/408 |

Per map (wins/games; delta vs base):

| map | base | gp | hp3 |
|---|---|---|---|
| around_unsw | 17/24 | 12/24 (-0.417) | 14/24 (-0.250) |
| australia | 15/24 | 14/24 (-0.083) | 13/24 (-0.167) |
| autarky | 9/24 | 20/24 (+0.917) | 13/24 (+0.333) |
| default | 13/24 | 16/24 (+0.250) | 16/24 (+0.250) |
| devil | 13/24 | 9/24 (-0.333) | 10/24 (-0.250) |
| islands | 9/24 | 11/24 (+0.167) | 11/24 (+0.167) |
| maze | 14/24 | 14/24 (+0.000) | 13/24 (-0.083) |
| portals | 13/24 | 8/24 (-0.417) | 14/24 (+0.083) |
| prisoners_dilemma | 5/24 | 9/24 (+0.333) | 6/24 (+0.083) |
| queen_of_spades | 16/24 | 19/24 (+0.250) | 17/24 (+0.083) |
| schooltime | 19/24 | 17/24 (-0.167) | 15/24 (-0.333) |
| slithery_fight | 14/24 | 16/24 (+0.167) | 18/24 (+0.333) |
| stripes | 14/24 | 12/24 (-0.167) | 14/24 (+0.000) |
| tower_defense | 14/24 | 17/24 (+0.250) | 13/24 (-0.083) |
| trauma | 14/24 | 18/24 (+0.333) | 11/24 (-0.250) |
| trophy | 10/24 | 13/24 (+0.250) | 10/24 (+0.000) |
| weakhold | 12/24 | 11/24 (-0.083) | 12/24 (+0.000) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.869 over 204 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.869^2 / (204 * K)): K=2: 0.119, K=3: 0.097, K=4: 0.084, K=6: 0.069, K=8: 0.060
