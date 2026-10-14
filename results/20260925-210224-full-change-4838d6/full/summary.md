# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 21-0-1 | 95% | 95% | 86-100% | +529 | 11 | 0 |
| nicked | 17-0-5 | 77% | 77% | 55-95% | +213 | 11 | 0 |
| nicked_v44 | 6-0-16 | 27% | 27% | 5-50% | -170 | 11 | 0 |
| v6 | 12-0-10 | 55% | 55% | 32-77% | +32 | 11 | 0 |
| **overall** | 56-0-32 | 64% | 64% | 52-76% | +97 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 3-0-5 | 38% | 38% | 8 | 0 |
| queen_of_spades | 4-0-4 | 50% | 50% | 8 | 0 |
| default | 4-0-4 | 50% | 50% | 8 | 0 |
| stronghold | 4-0-4 | 50% | 50% | 8 | 0 |
| big_empty | 4-0-4 | 50% | 50% | 8 | 0 |
| schooltime | 5-0-3 | 62% | 62% | 8 | 0 |
| arena | 5-0-3 | 62% | 62% | 8 | 0 |
| default_small | 6-0-2 | 75% | 75% | 8 | 0 |
| trophy | 7-0-1 | 88% | 88% | 8 | 0 |
| Devil | 7-0-1 | 88% | 88% | 8 | 0 |
| Colosseum | 7-0-1 | 88% | 88% | 8 | 0 |

candidate dragon deaths: head-to-head 4824, hit kelp 4437, hit other body 3782, no valid action/timeout 2114, hit itself 10

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, nicked_v44, v6: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
