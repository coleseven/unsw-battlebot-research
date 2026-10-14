# guard_all

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 9-0-13 | 41% | 41% | 18-64% | -64 | 11 | 0 |
| **overall** | 9-0-13 | 41% | 41% | 18-64% | -64 | 11 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Colosseum_3042ccc262f0211a | 0-0-2 | 0% | 0% | 2 | 0 |
| default_afc3707a967881d6 | 0-0-2 | 0% | 0% | 2 | 0 |
| big_empty_685baf0e797207b7 | 0-0-2 | 0% | 0% | 2 | 0 |
| stronghold_fb60e37176a8d1d3 | 0-0-2 | 0% | 0% | 2 | 0 |
| arena_728547b8376892d9 | 1-0-1 | 50% | 50% | 2 | 0 |
| default_small_f98ab391cccf33b1 | 1-0-1 | 50% | 50% | 2 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 1-0-1 | 50% | 50% | 2 | 0 |
| trophy_fd985019831fe135 | 1-0-1 | 50% | 50% | 2 | 0 |
| Trauma_d014b28abbd1abb0 | 1-0-1 | 50% | 50% | 2 | 0 |
| schooltime_8be7eda86910a849 | 2-0-0 | 100% | 100% | 2 | 0 |
| Devil_1b2147f4a8a775d2 | 2-0-0 | 100% | 100% | 2 | 0 |

guard_all dragon deaths: head-to-head 1937, hit kelp 1342, hit other body 1044, hit itself 63

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# guard_later

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 13-0-9 | 59% | 59% | 36-82% | +64 | 11 | 0 |
| **overall** | 13-0-9 | 59% | 59% | 36-82% | +64 | 11 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default_afc3707a967881d6 | 0-0-2 | 0% | 0% | 2 | 0 |
| Devil_1b2147f4a8a775d2 | 0-0-2 | 0% | 0% | 2 | 0 |
| default_small_f98ab391cccf33b1 | 1-0-1 | 50% | 50% | 2 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 1-0-1 | 50% | 50% | 2 | 0 |
| big_empty_685baf0e797207b7 | 1-0-1 | 50% | 50% | 2 | 0 |
| schooltime_8be7eda86910a849 | 1-0-1 | 50% | 50% | 2 | 0 |
| stronghold_fb60e37176a8d1d3 | 1-0-1 | 50% | 50% | 2 | 0 |
| arena_728547b8376892d9 | 2-0-0 | 100% | 100% | 2 | 0 |
| Colosseum_3042ccc262f0211a | 2-0-0 | 100% | 100% | 2 | 0 |
| trophy_fd985019831fe135 | 2-0-0 | 100% | 100% | 2 | 0 |
| Trauma_d014b28abbd1abb0 | 2-0-0 | 100% | 100% | 2 | 0 |

guard_later dragon deaths: head-to-head 1760, hit kelp 1271, hit other body 1110, hit itself 69

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.
