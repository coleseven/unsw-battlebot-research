# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 21-0-1 | 95% | 95% | 86-100% | +529 | 11 | 0 |
| nicked | 16-0-6 | 73% | 73% | 50-95% | +170 | 11 | 0 |
| nicked_v44 | 7-0-15 | 32% | 32% | 9-55% | -132 | 11 | 0 |
| v6 | 11-0-11 | 50% | 50% | 32-73% | -0 | 11 | 0 |
| **overall** | 55-0-33 | 62% | 62% | 50-75% | +89 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| big_empty | 2-0-6 | 25% | 25% | 8 | 0 |
| queen_of_spades | 3-0-5 | 38% | 38% | 8 | 0 |
| schooltime | 3-0-5 | 38% | 38% | 8 | 0 |
| Trauma | 4-0-4 | 50% | 50% | 8 | 0 |
| default_small | 5-0-3 | 62% | 62% | 8 | 0 |
| trophy | 5-0-3 | 62% | 62% | 8 | 0 |
| stronghold | 5-0-3 | 62% | 62% | 8 | 0 |
| Colosseum | 6-0-2 | 75% | 75% | 8 | 0 |
| default | 7-0-1 | 88% | 88% | 8 | 0 |
| arena | 7-0-1 | 88% | 88% | 8 | 0 |
| Devil | 8-0-0 | 100% | 100% | 8 | 0 |

candidate dragon deaths: head-to-head 3979, hit kelp 2209, hit other body 1876, no valid action/timeout 1040, hit itself 7

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, nicked_v44, v6: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
