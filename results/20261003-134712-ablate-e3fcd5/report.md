# Ablation report: 20261003-134712-ablate-e3fcd5

3 seeds [691001, 691002, 691003], opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy (families: cpp_leviathan3 1, nicked 4, ours 5); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.050, wins 534/1020; by opponent: cpp_nicked_v92 -0.667, cpp_nicked_v75 -0.314, cpp_leviathan3 +0.569, v7-base-bot +0.588, nicked_v44 +0.392, nicked_lab -0.157, opp-careful-queen +0.000, opp-raider -0.098, opp-growth-queen +0.137, opp-economy +0.049

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t2 | +0.070 [-0.003, +0.141] | unclear | +3.5 [-0.1, +7.1] | +0.070 | +0.080 | +0.294 | +0.039 | +0.098 | -0.176 | +0.020 | +0.118 | +0.157 | -0.078 | -0.059 | +0.284 | 571/1020 |

Per map (wins/games; delta vs base):

| map | base | t2 |
|---|---|---|
| around_unsw | 37/60 | 43/60 (+0.200) |
| australia | 31/60 | 37/60 (+0.200) |
| autarky | 32/60 | 39/60 (+0.233) |
| default | 38/60 | 39/60 (+0.033) |
| devil | 34/60 | 34/60 (+0.000) |
| islands | 28/60 | 32/60 (+0.133) |
| maze | 37/60 | 42/60 (+0.167) |
| portals | 28/60 | 34/60 (+0.200) |
| prisoners_dilemma | 21/60 | 21/60 (+0.000) |
| queen_of_spades | 34/60 | 36/60 (+0.067) |
| schooltime | 40/60 | 40/60 (+0.000) |
| slithery_fight | 33/60 | 44/60 (+0.367) |
| stripes | 28/60 | 25/60 (-0.100) |
| tower_defense | 30/60 | 20/60 (-0.333) |
| trauma | 36/60 | 40/60 (+0.133) |
| trophy | 26/60 | 26/60 (+0.000) |
| weakhold | 21/60 | 19/60 (-0.117) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.831 over 340 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.831^2 / (340 * K)): K=2: 0.088, K=3: 0.072, K=4: 0.062, K=6: 0.051, K=8: 0.044
