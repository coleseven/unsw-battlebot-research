# Ablation report: 20261003-114945-ablate-1bdd7a

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 17 official + 0 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.186, wins 242/408; by opponent: cpp_nicked_v92 -0.294, cpp_nicked_v75 -0.294, cpp_leviathan3 +0.588, v7-base-bot +0.529, nicked_v44 +0.500, nicked_lab +0.088

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| nobookmap | -0.217 [-0.450, -0.033] | essential | +0.000 | -0.064 [-0.176, +0.039] | neutral | -0.029 | -0.088 | +0.029 | -0.059 | -0.059 | -0.176 | -0.064 | - | 229/408 |
| nobooks | -0.400 [-0.667, -0.167] | essential | -0.014 | -0.127 [-0.275, +0.005] | neutral | -0.206 | -0.029 | +0.029 | -0.118 | -0.088 | -0.353 | -0.127 | - | 216/408 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.804 over 204 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.804^2 / (204 * K)): K=2: 0.110, K=3: 0.090, K=4: 0.078, K=6: 0.064, K=8: 0.055
