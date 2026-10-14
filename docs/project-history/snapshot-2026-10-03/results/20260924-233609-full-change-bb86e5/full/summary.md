# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 15-0-7 | 68% | 68% | 45-86% | +132 | 11 | 0 |
| nicked | 5-0-17 | 23% | 23% | 0-50% | -213 | 11 | 0 |
| v3 | 14-0-8 | 64% | 64% | 45-82% | +97 | 11 | 0 |
| **overall** | 34-0-32 | 52% | 52% | 36-65% | +11 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Devil | 1-0-5 | 17% | 17% | 6 | 0 |
| trophy | 1-0-5 | 17% | 17% | 6 | 0 |
| queen_of_spades | 2-0-4 | 33% | 33% | 6 | 0 |
| stronghold | 3-0-3 | 50% | 50% | 6 | 0 |
| schooltime | 3-0-3 | 50% | 50% | 6 | 0 |
| big_empty | 3-0-3 | 50% | 50% | 6 | 0 |
| default_small | 4-0-2 | 67% | 67% | 6 | 0 |
| default | 4-0-2 | 67% | 67% | 6 | 0 |
| Trauma | 4-0-2 | 67% | 67% | 6 | 0 |
| arena | 4-0-2 | 67% | 67% | 6 | 0 |
| Colosseum | 5-0-1 | 83% | 83% | 6 | 0 |

candidate dragon deaths: head-to-head 5356, hit kelp 4578, hit other body 2733, hit itself 199, no valid action/timeout 36

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
