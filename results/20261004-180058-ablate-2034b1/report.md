# Ablation report: 20261004-180058-ablate-2034b1

3 seeds [851001, 851002, 851003], opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy, v11t (families: cpp_leviathan3 1, nicked 4, ours 6); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.118, wins 627/1122; by opponent: cpp_nicked_v92 -0.490, cpp_nicked_v75 -0.098, cpp_leviathan3 +0.725, v7-base-bot +0.529, nicked_v44 +0.373, nicked_lab -0.118, opp-careful-queen +0.078, opp-raider -0.098, opp-growth-queen +0.078, opp-economy +0.314, v11t +0.000

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | vs v11t | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ft1 | +0.007 [-0.025, +0.039] | unclear | +0.4 [-1.2, +2.0] | +0.007 | +0.023 | -0.020 | -0.098 | +0.078 | -0.039 | +0.078 | -0.059 | +0.059 | +0.059 | +0.039 | -0.078 | +0.059 | 631/1122 |

Per map (wins/games; delta vs base):

| map | base | ft1 |
|---|---|---|
| around_unsw | 39/66 | 39/66 (+0.000) |
| australia | 31/66 | 34/66 (+0.091) |
| autarky | 45/66 | 45/66 (+0.000) |
| default | 43/66 | 41/66 (-0.061) |
| devil | 45/66 | 45/66 (+0.000) |
| islands | 32/66 | 32/66 (+0.000) |
| maze | 41/66 | 41/66 (+0.000) |
| portals | 40/66 | 43/66 (+0.091) |
| prisoners_dilemma | 34/66 | 34/66 (+0.000) |
| queen_of_spades | 41/66 | 41/66 (+0.000) |
| schooltime | 44/66 | 46/66 (+0.061) |
| slithery_fight | 49/66 | 50/66 (+0.030) |
| stripes | 19/66 | 19/66 (+0.000) |
| tower_defense | 32/66 | 33/66 (+0.030) |
| trauma | 47/66 | 44/66 (-0.091) |
| trophy | 23/66 | 22/66 (-0.030) |
| weakhold | 22/66 | 22/66 (+0.000) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.816 over 374 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.816^2 / (374 * K)): K=2: 0.083, K=3: 0.068, K=4: 0.059, K=6: 0.048, K=8: 0.041
