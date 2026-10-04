# Ablation report: 20261003-183034-ablate-3ac260

3 seeds [731001, 731002, 731003], opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy, v11q (families: cpp_leviathan3 1, nicked 4, ours 6); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.119, wins 627/1122; by opponent: cpp_nicked_v92 -0.373, cpp_nicked_v75 -0.275, cpp_leviathan3 +0.667, v7-base-bot +0.608, nicked_v44 +0.373, nicked_lab -0.078, opp-careful-queen +0.078, opp-raider -0.196, opp-growth-queen +0.137, opp-economy +0.284, v11q +0.078

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | vs v11q | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ref100 | +0.026 [-0.045, +0.097] | unclear | +1.3 [-2.2, +4.9] | +0.026 | +0.038 | +0.020 | +0.020 | +0.078 | +0.000 | +0.000 | -0.020 | -0.069 | +0.196 | +0.020 | +0.108 | -0.069 | 641/1122 |

Per map (wins/games; delta vs base):

| map | base | ref100 |
|---|---|---|
| around_unsw | 40/66 | 41/66 (+0.030) |
| australia | 35/66 | 44/66 (+0.273) |
| autarky | 38/66 | 43/66 (+0.152) |
| default | 53/66 | 48/66 (-0.152) |
| devil | 47/66 | 41/66 (-0.182) |
| islands | 34/66 | 36/66 (+0.061) |
| maze | 48/66 | 40/66 (-0.242) |
| portals | 42/66 | 39/66 (-0.076) |
| prisoners_dilemma | 27/66 | 33/66 (+0.182) |
| queen_of_spades | 38/66 | 46/66 (+0.242) |
| schooltime | 48/66 | 48/66 (+0.000) |
| slithery_fight | 46/66 | 42/66 (-0.121) |
| stripes | 16/66 | 13/66 (-0.091) |
| tower_defense | 22/66 | 27/66 (+0.152) |
| trauma | 38/66 | 44/66 (+0.182) |
| trophy | 29/66 | 29/66 (+0.000) |
| weakhold | 26/66 | 27/66 (+0.030) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.795 over 374 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.795^2 / (374 * K)): K=2: 0.081, K=3: 0.066, K=4: 0.057, K=6: 0.047, K=8: 0.040
