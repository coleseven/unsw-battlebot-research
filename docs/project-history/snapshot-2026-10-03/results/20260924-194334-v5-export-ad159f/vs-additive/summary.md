# export_scout

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 4-0-4 | 50% | 50% | 0-100% | -0 | 4 | 0 |
| **overall** | 4-0-4 | 50% | 50% | 0-100% | -0 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold | 0-0-4 | 0% | 0% | 4 | 0 |
| Trauma | 4-0-0 | 100% | 100% | 4 | 0 |

export_scout dragon deaths: hit kelp 1176, head-to-head 632, hit other body 204, no valid action/timeout 6, hit itself 4

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
