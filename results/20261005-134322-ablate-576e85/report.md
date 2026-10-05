# Ablation report: 20261005-134322-ablate-576e85

2 seeds [921001, 921002], opponents cpp_nicked_v92, cpp_leviathan3, nicked_lab, opp-careful-queen, opp-raider, opp-hunter, opp-economy (families: cpp_leviathan3 1, nicked 2, ours 4); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.067, wins 254/476; by opponent: cpp_nicked_v92 -0.324, cpp_leviathan3 +0.735, nicked_lab -0.059, opp-careful-queen +0.000, opp-raider +0.088, opp-hunter -0.235, opp-economy +0.265

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_leviathan3 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-hunter | vs opp-economy | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dq | +0.025 [-0.067, +0.122] | unclear | +1.3 [-3.4, +6.1] | +0.025 | +0.027 | +0.029 | +0.000 | +0.118 | +0.206 | +0.029 | -0.059 | -0.147 | 260/476 |
| bg2 | +0.000 [-0.021, +0.021] | unclear | +0.0 [-1.1, +1.1] | +0.000 | -0.002 | -0.029 | +0.000 | +0.000 | +0.029 | +0.029 | -0.029 | +0.000 | 254/476 |

Per map (wins/games; delta vs base):

| map | base | dq | bg2 |
|---|---|---|---|
| around_unsw | 16/28 | 12/28 (-0.286) | 16/28 (+0.000) |
| australia | 13/28 | 12/28 (-0.071) | 14/28 (+0.071) |
| autarky | 12/28 | 12/28 (+0.000) | 13/28 (+0.071) |
| default | 17/28 | 20/28 (+0.214) | 16/28 (-0.071) |
| devil | 16/28 | 17/28 (+0.071) | 15/28 (-0.071) |
| islands | 12/28 | 13/28 (+0.071) | 12/28 (+0.000) |
| maze | 16/28 | 20/28 (+0.286) | 16/28 (+0.000) |
| portals | 12/28 | 13/28 (+0.071) | 12/28 (+0.000) |
| prisoners_dilemma | 8/28 | 8/28 (+0.000) | 8/28 (+0.000) |
| queen_of_spades | 13/28 | 13/28 (+0.000) | 13/28 (+0.000) |
| schooltime | 15/28 | 16/28 (+0.071) | 15/28 (+0.000) |
| slithery_fight | 22/28 | 18/28 (-0.286) | 22/28 (+0.000) |
| stripes | 8/28 | 9/28 (+0.071) | 8/28 (+0.000) |
| tower_defense | 22/28 | 22/28 (+0.000) | 22/28 (+0.000) |
| trauma | 19/28 | 21/28 (+0.143) | 19/28 (+0.000) |
| trophy | 14/28 | 14/28 (+0.000) | 14/28 (+0.000) |
| weakhold | 19/28 | 20/28 (+0.071) | 19/28 (+0.000) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.810 over 238 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.810^2 / (238 * K)): K=2: 0.103, K=3: 0.084, K=4: 0.073, K=6: 0.059, K=8: 0.051
