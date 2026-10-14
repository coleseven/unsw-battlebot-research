# Corrected population result after map-identity audit

Excluded 96 games solely by map identity. Original results are retained, but their seven-map holdout is superseded. Screening selection is unchanged.

## pop_00

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 18-0-22 | 45% | 45% | 30-60% | -35 | 20 | 0 |
| splitter | 3-0-37 | 8% | 8% | 0-15% | -436 | 20 | 0 |
| v1 | 20-0-20 | 50% | 50% | 50-50% | -0 | 20 | 0 |
| **overall** | 41-0-79 | 34% | 34% | 27-42% | -114 | 60 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Devil_d0935a95185a8dd9 | 6-0-18 | 25% | 25% | 24 | 0 |
| Default_908dcc5cee06830e | 7-0-17 | 29% | 29% | 24 | 0 |
| arena_728547b8376892d9 | 8-0-16 | 33% | 33% | 24 | 0 |
| queen_of_spades_90867997b27cae7f | 9-0-15 | 38% | 38% | 24 | 0 |
| trophy_a3671180ec15b2b0 | 11-0-13 | 46% | 46% | 24 | 0 |

pop_00 dragon deaths: hit itself 106, hit kelp 55, hit other body 42, head-to-head 23

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


## pop_64

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 37-0-3 | 92% | 92% | 85-100% | +436 | 20 | 0 |
| splitter | 20-0-20 | 50% | 50% | 50-50% | -0 | 20 | 0 |
| v1 | 37-0-3 | 92% | 92% | 85-100% | +436 | 20 | 0 |
| **overall** | 94-0-26 | 78% | 78% | 72-85% | +223 | 60 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades_90867997b27cae7f | 16-0-8 | 67% | 67% | 24 | 0 |
| Default_908dcc5cee06830e | 18-0-6 | 75% | 75% | 24 | 0 |
| Devil_d0935a95185a8dd9 | 20-0-4 | 83% | 83% | 24 | 0 |
| arena_728547b8376892d9 | 20-0-4 | 83% | 83% | 24 | 0 |
| trophy_a3671180ec15b2b0 | 20-0-4 | 83% | 83% | 24 | 0 |

pop_64 dragon deaths: hit kelp 870, head-to-head 845, hit other body 786, hit itself 109

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

Paired improvement: 44.17 percentage points; 95% map-cluster interval [35.00, 52.50] points. Only 5 distinct held-out maps; conditional local evidence only.
