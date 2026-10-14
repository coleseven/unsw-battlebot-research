# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 8-0-14 | 36% | 36% | 14-64% | -97 | 11 | 0 |
| nicked | 1-0-21 | 5% | 5% | 0-14% | -529 | 11 | 0 |
| scout_king | 11-0-11 | 50% | 50% | 27-73% | -0 | 11 | 0 |
| **overall** | 20-0-46 | 30% | 30% | 18-44% | -145 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default_small | 0-0-6 | 0% | 0% | 6 | 0 |
| stronghold | 0-0-6 | 0% | 0% | 6 | 0 |
| Trauma | 1-0-5 | 17% | 17% | 6 | 0 |
| schooltime | 1-0-5 | 17% | 17% | 6 | 0 |
| big_empty | 1-0-5 | 17% | 17% | 6 | 0 |
| Devil | 2-0-4 | 33% | 33% | 6 | 0 |
| trophy | 2-0-4 | 33% | 33% | 6 | 0 |
| queen_of_spades | 3-0-3 | 50% | 50% | 6 | 0 |
| arena | 3-0-3 | 50% | 50% | 6 | 0 |
| Colosseum | 3-0-3 | 50% | 50% | 6 | 0 |
| default | 4-0-2 | 67% | 67% | 6 | 0 |

candidate dragon deaths: head-to-head 5339, hit kelp 4205, hit other body 2591, hit itself 170, no valid action/timeout 8

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, scout_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
