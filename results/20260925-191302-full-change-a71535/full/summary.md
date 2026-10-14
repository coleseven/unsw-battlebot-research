# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 21-0-1 | 95% | 95% | 86-100% | +529 | 11 | 0 |
| ctmes | 21-0-1 | 95% | 95% | 86-100% | +529 | 11 | 0 |
| nicked | 16-0-6 | 73% | 73% | 45-95% | +170 | 11 | 0 |
| nicked_v44 | 8-0-14 | 36% | 36% | 14-64% | -97 | 11 | 0 |
| v3 | 21-0-1 | 95% | 95% | 86-100% | +529 | 11 | 0 |
| v6-fair-search-bot | 16-0-6 | 73% | 73% | 59-86% | +170 | 11 | 0 |
| **overall** | 103-0-29 | 78% | 78% | 69-86% | +220 | 66 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 6-0-6 | 50% | 50% | 12 | 0 |
| queen_of_spades | 8-0-4 | 67% | 67% | 12 | 0 |
| trophy | 8-0-4 | 67% | 67% | 12 | 0 |
| big_empty | 8-0-4 | 67% | 67% | 12 | 0 |
| arena | 9-0-3 | 75% | 75% | 12 | 0 |
| schooltime | 9-0-3 | 75% | 75% | 12 | 0 |
| default | 10-0-2 | 83% | 83% | 12 | 0 |
| default_small | 11-0-1 | 92% | 92% | 12 | 0 |
| Devil | 11-0-1 | 92% | 92% | 12 | 0 |
| stronghold | 11-0-1 | 92% | 92% | 12 | 0 |
| Colosseum | 12-0-0 | 100% | 100% | 12 | 0 |

candidate dragon deaths: head-to-head 6706, hit kelp 5979, hit other body 5452, no valid action/timeout 3278, hit itself 9

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, ctmes, nicked, nicked_v44, v3, v6-fair-search-bot: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
