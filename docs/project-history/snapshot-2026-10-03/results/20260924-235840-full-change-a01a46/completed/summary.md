# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 13-0-9 | 59% | 59% | 36-77% | +64 | 11 | 0 |
| nicked | 3-0-19 | 14% | 14% | 0-36% | -321 | 11 | 0 |
| scout_king | 10-0-12 | 45% | 45% | 27-68% | -32 | 11 | 0 |
| **overall** | 26-0-40 | 39% | 39% | 27-52% | -75 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 0-0-6 | 0% | 0% | 6 | 0 |
| schooltime | 1-0-5 | 17% | 17% | 6 | 0 |
| Colosseum | 2-0-4 | 33% | 33% | 6 | 0 |
| Devil | 2-0-4 | 33% | 33% | 6 | 0 |
| big_empty | 2-0-4 | 33% | 33% | 6 | 0 |
| queen_of_spades | 2-0-4 | 33% | 33% | 6 | 0 |
| default_small | 3-0-3 | 50% | 50% | 6 | 0 |
| stronghold | 3-0-3 | 50% | 50% | 6 | 0 |
| trophy | 3-0-3 | 50% | 50% | 6 | 0 |
| arena | 4-0-2 | 67% | 67% | 6 | 0 |
| default | 4-0-2 | 67% | 67% | 6 | 0 |

candidate dragon deaths: hit kelp 5959, head-to-head 5646, hit other body 2775, hit itself 218, no valid action/timeout 39

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, scout_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
