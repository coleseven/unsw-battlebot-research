# Ablation report: 20261003-192712-ablate-d2ca26

2 seeds [751001, 751002], opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy (families: cpp_leviathan3 1, nicked 4, ours 5); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.182, wins 402/680; by opponent: cpp_nicked_v92 -0.382, cpp_nicked_v75 -0.294, cpp_leviathan3 +0.794, v7-base-bot +0.500, nicked_v44 +0.588, nicked_lab +0.147, opp-careful-queen +0.206, opp-raider -0.059, opp-growth-queen +0.265, opp-economy +0.059

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sx2 | -0.074 [-0.153, -0.009] | variant worse | -3.7 [-7.6, -0.4] | -0.074 | -0.077 | -0.088 | -0.059 | -0.088 | -0.118 | -0.059 | -0.088 | -0.147 | -0.059 | -0.088 | +0.059 | 377/680 |
| sx3 | -0.059 [-0.144, +0.009] | unclear | -2.9 [-7.2, +0.4] | -0.059 | -0.059 | +0.000 | +0.029 | -0.059 | -0.088 | -0.059 | -0.235 | -0.206 | -0.029 | -0.118 | +0.176 | 382/680 |

Per map (wins/games; delta vs base):

| map | base | sx2 | sx3 |
|---|---|---|---|
| around_unsw | 25/40 | 24/40 (-0.050) | 25/40 (+0.000) |
| australia | 26/40 | 26/40 (+0.000) | 27/40 (+0.050) |
| autarky | 26/40 | 27/40 (+0.050) | 26/40 (+0.000) |
| default | 33/40 | 30/40 (-0.150) | 28/40 (-0.250) |
| devil | 27/40 | 23/40 (-0.200) | 25/40 (-0.100) |
| islands | 29/40 | 28/40 (-0.050) | 28/40 (-0.050) |
| maze | 25/40 | 23/40 (-0.100) | 25/40 (+0.000) |
| portals | 20/40 | 24/40 (+0.200) | 24/40 (+0.200) |
| prisoners_dilemma | 18/40 | 18/40 (+0.000) | 18/40 (+0.000) |
| queen_of_spades | 28/40 | 28/40 (+0.000) | 27/40 (-0.050) |
| schooltime | 26/40 | 26/40 (+0.000) | 26/40 (+0.000) |
| slithery_fight | 33/40 | 17/40 (-0.800) | 17/40 (-0.800) |
| stripes | 7/40 | 6/40 (-0.050) | 7/40 (+0.000) |
| tower_defense | 18/40 | 18/40 (+0.000) | 21/40 (+0.150) |
| trauma | 26/40 | 25/40 (-0.050) | 26/40 (+0.000) |
| trophy | 21/40 | 21/40 (+0.000) | 19/40 (-0.100) |
| weakhold | 14/40 | 13/40 (-0.050) | 13/40 (-0.050) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.854 over 340 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.854^2 / (340 * K)): K=2: 0.091, K=3: 0.074, K=4: 0.064, K=6: 0.052, K=8: 0.045
