# feed_king

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 9-0-3 | 75% | 75% | 42-100% | +191 | 6 | 0 |
| **overall** | 9-0-3 | 75% | 75% | 42-100% | +191 | 6 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| trophy | 0-0-2 | 0% | 0% | 2 | 0 |
| big_empty | 1-0-1 | 50% | 50% | 2 | 0 |
| default | 2-0-0 | 100% | 100% | 2 | 0 |
| schooltime | 2-0-0 | 100% | 100% | 2 | 0 |
| stronghold | 2-0-0 | 100% | 100% | 2 | 0 |
| Trauma | 2-0-0 | 100% | 100% | 2 | 0 |

feed_king dragon deaths: hit kelp 748, head-to-head 482, hit other body 350, hit itself 67, no valid action/timeout 14

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
