# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 21-0-1 | 95% | 95% | 86-100% | +529 | 11 | 0 |
| nicked | 17-0-5 | 77% | 77% | 59-95% | +213 | 11 | 0 |
| nicked_v44 | 7-0-15 | 32% | 32% | 9-55% | -132 | 11 | 0 |
| v6 | 15-0-7 | 68% | 68% | 50-86% | +132 | 11 | 0 |
| **overall** | 60-0-28 | 68% | 68% | 57-80% | +132 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 4-0-4 | 50% | 50% | 8 | 0 |
| default | 4-0-4 | 50% | 50% | 8 | 0 |
| schooltime | 4-0-4 | 50% | 50% | 8 | 0 |
| big_empty | 5-0-3 | 62% | 62% | 8 | 0 |
| default_small | 5-0-3 | 62% | 62% | 8 | 0 |
| queen_of_spades | 5-0-3 | 62% | 62% | 8 | 0 |
| arena | 6-0-2 | 75% | 75% | 8 | 0 |
| stronghold | 6-0-2 | 75% | 75% | 8 | 0 |
| Colosseum | 7-0-1 | 88% | 88% | 8 | 0 |
| Devil | 7-0-1 | 88% | 88% | 8 | 0 |
| trophy | 7-0-1 | 88% | 88% | 8 | 0 |

candidate dragon deaths: head-to-head 4234, hit kelp 3481, hit other body 2602, no valid action/timeout 1609, hit itself 5

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, nicked_v44, v6: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
