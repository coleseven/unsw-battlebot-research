# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 14-0-8 | 64% | 64% | 45-82% | +97 | 11 | 0 |
| nicked | 4-0-18 | 18% | 18% | 0-41% | -261 | 11 | 0 |
| scout_king | 12-0-10 | 55% | 55% | 36-73% | +32 | 11 | 0 |
| **overall** | 30-0-36 | 45% | 45% | 33-59% | -32 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| trophy | 1-0-5 | 17% | 17% | 6 | 0 |
| Trauma | 1-0-5 | 17% | 17% | 6 | 0 |
| queen_of_spades | 2-0-4 | 33% | 33% | 6 | 0 |
| Devil | 2-0-4 | 33% | 33% | 6 | 0 |
| stronghold | 2-0-4 | 33% | 33% | 6 | 0 |
| arena | 2-0-4 | 33% | 33% | 6 | 0 |
| schooltime | 3-0-3 | 50% | 50% | 6 | 0 |
| big_empty | 3-0-3 | 50% | 50% | 6 | 0 |
| default_small | 4-0-2 | 67% | 67% | 6 | 0 |
| default | 4-0-2 | 67% | 67% | 6 | 0 |
| Colosseum | 6-0-0 | 100% | 100% | 6 | 0 |

candidate dragon deaths: head-to-head 5178, hit kelp 4567, hit other body 2832, hit itself 251, no valid action/timeout 35

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, scout_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
