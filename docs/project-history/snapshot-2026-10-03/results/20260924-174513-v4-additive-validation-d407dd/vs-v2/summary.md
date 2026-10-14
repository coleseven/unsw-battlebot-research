# additive

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 8-0-0 | 100% | 100% | 100-100% | +1200 | 4 | 0 |
| **overall** | 8-0-0 | 100% | 100% | 100-100% | +1200 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Devil | 2-0-0 | 100% | 100% | 2 | 0 |
| Trauma | 2-0-0 | 100% | 100% | 2 | 0 |
| queen_of_spades | 2-0-0 | 100% | 100% | 2 | 0 |
| Colosseum | 2-0-0 | 100% | 100% | 2 | 0 |

additive dragon deaths: head-to-head 908, hit kelp 525, hit other body 313, no valid action/timeout 3, hit itself 3

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v2: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
