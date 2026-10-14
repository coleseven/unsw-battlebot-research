# Ablation report: 20260927-190107-ablate-6028c1

3 seeds, opponents v7-base-bot, cpp_nicked_v75, cpp_leviathan3; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.143, wins 156/270; by opponent: v7-base-bot +0.294, cpp_nicked_v75 -0.187, cpp_leviathan3 +0.321

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs v7-base-bot | vs cpp_nicked_v75 | vs cpp_leviathan3 | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|
| age | +0.068 [-0.011, +0.148] | neutral | -0.075 | +0.020 [-0.043, +0.088] | neutral | -0.046 | +0.008 | +0.100 | +0.002 | +0.070 | 160/270 |
| vor | +0.016 [-0.080, +0.109] | neutral | -0.025 | +0.002 [-0.072, +0.072] | neutral | +0.036 | -0.045 | +0.016 | -0.003 | +0.018 | 158/270 |
| age_vor | +0.066 [-0.037, +0.177] | neutral | -0.069 | +0.021 [-0.062, +0.113] | neutral | +0.083 | -0.043 | +0.022 | +0.036 | -0.021 | 159/270 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.568 over 90 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.568^2 / (90 * K)): K=2: 0.117, K=3: 0.096, K=4: 0.083, K=6: 0.068, K=8: 0.059
