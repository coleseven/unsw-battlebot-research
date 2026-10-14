# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 12-0-10 | 55% | 55% | 27-82% | +32 | 11 | 0 |
| nicked | 5-0-17 | 23% | 23% | 0-50% | -213 | 11 | 0 |
| scout_king | 12-0-10 | 55% | 55% | 50-64% | +32 | 11 | 0 |
| **overall** | 29-0-37 | 44% | 44% | 30-58% | -42 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| trophy | 1-0-5 | 17% | 17% | 6 | 0 |
| big_empty | 1-0-5 | 17% | 17% | 6 | 0 |
| queen_of_spades | 2-0-4 | 33% | 33% | 6 | 0 |
| Devil | 2-0-4 | 33% | 33% | 6 | 0 |
| schooltime | 2-0-4 | 33% | 33% | 6 | 0 |
| default_small | 3-0-3 | 50% | 50% | 6 | 0 |
| default | 3-0-3 | 50% | 50% | 6 | 0 |
| Trauma | 3-0-3 | 50% | 50% | 6 | 0 |
| stronghold | 3-0-3 | 50% | 50% | 6 | 0 |
| arena | 4-0-2 | 67% | 67% | 6 | 0 |
| Colosseum | 5-0-1 | 83% | 83% | 6 | 0 |

candidate dragon deaths: head-to-head 5001, hit kelp 3910, hit other body 2476, hit itself 178, no valid action/timeout 25

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, scout_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
