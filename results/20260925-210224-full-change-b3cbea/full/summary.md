# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 21-0-1 | 95% | 95% | 86-100% | +529 | 11 | 0 |
| nicked | 14-0-8 | 64% | 64% | 41-86% | +97 | 11 | 0 |
| nicked_v44 | 7-0-15 | 32% | 32% | 14-50% | -132 | 11 | 0 |
| v6 | 13-0-9 | 59% | 59% | 36-82% | +64 | 11 | 0 |
| **overall** | 55-0-33 | 62% | 62% | 50-74% | +89 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades | 2-0-6 | 25% | 25% | 8 | 0 |
| big_empty | 2-0-6 | 25% | 25% | 8 | 0 |
| trophy | 4-0-4 | 50% | 50% | 8 | 0 |
| Trauma | 4-0-4 | 50% | 50% | 8 | 0 |
| stronghold | 4-0-4 | 50% | 50% | 8 | 0 |
| default_small | 6-0-2 | 75% | 75% | 8 | 0 |
| default | 6-0-2 | 75% | 75% | 8 | 0 |
| schooltime | 6-0-2 | 75% | 75% | 8 | 0 |
| Colosseum | 6-0-2 | 75% | 75% | 8 | 0 |
| arena | 7-0-1 | 88% | 88% | 8 | 0 |
| Devil | 8-0-0 | 100% | 100% | 8 | 0 |

candidate dragon deaths: head-to-head 3945, hit kelp 2128, hit other body 1775, no valid action/timeout 1076, hit itself 8

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, nicked_v44, v6: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
