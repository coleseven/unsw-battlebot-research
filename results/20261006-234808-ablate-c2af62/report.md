# Ablation report: 20261006-234808-ablate-c2af62

2 seeds [981001, 981002], opponents cpp_nicked_v92, cpp_leviathan3, nicked_lab, opp-careful-queen, opp-raider, opp-hunter, opp-sprinter, opp-economy (families: cpp_leviathan3 1, nicked 2, ours 5); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.004, wins 273/544; by opponent: cpp_nicked_v92 -0.471, cpp_leviathan3 +0.735, nicked_lab -0.059, opp-careful-queen +0.176, opp-raider -0.206, opp-hunter -0.265, opp-sprinter -0.118, opp-economy +0.235

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_leviathan3 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-hunter | vs opp-sprinter | vs opp-economy | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bk100 | +0.004 [-0.059, +0.051] | unclear | +0.2 [-2.9, +2.6] | +0.004 | -0.011 | -0.059 | -0.059 | +0.088 | -0.029 | +0.029 | -0.147 | +0.147 | +0.059 | 274/544 |
| bk200 | +0.004 [-0.059, +0.055] | unclear | +0.2 [-2.9, +2.8] | +0.004 | -0.011 | -0.059 | -0.059 | +0.088 | -0.029 | +0.029 | -0.147 | +0.147 | +0.059 | 274/544 |

Per map (wins/games; delta vs base):

| map | base | bk100 | bk200 |
|---|---|---|---|
| around_unsw | 14/32 | 18/32 (+0.250) | 18/32 (+0.250) |
| australia | 13/32 | 13/32 (+0.000) | 13/32 (+0.000) |
| autarky | 17/32 | 12/32 (-0.312) | 12/32 (-0.312) |
| default | 13/32 | 13/32 (+0.000) | 13/32 (+0.000) |
| devil | 20/32 | 20/32 (+0.000) | 20/32 (+0.000) |
| islands | 17/32 | 17/32 (+0.000) | 17/32 (+0.000) |
| maze | 20/32 | 20/32 (+0.000) | 20/32 (+0.000) |
| portals | 18/32 | 18/32 (+0.000) | 18/32 (+0.000) |
| prisoners_dilemma | 7/32 | 11/32 (+0.250) | 11/32 (+0.250) |
| queen_of_spades | 19/32 | 19/32 (+0.000) | 19/32 (+0.000) |
| schooltime | 17/32 | 17/32 (+0.000) | 17/32 (+0.000) |
| slithery_fight | 18/32 | 16/32 (-0.125) | 16/32 (-0.125) |
| stripes | 11/32 | 11/32 (+0.000) | 11/32 (+0.000) |
| tower_defense | 20/32 | 20/32 (+0.000) | 20/32 (+0.000) |
| trauma | 16/32 | 16/32 (+0.000) | 16/32 (+0.000) |
| trophy | 12/32 | 12/32 (+0.000) | 12/32 (+0.000) |
| weakhold | 21/32 | 21/32 (+0.000) | 21/32 (+0.000) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.903 over 272 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.903^2 / (272 * K)): K=2: 0.107, K=3: 0.088, K=4: 0.076, K=6: 0.062, K=8: 0.054
