# Ablation report: 20260926-204722-ablate-903314

6 seeds, opponents nicked; 11 official + 4 extra maps, both sides. Delta = variant margin minus base margin on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.147, wins 128/180; by opponent: nicked +0.147

| variant | delta all [95% CI] | verdict | vs nicked | official | extra | wins |
|---|---|---|---|---|---|---|

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.332 over 30 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.332^2 / (30 * K)): K=2: 0.119, K=3: 0.097, K=4: 0.084, K=6: 0.069, K=8: 0.059
