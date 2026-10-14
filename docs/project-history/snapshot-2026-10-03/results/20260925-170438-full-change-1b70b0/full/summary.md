# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 18-0-4 | 82% | 82% | 59-100% | +261 | 11 | 0 |
| nicked | 13-0-9 | 59% | 59% | 32-86% | +64 | 11 | 0 |
| scout_king | 17-0-5 | 77% | 77% | 55-100% | +213 | 11 | 0 |
| **overall** | 48-0-18 | 73% | 73% | 58-86% | +170 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold | 0-0-6 | 0% | 0% | 6 | 0 |
| Trauma | 1-0-5 | 17% | 17% | 6 | 0 |
| queen_of_spades | 4-0-2 | 67% | 67% | 6 | 0 |
| default | 4-0-2 | 67% | 67% | 6 | 0 |
| default_small | 5-0-1 | 83% | 83% | 6 | 0 |
| Devil | 5-0-1 | 83% | 83% | 6 | 0 |
| trophy | 5-0-1 | 83% | 83% | 6 | 0 |
| arena | 6-0-0 | 100% | 100% | 6 | 0 |
| Colosseum | 6-0-0 | 100% | 100% | 6 | 0 |
| schooltime | 6-0-0 | 100% | 100% | 6 | 0 |
| big_empty | 6-0-0 | 100% | 100% | 6 | 0 |

candidate dragon deaths: head-to-head 3493, hit kelp 3170, hit other body 2879, no valid action/timeout 2390, hit itself 15

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, scout_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
