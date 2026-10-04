# Ablation report: 20261003-214401-ablate-28bd72

2 seeds [761001, 761002], opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy (families: cpp_leviathan3 1, nicked 4, ours 5); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.159, wins 394/680; by opponent: cpp_nicked_v92 -0.235, cpp_nicked_v75 -0.412, cpp_leviathan3 +0.676, v7-base-bot +0.588, nicked_v44 +0.471, nicked_lab +0.088, opp-careful-queen +0.029, opp-raider -0.176, opp-growth-queen +0.176, opp-economy +0.382

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sp1 | -0.071 [-0.153, +0.015] | unclear | -3.5 [-7.6, +0.7] | -0.071 | -0.058 | -0.118 | +0.118 | -0.029 | -0.088 | -0.059 | -0.147 | -0.029 | +0.088 | -0.235 | -0.206 | 370/680 |
| sp2 | -0.062 [-0.132, +0.009] | unclear | -3.1 [-6.6, +0.4] | -0.062 | -0.036 | -0.206 | +0.176 | +0.029 | -0.235 | +0.000 | -0.118 | -0.029 | +0.176 | -0.265 | -0.147 | 373/680 |

Per map (wins/games; delta vs base):

| map | base | sp1 | sp2 |
|---|---|---|---|
| around_unsw | 29/40 | 28/40 (-0.050) | 26/40 (-0.150) |
| australia | 23/40 | 24/40 (+0.050) | 23/40 (+0.000) |
| autarky | 24/40 | 20/40 (-0.200) | 23/40 (-0.050) |
| default | 29/40 | 29/40 (+0.000) | 30/40 (+0.050) |
| devil | 27/40 | 27/40 (+0.000) | 25/40 (-0.100) |
| islands | 24/40 | 20/40 (-0.200) | 21/40 (-0.150) |
| maze | 28/40 | 25/40 (-0.150) | 29/40 (+0.050) |
| portals | 27/40 | 15/40 (-0.600) | 17/40 (-0.500) |
| prisoners_dilemma | 16/40 | 21/40 (+0.250) | 20/40 (+0.200) |
| queen_of_spades | 25/40 | 29/40 (+0.200) | 23/40 (-0.100) |
| schooltime | 29/40 | 29/40 (+0.000) | 29/40 (+0.000) |
| slithery_fight | 23/40 | 25/40 (+0.100) | 26/40 (+0.150) |
| stripes | 8/40 | 8/40 (+0.000) | 8/40 (+0.000) |
| tower_defense | 16/40 | 16/40 (+0.000) | 18/40 (+0.100) |
| trauma | 31/40 | 23/40 (-0.400) | 24/40 (-0.350) |
| trophy | 21/40 | 19/40 (-0.100) | 19/40 (-0.100) |
| weakhold | 14/40 | 12/40 (-0.100) | 12/40 (-0.100) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.790 over 340 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.790^2 / (340 * K)): K=2: 0.084, K=3: 0.069, K=4: 0.059, K=6: 0.048, K=8: 0.042
