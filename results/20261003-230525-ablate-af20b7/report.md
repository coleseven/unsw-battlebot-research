# Ablation report: 20261003-230525-ablate-af20b7

2 seeds [781001, 781002], opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy (families: cpp_leviathan3 1, nicked 4, ours 5); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.132, wins 385/680; by opponent: cpp_nicked_v92 -0.235, cpp_nicked_v75 -0.029, cpp_leviathan3 +0.559, v7-base-bot +0.412, nicked_v44 +0.382, nicked_lab -0.029, opp-careful-queen +0.059, opp-raider -0.118, opp-growth-queen +0.176, opp-economy +0.147

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bg2 | -0.012 [-0.029, +0.003] | unclear | -0.6 [-1.5, +0.1] | -0.012 | -0.009 | -0.029 | +0.000 | +0.000 | -0.029 | -0.059 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | 381/680 |
| bg3 | -0.018 [-0.050, +0.015] | unclear | -0.9 [-2.5, +0.7] | -0.018 | -0.012 | -0.029 | -0.059 | +0.000 | -0.029 | +0.000 | +0.059 | -0.118 | +0.029 | +0.000 | -0.029 | 379/680 |

Per map (wins/games; delta vs base):

| map | base | bg2 | bg3 |
|---|---|---|---|
| around_unsw | 26/40 | 26/40 (+0.000) | 26/40 (+0.000) |
| australia | 16/40 | 16/40 (+0.000) | 16/40 (+0.000) |
| autarky | 28/40 | 27/40 (-0.050) | 27/40 (-0.050) |
| default | 29/40 | 27/40 (-0.100) | 27/40 (-0.100) |
| devil | 29/40 | 29/40 (+0.000) | 29/40 (+0.000) |
| islands | 20/40 | 19/40 (-0.050) | 20/40 (+0.000) |
| maze | 29/40 | 29/40 (+0.000) | 28/40 (-0.050) |
| portals | 27/40 | 27/40 (+0.000) | 27/40 (+0.000) |
| prisoners_dilemma | 15/40 | 15/40 (+0.000) | 16/40 (+0.050) |
| queen_of_spades | 27/40 | 26/40 (-0.050) | 26/40 (-0.050) |
| schooltime | 28/40 | 28/40 (+0.000) | 27/40 (-0.050) |
| slithery_fight | 27/40 | 28/40 (+0.050) | 27/40 (+0.000) |
| stripes | 9/40 | 9/40 (+0.000) | 9/40 (+0.000) |
| tower_defense | 20/40 | 20/40 (+0.000) | 19/40 (-0.050) |
| trauma | 23/40 | 23/40 (+0.000) | 22/40 (-0.050) |
| trophy | 18/40 | 18/40 (+0.000) | 19/40 (+0.050) |
| weakhold | 14/40 | 14/40 (+0.000) | 14/40 (+0.000) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.822 over 340 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.822^2 / (340 * K)): K=2: 0.087, K=3: 0.071, K=4: 0.062, K=6: 0.050, K=8: 0.044
