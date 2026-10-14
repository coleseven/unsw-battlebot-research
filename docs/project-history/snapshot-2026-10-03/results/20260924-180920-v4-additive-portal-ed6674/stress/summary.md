# portal

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 1-0-1 | 50% | 50% | 0-100% | -0 | 1 | 0 |
| **overall** | 1-0-1 | 50% | 50% | 0-100% | -0 | 1 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| new_dense_small | 1-0-1 | 50% | 50% | 2 | 0 |

portal dragon deaths: hit kelp 751, head-to-head 512, hit other body 255

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
