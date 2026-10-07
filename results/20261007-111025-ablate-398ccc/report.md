# Ablation report: 20261007-111025-ablate-398ccc

2 seeds [1021001, 1021002], opponents cpp_nicked_v92, cpp_leviathan3, nicked_lab, opp-careful-queen, opp-raider, opp-hunter, opp-sprinter, opp-economy (families: cpp_leviathan3 1, nicked 2, ours 5); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.040, wins 283/544; by opponent: cpp_nicked_v92 -0.588, cpp_leviathan3 +0.647, nicked_lab +0.029, opp-careful-queen +0.088, opp-raider +0.118, opp-hunter -0.176, opp-sprinter -0.118, opp-economy +0.324

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_leviathan3 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-hunter | vs opp-sprinter | vs opp-economy | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hs1 | +0.081 [+0.011, +0.147] | variant better | +4.0 [+0.6, +7.4] | +0.081 | +0.074 | +0.029 | +0.059 | +0.118 | +0.029 | +0.059 | +0.118 | +0.176 | +0.059 | 305/544 |
| hs2 | +0.051 [-0.011, +0.114] | unclear | +2.6 [-0.6, +5.7] | +0.051 | +0.061 | +0.088 | +0.059 | +0.088 | -0.029 | +0.029 | +0.059 | +0.118 | +0.000 | 297/544 |
| hs3 | +0.051 [-0.011, +0.114] | unclear | +2.6 [-0.6, +5.7] | +0.051 | +0.058 | +0.059 | +0.059 | +0.088 | +0.000 | +0.029 | +0.059 | +0.118 | +0.000 | 297/544 |

Per map (wins/games; delta vs base):

| map | base | hs1 | hs2 | hs3 |
|---|---|---|---|---|
| around_unsw | 15/32 | 17/32 (+0.125) | 20/32 (+0.312) | 19/32 (+0.250) |
| australia | 14/32 | 21/32 (+0.438) | 19/32 (+0.312) | 19/32 (+0.312) |
| autarky | 19/32 | 17/32 (-0.125) | 16/32 (-0.188) | 16/32 (-0.188) |
| default | 20/32 | 21/32 (+0.062) | 19/32 (-0.062) | 19/32 (-0.062) |
| devil | 17/32 | 18/32 (+0.062) | 19/32 (+0.125) | 19/32 (+0.125) |
| islands | 15/32 | 16/32 (+0.062) | 17/32 (+0.125) | 17/32 (+0.125) |
| maze | 17/32 | 16/32 (-0.062) | 16/32 (-0.062) | 16/32 (-0.062) |
| portals | 17/32 | 17/32 (+0.000) | 17/32 (+0.000) | 17/32 (+0.000) |
| prisoners_dilemma | 6/32 | 9/32 (+0.188) | 8/32 (+0.125) | 8/32 (+0.125) |
| queen_of_spades | 16/32 | 17/32 (+0.062) | 14/32 (-0.125) | 14/32 (-0.125) |
| schooltime | 21/32 | 21/32 (+0.000) | 21/32 (+0.000) | 21/32 (+0.000) |
| slithery_fight | 20/32 | 21/32 (+0.062) | 20/32 (+0.000) | 21/32 (+0.062) |
| stripes | 8/32 | 10/32 (+0.125) | 10/32 (+0.125) | 10/32 (+0.125) |
| tower_defense | 21/32 | 24/32 (+0.188) | 24/32 (+0.188) | 24/32 (+0.188) |
| trauma | 23/32 | 25/32 (+0.125) | 24/32 (+0.062) | 24/32 (+0.062) |
| trophy | 13/32 | 12/32 (-0.062) | 12/32 (-0.062) | 12/32 (-0.062) |
| weakhold | 21/32 | 23/32 (+0.125) | 21/32 (+0.000) | 21/32 (+0.000) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.887 over 272 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.887^2 / (272 * K)): K=2: 0.105, K=3: 0.086, K=4: 0.075, K=6: 0.061, K=8: 0.053
