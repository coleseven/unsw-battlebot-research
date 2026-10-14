# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 22-0-0 | 100% | 100% | 100-100% | +1200 | 11 | 0 |
| nicked | 18-0-4 | 82% | 82% | 64-100% | +261 | 11 | 0 |
| nicked_v44 | 8-0-14 | 36% | 36% | 18-59% | -97 | 11 | 0 |
| v6 | 16-0-6 | 73% | 73% | 59-86% | +170 | 11 | 0 |
| **overall** | 64-0-24 | 73% | 73% | 62-83% | +170 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default_small | 5-0-3 | 62% | 62% | 8 | 0 |
| queen_of_spades | 5-0-3 | 62% | 62% | 8 | 0 |
| Trauma | 5-0-3 | 62% | 62% | 8 | 0 |
| schooltime | 5-0-3 | 62% | 62% | 8 | 0 |
| trophy | 6-0-2 | 75% | 75% | 8 | 0 |
| default | 6-0-2 | 75% | 75% | 8 | 0 |
| stronghold | 6-0-2 | 75% | 75% | 8 | 0 |
| arena | 6-0-2 | 75% | 75% | 8 | 0 |
| big_empty | 6-0-2 | 75% | 75% | 8 | 0 |
| Devil | 7-0-1 | 88% | 88% | 8 | 0 |
| Colosseum | 7-0-1 | 88% | 88% | 8 | 0 |

candidate dragon deaths: head-to-head 4261, hit kelp 3416, hit other body 2543, no valid action/timeout 1915, hit itself 9

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, nicked_v44, v6: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
