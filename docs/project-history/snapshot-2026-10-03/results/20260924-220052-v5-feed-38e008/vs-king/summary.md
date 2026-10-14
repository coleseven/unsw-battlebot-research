# feed_king

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| early_king | 6-0-6 | 50% | 50% | 25-75% | -0 | 6 | 0 |
| **overall** | 6-0-6 | 50% | 50% | 25-75% | -0 | 6 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| schooltime | 0-0-2 | 0% | 0% | 2 | 0 |
| big_empty | 1-0-1 | 50% | 50% | 2 | 0 |
| default | 1-0-1 | 50% | 50% | 2 | 0 |
| Trauma | 1-0-1 | 50% | 50% | 2 | 0 |
| trophy | 1-0-1 | 50% | 50% | 2 | 0 |
| stronghold | 2-0-0 | 100% | 100% | 2 | 0 |

feed_king dragon deaths: hit kelp 719, head-to-head 432, hit other body 354, hit itself 74, no valid action/timeout 12

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for early_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
