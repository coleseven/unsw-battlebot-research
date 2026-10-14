# additive

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 10-0-10 | 50% | 50% | 30-70% | -0 | 10 | 0 |
| **overall** | 10-0-10 | 50% | 50% | 30-70% | -0 | 10 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Colosseum | 0-0-4 | 0% | 0% | 4 | 0 |
| default | 2-0-2 | 50% | 50% | 4 | 0 |
| queen_of_spades | 2-0-2 | 50% | 50% | 4 | 0 |
| trophy | 2-0-2 | 50% | 50% | 4 | 0 |
| schooltime | 4-0-0 | 100% | 100% | 4 | 0 |

additive dragon deaths: hit kelp 1514, head-to-head 1134, hit other body 602, no valid action/timeout 12, hit itself 6

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# portal

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 8-0-12 | 40% | 40% | 15-60% | -70 | 10 | 0 |
| **overall** | 8-0-12 | 40% | 40% | 15-60% | -70 | 10 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default | 0-0-4 | 0% | 0% | 4 | 0 |
| trophy | 0-0-4 | 0% | 0% | 4 | 0 |
| Colosseum | 2-0-2 | 50% | 50% | 4 | 0 |
| queen_of_spades | 2-0-2 | 50% | 50% | 4 | 0 |
| schooltime | 4-0-0 | 100% | 100% | 4 | 0 |

portal dragon deaths: hit kelp 1618, head-to-head 1028, hit other body 622, hit itself 30, no valid action/timeout 2

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
