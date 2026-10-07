# Ablation report: 20261006-234331-ablate-647787

2 seeds [971001, 971002], opponents cpp_nicked_v92, cpp_leviathan3, nicked_lab, opp-careful-queen, opp-raider, opp-hunter, opp-sprinter, opp-economy (families: cpp_leviathan3 1, nicked 2, ours 5); 17 maps from the run's plan (around_unsw, australia, autarky, default, devil, islands, maze, portals, prisoners_dilemma, queen_of_spades, schooltime, slithery_fight, stripes, tower_defense, trauma, trophy, weakhold), both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side), where the variant is the base plus that group's parameter changes: **positive means the variant scored higher than the base**. 95% CI resamples (map, seed) blocks. Equal-map and equal-family deltas weight each map / opponent family equally.

base: mean margin +0.081, wins 294/544; by opponent: cpp_nicked_v92 -0.382, cpp_leviathan3 +0.735, nicked_lab -0.235, opp-careful-queen +0.353, opp-raider -0.029, opp-hunter -0.059, opp-sprinter +0.059, opp-economy +0.206

Objective wins is the signed outcome (win +1, draw 0, loss -1); the win-score column (win 1, draw 0.5, loss 0) is delta / 2 in percentage points.

| variant | delta all 17 maps [95% CI] | verdict | win-score pp [95% CI] | equal-map delta | equal-family delta | vs cpp_nicked_v92 | vs cpp_leviathan3 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-hunter | vs opp-sprinter | vs opp-economy | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sps3 | -0.132 [-0.232, -0.040] | variant worse | -6.6 [-11.6, -2.0] | -0.132 | -0.110 | -0.147 | -0.147 | +0.147 | -0.176 | -0.206 | -0.206 | -0.265 | -0.059 | 258/544 |
| flight | +0.033 [-0.018, +0.088] | unclear | +1.7 [-0.9, +4.4] | +0.033 | +0.014 | +0.029 | -0.059 | +0.088 | +0.000 | -0.029 | +0.000 | +0.000 | +0.235 | 303/544 |

Per map (wins/games; delta vs base):

| map | base | sps3 | flight |
|---|---|---|---|
| around_unsw | 18/32 | 15/32 (-0.188) | 17/32 (-0.062) |
| australia | 19/32 | 13/32 (-0.375) | 19/32 (+0.000) |
| autarky | 19/32 | 17/32 (-0.125) | 19/32 (+0.000) |
| default | 19/32 | 16/32 (-0.188) | 17/32 (-0.125) |
| devil | 17/32 | 13/32 (-0.250) | 17/32 (+0.000) |
| islands | 11/32 | 13/32 (+0.125) | 14/32 (+0.188) |
| maze | 18/32 | 21/32 (+0.188) | 22/32 (+0.250) |
| portals | 16/32 | 19/32 (+0.188) | 20/32 (+0.250) |
| prisoners_dilemma | 12/32 | 7/32 (-0.312) | 13/32 (+0.062) |
| queen_of_spades | 16/32 | 13/32 (-0.188) | 18/32 (+0.125) |
| schooltime | 20/32 | 20/32 (+0.000) | 20/32 (+0.000) |
| slithery_fight | 21/32 | 19/32 (-0.125) | 22/32 (+0.062) |
| stripes | 13/32 | 8/32 (-0.312) | 10/32 (-0.188) |
| tower_defense | 22/32 | 22/32 (+0.000) | 22/32 (+0.000) |
| trauma | 21/32 | 11/32 (-0.625) | 19/32 (-0.125) |
| trophy | 12/32 | 11/32 (-0.062) | 14/32 (+0.125) |
| weakhold | 20/32 | 20/32 (+0.000) | 20/32 (+0.000) |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.857 over 272 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.857^2 / (272 * K)): K=2: 0.102, K=3: 0.083, K=4: 0.072, K=6: 0.059, K=8: 0.051
