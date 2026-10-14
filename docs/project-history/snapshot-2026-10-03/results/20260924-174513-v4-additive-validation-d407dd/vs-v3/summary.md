# additive

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 8-0-8 | 50% | 50% | 25-75% | -0 | 8 | 0 |
| **overall** | 8-0-8 | 50% | 50% | 25-75% | -0 | 8 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Colosseum | 0-0-4 | 0% | 0% | 4 | 0 |
| Trauma | 2-0-2 | 50% | 50% | 4 | 0 |
| queen_of_spades | 2-0-2 | 50% | 50% | 4 | 0 |
| Devil | 4-0-0 | 100% | 100% | 4 | 0 |

additive dragon deaths: head-to-head 1416, hit other body 566, hit kelp 494, hit itself 4

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
