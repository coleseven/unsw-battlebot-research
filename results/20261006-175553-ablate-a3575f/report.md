# Ablation report: 20261006-175553-ablate-a3575f

3 seeds [951001, 951002, 951003], opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy, opp-hunter (families: cpp_leviathan3 1, nicked 4, ours 6); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.164, wins 653/1122; by opponent: cpp_nicked_v92 -0.392, cpp_nicked_v75 -0.275, cpp_leviathan3 +0.608, v7-base-bot +0.627, nicked_v44 +0.471, nicked_lab +0.039, opp-careful-queen +0.235, opp-raider -0.020, opp-growth-queen +0.216, opp-economy +0.333, opp-hunter -0.039

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | vs opp-hunter | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dq | +0.018 [-0.025, +0.061] | unclear | +0.9 [-1.2, +3.0] | +0.018 | +0.026 | +0.098 | +0.059 | +0.039 | -0.039 | +0.039 | -0.059 | -0.157 | +0.118 | +0.039 | +0.059 | +0.000 | 663/1122 |

Per map (wins/games; delta vs base):

| map | base | dq |
|---|---|---|
| around_unsw | 48/66 | 41/66 (-0.212) |
| australia | 36/66 | 32/66 (-0.121) |
| autarky | 39/66 | 39/66 (+0.000) |
| default | 44/66 | 42/66 (-0.061) |
| devil | 40/66 | 44/66 (+0.121) |
| islands | 33/66 | 40/66 (+0.212) |
| maze | 45/66 | 49/66 (+0.121) |
| portals | 36/66 | 32/66 (-0.121) |
| prisoners_dilemma | 28/66 | 28/66 (+0.000) |
| queen_of_spades | 37/66 | 41/66 (+0.121) |
| schooltime | 44/66 | 41/66 (-0.091) |
| slithery_fight | 45/66 | 46/66 (+0.030) |
| stripes | 14/66 | 14/66 (+0.000) |
| tower_defense | 50/66 | 54/66 (+0.121) |
| trauma | 42/66 | 47/66 (+0.152) |
| trophy | 28/66 | 28/66 (+0.000) |
| weakhold | 44/66 | 45/66 (+0.030) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.806 over 374 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.806^2 / (374 * K)): K=2: 0.082, K=3: 0.067, K=4: 0.058, K=6: 0.047, K=8: 0.041
