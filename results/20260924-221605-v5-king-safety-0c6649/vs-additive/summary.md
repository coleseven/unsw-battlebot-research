# safe_king

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 5-0-7 | 42% | 42% | 17-67% | -58 | 6 | 0 |
| **overall** | 5-0-7 | 42% | 42% | 17-67% | -58 | 6 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold | 0-0-2 | 0% | 0% | 2 | 0 |
| trophy | 0-0-2 | 0% | 0% | 2 | 0 |
| big_empty | 1-0-1 | 50% | 50% | 2 | 0 |
| schooltime | 1-0-1 | 50% | 50% | 2 | 0 |
| Trauma | 1-0-1 | 50% | 50% | 2 | 0 |
| default | 2-0-0 | 100% | 100% | 2 | 0 |

safe_king dragon deaths: hit kelp 747, head-to-head 476, hit other body 367, hit itself 68, no valid action/timeout 4

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
