# Ablation report: 20261007-022453-ablate-02982a

3 seeds [991001, 991002, 991003], opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy, opp-hunter, opp-sprinter (families: cpp_leviathan3 1, nicked 4, ours 7); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.176, wins 720/1224; by opponent: cpp_nicked_v92 -0.275, cpp_nicked_v75 -0.098, cpp_leviathan3 +0.745, v7-base-bot +0.608, nicked_v44 +0.451, nicked_lab +0.078, opp-careful-queen +0.098, opp-raider +0.039, opp-growth-queen +0.294, opp-economy +0.333, opp-hunter -0.078, opp-sprinter -0.078

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | vs opp-hunter | vs opp-sprinter | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fdq | +0.031 [-0.031, +0.093] | unclear | +1.6 [-1.6, +4.7] | +0.031 | +0.005 | +0.039 | +0.157 | -0.098 | +0.039 | +0.137 | +0.098 | +0.020 | -0.196 | +0.039 | +0.039 | +0.118 | -0.020 | 739/1224 |

Per map (wins/games; delta vs base):

| map | base | fdq |
|---|---|---|
| around_unsw | 40/72 | 42/72 (+0.056) |
| australia | 42/72 | 44/72 (+0.056) |
| autarky | 42/72 | 36/72 (-0.167) |
| default | 44/72 | 47/72 (+0.083) |
| devil | 46/72 | 47/72 (+0.028) |
| islands | 41/72 | 39/72 (-0.056) |
| maze | 44/72 | 52/72 (+0.222) |
| portals | 40/72 | 38/72 (-0.056) |
| prisoners_dilemma | 28/72 | 30/72 (+0.056) |
| queen_of_spades | 49/72 | 54/72 (+0.139) |
| schooltime | 40/72 | 45/72 (+0.139) |
| slithery_fight | 51/72 | 47/72 (-0.111) |
| stripes | 23/72 | 24/72 (+0.028) |
| tower_defense | 55/72 | 58/72 (+0.083) |
| trauma | 52/72 | 51/72 (-0.028) |
| trophy | 38/72 | 39/72 (+0.028) |
| weakhold | 45/72 | 46/72 (+0.028) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.834 over 408 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.834^2 / (408 * K)): K=2: 0.081, K=3: 0.066, K=4: 0.057, K=6: 0.047, K=8: 0.040
