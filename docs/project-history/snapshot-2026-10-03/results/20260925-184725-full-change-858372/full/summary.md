# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 17-0-5 | 77% | 77% | 55-100% | +213 | 11 | 0 |
| nicked | 12-0-10 | 55% | 55% | 32-77% | +32 | 11 | 0 |
| scout_king | 16-0-6 | 73% | 73% | 50-95% | +170 | 11 | 0 |
| **overall** | 45-0-21 | 68% | 68% | 55-82% | +132 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 0-0-6 | 0% | 0% | 6 | 0 |
| stronghold | 0-0-6 | 0% | 0% | 6 | 0 |
| queen_of_spades | 2-0-4 | 33% | 33% | 6 | 0 |
| trophy | 4-0-2 | 67% | 67% | 6 | 0 |
| default_small | 5-0-1 | 83% | 83% | 6 | 0 |
| default | 5-0-1 | 83% | 83% | 6 | 0 |
| big_empty | 5-0-1 | 83% | 83% | 6 | 0 |
| Devil | 6-0-0 | 100% | 100% | 6 | 0 |
| arena | 6-0-0 | 100% | 100% | 6 | 0 |
| Colosseum | 6-0-0 | 100% | 100% | 6 | 0 |
| schooltime | 6-0-0 | 100% | 100% | 6 | 0 |

candidate dragon deaths: head-to-head 3702, hit kelp 2921, hit other body 2760, no valid action/timeout 2420, hit itself 12

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, scout_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
