# export_scout

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 12-0-4 | 75% | 75% | 56-94% | +191 | 8 | 0 |
| **overall** | 12-0-4 | 75% | 75% | 56-94% | +191 | 8 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold | 4-0-4 | 50% | 50% | 8 | 0 |
| Trauma | 8-0-0 | 100% | 100% | 8 | 0 |

export_scout dragon deaths: hit kelp 1512, head-to-head 1000, hit other body 376, no valid action/timeout 4, hit itself 4

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
