# Ablation report: 20261003-183034-ablate-3ac260

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy, v11q; 17 official + 0 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.119, wins 627/1122; by opponent: cpp_nicked_v92 -0.373, cpp_nicked_v75 -0.275, cpp_leviathan3 +0.667, v7-base-bot +0.608, nicked_v44 +0.373, nicked_lab -0.078, opp-careful-queen +0.078, opp-raider -0.196, opp-growth-queen +0.137, opp-economy +0.284, v11q +0.078

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ref100 | +0.024 [-0.067, +0.145] | neutral | +0.027 | +0.026 [-0.045, +0.097] | neutral | +0.020 | +0.020 | +0.078 | +0.000 | +0.000 | -0.020 | -0.069 | +0.196 | +0.020 | +0.108 | -0.069 | +0.026 | - | 641/1122 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.795 over 374 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.795^2 / (374 * K)): K=2: 0.081, K=3: 0.066, K=4: 0.057, K=6: 0.047, K=8: 0.040
