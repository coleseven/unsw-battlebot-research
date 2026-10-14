# head_guard

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 1-0-3 | 25% | 25% | 0-50% | -191 | 2 | 0 |
| **overall** | 1-0-3 | 25% | 25% | 0-50% | -191 | 2 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 0-0-2 | 0% | 0% | 2 | 0 |
| default_small | 1-0-1 | 50% | 50% | 2 | 0 |

head_guard dragon deaths: hit kelp 295, head-to-head 148, hit other body 64, no valid action/timeout 4, hit itself 1

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for nicked: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
