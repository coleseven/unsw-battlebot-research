# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 1-0-21 | 5% | 5% | 0-14% | -529 | 11 | 0 |
| nicked | 0-0-22 | 0% | 0% | 0-0% | -1200 | 11 | 0 |
| scout_king | 2-0-20 | 9% | 9% | 0-23% | -400 | 11 | 0 |
| **overall** | 3-0-63 | 5% | 5% | 0-11% | -529 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades | 0-0-6 | 0% | 0% | 6 | 0 |
| default_small | 0-0-6 | 0% | 0% | 6 | 0 |
| Devil | 0-0-6 | 0% | 0% | 6 | 0 |
| Trauma | 0-0-6 | 0% | 0% | 6 | 0 |
| trophy | 0-0-6 | 0% | 0% | 6 | 0 |
| default | 0-0-6 | 0% | 0% | 6 | 0 |
| Colosseum | 0-0-6 | 0% | 0% | 6 | 0 |
| schooltime | 0-0-6 | 0% | 0% | 6 | 0 |
| big_empty | 0-0-6 | 0% | 0% | 6 | 0 |
| stronghold | 1-0-5 | 17% | 17% | 6 | 0 |
| arena | 2-0-4 | 33% | 33% | 6 | 0 |

candidate dragon deaths: head-to-head 1567, hit other body 1403, hit kelp 760, no valid action/timeout 151

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, scout_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
