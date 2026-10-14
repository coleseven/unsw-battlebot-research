# additive

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| old_route | 5-0-3 | 62% | 62% | 50-88% | +89 | 4 | 0 |
| **overall** | 5-0-3 | 62% | 62% | 50-88% | +89 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| big_empty_685baf0e797207b7 | 1-0-1 | 50% | 50% | 2 | 0 |
| schooltime_8be7eda86910a849 | 1-0-1 | 50% | 50% | 2 | 0 |
| stronghold_fb60e37176a8d1d3 | 1-0-1 | 50% | 50% | 2 | 0 |
| default_afc3707a967881d6 | 2-0-0 | 100% | 100% | 2 | 0 |

additive dragon deaths: hit kelp 576, head-to-head 366, hit other body 298, hit itself 65, no valid action/timeout 7

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for old_route: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
