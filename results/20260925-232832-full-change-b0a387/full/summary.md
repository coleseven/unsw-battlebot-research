# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 22-0-0 | 100% | 100% | 100-100% | +1200 | 11 | 0 |
| ctmes | 21-0-1 | 95% | 95% | 86-100% | +529 | 11 | 0 |
| nicked | 14-0-8 | 64% | 64% | 36-86% | +97 | 11 | 0 |
| nicked_v44 | 9-0-13 | 41% | 41% | 18-64% | -64 | 11 | 0 |
| v3 | 22-0-0 | 100% | 100% | 100-100% | +1200 | 11 | 0 |
| v61b-goal-bot | 12-0-10 | 55% | 55% | 32-77% | +32 | 11 | 0 |
| **overall** | 100-0-32 | 76% | 76% | 67-85% | +198 | 66 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades | 8-0-4 | 67% | 67% | 12 | 0 |
| Trauma | 8-0-4 | 67% | 67% | 12 | 0 |
| stronghold | 8-0-4 | 67% | 67% | 12 | 0 |
| schooltime | 8-0-4 | 67% | 67% | 12 | 0 |
| big_empty | 8-0-4 | 67% | 67% | 12 | 0 |
| default_small | 9-0-3 | 75% | 75% | 12 | 0 |
| default | 9-0-3 | 75% | 75% | 12 | 0 |
| arena | 9-0-3 | 75% | 75% | 12 | 0 |
| trophy | 10-0-2 | 83% | 83% | 12 | 0 |
| Colosseum | 11-0-1 | 92% | 92% | 12 | 0 |
| Devil | 12-0-0 | 100% | 100% | 12 | 0 |

candidate dragon deaths: head-to-head 6458, hit kelp 5106, hit other body 4024, no valid action/timeout 2873, hit itself 9

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, ctmes, nicked, nicked_v44, v3, v61b-goal-bot: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
