# additive

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 5-0-3 | 62% | 62% | 50-88% | +89 | 4 | 0 |
| **overall** | 5-0-3 | 62% | 62% | 50-88% | +89 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| big_empty_685baf0e797207b7 | 1-0-1 | 50% | 50% | 2 | 0 |
| default_afc3707a967881d6 | 1-0-1 | 50% | 50% | 2 | 0 |
| stronghold_fb60e37176a8d1d3 | 1-0-1 | 50% | 50% | 2 | 0 |
| schooltime_8be7eda86910a849 | 2-0-0 | 100% | 100% | 2 | 0 |

additive dragon deaths: hit kelp 576, head-to-head 369, hit other body 306, hit itself 60, no valid action/timeout 3

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# old_route

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 4-0-4 | 50% | 50% | 0-100% | -0 | 4 | 0 |
| **overall** | 4-0-4 | 50% | 50% | 0-100% | -0 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default_afc3707a967881d6 | 0-0-2 | 0% | 0% | 2 | 0 |
| stronghold_fb60e37176a8d1d3 | 0-0-2 | 0% | 0% | 2 | 0 |
| big_empty_685baf0e797207b7 | 2-0-0 | 100% | 100% | 2 | 0 |
| schooltime_8be7eda86910a849 | 2-0-0 | 100% | 100% | 2 | 0 |

old_route dragon deaths: hit kelp 547, head-to-head 374, hit other body 303, hit itself 67, no valid action/timeout 8

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
