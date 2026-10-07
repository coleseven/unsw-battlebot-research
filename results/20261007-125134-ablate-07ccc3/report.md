# Ablation report: 20261007-125134-ablate-07ccc3

3 seeds [1031001, 1031002, 1031003], opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy, opp-hunter, opp-sprinter (families: cpp_leviathan3 1, nicked 4, ours 7); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.096, wins 671/1224; by opponent: cpp_nicked_v92 -0.490, cpp_nicked_v75 -0.235, cpp_leviathan3 +0.588, v7-base-bot +0.627, nicked_v44 +0.569, nicked_lab -0.118, opp-careful-queen +0.157, opp-raider +0.000, opp-growth-queen +0.176, opp-economy +0.333, opp-hunter -0.176, opp-sprinter -0.275

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | vs opp-hunter | vs opp-sprinter | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hs1 | +0.075 [+0.031, +0.118] | variant better | +3.8 [+1.6, +5.9] | +0.075 | +0.102 | +0.059 | -0.078 | +0.196 | -0.039 | -0.020 | +0.118 | +0.078 | +0.000 | +0.098 | +0.118 | +0.098 | +0.275 | 717/1224 |
| hs1fdq | +0.114 [+0.047, +0.181] | variant better | +5.7 [+2.4, +9.1] | +0.114 | +0.134 | +0.275 | -0.039 | +0.196 | +0.078 | +0.059 | +0.059 | +0.039 | +0.000 | +0.059 | +0.216 | +0.078 | +0.353 | 741/1224 |

Per map (wins/games; delta vs base):

| map | base | hs1 | hs1fdq |
|---|---|---|---|
| around_unsw | 39/72 | 42/72 (+0.083) | 46/72 (+0.194) |
| australia | 37/72 | 46/72 (+0.250) | 53/72 (+0.444) |
| autarky | 35/72 | 42/72 (+0.194) | 50/72 (+0.417) |
| default | 44/72 | 49/72 (+0.139) | 50/72 (+0.167) |
| devil | 46/72 | 46/72 (+0.000) | 48/72 (+0.056) |
| islands | 34/72 | 34/72 (+0.000) | 37/72 (+0.083) |
| maze | 51/72 | 51/72 (+0.000) | 45/72 (-0.167) |
| portals | 41/72 | 41/72 (+0.000) | 39/72 (-0.056) |
| prisoners_dilemma | 25/72 | 29/72 (+0.111) | 29/72 (+0.111) |
| queen_of_spades | 39/72 | 38/72 (-0.028) | 44/72 (+0.139) |
| schooltime | 45/72 | 45/72 (+0.000) | 42/72 (-0.083) |
| slithery_fight | 45/72 | 54/72 (+0.250) | 49/72 (+0.111) |
| stripes | 21/72 | 21/72 (+0.000) | 25/72 (+0.111) |
| tower_defense | 50/72 | 53/72 (+0.083) | 55/72 (+0.139) |
| trauma | 46/72 | 49/72 (+0.083) | 51/72 (+0.139) |
| trophy | 33/72 | 34/72 (+0.028) | 33/72 (+0.000) |
| weakhold | 40/72 | 43/72 (+0.083) | 45/72 (+0.139) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.869 over 408 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.869^2 / (408 * K)): K=2: 0.084, K=3: 0.069, K=4: 0.060, K=6: 0.049, K=8: 0.042
