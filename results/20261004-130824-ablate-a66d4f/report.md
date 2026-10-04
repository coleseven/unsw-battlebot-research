# Ablation report: 20261004-130824-ablate-a66d4f

3 seeds [811001, 811002, 811003], opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy, v11t (families: cpp_leviathan3 1, nicked 4, ours 6); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.162, wins 652/1122; by opponent: cpp_nicked_v92 -0.431, cpp_nicked_v75 -0.098, cpp_leviathan3 +0.804, v7-base-bot +0.529, nicked_v44 +0.451, nicked_lab +0.098, opp-careful-queen +0.196, opp-raider -0.196, opp-growth-queen +0.118, opp-economy +0.314, v11t +0.000

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | vs v11t | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gp | +0.012 [-0.055, +0.082] | unclear | +0.6 [-2.8, +4.1] | +0.012 | -0.036 | +0.039 | -0.020 | -0.157 | +0.098 | +0.020 | -0.039 | -0.176 | +0.176 | +0.255 | -0.098 | +0.039 | 659/1122 |

Per map (wins/games; delta vs base):

| map | base | gp |
|---|---|---|
| around_unsw | 45/66 | 42/66 (-0.091) |
| australia | 41/66 | 35/66 (-0.182) |
| autarky | 45/66 | 42/66 (-0.091) |
| default | 48/66 | 50/66 (+0.061) |
| devil | 39/66 | 40/66 (+0.030) |
| islands | 36/66 | 41/66 (+0.152) |
| maze | 39/66 | 46/66 (+0.212) |
| portals | 34/66 | 37/66 (+0.091) |
| prisoners_dilemma | 27/66 | 31/66 (+0.121) |
| queen_of_spades | 43/66 | 43/66 (+0.000) |
| schooltime | 46/66 | 44/66 (-0.061) |
| slithery_fight | 50/66 | 48/66 (-0.061) |
| stripes | 21/66 | 12/66 (-0.273) |
| tower_defense | 39/66 | 42/66 (+0.091) |
| trauma | 46/66 | 55/66 (+0.273) |
| trophy | 30/66 | 25/66 (-0.152) |
| weakhold | 23/66 | 26/66 (+0.091) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.814 over 374 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.814^2 / (374 * K)): K=2: 0.083, K=3: 0.067, K=4: 0.058, K=6: 0.048, K=8: 0.041
