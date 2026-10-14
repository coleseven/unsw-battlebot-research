# scout_king

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 2-0-2 | 50% | 50% | 0-100% | -0 | 2 | 0 |
| **overall** | 2-0-2 | 50% | 50% | 0-100% | -0 | 2 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold | 0-0-2 | 0% | 0% | 2 | 0 |
| Trauma | 2-0-0 | 100% | 100% | 2 | 0 |

scout_king dragon deaths: hit kelp 366, head-to-head 252, hit other body 91, no valid action/timeout 1, hit itself 1

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
