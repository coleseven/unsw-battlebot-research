# early_king

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 14-0-10 | 58% | 58% | 33-83% | +58 | 12 | 0 |
| **overall** | 14-0-10 | 58% | 58% | 33-83% | +58 | 12 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold | 0-0-4 | 0% | 0% | 4 | 0 |
| trophy | 0-0-4 | 0% | 0% | 4 | 0 |
| big_empty | 2-0-2 | 50% | 50% | 4 | 0 |
| default | 4-0-0 | 100% | 100% | 4 | 0 |
| schooltime | 4-0-0 | 100% | 100% | 4 | 0 |
| Trauma | 4-0-0 | 100% | 100% | 4 | 0 |

early_king dragon deaths: hit kelp 1486, head-to-head 978, hit other body 686, hit itself 138, no valid action/timeout 16

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
