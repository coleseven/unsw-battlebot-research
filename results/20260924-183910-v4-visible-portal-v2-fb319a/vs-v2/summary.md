# visible_portal

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 7-0-3 | 70% | 70% | 30-100% | +147 | 5 | 0 |
| **overall** | 7-0-3 | 70% | 70% | 30-100% | +147 | 5 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default | 0-0-2 | 0% | 0% | 2 | 0 |
| schooltime | 1-0-1 | 50% | 50% | 2 | 0 |
| Colosseum | 2-0-0 | 100% | 100% | 2 | 0 |
| queen_of_spades | 2-0-0 | 100% | 100% | 2 | 0 |
| trophy | 2-0-0 | 100% | 100% | 2 | 0 |

visible_portal dragon deaths: hit kelp 675, head-to-head 462, hit other body 306, no valid action/timeout 19, hit itself 17

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v2: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
