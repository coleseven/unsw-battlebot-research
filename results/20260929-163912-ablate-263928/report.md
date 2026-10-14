# Ablation report: 20260929-163912-ablate-263928

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.149, wins 325/540; by opponent: cpp_nicked_v92 -0.415, cpp_nicked_v75 -0.068, cpp_leviathan3 +0.499, v7-base-bot +0.470, nicked_v44 +0.462, nicked_lab -0.054

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pf16 | -0.013 [-0.029, +0.000] | neutral | +0.000 | -0.009 [-0.019, +0.001] | neutral | -0.012 | -0.018 | -0.008 | +0.001 | -0.015 | -0.002 | -0.006 | -0.016 | 321/540 |
| pf16r5 | -0.006 [-0.022, +0.009] | neutral | +0.000 | -0.004 [-0.015, +0.006] | neutral | -0.013 | -0.018 | +0.004 | +0.003 | -0.013 | +0.013 | -0.006 | +0.001 | 323/540 |
| pf10r5 | -0.005 [-0.021, +0.011] | neutral | -0.012 | -0.007 [-0.020, +0.004] | neutral | +0.017 | -0.032 | -0.001 | -0.016 | -0.013 | +0.001 | -0.004 | -0.016 | 322/540 |
| shift40 | +0.026 [-0.007, +0.064] | neutral | +0.056 | +0.036 [+0.011, +0.064] | harmful (drop) | +0.022 | +0.080 | +0.011 | +0.023 | +0.002 | +0.079 | +0.037 | +0.035 | 344/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.624 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.624^2 / (180 * K)): K=2: 0.091, K=3: 0.074, K=4: 0.064, K=6: 0.053, K=8: 0.046
