# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 12-0-10 | 55% | 55% | 32-77% | +32 | 11 | 0 |
| nicked | 3-0-19 | 14% | 14% | 0-36% | -321 | 11 | 0 |
| scout_king | 12-0-10 | 55% | 55% | 32-77% | +32 | 11 | 0 |
| **overall** | 27-0-39 | 41% | 41% | 27-55% | -64 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena | 0-0-6 | 0% | 0% | 6 | 0 |
| trophy | 0-0-6 | 0% | 0% | 6 | 0 |
| big_empty | 1-0-5 | 17% | 17% | 6 | 0 |
| default_small | 1-0-5 | 17% | 17% | 6 | 0 |
| default | 2-0-4 | 33% | 33% | 6 | 0 |
| queen_of_spades | 3-0-3 | 50% | 50% | 6 | 0 |
| schooltime | 3-0-3 | 50% | 50% | 6 | 0 |
| Devil | 4-0-2 | 67% | 67% | 6 | 0 |
| Trauma | 4-0-2 | 67% | 67% | 6 | 0 |
| stronghold | 4-0-2 | 67% | 67% | 6 | 0 |
| Colosseum | 5-0-1 | 83% | 83% | 6 | 0 |

candidate dragon deaths: head-to-head 4835, hit kelp 4025, hit other body 2350, hit itself 240, no valid action/timeout 29

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, scout_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
