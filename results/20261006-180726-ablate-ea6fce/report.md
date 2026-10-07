# Ablation report: 20261006-180726-ablate-ea6fce

2 seeds [961001, 961002], opponents cpp_nicked_v92, cpp_leviathan3, nicked_lab, opp-careful-queen, opp-raider, opp-hunter, opp-sprinter, opp-economy (families: cpp_leviathan3 1, nicked 2, ours 5); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.004, wins 273/544; by opponent: cpp_nicked_v92 -0.588, cpp_leviathan3 +0.676, nicked_lab -0.059, opp-careful-queen +0.029, opp-raider -0.059, opp-hunter -0.176, opp-sprinter -0.029, opp-economy +0.235

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_leviathan3 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-hunter | vs opp-sprinter | vs opp-economy | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sp1 | -0.026 [-0.099, +0.051] | unclear | -1.3 [-5.0, +2.6] | -0.026 | -0.012 | +0.147 | -0.059 | +0.029 | +0.059 | -0.029 | -0.235 | -0.118 | +0.000 | 266/544 |
| sp2 | -0.037 [-0.121, +0.044] | unclear | -1.8 [-6.1, +2.2] | -0.037 | -0.031 | +0.235 | -0.088 | -0.118 | -0.088 | -0.088 | -0.059 | -0.118 | +0.029 | 263/544 |

Per map (wins/games; delta vs base):

| map | base | sp1 | sp2 |
|---|---|---|---|
| around_unsw | 17/32 | 13/32 (-0.250) | 15/32 (-0.125) |
| australia | 11/32 | 14/32 (+0.188) | 17/32 (+0.375) |
| autarky | 14/32 | 8/32 (-0.375) | 11/32 (-0.188) |
| default | 16/32 | 17/32 (+0.062) | 6/32 (-0.625) |
| devil | 19/32 | 22/32 (+0.188) | 19/32 (+0.000) |
| islands | 19/32 | 14/32 (-0.312) | 15/32 (-0.250) |
| maze | 14/32 | 17/32 (+0.188) | 17/32 (+0.188) |
| portals | 17/32 | 20/32 (+0.188) | 19/32 (+0.125) |
| prisoners_dilemma | 12/32 | 8/32 (-0.250) | 8/32 (-0.250) |
| queen_of_spades | 13/32 | 14/32 (+0.062) | 13/32 (+0.000) |
| schooltime | 20/32 | 20/32 (+0.000) | 20/32 (+0.000) |
| slithery_fight | 18/32 | 16/32 (-0.125) | 18/32 (+0.000) |
| stripes | 9/32 | 8/32 (-0.062) | 9/32 (+0.000) |
| tower_defense | 21/32 | 23/32 (+0.125) | 24/32 (+0.188) |
| trauma | 17/32 | 16/32 (-0.062) | 16/32 (-0.062) |
| trophy | 14/32 | 14/32 (+0.000) | 14/32 (+0.000) |
| weakhold | 22/32 | 22/32 (+0.000) | 22/32 (+0.000) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.845 over 272 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.845^2 / (272 * K)): K=2: 0.100, K=3: 0.082, K=4: 0.071, K=6: 0.058, K=8: 0.050
