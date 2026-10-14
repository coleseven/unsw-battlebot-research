# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 12-0-10 | 55% | 55% | 27-82% | +32 | 11 | 0 |
| nicked | 5-0-17 | 23% | 23% | 0-50% | -213 | 11 | 0 |
| scout_king | 7-0-15 | 32% | 32% | 14-50% | -132 | 11 | 0 |
| **overall** | 24-0-42 | 36% | 36% | 23-52% | -97 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| trophy | 0-0-6 | 0% | 0% | 6 | 0 |
| Devil | 0-0-6 | 0% | 0% | 6 | 0 |
| default | 0-0-6 | 0% | 0% | 6 | 0 |
| queen_of_spades | 1-0-5 | 17% | 17% | 6 | 0 |
| stronghold | 2-0-4 | 33% | 33% | 6 | 0 |
| big_empty | 2-0-4 | 33% | 33% | 6 | 0 |
| Colosseum | 3-0-3 | 50% | 50% | 6 | 0 |
| schooltime | 3-0-3 | 50% | 50% | 6 | 0 |
| Trauma | 4-0-2 | 67% | 67% | 6 | 0 |
| arena | 4-0-2 | 67% | 67% | 6 | 0 |
| default_small | 5-0-1 | 83% | 83% | 6 | 0 |

candidate dragon deaths: head-to-head 5070, hit kelp 4812, hit other body 2802, hit itself 262, no valid action/timeout 38

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, scout_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
