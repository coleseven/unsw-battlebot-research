# Ablation report: 20261005-032739-ablate-617f76

3 seeds [901001, 901002, 901003], opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy, v11t (families: cpp_leviathan3 1, nicked 4, ours 6); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.125, wins 631/1122; by opponent: cpp_nicked_v92 -0.353, cpp_nicked_v75 -0.118, cpp_leviathan3 +0.627, v7-base-bot +0.588, nicked_v44 +0.412, nicked_lab -0.059, opp-careful-queen +0.118, opp-raider -0.196, opp-growth-queen +0.098, opp-economy +0.255, v11t +0.000

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | vs v11t | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| x30gp | +0.084 [-0.002, +0.173] | unclear | +4.2 [-0.1, +8.6] | +0.084 | +0.071 | -0.020 | +0.000 | +0.039 | +0.020 | +0.235 | +0.098 | -0.020 | +0.235 | +0.098 | +0.098 | +0.137 | 678/1122 |
| x30gp_s | +0.094 [+0.012, +0.178] | variant better | +4.7 [+0.6, +8.9] | +0.094 | +0.072 | -0.020 | +0.000 | +0.020 | +0.059 | +0.235 | +0.098 | +0.000 | +0.255 | +0.118 | +0.098 | +0.176 | 684/1122 |

Per map (wins/games; delta vs base):

| map | base | x30gp | x30gp_s |
|---|---|---|---|
| around_unsw | 43/66 | 44/66 (+0.030) | 44/66 (+0.030) |
| australia | 42/66 | 38/66 (-0.121) | 38/66 (-0.121) |
| autarky | 39/66 | 35/66 (-0.121) | 35/66 (-0.121) |
| default | 45/66 | 45/66 (+0.000) | 45/66 (+0.000) |
| devil | 42/66 | 42/66 (+0.000) | 42/66 (+0.000) |
| islands | 34/66 | 36/66 (+0.061) | 36/66 (+0.061) |
| maze | 43/66 | 43/66 (+0.000) | 43/66 (+0.000) |
| portals | 32/66 | 38/66 (+0.182) | 38/66 (+0.182) |
| prisoners_dilemma | 30/66 | 26/66 (-0.121) | 26/66 (-0.121) |
| queen_of_spades | 40/66 | 40/66 (+0.000) | 40/66 (+0.000) |
| schooltime | 50/66 | 47/66 (-0.091) | 47/66 (-0.091) |
| slithery_fight | 44/66 | 50/66 (+0.182) | 50/66 (+0.182) |
| stripes | 20/66 | 11/66 (-0.273) | 17/66 (-0.091) |
| tower_defense | 28/66 | 52/66 (+0.727) | 52/66 (+0.727) |
| trauma | 43/66 | 50/66 (+0.212) | 50/66 (+0.212) |
| trophy | 32/66 | 36/66 (+0.121) | 36/66 (+0.121) |
| weakhold | 24/66 | 45/66 (+0.636) | 45/66 (+0.636) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.853 over 374 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.853^2 / (374 * K)): K=2: 0.086, K=3: 0.071, K=4: 0.061, K=6: 0.050, K=8: 0.043
