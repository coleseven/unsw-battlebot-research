# Ablation report: 20261003-224713-ablate-d440c5

3 seeds [771001, 771002, 771003], opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy, v11q (families: cpp_leviathan3 1, nicked 4, ours 6); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.153, wins 647/1122; by opponent: cpp_nicked_v92 -0.392, cpp_nicked_v75 -0.137, cpp_leviathan3 +0.608, v7-base-bot +0.706, nicked_v44 +0.451, nicked_lab -0.157, opp-careful-queen +0.118, opp-raider -0.216, opp-growth-queen +0.275, opp-economy +0.314, v11q +0.118

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | vs v11q | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dq | -0.004 [-0.064, +0.052] | unclear | -0.2 [-3.2, +2.6] | -0.004 | +0.007 | +0.059 | -0.137 | +0.020 | +0.020 | -0.098 | +0.314 | -0.039 | +0.059 | -0.196 | +0.000 | -0.039 | 645/1122 |

Per map (wins/games; delta vs base):

| map | base | dq |
|---|---|---|
| around_unsw | 36/66 | 40/66 (+0.121) |
| australia | 41/66 | 45/66 (+0.121) |
| autarky | 46/66 | 46/66 (+0.000) |
| default | 42/66 | 41/66 (-0.030) |
| devil | 47/66 | 49/66 (+0.061) |
| islands | 37/66 | 40/66 (+0.091) |
| maze | 46/66 | 46/66 (+0.000) |
| portals | 36/66 | 42/66 (+0.182) |
| prisoners_dilemma | 25/66 | 25/66 (+0.000) |
| queen_of_spades | 43/66 | 38/66 (-0.152) |
| schooltime | 49/66 | 35/66 (-0.424) |
| slithery_fight | 48/66 | 44/66 (-0.121) |
| stripes | 19/66 | 17/66 (-0.061) |
| tower_defense | 26/66 | 28/66 (+0.061) |
| trauma | 48/66 | 51/66 (+0.091) |
| trophy | 34/66 | 32/66 (-0.061) |
| weakhold | 24/66 | 26/66 (+0.061) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.825 over 374 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.825^2 / (374 * K)): K=2: 0.084, K=3: 0.068, K=4: 0.059, K=6: 0.048, K=8: 0.042
