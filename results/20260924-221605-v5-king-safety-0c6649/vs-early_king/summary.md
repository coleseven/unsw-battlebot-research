# safe_king

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| early_king | 5-0-7 | 42% | 42% | 25-50% | -58 | 6 | 0 |
| **overall** | 5-0-7 | 42% | 42% | 25-50% | -58 | 6 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 0-0-2 | 0% | 0% | 2 | 0 |
| big_empty | 1-0-1 | 50% | 50% | 2 | 0 |
| default | 1-0-1 | 50% | 50% | 2 | 0 |
| schooltime | 1-0-1 | 50% | 50% | 2 | 0 |
| stronghold | 1-0-1 | 50% | 50% | 2 | 0 |
| trophy | 1-0-1 | 50% | 50% | 2 | 0 |

safe_king dragon deaths: hit kelp 732, head-to-head 450, hit other body 371, hit itself 81, no valid action/timeout 6

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for early_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
