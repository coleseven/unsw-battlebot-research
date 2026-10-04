# Ablation report: 20261004-162434-ablate-333e9c

2 seeds [831001, 831002], opponents cpp_nicked_v92, cpp_leviathan3, nicked_lab, opp-careful-queen, opp-raider, opp-economy (families: cpp_leviathan3 1, nicked 2, ours 3); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.005, wins 205/408; by opponent: cpp_nicked_v92 -0.500, cpp_leviathan3 +0.647, nicked_lab -0.088, opp-careful-queen +0.029, opp-raider -0.235, opp-economy +0.176

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_leviathan3 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-economy | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ft1 | +0.059 [+0.010, +0.113] | variant better | +2.9 [+0.5, +5.6] | +0.059 | +0.052 | +0.059 | +0.000 | +0.176 | +0.147 | +0.029 | -0.059 | 217/408 |

Per map (wins/games; delta vs base):

| map | base | ft1 |
|---|---|---|
| around_unsw | 17/24 | 17/24 (+0.000) |
| australia | 14/24 | 14/24 (+0.000) |
| autarky | 12/24 | 12/24 (+0.000) |
| default | 16/24 | 17/24 (+0.083) |
| devil | 14/24 | 14/24 (+0.000) |
| islands | 9/24 | 14/24 (+0.417) |
| maze | 12/24 | 14/24 (+0.167) |
| portals | 12/24 | 14/24 (+0.167) |
| prisoners_dilemma | 4/24 | 4/24 (+0.000) |
| queen_of_spades | 11/24 | 11/24 (+0.000) |
| schooltime | 16/24 | 17/24 (+0.083) |
| slithery_fight | 14/24 | 14/24 (+0.000) |
| stripes | 6/24 | 6/24 (+0.000) |
| tower_defense | 8/24 | 8/24 (+0.000) |
| trauma | 17/24 | 18/24 (+0.083) |
| trophy | 11/24 | 11/24 (+0.000) |
| weakhold | 12/24 | 12/24 (+0.000) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.810 over 204 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.810^2 / (204 * K)): K=2: 0.111, K=3: 0.091, K=4: 0.079, K=6: 0.064, K=8: 0.056
