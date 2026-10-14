# grower

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 3-0-5 | 38% | 38% | 0-75% | -89 | 4 | 0 |
| **overall** | 3-0-5 | 38% | 38% | 0-75% | -89 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default_afc3707a967881d6 | 0-0-2 | 0% | 0% | 2 | 0 |
| stronghold_fb60e37176a8d1d3 | 0-0-2 | 0% | 0% | 2 | 0 |
| schooltime_8be7eda86910a849 | 1-0-1 | 50% | 50% | 2 | 0 |
| big_empty_685baf0e797207b7 | 2-0-0 | 100% | 100% | 2 | 0 |

grower dragon deaths: hit kelp 551, head-to-head 372, hit other body 300, hit itself 69

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
