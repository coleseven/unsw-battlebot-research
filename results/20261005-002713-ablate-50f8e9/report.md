# Ablation report: 20261005-002713-ablate-50f8e9

3 seeds [871001, 871002, 871003], opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy, v11t (families: cpp_leviathan3 1, nicked 4, ours 6); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.130, wins 634/1122; by opponent: cpp_nicked_v92 -0.314, cpp_nicked_v75 -0.294, cpp_leviathan3 +0.706, v7-base-bot +0.569, nicked_v44 +0.431, nicked_lab -0.059, opp-careful-queen +0.137, opp-raider -0.078, opp-growth-queen +0.176, opp-economy +0.157, v11t +0.000

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | vs v11t | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| e40 | +0.024 [-0.047, +0.099] | unclear | +1.2 [-2.4, +4.9] | +0.024 | -0.002 | -0.176 | -0.059 | -0.039 | +0.098 | +0.020 | +0.020 | +0.010 | +0.118 | +0.118 | +0.039 | +0.118 | 647/1122 |

Per map (wins/games; delta vs base):

| map | base | e40 |
|---|---|---|
| around_unsw | 37/66 | 40/66 (+0.091) |
| australia | 44/66 | 37/66 (-0.212) |
| autarky | 47/66 | 45/66 (-0.061) |
| default | 42/66 | 45/66 (+0.091) |
| devil | 39/66 | 42/66 (+0.091) |
| islands | 35/66 | 35/66 (+0.000) |
| maze | 44/66 | 42/66 (-0.061) |
| portals | 42/66 | 37/66 (-0.136) |
| prisoners_dilemma | 28/66 | 33/66 (+0.152) |
| queen_of_spades | 44/66 | 31/66 (-0.394) |
| schooltime | 48/66 | 48/66 (+0.000) |
| slithery_fight | 41/66 | 46/66 (+0.152) |
| stripes | 20/66 | 40/66 (+0.606) |
| tower_defense | 23/66 | 26/66 (+0.091) |
| trauma | 43/66 | 43/66 (+0.000) |
| trophy | 34/66 | 30/66 (-0.121) |
| weakhold | 23/66 | 27/66 (+0.121) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.842 over 374 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.842^2 / (374 * K)): K=2: 0.085, K=3: 0.070, K=4: 0.060, K=6: 0.049, K=8: 0.043
