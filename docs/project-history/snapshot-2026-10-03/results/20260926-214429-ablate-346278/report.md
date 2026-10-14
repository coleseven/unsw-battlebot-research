# Ablation report: 20260926-214429-ablate-346278

4 seeds, opponents v7-base-bot, nicked; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.134, wins 141/240; by opponent: v7-base-bot +0.000, nicked +0.267

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs v7-base-bot | vs nicked | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|
| no_food | -0.255 [-0.376, -0.137] | essential | -0.235 | -0.248 [-0.355, -0.143] | essential | -0.309 | -0.188 | -0.282 | -0.155 | 103/240 |
| no_spawn | -0.123 [-0.218, -0.014] | essential | -0.099 | -0.115 [-0.205, -0.026] | essential | -0.168 | -0.063 | -0.150 | -0.020 | 123/240 |
| no_explore | +0.008 [-0.109, +0.117] | neutral | -0.010 | +0.002 [-0.080, +0.078] | neutral | +0.039 | -0.034 | +0.044 | -0.113 | 142/240 |
| no_trap | +0.131 [+0.024, +0.231] | harmful (drop) | -0.066 | +0.065 [-0.013, +0.147] | neutral | +0.123 | +0.007 | -0.025 | +0.315 | 154/240 |
| no_deadend | -0.029 [-0.123, +0.063] | neutral | -0.052 | -0.037 [-0.112, +0.037] | neutral | -0.076 | +0.002 | -0.065 | +0.041 | 134/240 |
| no_headsafe | -0.017 [-0.101, +0.078] | neutral | -0.024 | -0.019 [-0.089, +0.059] | neutral | -0.077 | +0.039 | -0.022 | -0.011 | 139/240 |
| no_revisit | +0.055 [-0.059, +0.171] | neutral | -0.005 | +0.035 [-0.052, +0.121] | neutral | -0.039 | +0.109 | +0.004 | +0.121 | 147/240 |
| no_fan | -0.016 [-0.114, +0.083] | neutral | +0.085 | +0.018 [-0.055, +0.094] | neutral | +0.063 | -0.027 | +0.047 | -0.061 | 146/240 |
| no_straight | -0.004 [-0.100, +0.102] | neutral | -0.001 | -0.003 [-0.080, +0.076] | neutral | -0.019 | +0.013 | -0.043 | +0.107 | 141/240 |
| no_portal | -0.006 [-0.080, +0.065] | neutral | -0.022 | -0.012 [-0.066, +0.041] | neutral | -0.003 | -0.020 | -0.003 | -0.035 | 139/240 |
| no_v3model | -0.355 [-0.463, -0.252] | essential | -0.271 | -0.327 [-0.415, -0.240] | essential | -0.320 | -0.334 | -0.381 | -0.179 | 92/240 |
| no_attack | -0.029 [-0.130, +0.066] | neutral | -0.195 | -0.085 [-0.165, -0.002] | essential | -0.173 | +0.004 | -0.117 | +0.004 | 130/240 |
| no_hunt | +0.028 [-0.045, +0.100] | neutral | +0.023 | +0.026 [-0.043, +0.093] | neutral | +0.021 | +0.032 | +0.011 | +0.069 | 146/240 |
| no_defend | +0.025 [-0.020, +0.068] | neutral | +0.118 | +0.056 [+0.016, +0.098] | harmful (drop) | +0.092 | +0.019 | +0.063 | +0.034 | 153/240 |
| no_hub | -0.115 [-0.200, -0.033] | essential | +0.051 | -0.060 [-0.130, +0.015] | neutral | -0.081 | -0.039 | -0.040 | -0.115 | 130/240 |
| no_goal | +0.037 [-0.094, +0.174] | neutral | +0.012 | +0.029 [-0.077, +0.138] | neutral | +0.047 | +0.011 | +0.019 | +0.056 | 147/240 |
| no_feed | -0.038 [-0.097, +0.025] | neutral | -0.086 | -0.054 [-0.110, +0.001] | neutral | -0.048 | -0.060 | -0.045 | -0.077 | 130/240 |
| no_protect | +0.017 [-0.038, +0.069] | neutral | +0.000 | +0.011 [-0.025, +0.047] | neutral | -0.043 | +0.066 | +0.004 | +0.030 | 143/240 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.649 over 60 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.649^2 / (60 * K)): K=2: 0.164, K=3: 0.134, K=4: 0.116, K=6: 0.095, K=8: 0.082
