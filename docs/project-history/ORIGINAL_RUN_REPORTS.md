# Original run reports — preserved excerpts in full

These are original reports, not corrected conclusions. Old generated headers, intervals, engine assumptions, duplicate seeds and invalid maps remain as written. Read the corrections in PROJECT_HISTORY.md first. A report may be partial; inclusion is not endorsement.

---

## results/20260922-150650-mybot/summary.md

SHA-256: `2a709716f6c53dd63249428420699802cf7f93be81b411ee2b906932cf5184f4`

# mybot evaluation

2026-09-22 15:07 · git f876927 · 180 games

| opponent | score | win % | 95% CI | Elo diff | games |
|---|---|---|---|---|---|
| greedy | 18/36 | 50% | 34–66% | -0 | 36 |
| hunter | 17/36 | 47% | 32–63% | -19 | 36 |
| splitter | 4/36 | 11% | 4–25% | -361 | 36 |
| turtle | 20/36 | 56% | 40–70% | +39 | 36 |
| wanderer | 22/36 | 61% | 45–75% | +79 | 36 |
| **overall** | 81/180 | **45%** | 38–52% | -35 | 180 |

| map | win % | games |
|---|---|---|
| default_small | 35% | 20 |
| schooltime | 35% | 20 |
| Devil | 40% | 20 |
| arena | 42% | 20 |
| trophy | 45% | 20 |
| default | 45% | 20 |
| Colosseum | 50% | 20 |
| big_empty | 52% | 20 |
| queen_of_spades | 60% | 20 |

mybot dragon deaths: hit itself 151, hit kelp 105, hit other body 40, head-to-head 10


---

## results/20260922-153401-tournament/summary.md

SHA-256: `bf9d651a20e579a86c5e300cd50dca3529857a0d5f8ed31d4f3c2dacaca16f20`

# Tournament

2026-09-22 15:36 · 540 games

| # | bot | Elo | splitter | v1 | greedy | hunter | turtle | wanderer |
|---|---|---|---|---|---|---|---|---|
| 1 | splitter | 1779 | — | 89% | 89% | 89% | 86% | 83% |
| 2 | v1 | 1460 | 11% | — | 50% | 47% | 56% | 61% |
| 3 | greedy | 1460 | 11% | 50% | — | 47% | 56% | 61% |
| 4 | hunter | 1458 | 11% | 53% | 53% | — | 53% | 54% |
| 5 | turtle | 1430 | 14% | 44% | 44% | 47% | — | 51% |
| 6 | wanderer | 1414 | 17% | 39% | 39% | 46% | 49% | — |


---

## results/20260922-155504-mybot/summary.md

SHA-256: `c771551722b7330f378c52567040dd9daec97848e35d454143da4190e8079276`

# mybot evaluation

2026-09-22 15:55:05 - git b809acc+dirty - 36 games

code: mybot ffe736af6c14ea33, splitter c50e10c521282fec, v1 ffe736af6c14ea33

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| splitter | 2-0-16 | 11% | 11% | 0-28% | -361 | 9 | 0 |
| v1 | 9-0-9 | 50% | 50% | 50-50% | -0 | 9 | 0 |
| **overall** | 11-0-25 | 31% | 31% | 19-42% | -143 | 18 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena | 3-0-9 | 25% | 25% | 12 | 0 |
| Colosseum | 3-0-9 | 25% | 25% | 12 | 0 |
| default | 5-0-7 | 42% | 42% | 12 | 0 |

mybot dragon deaths: hit itself 30, hit other body 20, hit kelp 6, head-to-head 1

Score counts a draw as half a win; win rate counts wins only. CI: bootstrap over map+seed blocks (both sides).


---

## results/20260922-160702-mybot/summary.md

SHA-256: `f0003f30dc662798056f5bdaa1f25b5d6c099ce6c1160ec45be9251b044cc306`

# mybot evaluation

2026-09-22 16:07:03 - git 6bd4092+dirty - 24 games

code: mybot ffe736af6c14ea33, splitter c50e10c521282fec, v1 ffe736af6c14ea33, starter 923296c73bfd4a1c

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| splitter | 0-0-8 | 0% | 0% | 0-0% | -1200 | 4 | 0 |
| starter | 8-0-0 | 100% | 100% | 100-100% | +1200 | 4 | 0 |
| v1 | 4-0-4 | 50% | 50% | 50-50% | -0 | 4 | 0 |
| **overall** | 12-0-12 | 50% | 50% | 29-71% | -0 | 12 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena | 6-0-6 | 50% | 50% | 12 | 0 |
| Colosseum | 6-0-6 | 50% | 50% | 12 | 0 |

mybot dragon deaths: hit itself 8, hit other body 2, hit kelp 1, head-to-head 1

Score counts a draw as half a win; win rate counts wins only. CI: bootstrap over map+seed blocks (both sides).


---

## results/20260922-161702-population-94dab2/summary.md

SHA-256: `dc6971bc61c142ae09531ceb09133aa3b3c7c72da3966c66f26f061edcdb1158`

# Population experiment

> SUPERSEDED: map-identity audit found a screening-map copy and a repeated
> held-out map. Use `map-audit/summary.md` for corrected figures: 34.2% versus
> 78.3%, gain 44.2 percentage points, map-cluster interval +35.0 to +52.5.
> Original measurements below are retained for audit, not final reporting.

Selected on screen only: pop_64.

| policy | screen score | held-out score |
|---|---:|---:|
| pop_00 | 37.5% | 34.5% |
| pop_02 | 64.6% | not tested |
| pop_04 | 68.8% | not tested |
| pop_08 | 72.9% | not tested |
| pop_64 | 83.3% | 78.6% |

Held-out improvement over no-split: +44.0%; 95% map-cluster bootstrap interval [+37.5%, +50.0%].

Only 7 reserved maps: this is conditional local-pool evidence, not a ladder-strength or CPU-budget claim. Map families may overlap between stages.

Score = wins + half draws, divided by games. Errors invalidate the stage.

mybot and all original bots/data remain unchanged. See plan.json, both stage summaries, raw games and held-out replays for audit.


---

## results/20260922-161702-population-94dab2/holdout/summary.md

SHA-256: `372377326fff0a949fd3807d32901d792753cfb34781ac8a55e3a54007b8584c`

## pop_00

> SUPERSEDED by `../map-audit/summary.md`: two map copies were excluded
> after semantic-identity auditing. Original results retained below.

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 26-0-30 | 46% | 46% | 34-59% | -25 | 28 | 0 |
| splitter | 4-0-52 | 7% | 7% | 2-14% | -446 | 28 | 0 |
| v1 | 28-0-28 | 50% | 50% | 50-50% | -0 | 28 | 0 |
| **overall** | 58-0-110 | 35% | 35% | 29-41% | -111 | 84 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Devil_d0935a95185a8dd9 | 6-0-18 | 25% | 25% | 24 | 0 |
| Default_908dcc5cee06830e | 7-0-17 | 29% | 29% | 24 | 0 |
| default_c14ae35451fc0e61 | 7-0-17 | 29% | 29% | 24 | 0 |
| arena_728547b8376892d9 | 8-0-16 | 33% | 33% | 24 | 0 |
| queen_of_spades_90867997b27cae7f | 9-0-15 | 38% | 38% | 24 | 0 |
| Big_Empty_60f7d35583505a93 | 10-0-14 | 42% | 42% | 24 | 0 |
| trophy_a3671180ec15b2b0 | 11-0-13 | 46% | 46% | 24 | 0 |

pop_00 dragon deaths: hit itself 187, hit other body 72, hit kelp 65, head-to-head 27

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


## pop_64

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 52-0-4 | 93% | 93% | 86-98% | +446 | 28 | 0 |
| splitter | 28-0-28 | 50% | 50% | 50-50% | -0 | 28 | 0 |
| v1 | 52-0-4 | 93% | 93% | 86-98% | +446 | 28 | 0 |
| **overall** | 132-0-36 | 79% | 79% | 73-83% | +226 | 84 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades_90867997b27cae7f | 16-0-8 | 67% | 67% | 24 | 0 |
| Default_908dcc5cee06830e | 18-0-6 | 75% | 75% | 24 | 0 |
| default_c14ae35451fc0e61 | 18-0-6 | 75% | 75% | 24 | 0 |
| Big_Empty_60f7d35583505a93 | 20-0-4 | 83% | 83% | 24 | 0 |
| Devil_d0935a95185a8dd9 | 20-0-4 | 83% | 83% | 24 | 0 |
| arena_728547b8376892d9 | 20-0-4 | 83% | 83% | 24 | 0 |
| trophy_a3671180ec15b2b0 | 20-0-4 | 83% | 83% | 24 | 0 |

pop_64 dragon deaths: hit other body 2129, head-to-head 1767, hit kelp 1005, hit itself 507

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).



---

## results/20260922-161702-population-94dab2/map-audit/summary.md

SHA-256: `d96e629590bddfedfb1c658922fdfea161125dfee1e3c59f38f144fb07943684`

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


---

## results/20260922-161702-population-94dab2/screen/summary.md

SHA-256: `fc00146f104526a16d38aad649fc8af8327f76ab4ec086daee597ade023d8bbc`

## pop_00

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 10-0-6 | 62% | 62% | 50-75% | +89 | 8 | 0 |
| splitter | 0-0-16 | 0% | 0% | 0-0% | -1200 | 8 | 0 |
| v1 | 8-0-8 | 50% | 50% | 50-50% | -0 | 8 | 0 |
| **overall** | 18-0-30 | 38% | 38% | 25-50% | -89 | 24 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Colosseum_40ea25a274d937f2 | 4-0-8 | 33% | 33% | 12 | 0 |
| default_small_25ddea344f5fb7a0 | 4-0-8 | 33% | 33% | 12 | 0 |
| big_empty_220696c19d5385bb | 5-0-7 | 42% | 42% | 12 | 0 |
| schooltime_38ce8ffaff5c12bc | 5-0-7 | 42% | 42% | 12 | 0 |

pop_00 dragon deaths: hit itself 38, hit kelp 32, hit other body 6, head-to-head 2

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for hunter, splitter, v1: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


## pop_02

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 14-0-2 | 88% | 88% | 75-100% | +338 | 8 | 0 |
| splitter | 2-0-14 | 12% | 12% | 0-31% | -338 | 8 | 0 |
| v1 | 15-0-1 | 94% | 94% | 81-100% | +470 | 8 | 0 |
| **overall** | 31-0-17 | 65% | 65% | 48-81% | +104 | 24 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| big_empty_220696c19d5385bb | 7-0-5 | 58% | 58% | 12 | 0 |
| default_small_25ddea344f5fb7a0 | 7-0-5 | 58% | 58% | 12 | 0 |
| Colosseum_40ea25a274d937f2 | 8-0-4 | 67% | 67% | 12 | 0 |
| schooltime_38ce8ffaff5c12bc | 9-0-3 | 75% | 75% | 12 | 0 |

pop_02 dragon deaths: hit kelp 77, hit itself 65, hit other body 45, head-to-head 31

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for hunter, splitter, v1: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


## pop_04

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 15-0-1 | 94% | 94% | 81-100% | +470 | 8 | 0 |
| splitter | 3-0-13 | 19% | 19% | 0-38% | -255 | 8 | 0 |
| v1 | 15-0-1 | 94% | 94% | 81-100% | +470 | 8 | 0 |
| **overall** | 33-0-15 | 69% | 69% | 52-83% | +137 | 24 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| big_empty_220696c19d5385bb | 7-0-5 | 58% | 58% | 12 | 0 |
| default_small_25ddea344f5fb7a0 | 8-0-4 | 67% | 67% | 12 | 0 |
| Colosseum_40ea25a274d937f2 | 9-0-3 | 75% | 75% | 12 | 0 |
| schooltime_38ce8ffaff5c12bc | 9-0-3 | 75% | 75% | 12 | 0 |

pop_04 dragon deaths: hit kelp 176, hit other body 114, hit itself 97, head-to-head 86

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for hunter, splitter, v1: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


## pop_08

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 13-0-3 | 81% | 81% | 56-100% | +255 | 8 | 0 |
| splitter | 7-0-9 | 44% | 44% | 19-75% | -44 | 8 | 0 |
| v1 | 15-0-1 | 94% | 94% | 81-100% | +470 | 8 | 0 |
| **overall** | 35-0-13 | 73% | 73% | 58-88% | +172 | 24 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| big_empty_220696c19d5385bb | 5-0-7 | 42% | 42% | 12 | 0 |
| schooltime_38ce8ffaff5c12bc | 8-0-4 | 67% | 67% | 12 | 0 |
| default_small_25ddea344f5fb7a0 | 10-0-2 | 83% | 83% | 12 | 0 |
| Colosseum_40ea25a274d937f2 | 12-0-0 | 100% | 100% | 12 | 0 |

pop_08 dragon deaths: hit kelp 398, hit other body 312, head-to-head 232, hit itself 202

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for hunter, splitter, v1: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


## pop_64

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 16-0-0 | 100% | 100% | 100-100% | +1200 | 8 | 0 |
| splitter | 8-0-8 | 50% | 50% | 50-50% | -0 | 8 | 0 |
| v1 | 16-0-0 | 100% | 100% | 100-100% | +1200 | 8 | 0 |
| **overall** | 40-0-8 | 83% | 83% | 73-92% | +280 | 24 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Colosseum_40ea25a274d937f2 | 10-0-2 | 83% | 83% | 12 | 0 |
| big_empty_220696c19d5385bb | 10-0-2 | 83% | 83% | 12 | 0 |
| default_small_25ddea344f5fb7a0 | 10-0-2 | 83% | 83% | 12 | 0 |
| schooltime_38ce8ffaff5c12bc | 10-0-2 | 83% | 83% | 12 | 0 |

pop_64 dragon deaths: hit other body 1163, head-to-head 969, hit kelp 923, hit itself 303

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for hunter, splitter, v1: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.



---

## results/20260922-171805-endgame-b67e3b/summary.md

SHA-256: `4e0c19bd3c7f274ce37aa1a04fbcfe1cc3fd616b27286d2d0267d92bca1e16ad`

# Split-cutoff experiment

Selected using screen only: stop_450.

| Policy | Screen score | Held-out score |
|---|---:|---:|
| perpetual | 79.2% | 79.2% |
| stop_200 | 81.2% | not tested |
| stop_300 | 83.3% | not tested |
| stop_400 | 83.3% | not tested |
| stop_450 | 87.5% | 90.0% |

Paired delta: +10.83 percentage points; 95% map-cluster interval [+4.17, +16.67].

Selected candidate vs splitter: 33-0-7 W-D-L, 82.5% score. Success gate passed: True.

No live bot changed or submitted. Only five validation maps and a scripted pool; not an online-strength claim. Negative/inconclusive results are retained.


---

## results/20260922-171805-endgame-b67e3b/holdout/summary.md

SHA-256: `9756db1e619095ef09f53987a3a9c603f3064dba5059344408cd851d204c0444`

## perpetual

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 37-0-3 | 92% | 92% | 85-100% | +436 | 20 | 0 |
| splitter | 20-0-20 | 50% | 50% | 50-50% | -0 | 20 | 0 |
| v1 | 38-0-2 | 95% | 95% | 88-100% | +512 | 20 | 0 |
| **overall** | 95-0-25 | 79% | 79% | 72-86% | +232 | 60 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default_afc3707a967881d6 | 15-0-9 | 62% | 62% | 24 | 0 |
| arena_728547b8376892d9 | 20-0-4 | 83% | 83% | 24 | 0 |
| default_small_f98ab391cccf33b1 | 20-0-4 | 83% | 83% | 24 | 0 |
| schooltime_8be7eda86910a849 | 20-0-4 | 83% | 83% | 24 | 0 |
| trophy_fd985019831fe135 | 20-0-4 | 83% | 83% | 24 | 0 |

perpetual dragon deaths: hit kelp 2866, head-to-head 1299, hit other body 1291, hit itself 137

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


## stop_450

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 36-0-4 | 90% | 90% | 78-100% | +382 | 20 | 0 |
| splitter | 33-0-7 | 82% | 82% | 70-92% | +269 | 20 | 0 |
| v1 | 39-0-1 | 98% | 98% | 92-100% | +636 | 20 | 0 |
| **overall** | 108-0-12 | 90% | 90% | 84-95% | +382 | 60 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default_afc3707a967881d6 | 19-0-5 | 79% | 79% | 24 | 0 |
| arena_728547b8376892d9 | 20-0-4 | 83% | 83% | 24 | 0 |
| default_small_f98ab391cccf33b1 | 21-0-3 | 88% | 88% | 24 | 0 |
| schooltime_8be7eda86910a849 | 24-0-0 | 100% | 100% | 24 | 0 |
| trophy_fd985019831fe135 | 24-0-0 | 100% | 100% | 24 | 0 |

stop_450 dragon deaths: hit kelp 2750, head-to-head 1263, hit other body 1240, hit itself 159

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).



---

## results/20260922-171805-endgame-b67e3b/screen/summary.md

SHA-256: `dcb3d7684c354ab6c6e5547438ac4f5ee6a7c227f0d15c62dad9572372db5a7b`

## perpetual

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 15-0-1 | 94% | 94% | 81-100% | +470 | 8 | 0 |
| splitter | 8-0-8 | 50% | 50% | 50-50% | -0 | 8 | 0 |
| v1 | 15-0-1 | 94% | 94% | 81-100% | +470 | 8 | 0 |
| **overall** | 38-0-10 | 79% | 79% | 69-90% | +232 | 24 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades_6cdb74a7a52d715a | 8-0-4 | 67% | 67% | 12 | 0 |
| Colosseum_3042ccc262f0211a | 10-0-2 | 83% | 83% | 12 | 0 |
| Devil_1b2147f4a8a775d2 | 10-0-2 | 83% | 83% | 12 | 0 |
| big_empty_685baf0e797207b7 | 10-0-2 | 83% | 83% | 12 | 0 |

perpetual dragon deaths: hit other body 894, head-to-head 717, hit itself 263, hit kelp 197

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for hunter, splitter, v1: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


## stop_200

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 15-0-1 | 94% | 94% | 81-100% | +470 | 8 | 0 |
| splitter | 8-0-8 | 50% | 50% | 25-75% | -0 | 8 | 0 |
| v1 | 16-0-0 | 100% | 100% | 100-100% | +1200 | 8 | 0 |
| **overall** | 39-0-9 | 81% | 81% | 67-94% | +255 | 24 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Colosseum_3042ccc262f0211a | 8-0-4 | 67% | 67% | 12 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 9-0-3 | 75% | 75% | 12 | 0 |
| Devil_1b2147f4a8a775d2 | 10-0-2 | 83% | 83% | 12 | 0 |
| big_empty_685baf0e797207b7 | 12-0-0 | 100% | 100% | 12 | 0 |

stop_200 dragon deaths: hit other body 509, head-to-head 427, hit itself 254, hit kelp 137

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for hunter, splitter, v1: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


## stop_300

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 15-0-1 | 94% | 94% | 81-100% | +470 | 8 | 0 |
| splitter | 9-0-7 | 56% | 56% | 31-81% | +44 | 8 | 0 |
| v1 | 16-0-0 | 100% | 100% | 100-100% | +1200 | 8 | 0 |
| **overall** | 40-0-8 | 83% | 83% | 71-96% | +280 | 24 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Colosseum_3042ccc262f0211a | 8-0-4 | 67% | 67% | 12 | 0 |
| Devil_1b2147f4a8a775d2 | 10-0-2 | 83% | 83% | 12 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 10-0-2 | 83% | 83% | 12 | 0 |
| big_empty_685baf0e797207b7 | 12-0-0 | 100% | 100% | 12 | 0 |

stop_300 dragon deaths: hit other body 656, head-to-head 563, hit itself 267, hit kelp 157

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for hunter, splitter, v1: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


## stop_400

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 15-0-1 | 94% | 94% | 81-100% | +470 | 8 | 0 |
| splitter | 10-0-6 | 62% | 62% | 50-81% | +89 | 8 | 0 |
| v1 | 15-0-1 | 94% | 94% | 81-100% | +470 | 8 | 0 |
| **overall** | 40-0-8 | 83% | 83% | 73-92% | +280 | 24 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades_6cdb74a7a52d715a | 9-0-3 | 75% | 75% | 12 | 0 |
| Colosseum_3042ccc262f0211a | 10-0-2 | 83% | 83% | 12 | 0 |
| Devil_1b2147f4a8a775d2 | 10-0-2 | 83% | 83% | 12 | 0 |
| big_empty_685baf0e797207b7 | 11-0-1 | 92% | 92% | 12 | 0 |

stop_400 dragon deaths: hit other body 819, head-to-head 677, hit itself 273, hit kelp 179

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for hunter, splitter, v1: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


## stop_450

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 15-0-1 | 94% | 94% | 81-100% | +470 | 8 | 0 |
| splitter | 12-0-4 | 75% | 75% | 56-94% | +191 | 8 | 0 |
| v1 | 15-0-1 | 94% | 94% | 81-100% | +470 | 8 | 0 |
| **overall** | 42-0-6 | 88% | 88% | 79-96% | +338 | 24 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades_6cdb74a7a52d715a | 9-0-3 | 75% | 75% | 12 | 0 |
| Devil_1b2147f4a8a775d2 | 10-0-2 | 83% | 83% | 12 | 0 |
| big_empty_685baf0e797207b7 | 11-0-1 | 92% | 92% | 12 | 0 |
| Colosseum_3042ccc262f0211a | 12-0-0 | 100% | 100% | 12 | 0 |

stop_450 dragon deaths: hit other body 861, head-to-head 700, hit itself 268, hit kelp 188

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for hunter, splitter, v1: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.



---

## results/20260922-173739-movement-659d1f/summary.md

SHA-256: `91aed616f48d6a1b93bad4c36d6e5d23ab6f76bdf41f748abe160e6c02b5648f`

# Independent movement experiments

| Policy | Validation score | W-D-L vs round-450 baseline | Gate |
|---|---:|---|---|
| control_450 | 74.2% | 20-0-20 | control |
| trap | 79.2% | 23-0-17 | False |
| sprint | 73.3% | 21-0-19 | False |

trap: paired gain +5.00 percentage points; 97.5% map-cluster interval [-2.50, +15.83].

sprint: paired gain -0.83 percentage points; 97.5% map-cluster interval [-2.50, +0.00].

Five validation maps; no policy tuning after screening. No combination tested. Live bot and prior snapshots unchanged. Sandbox CPU verification is separate.


---

## results/20260922-173739-movement-659d1f/holdout/summary.md

SHA-256: `14128d021e214350659a77eae092d62664ced28cc3af35e71ac15bbbb85fae71`

## control_450

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 37-0-3 | 92% | 92% | 80-100% | +436 | 20 | 0 |
| reference_450 | 20-0-20 | 50% | 50% | 50-50% | -0 | 20 | 0 |
| splitter | 32-0-8 | 80% | 80% | 70-90% | +241 | 20 | 0 |
| **overall** | 89-0-31 | 74% | 74% | 68-81% | +183 | 60 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena_728547b8376892d9 | 16-0-8 | 67% | 67% | 24 | 0 |
| default_afc3707a967881d6 | 17-0-7 | 71% | 71% | 24 | 0 |
| default_small_f98ab391cccf33b1 | 17-0-7 | 71% | 71% | 24 | 0 |
| trophy_fd985019831fe135 | 19-0-5 | 79% | 79% | 24 | 0 |
| schooltime_8be7eda86910a849 | 20-0-4 | 83% | 83% | 24 | 0 |

control_450 dragon deaths: hit kelp 3520, hit other body 1699, head-to-head 1686, hit itself 196

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


## trap

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 38-0-2 | 95% | 95% | 88-100% | +512 | 20 | 0 |
| reference_450 | 23-0-17 | 57% | 57% | 40-72% | +53 | 20 | 0 |
| splitter | 34-0-6 | 85% | 85% | 75-95% | +301 | 20 | 0 |
| **overall** | 95-0-25 | 79% | 79% | 72-87% | +232 | 60 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default_small_f98ab391cccf33b1 | 17-0-7 | 71% | 71% | 24 | 0 |
| default_afc3707a967881d6 | 18-0-6 | 75% | 75% | 24 | 0 |
| schooltime_8be7eda86910a849 | 19-0-5 | 79% | 79% | 24 | 0 |
| trophy_fd985019831fe135 | 19-0-5 | 79% | 79% | 24 | 0 |
| arena_728547b8376892d9 | 22-0-2 | 92% | 92% | 24 | 0 |

trap dragon deaths: hit kelp 3179, head-to-head 1651, hit other body 1624, hit itself 214

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


## sprint

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 37-0-3 | 92% | 92% | 80-100% | +436 | 20 | 0 |
| reference_450 | 21-0-19 | 52% | 52% | 45-60% | +17 | 20 | 0 |
| splitter | 30-0-10 | 75% | 75% | 62-88% | +191 | 20 | 0 |
| **overall** | 88-0-32 | 73% | 73% | 66-81% | +176 | 60 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena_728547b8376892d9 | 15-0-9 | 62% | 62% | 24 | 0 |
| default_afc3707a967881d6 | 17-0-7 | 71% | 71% | 24 | 0 |
| default_small_f98ab391cccf33b1 | 17-0-7 | 71% | 71% | 24 | 0 |
| trophy_fd985019831fe135 | 19-0-5 | 79% | 79% | 24 | 0 |
| schooltime_8be7eda86910a849 | 20-0-4 | 83% | 83% | 24 | 0 |

sprint dragon deaths: hit kelp 3247, hit other body 1844, head-to-head 1779, hit itself 242

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).



---

## results/20260922-173739-movement-659d1f/screen/summary.md

SHA-256: `2b469e2042d0b6f5bbabae42ecfd24cfd50c67c4797c97e68880d2d750127fae`

## control_450

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 15-0-1 | 94% | 94% | 81-100% | +470 | 8 | 0 |
| reference_450 | 8-0-8 | 50% | 50% | 50-50% | -0 | 8 | 0 |
| splitter | 12-0-4 | 75% | 75% | 56-94% | +191 | 8 | 0 |
| **overall** | 35-0-13 | 73% | 73% | 62-83% | +172 | 24 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades_6cdb74a7a52d715a | 8-0-4 | 67% | 67% | 12 | 0 |
| Colosseum_3042ccc262f0211a | 9-0-3 | 75% | 75% | 12 | 0 |
| Devil_1b2147f4a8a775d2 | 9-0-3 | 75% | 75% | 12 | 0 |
| big_empty_685baf0e797207b7 | 9-0-3 | 75% | 75% | 12 | 0 |

control_450 dragon deaths: hit other body 1343, head-to-head 945, hit kelp 355, hit itself 294

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for hunter, reference_450, splitter: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


## trap

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 15-0-1 | 94% | 94% | 81-100% | +470 | 8 | 0 |
| reference_450 | 9-0-7 | 56% | 56% | 50-69% | +44 | 8 | 0 |
| splitter | 13-0-3 | 81% | 81% | 62-100% | +255 | 8 | 0 |
| **overall** | 37-0-11 | 77% | 77% | 67-88% | +211 | 24 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades_6cdb74a7a52d715a | 8-0-4 | 67% | 67% | 12 | 0 |
| Colosseum_3042ccc262f0211a | 9-0-3 | 75% | 75% | 12 | 0 |
| Devil_1b2147f4a8a775d2 | 10-0-2 | 83% | 83% | 12 | 0 |
| big_empty_685baf0e797207b7 | 10-0-2 | 83% | 83% | 12 | 0 |

trap dragon deaths: hit other body 1420, head-to-head 1130, hit kelp 394, hit itself 294

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for hunter, reference_450, splitter: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


## sprint

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 15-0-1 | 94% | 94% | 81-100% | +470 | 8 | 0 |
| reference_450 | 9-0-7 | 56% | 56% | 38-75% | +44 | 8 | 0 |
| splitter | 12-0-4 | 75% | 75% | 56-94% | +191 | 8 | 0 |
| **overall** | 36-0-12 | 75% | 75% | 65-88% | +191 | 24 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Colosseum_3042ccc262f0211a | 7-0-5 | 58% | 58% | 12 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 8-0-4 | 67% | 67% | 12 | 0 |
| Devil_1b2147f4a8a775d2 | 10-0-2 | 83% | 83% | 12 | 0 |
| big_empty_685baf0e797207b7 | 11-0-1 | 92% | 92% | 12 | 0 |

sprint dragon deaths: hit other body 1218, head-to-head 978, hit kelp 282, hit itself 266

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for hunter, reference_450, splitter: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.



---

## results/20260922-175423-trap-followup-a1e642/summary.md

SHA-256: `d3e9e5c6a7747bcda25f5b5bb5dabee848ef958cba56a7893269b6ea29464e30`

# Trap transfer follow-up

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| control_450 | 70-0-50 | 58% | 58% | 48-68% | +58 | 60 | 0 |
| **overall** | 70-0-50 | 58% | 58% | 48-68% | +58 | 60 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena_pockets | 6-0-18 | 25% | 25% | 24 | 0 |
| arena_slow_food | 12-0-12 | 50% | 50% | 24 | 0 |
| arena_baffles | 16-0-8 | 67% | 67% | 24 | 0 |
| schooltime | 17-0-7 | 71% | 71% | 24 | 0 |
| arena | 19-0-5 | 79% | 79% | 24 | 0 |

trap dragon deaths: head-to-head 3886, hit kelp 3875, hit other body 3686, hit itself 358

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

Related Arena variants are NOT independent map families. Per-map side-paired scores are exploratory; no live bot is promoted from this test.


---

## results/20260922-232135-guarded-0cb56c/screen/summary.md

SHA-256: `382bea46dd22c62c7bbcf2b7494c9479735a254a8fd5914cbc7ad927082c002a`

# trap

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_450 | 32-0-16 | 67% | 67% | 56-77% | +120 | 24 | 0 |
| **overall** | 32-0-16 | 67% | 67% | 56-77% | +120 | 24 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena_pockets | 1-0-3 | 25% | 25% | 4 | 0 |
| official_Colosseum_3042ccc262f0211a | 2-0-2 | 50% | 50% | 4 | 0 |
| official_default_small_f98ab391cccf33b1 | 2-0-2 | 50% | 50% | 4 | 0 |
| official_queen_of_spades_6cdb74a7a52d715a | 2-0-2 | 50% | 50% | 4 | 0 |
| arena_baffles | 2-0-2 | 50% | 50% | 4 | 0 |
| arena_slow_food | 2-0-2 | 50% | 50% | 4 | 0 |
| official_default_afc3707a967881d6 | 3-0-1 | 75% | 75% | 4 | 0 |
| official_schooltime_8be7eda86910a849 | 3-0-1 | 75% | 75% | 4 | 0 |
| official_Devil_1b2147f4a8a775d2 | 3-0-1 | 75% | 75% | 4 | 0 |
| official_arena_728547b8376892d9 | 4-0-0 | 100% | 100% | 4 | 0 |
| official_big_empty_685baf0e797207b7 | 4-0-0 | 100% | 100% | 4 | 0 |
| official_trophy_fd985019831fe135 | 4-0-0 | 100% | 100% | 4 | 0 |

trap dragon deaths: hit other body 1162, head-to-head 1056, hit kelp 865, hit itself 164

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# head_guard

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_450 | 22-0-26 | 46% | 46% | 31-60% | -29 | 24 | 0 |
| **overall** | 22-0-26 | 46% | 46% | 31-60% | -29 | 24 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| official_default_afc3707a967881d6 | 1-0-3 | 25% | 25% | 4 | 0 |
| official_default_small_f98ab391cccf33b1 | 1-0-3 | 25% | 25% | 4 | 0 |
| official_queen_of_spades_6cdb74a7a52d715a | 1-0-3 | 25% | 25% | 4 | 0 |
| arena_baffles | 1-0-3 | 25% | 25% | 4 | 0 |
| official_arena_728547b8376892d9 | 2-0-2 | 50% | 50% | 4 | 0 |
| official_Colosseum_3042ccc262f0211a | 2-0-2 | 50% | 50% | 4 | 0 |
| official_big_empty_685baf0e797207b7 | 2-0-2 | 50% | 50% | 4 | 0 |
| official_trophy_fd985019831fe135 | 2-0-2 | 50% | 50% | 4 | 0 |
| official_schooltime_8be7eda86910a849 | 2-0-2 | 50% | 50% | 4 | 0 |
| arena_pockets | 2-0-2 | 50% | 50% | 4 | 0 |
| arena_slow_food | 2-0-2 | 50% | 50% | 4 | 0 |
| official_Devil_1b2147f4a8a775d2 | 4-0-0 | 100% | 100% | 4 | 0 |

head_guard dragon deaths: hit other body 1351, head-to-head 1204, hit kelp 1035, hit itself 189

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# tail_guard

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_450 | 28-0-20 | 58% | 58% | 44-73% | +58 | 24 | 0 |
| **overall** | 28-0-20 | 58% | 58% | 44-73% | +58 | 24 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| official_Devil_1b2147f4a8a775d2 | 1-0-3 | 25% | 25% | 4 | 0 |
| arena_baffles | 1-0-3 | 25% | 25% | 4 | 0 |
| arena_slow_food | 1-0-3 | 25% | 25% | 4 | 0 |
| official_arena_728547b8376892d9 | 2-0-2 | 50% | 50% | 4 | 0 |
| official_default_afc3707a967881d6 | 2-0-2 | 50% | 50% | 4 | 0 |
| official_schooltime_8be7eda86910a849 | 2-0-2 | 50% | 50% | 4 | 0 |
| arena_pockets | 2-0-2 | 50% | 50% | 4 | 0 |
| official_Colosseum_3042ccc262f0211a | 3-0-1 | 75% | 75% | 4 | 0 |
| official_default_small_f98ab391cccf33b1 | 3-0-1 | 75% | 75% | 4 | 0 |
| official_trophy_fd985019831fe135 | 3-0-1 | 75% | 75% | 4 | 0 |
| official_queen_of_spades_6cdb74a7a52d715a | 4-0-0 | 100% | 100% | 4 | 0 |
| official_big_empty_685baf0e797207b7 | 4-0-0 | 100% | 100% | 4 | 0 |

tail_guard dragon deaths: hit other body 1334, head-to-head 1217, hit kelp 1030, hit itself 198

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# food_guard

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_450 | 24-0-24 | 50% | 50% | 40-60% | -0 | 24 | 0 |
| **overall** | 24-0-24 | 50% | 50% | 40-60% | -0 | 24 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| official_default_afc3707a967881d6 | 1-0-3 | 25% | 25% | 4 | 0 |
| official_queen_of_spades_6cdb74a7a52d715a | 1-0-3 | 25% | 25% | 4 | 0 |
| arena_baffles | 1-0-3 | 25% | 25% | 4 | 0 |
| official_arena_728547b8376892d9 | 2-0-2 | 50% | 50% | 4 | 0 |
| official_default_small_f98ab391cccf33b1 | 2-0-2 | 50% | 50% | 4 | 0 |
| official_big_empty_685baf0e797207b7 | 2-0-2 | 50% | 50% | 4 | 0 |
| official_schooltime_8be7eda86910a849 | 2-0-2 | 50% | 50% | 4 | 0 |
| official_trophy_fd985019831fe135 | 2-0-2 | 50% | 50% | 4 | 0 |
| official_Devil_1b2147f4a8a775d2 | 2-0-2 | 50% | 50% | 4 | 0 |
| arena_slow_food | 2-0-2 | 50% | 50% | 4 | 0 |
| official_Colosseum_3042ccc262f0211a | 3-0-1 | 75% | 75% | 4 | 0 |
| arena_pockets | 4-0-0 | 100% | 100% | 4 | 0 |

food_guard dragon deaths: hit other body 1350, head-to-head 1183, hit kelp 1073, hit itself 194

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260922-232135-guarded-0cb56c/stress/summary.md

SHA-256: `f6d16e47a6eb825c6d58676b3de44d9afcd90036db66aa63ca2d0cd3b0f7800f`

# tail_guard

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_450 | 31-0-17 | 65% | 65% | 52-77% | +104 | 24 | 0 |
| **overall** | 31-0-17 | 65% | 65% | 52-77% | +104 | 24 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena_pockets | 8-0-8 | 50% | 50% | 16 | 0 |
| arena_slow_food | 9-0-7 | 56% | 56% | 16 | 0 |
| arena_baffles | 14-0-2 | 88% | 88% | 16 | 0 |

tail_guard dragon deaths: hit other body 1258, head-to-head 1056, hit kelp 502, hit itself 120

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260922-232135-guarded-0cb56c/validation/summary.md

SHA-256: `fa6069dc064b3d3d8908e66bb6e38ee50bfd68060029fedc96ad1e97ba6b7a9f`

# control_450

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 135-0-9 | 94% | 94% | 89-97% | +470 | 72 | 0 |
| reference_450 | 72-0-72 | 50% | 50% | 50-50% | -0 | 72 | 0 |
| splitter | 113-0-31 | 78% | 78% | 72-84% | +225 | 72 | 0 |
| **overall** | 320-0-112 | 74% | 74% | 70-78% | +182 | 216 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| official_queen_of_spades_6cdb74a7a52d715a | 31-0-17 | 65% | 65% | 48 | 0 |
| official_arena_728547b8376892d9 | 32-0-16 | 67% | 67% | 48 | 0 |
| official_big_empty_685baf0e797207b7 | 34-0-14 | 71% | 71% | 48 | 0 |
| official_default_afc3707a967881d6 | 34-0-14 | 71% | 71% | 48 | 0 |
| official_default_small_f98ab391cccf33b1 | 36-0-12 | 75% | 75% | 48 | 0 |
| official_Devil_1b2147f4a8a775d2 | 36-0-12 | 75% | 75% | 48 | 0 |
| official_Colosseum_3042ccc262f0211a | 38-0-10 | 79% | 79% | 48 | 0 |
| official_trophy_fd985019831fe135 | 39-0-9 | 81% | 81% | 48 | 0 |
| official_schooltime_8be7eda86910a849 | 40-0-8 | 83% | 83% | 48 | 0 |

control_450 dragon deaths: hit other body 8950, hit kelp 8571, head-to-head 7931, hit itself 1863

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# tail_guard

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 136-0-8 | 94% | 94% | 90-99% | +492 | 72 | 0 |
| reference_450 | 75-0-69 | 52% | 52% | 44-60% | +14 | 72 | 0 |
| splitter | 112-0-32 | 78% | 78% | 71-85% | +218 | 72 | 0 |
| **overall** | 323-0-109 | 75% | 75% | 70-79% | +189 | 216 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| official_arena_728547b8376892d9 | 28-0-20 | 58% | 58% | 48 | 0 |
| official_queen_of_spades_6cdb74a7a52d715a | 28-0-20 | 58% | 58% | 48 | 0 |
| official_big_empty_685baf0e797207b7 | 33-0-15 | 69% | 69% | 48 | 0 |
| official_default_small_f98ab391cccf33b1 | 38-0-10 | 79% | 79% | 48 | 0 |
| official_Colosseum_3042ccc262f0211a | 39-0-9 | 81% | 81% | 48 | 0 |
| official_default_afc3707a967881d6 | 39-0-9 | 81% | 81% | 48 | 0 |
| official_trophy_fd985019831fe135 | 39-0-9 | 81% | 81% | 48 | 0 |
| official_Devil_1b2147f4a8a775d2 | 39-0-9 | 81% | 81% | 48 | 0 |
| official_schooltime_8be7eda86910a849 | 40-0-8 | 83% | 83% | 48 | 0 |

tail_guard dragon deaths: hit other body 9499, head-to-head 8466, hit kelp 8134, hit itself 1836

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260922-232921-fission-5df835/screen/summary.md

SHA-256: `41aa69ff6d6656f2442fd881a2b370b5c289fda7059df059a09e72f4f2157b4e`

# control_450

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_450 | 18-0-18 | 50% | 50% | 50-50% | -0 | 18 | 0 |
| **overall** | 18-0-18 | 50% | 50% | 50-50% | -0 | 18 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena_728547b8376892d9 | 2-0-2 | 50% | 50% | 4 | 0 |
| big_empty_685baf0e797207b7 | 2-0-2 | 50% | 50% | 4 | 0 |
| Colosseum_3042ccc262f0211a | 2-0-2 | 50% | 50% | 4 | 0 |
| default_afc3707a967881d6 | 2-0-2 | 50% | 50% | 4 | 0 |
| default_small_f98ab391cccf33b1 | 2-0-2 | 50% | 50% | 4 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 2-0-2 | 50% | 50% | 4 | 0 |
| schooltime_8be7eda86910a849 | 2-0-2 | 50% | 50% | 4 | 0 |
| trophy_fd985019831fe135 | 2-0-2 | 50% | 50% | 4 | 0 |
| Devil_1b2147f4a8a775d2 | 2-0-2 | 50% | 50% | 4 | 0 |

control_450 dragon deaths: hit other body 977, hit kelp 837, head-to-head 830, hit itself 160

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_450: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# split4

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_450 | 28-0-8 | 78% | 78% | 61-92% | +218 | 18 | 0 |
| **overall** | 28-0-8 | 78% | 78% | 61-92% | +218 | 18 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default_afc3707a967881d6 | 1-0-3 | 25% | 25% | 4 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 1-0-3 | 25% | 25% | 4 | 0 |
| big_empty_685baf0e797207b7 | 2-0-2 | 50% | 50% | 4 | 0 |
| arena_728547b8376892d9 | 4-0-0 | 100% | 100% | 4 | 0 |
| Colosseum_3042ccc262f0211a | 4-0-0 | 100% | 100% | 4 | 0 |
| default_small_f98ab391cccf33b1 | 4-0-0 | 100% | 100% | 4 | 0 |
| schooltime_8be7eda86910a849 | 4-0-0 | 100% | 100% | 4 | 0 |
| trophy_fd985019831fe135 | 4-0-0 | 100% | 100% | 4 | 0 |
| Devil_1b2147f4a8a775d2 | 4-0-0 | 100% | 100% | 4 | 0 |

split4 dragon deaths: head-to-head 3008, hit kelp 2797, hit other body 1532, hit itself 110

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_450: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# split6

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_450 | 26-0-10 | 72% | 72% | 58-86% | +166 | 18 | 0 |
| **overall** | 26-0-10 | 72% | 72% | 58-86% | +166 | 18 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| trophy_fd985019831fe135 | 1-0-3 | 25% | 25% | 4 | 0 |
| default_afc3707a967881d6 | 2-0-2 | 50% | 50% | 4 | 0 |
| default_small_f98ab391cccf33b1 | 2-0-2 | 50% | 50% | 4 | 0 |
| arena_728547b8376892d9 | 3-0-1 | 75% | 75% | 4 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 3-0-1 | 75% | 75% | 4 | 0 |
| schooltime_8be7eda86910a849 | 3-0-1 | 75% | 75% | 4 | 0 |
| big_empty_685baf0e797207b7 | 4-0-0 | 100% | 100% | 4 | 0 |
| Colosseum_3042ccc262f0211a | 4-0-0 | 100% | 100% | 4 | 0 |
| Devil_1b2147f4a8a775d2 | 4-0-0 | 100% | 100% | 4 | 0 |

split6 dragon deaths: head-to-head 1995, hit kelp 1801, hit other body 1400, hit itself 104

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_450: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# split10

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_450 | 11-0-25 | 31% | 31% | 14-50% | -143 | 18 | 0 |
| **overall** | 11-0-25 | 31% | 31% | 14-50% | -143 | 18 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena_728547b8376892d9 | 0-0-4 | 0% | 0% | 4 | 0 |
| big_empty_685baf0e797207b7 | 0-0-4 | 0% | 0% | 4 | 0 |
| trophy_fd985019831fe135 | 0-0-4 | 0% | 0% | 4 | 0 |
| Devil_1b2147f4a8a775d2 | 0-0-4 | 0% | 0% | 4 | 0 |
| default_afc3707a967881d6 | 1-0-3 | 25% | 25% | 4 | 0 |
| default_small_f98ab391cccf33b1 | 1-0-3 | 25% | 25% | 4 | 0 |
| Colosseum_3042ccc262f0211a | 2-0-2 | 50% | 50% | 4 | 0 |
| schooltime_8be7eda86910a849 | 3-0-1 | 75% | 75% | 4 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 4-0-0 | 100% | 100% | 4 | 0 |

split10 dragon deaths: hit other body 551, hit kelp 490, head-to-head 388, hit itself 168

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_450: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# split12

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_450 | 8-0-28 | 22% | 22% | 8-39% | -218 | 18 | 0 |
| **overall** | 8-0-28 | 22% | 22% | 8-39% | -218 | 18 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena_728547b8376892d9 | 0-0-4 | 0% | 0% | 4 | 0 |
| big_empty_685baf0e797207b7 | 0-0-4 | 0% | 0% | 4 | 0 |
| Colosseum_3042ccc262f0211a | 0-0-4 | 0% | 0% | 4 | 0 |
| default_small_f98ab391cccf33b1 | 0-0-4 | 0% | 0% | 4 | 0 |
| Devil_1b2147f4a8a775d2 | 0-0-4 | 0% | 0% | 4 | 0 |
| trophy_fd985019831fe135 | 1-0-3 | 25% | 25% | 4 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 2-0-2 | 50% | 50% | 4 | 0 |
| schooltime_8be7eda86910a849 | 2-0-2 | 50% | 50% | 4 | 0 |
| default_afc3707a967881d6 | 3-0-1 | 75% | 75% | 4 | 0 |

split12 dragon deaths: hit other body 359, hit kelp 237, head-to-head 220, hit itself 157

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_450: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# child2

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_450 | 21-0-15 | 58% | 58% | 44-72% | +58 | 18 | 0 |
| **overall** | 21-0-15 | 58% | 58% | 44-72% | +58 | 18 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| schooltime_8be7eda86910a849 | 1-0-3 | 25% | 25% | 4 | 0 |
| Colosseum_3042ccc262f0211a | 2-0-2 | 50% | 50% | 4 | 0 |
| default_small_f98ab391cccf33b1 | 2-0-2 | 50% | 50% | 4 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 2-0-2 | 50% | 50% | 4 | 0 |
| Devil_1b2147f4a8a775d2 | 2-0-2 | 50% | 50% | 4 | 0 |
| arena_728547b8376892d9 | 3-0-1 | 75% | 75% | 4 | 0 |
| big_empty_685baf0e797207b7 | 3-0-1 | 75% | 75% | 4 | 0 |
| default_afc3707a967881d6 | 3-0-1 | 75% | 75% | 4 | 0 |
| trophy_fd985019831fe135 | 3-0-1 | 75% | 75% | 4 | 0 |

child2 dragon deaths: hit other body 987, hit kelp 911, head-to-head 827, hit itself 205

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_450: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260922-232921-fission-5df835/validation/summary.md

SHA-256: `089f444fa9265f34232086eaf40a77c1b08dea9014fe82e3b90651b9a04d720c`

# control_450

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 136-0-8 | 94% | 94% | 90-98% | +492 | 72 | 0 |
| reference_450 | 72-0-72 | 50% | 50% | 50-50% | -0 | 72 | 0 |
| splitter | 109-0-35 | 76% | 76% | 69-82% | +197 | 72 | 0 |
| **overall** | 317-0-115 | 73% | 73% | 70-77% | +176 | 216 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena_728547b8376892d9 | 31-0-17 | 65% | 65% | 48 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 31-0-17 | 65% | 65% | 48 | 0 |
| Devil_1b2147f4a8a775d2 | 33-0-15 | 69% | 69% | 48 | 0 |
| default_small_f98ab391cccf33b1 | 34-0-14 | 71% | 71% | 48 | 0 |
| big_empty_685baf0e797207b7 | 35-0-13 | 73% | 73% | 48 | 0 |
| default_afc3707a967881d6 | 36-0-12 | 75% | 75% | 48 | 0 |
| Colosseum_3042ccc262f0211a | 38-0-10 | 79% | 79% | 48 | 0 |
| schooltime_8be7eda86910a849 | 39-0-9 | 81% | 81% | 48 | 0 |
| trophy_fd985019831fe135 | 40-0-8 | 83% | 83% | 48 | 0 |

control_450 dragon deaths: hit other body 9050, hit kelp 8230, head-to-head 7947, hit itself 1600

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# split4

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 135-0-9 | 94% | 94% | 90-97% | +470 | 72 | 0 |
| reference_450 | 117-0-27 | 81% | 81% | 74-88% | +255 | 72 | 0 |
| splitter | 134-0-10 | 93% | 93% | 88-97% | +451 | 72 | 0 |
| **overall** | 386-0-46 | 89% | 89% | 86-92% | +370 | 216 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades_6cdb74a7a52d715a | 27-0-21 | 56% | 56% | 48 | 0 |
| default_afc3707a967881d6 | 36-0-12 | 75% | 75% | 48 | 0 |
| big_empty_685baf0e797207b7 | 39-0-9 | 81% | 81% | 48 | 0 |
| trophy_fd985019831fe135 | 46-0-2 | 96% | 96% | 48 | 0 |
| default_small_f98ab391cccf33b1 | 47-0-1 | 98% | 98% | 48 | 0 |
| schooltime_8be7eda86910a849 | 47-0-1 | 98% | 98% | 48 | 0 |
| arena_728547b8376892d9 | 48-0-0 | 100% | 100% | 48 | 0 |
| Colosseum_3042ccc262f0211a | 48-0-0 | 100% | 100% | 48 | 0 |
| Devil_1b2147f4a8a775d2 | 48-0-0 | 100% | 100% | 48 | 0 |

split4 dragon deaths: hit kelp 28230, head-to-head 27986, hit other body 14866, hit itself 1384

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260922-233553-corpus-strategy-3d71b9/summary.md

SHA-256: `b0ad6e0c721846fc65ead9aad1c3bcf4c23232ac8778e423dddd32adecadea27`

# Downloaded strong-player strategy audit

Twelve highest-minimum-recorded-Elo complete battles with distinct submission pairs. Observational, selection-biased, possibly repeated policies; not independent policy tests or causal evidence that frequent actions are good. No private source code accessed.

| Team / submission | Games | Splits | Common split lengths | Common child sizes | Late splits | Sprint share |
|---|---:|---:|---|---|---:|---:|
| Stockfish (206:2057) | 5 | 766 | [(4, 333), (5, 82), (6, 45)] | [(2, 404), (3, 39), (7, 30)] | 67 | 0.54% |
| Sponge(Albert and Bob) (213:1747) | 20 | 3152 | [(4, 1842), (5, 265), (6, 212)] | [(2, 2030), (3, 260), (4, 210)] | 258 | 0.33% |
| Sponge(Albert and Bob) (213:1983) | 20 | 3582 | [(4, 2383), (5, 263), (6, 191)] | [(2, 2550), (3, 256), (4, 182)] | 232 | 0.37% |
| PPP (27:1920) | 15 | 3878 | [(4, 2992), (5, 227), (6, 158)] | [(2, 3878)] | 213 | 0.00% |
| SHINK AI 6500 (280:1744) | 15 | 2456 | [(4, 1687), (5, 211), (6, 142)] | [(2, 1769), (3, 198), (4, 145)] | 174 | 0.89% |
| dev test 1 :P (545:1302) | 15 | 2745 | [(4, 2242), (5, 130), (6, 93)] | [(2, 2554), (3, 37), (4, 31)] | 130 | 0.49% |
| dev test 1 :P (545:2050) | 5 | 1297 | [(4, 1210), (5, 33), (6, 22)] | [(2, 1254), (3, 20), (4, 12)] | 65 | 0.13% |
| cheji bt (70:1717) | 20 | 2959 | [(4, 1953), (5, 375), (6, 196)] | [(2, 2174), (3, 274), (4, 128)] | 263 | 0.20% |
| SSS (91:712) | 5 | 817 | [(4, 625), (6, 20), (5, 20)] | [(2, 625), (4, 20), (3, 20)] | 43 | 1.82% |


---

## results/20260922-234132-corpus-strategy-de8cf0/summary.md

SHA-256: `b0ad6e0c721846fc65ead9aad1c3bcf4c23232ac8778e423dddd32adecadea27`

# Downloaded strong-player strategy audit

Twelve highest-minimum-recorded-Elo complete battles with distinct submission pairs. Observational, selection-biased, possibly repeated policies; not independent policy tests or causal evidence that frequent actions are good. No private source code accessed.

| Team / submission | Games | Splits | Common split lengths | Common child sizes | Late splits | Sprint share |
|---|---:|---:|---|---|---:|---:|
| Stockfish (206:2057) | 5 | 766 | [(4, 333), (5, 82), (6, 45)] | [(2, 404), (3, 39), (7, 30)] | 67 | 0.54% |
| Sponge(Albert and Bob) (213:1747) | 20 | 3152 | [(4, 1842), (5, 265), (6, 212)] | [(2, 2030), (3, 260), (4, 210)] | 258 | 0.33% |
| Sponge(Albert and Bob) (213:1983) | 20 | 3582 | [(4, 2383), (5, 263), (6, 191)] | [(2, 2550), (3, 256), (4, 182)] | 232 | 0.37% |
| PPP (27:1920) | 15 | 3878 | [(4, 2992), (5, 227), (6, 158)] | [(2, 3878)] | 213 | 0.00% |
| SHINK AI 6500 (280:1744) | 15 | 2456 | [(4, 1687), (5, 211), (6, 142)] | [(2, 1769), (3, 198), (4, 145)] | 174 | 0.89% |
| dev test 1 :P (545:1302) | 15 | 2745 | [(4, 2242), (5, 130), (6, 93)] | [(2, 2554), (3, 37), (4, 31)] | 130 | 0.49% |
| dev test 1 :P (545:2050) | 5 | 1297 | [(4, 1210), (5, 33), (6, 22)] | [(2, 1254), (3, 20), (4, 12)] | 65 | 0.13% |
| cheji bt (70:1717) | 20 | 2959 | [(4, 1953), (5, 375), (6, 196)] | [(2, 2174), (3, 274), (4, 128)] | 263 | 0.20% |
| SSS (91:712) | 5 | 817 | [(4, 625), (6, 20), (5, 20)] | [(2, 625), (4, 20), (3, 20)] | 43 | 1.82% |


---

## results/20260922-235151-novel-maps-db3a9c/transfer/summary.md

SHA-256: `6e45f69ebcb5310a49996ec2e3addd7d3d838e9307e09bb3f471a07a99fd72d8`

# split4

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_450 | 124-0-4 | 97% | 97% | 94-99% | +597 | 64 | 0 |
| **overall** | 124-0-4 | 97% | 97% | 94-99% | +597 | 64 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| open_large | 13-0-3 | 81% | 81% | 16 | 0 |
| scarce_large | 15-0-1 | 94% | 94% | 16 | 0 |
| open_small | 16-0-0 | 100% | 100% | 16 | 0 |
| baffles_small | 16-0-0 | 100% | 100% | 16 | 0 |
| baffles_large | 16-0-0 | 100% | 100% | 16 | 0 |
| dense_small | 16-0-0 | 100% | 100% | 16 | 0 |
| dense_large | 16-0-0 | 100% | 100% | 16 | 0 |
| scarce_small | 16-0-0 | 100% | 100% | 16 | 0 |

split4 dragon deaths: head-to-head 22298, hit other body 14914, hit kelp 8504, hit itself 426

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260923-084317-growers-5ac330/screen/summary.md

SHA-256: `647b96b8ef03246920fcd597da50c16f376f2edb31ce9f5beb6466848b79aac9`

# control_450

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 18-0-18 | 50% | 50% | 50-50% | -0 | 18 | 0 |
| **overall** | 18-0-18 | 50% | 50% | 50-50% | -0 | 18 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena_728547b8376892d9 | 2-0-2 | 50% | 50% | 4 | 0 |
| Colosseum_3042ccc262f0211a | 2-0-2 | 50% | 50% | 4 | 0 |
| default_afc3707a967881d6 | 2-0-2 | 50% | 50% | 4 | 0 |
| big_empty_685baf0e797207b7 | 2-0-2 | 50% | 50% | 4 | 0 |
| default_small_f98ab391cccf33b1 | 2-0-2 | 50% | 50% | 4 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 2-0-2 | 50% | 50% | 4 | 0 |
| trophy_fd985019831fe135 | 2-0-2 | 50% | 50% | 4 | 0 |
| schooltime_8be7eda86910a849 | 2-0-2 | 50% | 50% | 4 | 0 |
| Devil_1b2147f4a8a775d2 | 2-0-2 | 50% | 50% | 4 | 0 |

control_450 dragon deaths: head-to-head 3148, hit kelp 2195, hit other body 1548, hit itself 80

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v2: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# stop425

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 13-1-22 | 36% | 38% | 26-49% | -89 | 18 | 0 |
| **overall** | 13-1-22 | 36% | 38% | 26-49% | -89 | 18 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena_728547b8376892d9 | 0-0-4 | 0% | 0% | 4 | 0 |
| schooltime_8be7eda86910a849 | 0-0-4 | 0% | 0% | 4 | 0 |
| Devil_1b2147f4a8a775d2 | 1-0-3 | 25% | 25% | 4 | 0 |
| default_afc3707a967881d6 | 2-0-2 | 50% | 50% | 4 | 0 |
| big_empty_685baf0e797207b7 | 2-0-2 | 50% | 50% | 4 | 0 |
| default_small_f98ab391cccf33b1 | 2-0-2 | 50% | 50% | 4 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 2-0-2 | 50% | 50% | 4 | 0 |
| trophy_fd985019831fe135 | 2-0-2 | 50% | 50% | 4 | 0 |
| Colosseum_3042ccc262f0211a | 2-1-1 | 50% | 62% | 4 | 0 |

stop425 dragon deaths: head-to-head 2995, hit kelp 2075, hit other body 1468, hit itself 85

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v2: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# stop400

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 15-0-21 | 42% | 42% | 25-58% | -58 | 18 | 0 |
| **overall** | 15-0-21 | 42% | 42% | 25-58% | -58 | 18 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena_728547b8376892d9 | 0-0-4 | 0% | 0% | 4 | 0 |
| trophy_fd985019831fe135 | 0-0-4 | 0% | 0% | 4 | 0 |
| default_small_f98ab391cccf33b1 | 1-0-3 | 25% | 25% | 4 | 0 |
| schooltime_8be7eda86910a849 | 1-0-3 | 25% | 25% | 4 | 0 |
| Devil_1b2147f4a8a775d2 | 1-0-3 | 25% | 25% | 4 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 2-0-2 | 50% | 50% | 4 | 0 |
| Colosseum_3042ccc262f0211a | 3-0-1 | 75% | 75% | 4 | 0 |
| default_afc3707a967881d6 | 3-0-1 | 75% | 75% | 4 | 0 |
| big_empty_685baf0e797207b7 | 4-0-0 | 100% | 100% | 4 | 0 |

stop400 dragon deaths: head-to-head 2824, hit kelp 1943, hit other body 1400, hit itself 82

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v2: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# stop350

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 14-0-22 | 39% | 39% | 28-50% | -79 | 18 | 0 |
| **overall** | 14-0-22 | 39% | 39% | 28-50% | -79 | 18 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena_728547b8376892d9 | 0-0-4 | 0% | 0% | 4 | 0 |
| big_empty_685baf0e797207b7 | 1-0-3 | 25% | 25% | 4 | 0 |
| trophy_fd985019831fe135 | 1-0-3 | 25% | 25% | 4 | 0 |
| Devil_1b2147f4a8a775d2 | 1-0-3 | 25% | 25% | 4 | 0 |
| Colosseum_3042ccc262f0211a | 2-0-2 | 50% | 50% | 4 | 0 |
| default_small_f98ab391cccf33b1 | 2-0-2 | 50% | 50% | 4 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 2-0-2 | 50% | 50% | 4 | 0 |
| schooltime_8be7eda86910a849 | 2-0-2 | 50% | 50% | 4 | 0 |
| default_afc3707a967881d6 | 3-0-1 | 75% | 75% | 4 | 0 |

stop350 dragon deaths: head-to-head 2440, hit kelp 1691, hit other body 1208, hit itself 112

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v2: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# quarter350

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 21-0-15 | 58% | 58% | 44-72% | +58 | 18 | 0 |
| **overall** | 21-0-15 | 58% | 58% | 44-72% | +58 | 18 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| schooltime_8be7eda86910a849 | 1-0-3 | 25% | 25% | 4 | 0 |
| default_small_f98ab391cccf33b1 | 2-0-2 | 50% | 50% | 4 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 2-0-2 | 50% | 50% | 4 | 0 |
| trophy_fd985019831fe135 | 2-0-2 | 50% | 50% | 4 | 0 |
| Devil_1b2147f4a8a775d2 | 2-0-2 | 50% | 50% | 4 | 0 |
| arena_728547b8376892d9 | 3-0-1 | 75% | 75% | 4 | 0 |
| Colosseum_3042ccc262f0211a | 3-0-1 | 75% | 75% | 4 | 0 |
| default_afc3707a967881d6 | 3-0-1 | 75% | 75% | 4 | 0 |
| big_empty_685baf0e797207b7 | 3-0-1 | 75% | 75% | 4 | 0 |

quarter350 dragon deaths: head-to-head 2972, hit kelp 2055, hit other body 1474, hit itself 77

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v2: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# quarter400

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 17-0-19 | 47% | 47% | 33-61% | -19 | 18 | 0 |
| **overall** | 17-0-19 | 47% | 47% | 33-61% | -19 | 18 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| schooltime_8be7eda86910a849 | 0-0-4 | 0% | 0% | 4 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 1-0-3 | 25% | 25% | 4 | 0 |
| arena_728547b8376892d9 | 2-0-2 | 50% | 50% | 4 | 0 |
| Colosseum_3042ccc262f0211a | 2-0-2 | 50% | 50% | 4 | 0 |
| default_small_f98ab391cccf33b1 | 2-0-2 | 50% | 50% | 4 | 0 |
| trophy_fd985019831fe135 | 2-0-2 | 50% | 50% | 4 | 0 |
| Devil_1b2147f4a8a775d2 | 2-0-2 | 50% | 50% | 4 | 0 |
| default_afc3707a967881d6 | 3-0-1 | 75% | 75% | 4 | 0 |
| big_empty_685baf0e797207b7 | 3-0-1 | 75% | 75% | 4 | 0 |

quarter400 dragon deaths: head-to-head 3132, hit kelp 2170, hit other body 1574, hit itself 87

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v2: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260923-084317-growers-5ac330/validation/summary.md

SHA-256: `bdf46a7233b0f98da15e28c47c6948f91b6b3db8fa1ef9fe1692c661084f8b83`

# control_450

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 137-0-7 | 95% | 95% | 92-98% | +517 | 72 | 0 |
| reference_v2 | 72-0-72 | 50% | 50% | 50-50% | -0 | 72 | 0 |
| splitter | 134-0-10 | 93% | 93% | 88-97% | +451 | 72 | 0 |
| **overall** | 343-0-89 | 79% | 79% | 76-83% | +234 | 216 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades_6cdb74a7a52d715a | 31-0-17 | 65% | 65% | 48 | 0 |
| default_afc3707a967881d6 | 34-0-14 | 71% | 71% | 48 | 0 |
| big_empty_685baf0e797207b7 | 39-0-9 | 81% | 81% | 48 | 0 |
| trophy_fd985019831fe135 | 39-0-9 | 81% | 81% | 48 | 0 |
| arena_728547b8376892d9 | 40-0-8 | 83% | 83% | 48 | 0 |
| Colosseum_3042ccc262f0211a | 40-0-8 | 83% | 83% | 48 | 0 |
| default_small_f98ab391cccf33b1 | 40-0-8 | 83% | 83% | 48 | 0 |
| schooltime_8be7eda86910a849 | 40-0-8 | 83% | 83% | 48 | 0 |
| Devil_1b2147f4a8a775d2 | 40-0-8 | 83% | 83% | 48 | 0 |

control_450 dragon deaths: head-to-head 28096, hit kelp 25704, hit other body 14686, hit itself 1120

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# quarter350

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 137-0-7 | 95% | 95% | 92-98% | +517 | 72 | 0 |
| reference_v2 | 74-0-70 | 51% | 51% | 44-59% | +10 | 72 | 0 |
| splitter | 136-0-8 | 94% | 94% | 90-98% | +492 | 72 | 0 |
| **overall** | 347-0-85 | 80% | 80% | 76-84% | +244 | 216 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades_6cdb74a7a52d715a | 34-0-14 | 71% | 71% | 48 | 0 |
| default_afc3707a967881d6 | 36-0-12 | 75% | 75% | 48 | 0 |
| default_small_f98ab391cccf33b1 | 36-0-12 | 75% | 75% | 48 | 0 |
| schooltime_8be7eda86910a849 | 37-0-11 | 77% | 77% | 48 | 0 |
| Devil_1b2147f4a8a775d2 | 38-0-10 | 79% | 79% | 48 | 0 |
| Colosseum_3042ccc262f0211a | 41-0-7 | 85% | 85% | 48 | 0 |
| trophy_fd985019831fe135 | 41-0-7 | 85% | 85% | 48 | 0 |
| arena_728547b8376892d9 | 42-0-6 | 88% | 88% | 48 | 0 |
| big_empty_685baf0e797207b7 | 42-0-6 | 88% | 88% | 48 | 0 |

quarter350 dragon deaths: head-to-head 26919, hit kelp 24934, hit other body 14572, hit itself 1141

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260923-085446-portal-9297e0/validation/summary.md

SHA-256: `472e44392587c5ffedd1b09edb0f60fd78d5d5e79c5269568a23185118bf996b`

# portal_escape

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 131-0-109 | 55% | 55% | 49-60% | +32 | 120 | 0 |
| **overall** | 131-0-109 | 55% | 55% | 49-60% | +32 | 120 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| trophy_fd985019831fe135 | 22-0-26 | 46% | 46% | 48 | 0 |
| schooltime_8be7eda86910a849 | 24-0-24 | 50% | 50% | 48 | 0 |
| default_afc3707a967881d6 | 27-0-21 | 56% | 56% | 48 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 28-0-20 | 58% | 58% | 48 | 0 |
| Colosseum_3042ccc262f0211a | 30-0-18 | 62% | 62% | 48 | 0 |

portal_escape dragon deaths: hit kelp 19140, head-to-head 13972, hit other body 6657, hit itself 92

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260923-091759-portal-followup-206dc9/transfer/summary.md

SHA-256: `34f22e7c0b9231ddf8c5fbf9aa97b03b4ede23783e10d6b96df33121afbd995f`

# portal_escape

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 172-1-83 | 67% | 67% | 62-73% | +126 | 128 | 0 |
| **overall** | 172-1-83 | 67% | 67% | 62-73% | +126 | 128 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| new_open_large | 17-0-15 | 53% | 53% | 32 | 0 |
| new_baffles_large | 20-0-12 | 62% | 62% | 32 | 0 |
| new_dense_small | 21-0-11 | 66% | 66% | 32 | 0 |
| new_dense_large | 22-0-10 | 69% | 69% | 32 | 0 |
| new_scarce_small | 22-0-10 | 69% | 69% | 32 | 0 |
| new_open_small | 22-1-9 | 69% | 70% | 32 | 0 |
| new_baffles_small | 24-0-8 | 75% | 75% | 32 | 0 |
| new_scarce_large | 24-0-8 | 75% | 75% | 32 | 0 |

portal_escape dragon deaths: head-to-head 93639, hit kelp 60630, hit other body 55027, hit itself 3903

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260923-091759-portal-followup-206dc9/validation/summary.md

SHA-256: `060e5127e9ea12428a2c6a22996f88526db529122e1a07d1f84c353531627e87`

# control_450

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 277-0-11 | 96% | 96% | 93-98% | +560 | 144 | 0 |
| reference_v2 | 143-2-143 | 50% | 50% | 50-50% | -0 | 144 | 0 |
| splitter | 264-1-23 | 92% | 92% | 88-95% | +421 | 144 | 0 |
| **overall** | 684-3-177 | 79% | 79% | 77-82% | +234 | 432 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| official_queen_of_spades_6cdb74a7a52d715a | 61-1-34 | 64% | 64% | 96 | 0 |
| official_big_empty_685baf0e797207b7 | 72-0-24 | 75% | 75% | 96 | 0 |
| official_default_afc3707a967881d6 | 72-0-24 | 75% | 75% | 96 | 0 |
| official_arena_728547b8376892d9 | 80-0-16 | 83% | 83% | 96 | 0 |
| official_Colosseum_3042ccc262f0211a | 80-0-16 | 83% | 83% | 96 | 0 |
| official_default_small_f98ab391cccf33b1 | 79-2-15 | 82% | 83% | 96 | 0 |
| official_schooltime_8be7eda86910a849 | 80-0-16 | 83% | 83% | 96 | 0 |
| official_trophy_fd985019831fe135 | 80-0-16 | 83% | 83% | 96 | 0 |
| official_Devil_1b2147f4a8a775d2 | 80-0-16 | 83% | 83% | 96 | 0 |

control_450 dragon deaths: head-to-head 55983, hit kelp 51318, hit other body 28904, hit itself 2290

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# portal_escape

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 274-0-14 | 95% | 95% | 92-98% | +517 | 144 | 0 |
| reference_v2 | 148-2-138 | 51% | 52% | 48-56% | +12 | 144 | 0 |
| splitter | 270-0-18 | 94% | 94% | 90-97% | +470 | 144 | 0 |
| **overall** | 692-2-170 | 80% | 80% | 77-83% | +243 | 432 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| official_queen_of_spades_6cdb74a7a52d715a | 62-0-34 | 65% | 65% | 96 | 0 |
| official_big_empty_685baf0e797207b7 | 72-0-24 | 75% | 75% | 96 | 0 |
| official_default_afc3707a967881d6 | 78-0-18 | 81% | 81% | 96 | 0 |
| official_schooltime_8be7eda86910a849 | 78-0-18 | 81% | 81% | 96 | 0 |
| official_arena_728547b8376892d9 | 80-0-16 | 83% | 83% | 96 | 0 |
| official_default_small_f98ab391cccf33b1 | 79-2-15 | 82% | 83% | 96 | 0 |
| official_Devil_1b2147f4a8a775d2 | 80-0-16 | 83% | 83% | 96 | 0 |
| official_Colosseum_3042ccc262f0211a | 81-0-15 | 84% | 84% | 96 | 0 |
| official_trophy_fd985019831fe135 | 82-0-14 | 85% | 85% | 96 | 0 |

portal_escape dragon deaths: head-to-head 55679, hit kelp 51362, hit other body 28698, hit itself 2345

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260923-140427-navigation-6e47f4/screen/summary.md

SHA-256: `f05fe1234b52f2a9281504a609c569c073a2d6b3c7e6d74e58c68b6783d48130`

# control_450

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 36-0-36 | 50% | 50% | 50-50% | -0 | 36 | 0 |
| **overall** | 36-0-36 | 50% | 50% | 50-50% | -0 | 36 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena_728547b8376892d9 | 4-0-4 | 50% | 50% | 8 | 0 |
| big_empty_685baf0e797207b7 | 4-0-4 | 50% | 50% | 8 | 0 |
| Colosseum_3042ccc262f0211a | 4-0-4 | 50% | 50% | 8 | 0 |
| default_afc3707a967881d6 | 4-0-4 | 50% | 50% | 8 | 0 |
| default_small_f98ab391cccf33b1 | 4-0-4 | 50% | 50% | 8 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 4-0-4 | 50% | 50% | 8 | 0 |
| schooltime_8be7eda86910a849 | 4-0-4 | 50% | 50% | 8 | 0 |
| trophy_fd985019831fe135 | 4-0-4 | 50% | 50% | 8 | 0 |
| Devil_1b2147f4a8a775d2 | 4-0-4 | 50% | 50% | 8 | 0 |

control_450 dragon deaths: head-to-head 5886, hit kelp 4345, hit other body 2870, hit itself 143

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# terrain_memory

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 39-1-32 | 54% | 55% | 45-65% | +34 | 36 | 0 |
| **overall** | 39-1-32 | 54% | 55% | 45-65% | +34 | 36 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| trophy_fd985019831fe135 | 2-0-6 | 25% | 25% | 8 | 0 |
| default_small_f98ab391cccf33b1 | 3-0-5 | 38% | 38% | 8 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 3-1-4 | 38% | 44% | 8 | 0 |
| Devil_1b2147f4a8a775d2 | 4-0-4 | 50% | 50% | 8 | 0 |
| Colosseum_3042ccc262f0211a | 5-0-3 | 62% | 62% | 8 | 0 |
| default_afc3707a967881d6 | 5-0-3 | 62% | 62% | 8 | 0 |
| schooltime_8be7eda86910a849 | 5-0-3 | 62% | 62% | 8 | 0 |
| arena_728547b8376892d9 | 6-0-2 | 75% | 75% | 8 | 0 |
| big_empty_685baf0e797207b7 | 6-0-2 | 75% | 75% | 8 | 0 |

terrain_memory dragon deaths: head-to-head 6441, hit kelp 3966, hit other body 2664, hit itself 165

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# portal_memory

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 40-0-32 | 56% | 56% | 43-68% | +39 | 36 | 0 |
| **overall** | 40-0-32 | 56% | 56% | 43-68% | +39 | 36 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades_6cdb74a7a52d715a | 1-0-7 | 12% | 12% | 8 | 0 |
| Colosseum_3042ccc262f0211a | 3-0-5 | 38% | 38% | 8 | 0 |
| default_small_f98ab391cccf33b1 | 3-0-5 | 38% | 38% | 8 | 0 |
| schooltime_8be7eda86910a849 | 4-0-4 | 50% | 50% | 8 | 0 |
| Devil_1b2147f4a8a775d2 | 4-0-4 | 50% | 50% | 8 | 0 |
| trophy_fd985019831fe135 | 5-0-3 | 62% | 62% | 8 | 0 |
| arena_728547b8376892d9 | 6-0-2 | 75% | 75% | 8 | 0 |
| big_empty_685baf0e797207b7 | 6-0-2 | 75% | 75% | 8 | 0 |
| default_afc3707a967881d6 | 8-0-0 | 100% | 100% | 8 | 0 |

portal_memory dragon deaths: head-to-head 6670, hit kelp 4819, hit other body 2919, hit itself 169

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260923-140427-navigation-6e47f4/validation/summary.md

SHA-256: `b10a73ce24084be7415cec260262a4dc946bd2492bf0f03c99eb3b74bb2e9971`

# control_450

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 140-0-4 | 97% | 97% | 94-99% | +618 | 72 | 0 |
| reference_v2 | 72-0-72 | 50% | 50% | 50-50% | -0 | 72 | 0 |
| splitter | 131-0-13 | 91% | 91% | 86-95% | +401 | 72 | 0 |
| **overall** | 343-0-89 | 79% | 79% | 76-83% | +234 | 216 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades_6cdb74a7a52d715a | 33-0-15 | 69% | 69% | 48 | 0 |
| big_empty_685baf0e797207b7 | 35-0-13 | 73% | 73% | 48 | 0 |
| default_afc3707a967881d6 | 36-0-12 | 75% | 75% | 48 | 0 |
| schooltime_8be7eda86910a849 | 39-0-9 | 81% | 81% | 48 | 0 |
| arena_728547b8376892d9 | 40-0-8 | 83% | 83% | 48 | 0 |
| Colosseum_3042ccc262f0211a | 40-0-8 | 83% | 83% | 48 | 0 |
| default_small_f98ab391cccf33b1 | 40-0-8 | 83% | 83% | 48 | 0 |
| trophy_fd985019831fe135 | 40-0-8 | 83% | 83% | 48 | 0 |
| Devil_1b2147f4a8a775d2 | 40-0-8 | 83% | 83% | 48 | 0 |

control_450 dragon deaths: head-to-head 27999, hit kelp 24063, hit other body 14411, hit itself 1129

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# portal_memory

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 132-0-12 | 92% | 92% | 85-97% | +417 | 72 | 0 |
| reference_v2 | 70-2-72 | 49% | 49% | 41-58% | -5 | 72 | 0 |
| splitter | 140-0-4 | 97% | 97% | 94-99% | +618 | 72 | 0 |
| **overall** | 342-2-88 | 79% | 79% | 75-84% | +234 | 216 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades_6cdb74a7a52d715a | 18-1-29 | 38% | 39% | 48 | 0 |
| schooltime_8be7eda86910a849 | 37-0-11 | 77% | 77% | 48 | 0 |
| default_small_f98ab391cccf33b1 | 38-0-10 | 79% | 79% | 48 | 0 |
| trophy_fd985019831fe135 | 38-0-10 | 79% | 79% | 48 | 0 |
| big_empty_685baf0e797207b7 | 40-0-8 | 83% | 83% | 48 | 0 |
| Colosseum_3042ccc262f0211a | 40-0-8 | 83% | 83% | 48 | 0 |
| arena_728547b8376892d9 | 40-1-7 | 83% | 84% | 48 | 0 |
| Devil_1b2147f4a8a775d2 | 43-0-5 | 90% | 90% | 48 | 0 |
| default_afc3707a967881d6 | 48-0-0 | 100% | 100% | 48 | 0 |

portal_memory dragon deaths: head-to-head 30482, hit kelp 28349, hit other body 14278, hit itself 1163

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260923-231438-hybrid-b0801d/evaluators-screen/summary.md

SHA-256: `be0897264aae5be64aa91b10e584472fead06a0b9023114c8bded18701234b1b`

# control_450

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 44-0-44 | 50% | 50% | 50-50% | -0 | 44 | 0 |
| **overall** | 44-0-44 | 50% | 50% | 50-50% | -0 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena_728547b8376892d9 | 4-0-4 | 50% | 50% | 8 | 0 |
| big_empty_685baf0e797207b7 | 4-0-4 | 50% | 50% | 8 | 0 |
| Colosseum_3042ccc262f0211a | 4-0-4 | 50% | 50% | 8 | 0 |
| default_afc3707a967881d6 | 4-0-4 | 50% | 50% | 8 | 0 |
| default_small_f98ab391cccf33b1 | 4-0-4 | 50% | 50% | 8 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 4-0-4 | 50% | 50% | 8 | 0 |
| schooltime_8be7eda86910a849 | 4-0-4 | 50% | 50% | 8 | 0 |
| trophy_fd985019831fe135 | 4-0-4 | 50% | 50% | 8 | 0 |
| Devil_1b2147f4a8a775d2 | 4-0-4 | 50% | 50% | 8 | 0 |
| stronghold_fb60e37176a8d1d3 | 4-0-4 | 50% | 50% | 8 | 0 |
| Trauma_d014b28abbd1abb0 | 4-0-4 | 50% | 50% | 8 | 0 |

control_450 dragon deaths: head-to-head 6940, hit kelp 5056, hit other body 3483, hit itself 150

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# heuristic

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 63-0-25 | 72% | 72% | 61-82% | +161 | 44 | 0 |
| **overall** | 63-0-25 | 72% | 72% | 61-82% | +161 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold_fb60e37176a8d1d3 | 1-0-7 | 12% | 12% | 8 | 0 |
| default_afc3707a967881d6 | 2-0-6 | 25% | 25% | 8 | 0 |
| schooltime_8be7eda86910a849 | 5-0-3 | 62% | 62% | 8 | 0 |
| big_empty_685baf0e797207b7 | 6-0-2 | 75% | 75% | 8 | 0 |
| Trauma_d014b28abbd1abb0 | 6-0-2 | 75% | 75% | 8 | 0 |
| arena_728547b8376892d9 | 7-0-1 | 88% | 88% | 8 | 0 |
| default_small_f98ab391cccf33b1 | 7-0-1 | 88% | 88% | 8 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 7-0-1 | 88% | 88% | 8 | 0 |
| trophy_fd985019831fe135 | 7-0-1 | 88% | 88% | 8 | 0 |
| Devil_1b2147f4a8a775d2 | 7-0-1 | 88% | 88% | 8 | 0 |
| Colosseum_3042ccc262f0211a | 8-0-0 | 100% | 100% | 8 | 0 |

heuristic dragon deaths: head-to-head 7786, hit kelp 4150, hit other body 3609, hit itself 258

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# linear

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 67-0-21 | 76% | 76% | 66-85% | +202 | 44 | 0 |
| **overall** | 67-0-21 | 76% | 76% | 66-85% | +202 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default_afc3707a967881d6 | 2-0-6 | 25% | 25% | 8 | 0 |
| stronghold_fb60e37176a8d1d3 | 3-0-5 | 38% | 38% | 8 | 0 |
| default_small_f98ab391cccf33b1 | 5-0-3 | 62% | 62% | 8 | 0 |
| schooltime_8be7eda86910a849 | 5-0-3 | 62% | 62% | 8 | 0 |
| trophy_fd985019831fe135 | 6-0-2 | 75% | 75% | 8 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 7-0-1 | 88% | 88% | 8 | 0 |
| Trauma_d014b28abbd1abb0 | 7-0-1 | 88% | 88% | 8 | 0 |
| arena_728547b8376892d9 | 8-0-0 | 100% | 100% | 8 | 0 |
| big_empty_685baf0e797207b7 | 8-0-0 | 100% | 100% | 8 | 0 |
| Colosseum_3042ccc262f0211a | 8-0-0 | 100% | 100% | 8 | 0 |
| Devil_1b2147f4a8a775d2 | 8-0-0 | 100% | 100% | 8 | 0 |

linear dragon deaths: head-to-head 7806, hit kelp 5402, hit other body 3686, hit itself 233

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# neural

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 63-0-25 | 72% | 72% | 61-82% | +161 | 44 | 0 |
| **overall** | 63-0-25 | 72% | 72% | 61-82% | +161 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| schooltime_8be7eda86910a849 | 3-0-5 | 38% | 38% | 8 | 0 |
| default_afc3707a967881d6 | 4-0-4 | 50% | 50% | 8 | 0 |
| Trauma_d014b28abbd1abb0 | 4-0-4 | 50% | 50% | 8 | 0 |
| big_empty_685baf0e797207b7 | 6-0-2 | 75% | 75% | 8 | 0 |
| default_small_f98ab391cccf33b1 | 6-0-2 | 75% | 75% | 8 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 6-0-2 | 75% | 75% | 8 | 0 |
| trophy_fd985019831fe135 | 6-0-2 | 75% | 75% | 8 | 0 |
| stronghold_fb60e37176a8d1d3 | 6-0-2 | 75% | 75% | 8 | 0 |
| arena_728547b8376892d9 | 7-0-1 | 88% | 88% | 8 | 0 |
| Colosseum_3042ccc262f0211a | 7-0-1 | 88% | 88% | 8 | 0 |
| Devil_1b2147f4a8a775d2 | 8-0-0 | 100% | 100% | 8 | 0 |

neural dragon deaths: head-to-head 6598, hit kelp 4791, hit other body 3477, hit itself 216

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260923-231438-hybrid-b0801d/roles-screen/summary.md

SHA-256: `5066fa7160cffb923f0e9b35a4e69ea4c955e51bef963d744f3b38af0b4dae3b`

# control_450

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 44-0-44 | 50% | 50% | 50-50% | -0 | 44 | 0 |
| **overall** | 44-0-44 | 50% | 50% | 50-50% | -0 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena_728547b8376892d9 | 4-0-4 | 50% | 50% | 8 | 0 |
| big_empty_685baf0e797207b7 | 4-0-4 | 50% | 50% | 8 | 0 |
| Colosseum_3042ccc262f0211a | 4-0-4 | 50% | 50% | 8 | 0 |
| default_afc3707a967881d6 | 4-0-4 | 50% | 50% | 8 | 0 |
| default_small_f98ab391cccf33b1 | 4-0-4 | 50% | 50% | 8 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 4-0-4 | 50% | 50% | 8 | 0 |
| schooltime_8be7eda86910a849 | 4-0-4 | 50% | 50% | 8 | 0 |
| trophy_fd985019831fe135 | 4-0-4 | 50% | 50% | 8 | 0 |
| Devil_1b2147f4a8a775d2 | 4-0-4 | 50% | 50% | 8 | 0 |
| stronghold_fb60e37176a8d1d3 | 4-0-4 | 50% | 50% | 8 | 0 |
| Trauma_d014b28abbd1abb0 | 4-0-4 | 50% | 50% | 8 | 0 |

control_450 dragon deaths: head-to-head 6940, hit kelp 5056, hit other body 3483, hit itself 150

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# mature

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 45-0-43 | 51% | 51% | 48-56% | +8 | 44 | 0 |
| **overall** | 45-0-43 | 51% | 51% | 48-56% | +8 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena_728547b8376892d9 | 4-0-4 | 50% | 50% | 8 | 0 |
| Colosseum_3042ccc262f0211a | 4-0-4 | 50% | 50% | 8 | 0 |
| default_afc3707a967881d6 | 4-0-4 | 50% | 50% | 8 | 0 |
| default_small_f98ab391cccf33b1 | 4-0-4 | 50% | 50% | 8 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 4-0-4 | 50% | 50% | 8 | 0 |
| schooltime_8be7eda86910a849 | 4-0-4 | 50% | 50% | 8 | 0 |
| trophy_fd985019831fe135 | 4-0-4 | 50% | 50% | 8 | 0 |
| Devil_1b2147f4a8a775d2 | 4-0-4 | 50% | 50% | 8 | 0 |
| stronghold_fb60e37176a8d1d3 | 4-0-4 | 50% | 50% | 8 | 0 |
| Trauma_d014b28abbd1abb0 | 4-0-4 | 50% | 50% | 8 | 0 |
| big_empty_685baf0e797207b7 | 5-0-3 | 62% | 62% | 8 | 0 |

mature dragon deaths: head-to-head 6938, hit kelp 5044, hit other body 3447, hit itself 154

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# opportunity

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 35-1-52 | 40% | 40% | 32-48% | -68 | 44 | 0 |
| **overall** | 35-1-52 | 40% | 40% | 32-48% | -68 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| big_empty_685baf0e797207b7 | 1-0-7 | 12% | 12% | 8 | 0 |
| default_afc3707a967881d6 | 2-0-6 | 25% | 25% | 8 | 0 |
| schooltime_8be7eda86910a849 | 2-0-6 | 25% | 25% | 8 | 0 |
| Devil_1b2147f4a8a775d2 | 2-0-6 | 25% | 25% | 8 | 0 |
| Trauma_d014b28abbd1abb0 | 3-0-5 | 38% | 38% | 8 | 0 |
| arena_728547b8376892d9 | 3-1-4 | 38% | 44% | 8 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 4-0-4 | 50% | 50% | 8 | 0 |
| trophy_fd985019831fe135 | 4-0-4 | 50% | 50% | 8 | 0 |
| stronghold_fb60e37176a8d1d3 | 4-0-4 | 50% | 50% | 8 | 0 |
| Colosseum_3042ccc262f0211a | 5-0-3 | 62% | 62% | 8 | 0 |
| default_small_f98ab391cccf33b1 | 5-0-3 | 62% | 62% | 8 | 0 |

opportunity dragon deaths: head-to-head 5972, hit kelp 3993, hit other body 3091, hit itself 194

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260923-231438-hybrid-b0801d/validation/summary.md

SHA-256: `4eec6ebd4f137594f8b0e03ebf91b411517f917951313df0aa086307258058cf`

# control_450

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 157-0-19 | 89% | 89% | 83-95% | +367 | 88 | 0 |
| reference_v2 | 88-0-88 | 50% | 50% | 50-50% | -0 | 88 | 0 |
| splitter | 148-0-28 | 84% | 84% | 77-91% | +289 | 88 | 0 |
| **overall** | 393-0-135 | 74% | 74% | 71-78% | +186 | 264 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma_d014b28abbd1abb0 | 9-0-39 | 19% | 19% | 48 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 33-0-15 | 69% | 69% | 48 | 0 |
| big_empty_685baf0e797207b7 | 35-0-13 | 73% | 73% | 48 | 0 |
| stronghold_fb60e37176a8d1d3 | 36-0-12 | 75% | 75% | 48 | 0 |
| arena_728547b8376892d9 | 40-0-8 | 83% | 83% | 48 | 0 |
| Colosseum_3042ccc262f0211a | 40-0-8 | 83% | 83% | 48 | 0 |
| default_afc3707a967881d6 | 40-0-8 | 83% | 83% | 48 | 0 |
| default_small_f98ab391cccf33b1 | 40-0-8 | 83% | 83% | 48 | 0 |
| schooltime_8be7eda86910a849 | 40-0-8 | 83% | 83% | 48 | 0 |
| trophy_fd985019831fe135 | 40-0-8 | 83% | 83% | 48 | 0 |
| Devil_1b2147f4a8a775d2 | 40-0-8 | 83% | 83% | 48 | 0 |

control_450 dragon deaths: head-to-head 31221, hit kelp 27247, hit other body 15955, hit itself 1255

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# mature

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 159-0-17 | 90% | 90% | 84-96% | +388 | 88 | 0 |
| reference_v2 | 92-0-84 | 52% | 52% | 50-55% | +16 | 88 | 0 |
| splitter | 149-0-27 | 85% | 85% | 78-91% | +297 | 88 | 0 |
| **overall** | 400-0-128 | 76% | 76% | 72-80% | +198 | 264 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma_d014b28abbd1abb0 | 9-0-39 | 19% | 19% | 48 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 33-0-15 | 69% | 69% | 48 | 0 |
| stronghold_fb60e37176a8d1d3 | 36-0-12 | 75% | 75% | 48 | 0 |
| arena_728547b8376892d9 | 40-0-8 | 83% | 83% | 48 | 0 |
| Colosseum_3042ccc262f0211a | 40-0-8 | 83% | 83% | 48 | 0 |
| default_afc3707a967881d6 | 40-0-8 | 83% | 83% | 48 | 0 |
| default_small_f98ab391cccf33b1 | 40-0-8 | 83% | 83% | 48 | 0 |
| schooltime_8be7eda86910a849 | 40-0-8 | 83% | 83% | 48 | 0 |
| trophy_fd985019831fe135 | 40-0-8 | 83% | 83% | 48 | 0 |
| Devil_1b2147f4a8a775d2 | 40-0-8 | 83% | 83% | 48 | 0 |
| big_empty_685baf0e797207b7 | 42-0-6 | 88% | 88% | 48 | 0 |

mature dragon deaths: head-to-head 31177, hit kelp 27196, hit other body 15904, hit itself 1240

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# linear

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 158-0-18 | 90% | 90% | 84-95% | +377 | 88 | 0 |
| reference_v2 | 126-0-50 | 72% | 72% | 64-78% | +161 | 88 | 0 |
| splitter | 161-0-15 | 91% | 91% | 86-96% | +412 | 88 | 0 |
| **overall** | 445-0-83 | 84% | 84% | 80-88% | +292 | 264 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma_d014b28abbd1abb0 | 15-0-33 | 31% | 31% | 48 | 0 |
| default_afc3707a967881d6 | 35-0-13 | 73% | 73% | 48 | 0 |
| stronghold_fb60e37176a8d1d3 | 36-0-12 | 75% | 75% | 48 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 42-0-6 | 88% | 88% | 48 | 0 |
| default_small_f98ab391cccf33b1 | 43-0-5 | 90% | 90% | 48 | 0 |
| arena_728547b8376892d9 | 45-0-3 | 94% | 94% | 48 | 0 |
| Colosseum_3042ccc262f0211a | 45-0-3 | 94% | 94% | 48 | 0 |
| schooltime_8be7eda86910a849 | 45-0-3 | 94% | 94% | 48 | 0 |
| big_empty_685baf0e797207b7 | 46-0-2 | 96% | 96% | 48 | 0 |
| Devil_1b2147f4a8a775d2 | 46-0-2 | 96% | 96% | 48 | 0 |
| trophy_fd985019831fe135 | 47-0-1 | 98% | 98% | 48 | 0 |

linear dragon deaths: head-to-head 26826, hit kelp 23280, hit other body 13873, hit itself 1368

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260923-231438-hybrid-b0801d/validation-core/summary.md

SHA-256: `1cb72477debde1569309341f04c077fb599de171eb4c079c4577407b596beac1`

# control_450

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 157-0-19 | 89% | 89% | 83-95% | +367 | 88 | 0 |
| reference_v2 | 88-0-88 | 50% | 50% | 50-50% | -0 | 88 | 0 |
| splitter | 148-0-28 | 84% | 84% | 77-91% | +289 | 88 | 0 |
| **overall** | 393-0-135 | 74% | 74% | 71-78% | +186 | 264 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma_d014b28abbd1abb0 | 9-0-39 | 19% | 19% | 48 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 33-0-15 | 69% | 69% | 48 | 0 |
| big_empty_685baf0e797207b7 | 35-0-13 | 73% | 73% | 48 | 0 |
| stronghold_fb60e37176a8d1d3 | 36-0-12 | 75% | 75% | 48 | 0 |
| arena_728547b8376892d9 | 40-0-8 | 83% | 83% | 48 | 0 |
| Colosseum_3042ccc262f0211a | 40-0-8 | 83% | 83% | 48 | 0 |
| default_afc3707a967881d6 | 40-0-8 | 83% | 83% | 48 | 0 |
| default_small_f98ab391cccf33b1 | 40-0-8 | 83% | 83% | 48 | 0 |
| schooltime_8be7eda86910a849 | 40-0-8 | 83% | 83% | 48 | 0 |
| trophy_fd985019831fe135 | 40-0-8 | 83% | 83% | 48 | 0 |
| Devil_1b2147f4a8a775d2 | 40-0-8 | 83% | 83% | 48 | 0 |

control_450 dragon deaths: head-to-head 31221, hit kelp 27247, hit other body 15955, hit itself 1255

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# mature

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 159-0-17 | 90% | 90% | 84-96% | +388 | 88 | 0 |
| reference_v2 | 92-0-84 | 52% | 52% | 50-55% | +16 | 88 | 0 |
| splitter | 149-0-27 | 85% | 85% | 78-91% | +297 | 88 | 0 |
| **overall** | 400-0-128 | 76% | 76% | 72-80% | +198 | 264 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma_d014b28abbd1abb0 | 9-0-39 | 19% | 19% | 48 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 33-0-15 | 69% | 69% | 48 | 0 |
| stronghold_fb60e37176a8d1d3 | 36-0-12 | 75% | 75% | 48 | 0 |
| arena_728547b8376892d9 | 40-0-8 | 83% | 83% | 48 | 0 |
| Colosseum_3042ccc262f0211a | 40-0-8 | 83% | 83% | 48 | 0 |
| default_afc3707a967881d6 | 40-0-8 | 83% | 83% | 48 | 0 |
| default_small_f98ab391cccf33b1 | 40-0-8 | 83% | 83% | 48 | 0 |
| schooltime_8be7eda86910a849 | 40-0-8 | 83% | 83% | 48 | 0 |
| trophy_fd985019831fe135 | 40-0-8 | 83% | 83% | 48 | 0 |
| Devil_1b2147f4a8a775d2 | 40-0-8 | 83% | 83% | 48 | 0 |
| big_empty_685baf0e797207b7 | 42-0-6 | 88% | 88% | 48 | 0 |

mature dragon deaths: head-to-head 31177, hit kelp 27196, hit other body 15904, hit itself 1240

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260923-231438-hybrid-b0801d/validation-evaluator/summary.md

SHA-256: `3b783a75c1fd7309bdbd93fb0d55c2a0122428b597d2a2fca8dde6b51ba13abd`

# linear

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 158-0-18 | 90% | 90% | 84-95% | +377 | 88 | 0 |
| reference_v2 | 126-0-50 | 72% | 72% | 64-78% | +161 | 88 | 0 |
| splitter | 161-0-15 | 91% | 91% | 86-96% | +412 | 88 | 0 |
| **overall** | 445-0-83 | 84% | 84% | 80-88% | +292 | 264 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma_d014b28abbd1abb0 | 15-0-33 | 31% | 31% | 48 | 0 |
| default_afc3707a967881d6 | 35-0-13 | 73% | 73% | 48 | 0 |
| stronghold_fb60e37176a8d1d3 | 36-0-12 | 75% | 75% | 48 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 42-0-6 | 88% | 88% | 48 | 0 |
| default_small_f98ab391cccf33b1 | 43-0-5 | 90% | 90% | 48 | 0 |
| arena_728547b8376892d9 | 45-0-3 | 94% | 94% | 48 | 0 |
| Colosseum_3042ccc262f0211a | 45-0-3 | 94% | 94% | 48 | 0 |
| schooltime_8be7eda86910a849 | 45-0-3 | 94% | 94% | 48 | 0 |
| big_empty_685baf0e797207b7 | 46-0-2 | 96% | 96% | 48 | 0 |
| Devil_1b2147f4a8a775d2 | 46-0-2 | 96% | 96% | 48 | 0 |
| trophy_fd985019831fe135 | 47-0-1 | 98% | 98% | 48 | 0 |

linear dragon deaths: head-to-head 26826, hit kelp 23280, hit other body 13873, hit itself 1368

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260924-113203-v4-abbee0/screen-direct/summary.md

SHA-256: `4734d8738183d5f768cabd01e0ab59ce1ddc3051ac11594142c468e8785b9cb5`

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


---

## results/20260924-113203-v4-abbee0/screen-pool/summary.md

SHA-256: `c46473a48e53d621cd75aacecadb8dbfd5ccd919e38a02a4ffb3a10e001b3569`

# control_v3

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 40-0-4 | 91% | 91% | 77-100% | +400 | 22 | 0 |
| splitter | 40-0-4 | 91% | 91% | 77-100% | +400 | 22 | 0 |
| **overall** | 80-0-8 | 91% | 91% | 82-98% | +400 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma_d014b28abbd1abb0 | 0-0-8 | 0% | 0% | 8 | 0 |
| arena_728547b8376892d9 | 8-0-0 | 100% | 100% | 8 | 0 |
| big_empty_685baf0e797207b7 | 8-0-0 | 100% | 100% | 8 | 0 |
| Colosseum_3042ccc262f0211a | 8-0-0 | 100% | 100% | 8 | 0 |
| default_afc3707a967881d6 | 8-0-0 | 100% | 100% | 8 | 0 |
| default_small_f98ab391cccf33b1 | 8-0-0 | 100% | 100% | 8 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 8-0-0 | 100% | 100% | 8 | 0 |
| schooltime_8be7eda86910a849 | 8-0-0 | 100% | 100% | 8 | 0 |
| trophy_fd985019831fe135 | 8-0-0 | 100% | 100% | 8 | 0 |
| Devil_1b2147f4a8a775d2 | 8-0-0 | 100% | 100% | 8 | 0 |
| stronghold_fb60e37176a8d1d3 | 8-0-0 | 100% | 100% | 8 | 0 |

control_v3 dragon deaths: hit kelp 2801, head-to-head 2742, hit other body 1463, hit itself 235

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# guard_all

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 39-0-5 | 89% | 89% | 75-100% | +357 | 22 | 0 |
| splitter | 40-0-4 | 91% | 91% | 77-100% | +400 | 22 | 0 |
| **overall** | 79-0-9 | 90% | 90% | 80-98% | +377 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma_d014b28abbd1abb0 | 0-0-8 | 0% | 0% | 8 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 7-0-1 | 88% | 88% | 8 | 0 |
| arena_728547b8376892d9 | 8-0-0 | 100% | 100% | 8 | 0 |
| big_empty_685baf0e797207b7 | 8-0-0 | 100% | 100% | 8 | 0 |
| Colosseum_3042ccc262f0211a | 8-0-0 | 100% | 100% | 8 | 0 |
| default_afc3707a967881d6 | 8-0-0 | 100% | 100% | 8 | 0 |
| default_small_f98ab391cccf33b1 | 8-0-0 | 100% | 100% | 8 | 0 |
| schooltime_8be7eda86910a849 | 8-0-0 | 100% | 100% | 8 | 0 |
| trophy_fd985019831fe135 | 8-0-0 | 100% | 100% | 8 | 0 |
| Devil_1b2147f4a8a775d2 | 8-0-0 | 100% | 100% | 8 | 0 |
| stronghold_fb60e37176a8d1d3 | 8-0-0 | 100% | 100% | 8 | 0 |

guard_all dragon deaths: hit kelp 2968, head-to-head 2105, hit other body 1475, hit itself 267

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).

# guard_later

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| hunter | 39-0-5 | 89% | 89% | 75-100% | +357 | 22 | 0 |
| splitter | 40-0-4 | 91% | 91% | 82-98% | +400 | 22 | 0 |
| **overall** | 79-0-9 | 90% | 90% | 82-97% | +377 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma_d014b28abbd1abb0 | 2-0-6 | 25% | 25% | 8 | 0 |
| default_afc3707a967881d6 | 5-0-3 | 62% | 62% | 8 | 0 |
| arena_728547b8376892d9 | 8-0-0 | 100% | 100% | 8 | 0 |
| big_empty_685baf0e797207b7 | 8-0-0 | 100% | 100% | 8 | 0 |
| Colosseum_3042ccc262f0211a | 8-0-0 | 100% | 100% | 8 | 0 |
| default_small_f98ab391cccf33b1 | 8-0-0 | 100% | 100% | 8 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 8-0-0 | 100% | 100% | 8 | 0 |
| schooltime_8be7eda86910a849 | 8-0-0 | 100% | 100% | 8 | 0 |
| trophy_fd985019831fe135 | 8-0-0 | 100% | 100% | 8 | 0 |
| Devil_1b2147f4a8a775d2 | 8-0-0 | 100% | 100% | 8 | 0 |
| stronghold_fb60e37176a8d1d3 | 8-0-0 | 100% | 100% | 8 | 0 |

guard_later dragon deaths: hit kelp 2897, head-to-head 2480, hit other body 1497, hit itself 280

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260924-115357-v4-grower-374d2b/screen-direct/summary.md

SHA-256: `b3e961bb6f3d66c0df729692d11d69ac664d22219e99f0ec1d7a421fdb4a942a`

# mature

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 4-0-4 | 50% | 50% | 50-50% | -0 | 4 | 0 |
| **overall** | 4-0-4 | 50% | 50% | 50-50% | -0 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default_small_f98ab391cccf33b1 | 1-0-1 | 50% | 50% | 2 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 1-0-1 | 50% | 50% | 2 | 0 |
| default_afc3707a967881d6 | 1-0-1 | 50% | 50% | 2 | 0 |
| Trauma_d014b28abbd1abb0 | 1-0-1 | 50% | 50% | 2 | 0 |

mature dragon deaths: hit kelp 156, head-to-head 120, hit other body 71, hit itself 1

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# opportunity

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 5-0-3 | 62% | 62% | 50-88% | +89 | 4 | 0 |
| **overall** | 5-0-3 | 62% | 62% | 50-88% | +89 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default_afc3707a967881d6 | 1-0-1 | 50% | 50% | 2 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 1-0-1 | 50% | 50% | 2 | 0 |
| Trauma_d014b28abbd1abb0 | 1-0-1 | 50% | 50% | 2 | 0 |
| default_small_f98ab391cccf33b1 | 2-0-0 | 100% | 100% | 2 | 0 |

opportunity dragon deaths: hit kelp 134, head-to-head 103, hit other body 68, hit itself 2

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-115357-v4-grower-374d2b/screen-pool/summary.md

SHA-256: `64bcf46a823b4fc373cfae2428e7157af214f622e6028383f8bbdc27b74229e0`

# control_v3

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| ctmes | 5-0-3 | 62% | 62% | 25-100% | +89 | 4 | 0 |
| nicked | 0-0-8 | 0% | 0% | 0-0% | -1200 | 4 | 0 |
| **overall** | 5-0-11 | 31% | 31% | 6-62% | -137 | 8 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma_d014b28abbd1abb0 | 0-0-4 | 0% | 0% | 4 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 1-0-3 | 25% | 25% | 4 | 0 |
| default_small_f98ab391cccf33b1 | 2-0-2 | 50% | 50% | 4 | 0 |
| default_afc3707a967881d6 | 2-0-2 | 50% | 50% | 4 | 0 |

control_v3 dragon deaths: hit kelp 425, head-to-head 312, hit other body 134

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for ctmes, nicked: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# mature

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| ctmes | 5-0-3 | 62% | 62% | 25-100% | +89 | 4 | 0 |
| nicked | 0-0-8 | 0% | 0% | 0-0% | -1200 | 4 | 0 |
| **overall** | 5-0-11 | 31% | 31% | 6-62% | -137 | 8 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma_d014b28abbd1abb0 | 0-0-4 | 0% | 0% | 4 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 1-0-3 | 25% | 25% | 4 | 0 |
| default_afc3707a967881d6 | 2-0-2 | 50% | 50% | 4 | 0 |
| default_small_f98ab391cccf33b1 | 2-0-2 | 50% | 50% | 4 | 0 |

mature dragon deaths: hit kelp 425, head-to-head 312, hit other body 134

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for ctmes, nicked: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# opportunity

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| ctmes | 4-0-4 | 50% | 50% | 12-88% | -0 | 4 | 0 |
| nicked | 0-0-8 | 0% | 0% | 0-0% | -1200 | 4 | 0 |
| **overall** | 4-0-12 | 25% | 25% | 6-50% | -191 | 8 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma_d014b28abbd1abb0 | 0-0-4 | 0% | 0% | 4 | 0 |
| default_afc3707a967881d6 | 1-0-3 | 25% | 25% | 4 | 0 |
| queen_of_spades_6cdb74a7a52d715a | 1-0-3 | 25% | 25% | 4 | 0 |
| default_small_f98ab391cccf33b1 | 2-0-2 | 50% | 50% | 4 | 0 |

opportunity dragon deaths: hit kelp 301, head-to-head 232, hit other body 128, hit itself 1

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for ctmes, nicked: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-131752-v4-feed-48a467/feed-vs-grower/summary.md

SHA-256: `c3cbf1e053e6e4125e24f7744a324cb74df3f34f444f3baea6e9a9e4dd4f82e3`

# feed

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| grower | 4-0-4 | 50% | 50% | 50-50% | -0 | 4 | 0 |
| **overall** | 4-0-4 | 50% | 50% | 50-50% | -0 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| big_empty_685baf0e797207b7 | 1-0-1 | 50% | 50% | 2 | 0 |
| default_afc3707a967881d6 | 1-0-1 | 50% | 50% | 2 | 0 |
| schooltime_8be7eda86910a849 | 1-0-1 | 50% | 50% | 2 | 0 |
| stronghold_fb60e37176a8d1d3 | 1-0-1 | 50% | 50% | 2 | 0 |

feed dragon deaths: hit kelp 547, head-to-head 353, hit other body 298, hit itself 64, no valid action/timeout 7

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for grower: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-131752-v4-feed-48a467/feed-vs-reference_v3/summary.md

SHA-256: `f06f136b1dd5ee21d93e04ef43aac4d0815add9c7aeb91c10132815af9483448`

# feed

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 3-0-5 | 38% | 38% | 0-75% | -89 | 4 | 0 |
| **overall** | 3-0-5 | 38% | 38% | 0-75% | -89 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default_afc3707a967881d6 | 0-0-2 | 0% | 0% | 2 | 0 |
| stronghold_fb60e37176a8d1d3 | 0-0-2 | 0% | 0% | 2 | 0 |
| schooltime_8be7eda86910a849 | 1-0-1 | 50% | 50% | 2 | 0 |
| big_empty_685baf0e797207b7 | 2-0-0 | 100% | 100% | 2 | 0 |

feed dragon deaths: hit kelp 548, head-to-head 370, hit other body 305, hit itself 69, no valid action/timeout 8

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-131752-v4-feed-48a467/grower-vs-reference_v3/summary.md

SHA-256: `b45b4bbbf80c19bc873e7bc1369a2186513ddbc2a4bb2c2504fe5acf79845e97`

# grower

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 3-0-5 | 38% | 38% | 0-75% | -89 | 4 | 0 |
| **overall** | 3-0-5 | 38% | 38% | 0-75% | -89 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default_afc3707a967881d6 | 0-0-2 | 0% | 0% | 2 | 0 |
| stronghold_fb60e37176a8d1d3 | 0-0-2 | 0% | 0% | 2 | 0 |
| schooltime_8be7eda86910a849 | 1-0-1 | 50% | 50% | 2 | 0 |
| big_empty_685baf0e797207b7 | 2-0-0 | 100% | 100% | 2 | 0 |

grower dragon deaths: hit kelp 551, head-to-head 372, hit other body 300, hit itself 69

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-133212-v4-sonar-e451f4/route-vs-beacon/summary.md

SHA-256: `f3d57c8718cf9e6f1471793651dec648ba8d8d96666e8536c2f9b211f9d7d3c3`

# route

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| beacon | 2-0-2 | 50% | 50% | 50-50% | -0 | 2 | 0 |
| **overall** | 2-0-2 | 50% | 50% | 50-50% | -0 | 2 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| schooltime_8be7eda86910a849 | 1-0-1 | 50% | 50% | 2 | 0 |
| stronghold_fb60e37176a8d1d3 | 1-0-1 | 50% | 50% | 2 | 0 |

route dragon deaths: hit kelp 540, head-to-head 279, hit other body 156, no valid action/timeout 7, hit itself 5

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for beacon: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-133212-v4-sonar-e451f4/screen-v3/summary.md

SHA-256: `5944baa4ce72f4dc12f2d21499bd9182d6eeaa89d115d534269ab7f65b08da07`

# feed_base

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 1-0-3 | 25% | 25% | 0-50% | -191 | 2 | 0 |
| **overall** | 1-0-3 | 25% | 25% | 0-50% | -191 | 2 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold_fb60e37176a8d1d3 | 0-0-2 | 0% | 0% | 2 | 0 |
| schooltime_8be7eda86910a849 | 1-0-1 | 50% | 50% | 2 | 0 |

feed_base dragon deaths: hit kelp 545, head-to-head 293, hit other body 163, hit itself 8, no valid action/timeout 8

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# beacon

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 1-0-3 | 25% | 25% | 0-50% | -191 | 2 | 0 |
| **overall** | 1-0-3 | 25% | 25% | 0-50% | -191 | 2 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold_fb60e37176a8d1d3 | 0-0-2 | 0% | 0% | 2 | 0 |
| schooltime_8be7eda86910a849 | 1-0-1 | 50% | 50% | 2 | 0 |

beacon dragon deaths: hit kelp 545, head-to-head 293, hit other body 163, hit itself 8, no valid action/timeout 8

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# route

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 2-0-2 | 50% | 50% | 0-100% | -0 | 2 | 0 |
| **overall** | 2-0-2 | 50% | 50% | 0-100% | -0 | 2 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold_fb60e37176a8d1d3 | 0-0-2 | 0% | 0% | 2 | 0 |
| schooltime_8be7eda86910a849 | 2-0-0 | 100% | 100% | 2 | 0 |

route dragon deaths: hit kelp 544, head-to-head 291, hit other body 164, hit itself 7, no valid action/timeout 7

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-172250-v4-additive-9c22dc/vs-old-route/summary.md

SHA-256: `dd25f112ec7425d2218072d81f0ca0db7673fd5bf8f6f1d4b6b032d8453681b1`

# additive

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| old_route | 5-0-3 | 62% | 62% | 50-88% | +89 | 4 | 0 |
| **overall** | 5-0-3 | 62% | 62% | 50-88% | +89 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| big_empty_685baf0e797207b7 | 1-0-1 | 50% | 50% | 2 | 0 |
| schooltime_8be7eda86910a849 | 1-0-1 | 50% | 50% | 2 | 0 |
| stronghold_fb60e37176a8d1d3 | 1-0-1 | 50% | 50% | 2 | 0 |
| default_afc3707a967881d6 | 2-0-0 | 100% | 100% | 2 | 0 |

additive dragon deaths: hit kelp 576, head-to-head 366, hit other body 298, hit itself 65, no valid action/timeout 7

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for old_route: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-172250-v4-additive-9c22dc/vs-v3/summary.md

SHA-256: `fc0767e4d68b4ae724df74cfc6142666c41f9807b20e63a3ff5afd0b4f07a616`

# additive

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 5-0-3 | 62% | 62% | 50-88% | +89 | 4 | 0 |
| **overall** | 5-0-3 | 62% | 62% | 50-88% | +89 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| big_empty_685baf0e797207b7 | 1-0-1 | 50% | 50% | 2 | 0 |
| default_afc3707a967881d6 | 1-0-1 | 50% | 50% | 2 | 0 |
| stronghold_fb60e37176a8d1d3 | 1-0-1 | 50% | 50% | 2 | 0 |
| schooltime_8be7eda86910a849 | 2-0-0 | 100% | 100% | 2 | 0 |

additive dragon deaths: hit kelp 576, head-to-head 369, hit other body 306, hit itself 60, no valid action/timeout 3

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# old_route

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 4-0-4 | 50% | 50% | 0-100% | -0 | 4 | 0 |
| **overall** | 4-0-4 | 50% | 50% | 0-100% | -0 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default_afc3707a967881d6 | 0-0-2 | 0% | 0% | 2 | 0 |
| stronghold_fb60e37176a8d1d3 | 0-0-2 | 0% | 0% | 2 | 0 |
| big_empty_685baf0e797207b7 | 2-0-0 | 100% | 100% | 2 | 0 |
| schooltime_8be7eda86910a849 | 2-0-0 | 100% | 100% | 2 | 0 |

old_route dragon deaths: hit kelp 547, head-to-head 374, hit other body 303, hit itself 67, no valid action/timeout 8

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-174513-v4-additive-validation-d407dd/vs-v2/summary.md

SHA-256: `ae6a6b85a7da926ea9532febbe9f4836f8a5a426aa83135861dd13047971b496`

# additive

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 8-0-0 | 100% | 100% | 100-100% | +1200 | 4 | 0 |
| **overall** | 8-0-0 | 100% | 100% | 100-100% | +1200 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Devil | 2-0-0 | 100% | 100% | 2 | 0 |
| Trauma | 2-0-0 | 100% | 100% | 2 | 0 |
| queen_of_spades | 2-0-0 | 100% | 100% | 2 | 0 |
| Colosseum | 2-0-0 | 100% | 100% | 2 | 0 |

additive dragon deaths: head-to-head 908, hit kelp 525, hit other body 313, no valid action/timeout 3, hit itself 3

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v2: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-174513-v4-additive-validation-d407dd/vs-v3/summary.md

SHA-256: `22daf1f103936800e21519433eda1c8f6c1e0fbaac585455925602837e4cdca2`

# additive

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 8-0-8 | 50% | 50% | 25-75% | -0 | 8 | 0 |
| **overall** | 8-0-8 | 50% | 50% | 25-75% | -0 | 8 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Colosseum | 0-0-4 | 0% | 0% | 4 | 0 |
| Trauma | 2-0-2 | 50% | 50% | 4 | 0 |
| queen_of_spades | 2-0-2 | 50% | 50% | 4 | 0 |
| Devil | 4-0-0 | 100% | 100% | 4 | 0 |

additive dragon deaths: head-to-head 1416, hit other body 566, hit kelp 494, hit itself 4

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-180920-v4-additive-portal-ed6674/official/summary.md

SHA-256: `e3f3e11ca1b1cbb0de00f841bd2345376b0d1f2bf8f6ad9aa7e6fee5c5ac3292`

# additive

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 10-0-10 | 50% | 50% | 30-70% | -0 | 10 | 0 |
| **overall** | 10-0-10 | 50% | 50% | 30-70% | -0 | 10 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Colosseum | 0-0-4 | 0% | 0% | 4 | 0 |
| default | 2-0-2 | 50% | 50% | 4 | 0 |
| queen_of_spades | 2-0-2 | 50% | 50% | 4 | 0 |
| trophy | 2-0-2 | 50% | 50% | 4 | 0 |
| schooltime | 4-0-0 | 100% | 100% | 4 | 0 |

additive dragon deaths: hit kelp 1514, head-to-head 1134, hit other body 602, no valid action/timeout 12, hit itself 6

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# portal

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 8-0-12 | 40% | 40% | 15-60% | -70 | 10 | 0 |
| **overall** | 8-0-12 | 40% | 40% | 15-60% | -70 | 10 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default | 0-0-4 | 0% | 0% | 4 | 0 |
| trophy | 0-0-4 | 0% | 0% | 4 | 0 |
| Colosseum | 2-0-2 | 50% | 50% | 4 | 0 |
| queen_of_spades | 2-0-2 | 50% | 50% | 4 | 0 |
| schooltime | 4-0-0 | 100% | 100% | 4 | 0 |

portal dragon deaths: hit kelp 1618, head-to-head 1028, hit other body 622, hit itself 30, no valid action/timeout 2

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-180920-v4-additive-portal-ed6674/stress/summary.md

SHA-256: `cf97c7401c48d263e6ffd90fdc990938bae991c84e7dd3353c45faa8dd2e7f19`

# portal

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 1-0-1 | 50% | 50% | 0-100% | -0 | 1 | 0 |
| **overall** | 1-0-1 | 50% | 50% | 0-100% | -0 | 1 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| new_dense_small | 1-0-1 | 50% | 50% | 2 | 0 |

portal dragon deaths: hit kelp 751, head-to-head 512, hit other body 255

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-182411-v4-visible-portal-ada92a/official/summary.md

SHA-256: `9c067aa3e2acb029bc9f54076b1086fb51d601a9968f1949320b6a85ec8adcec`

# additive

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 5-0-5 | 50% | 50% | 20-80% | -0 | 5 | 0 |
| **overall** | 5-0-5 | 50% | 50% | 20-80% | -0 | 5 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Colosseum | 0-0-2 | 0% | 0% | 2 | 0 |
| default | 1-0-1 | 50% | 50% | 2 | 0 |
| queen_of_spades | 1-0-1 | 50% | 50% | 2 | 0 |
| trophy | 1-0-1 | 50% | 50% | 2 | 0 |
| schooltime | 2-0-0 | 100% | 100% | 2 | 0 |

additive dragon deaths: hit kelp 757, head-to-head 567, hit other body 301, no valid action/timeout 6, hit itself 3

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# visible_portal

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v3 | 5-0-5 | 50% | 50% | 20-80% | -0 | 5 | 0 |
| **overall** | 5-0-5 | 50% | 50% | 20-80% | -0 | 5 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Colosseum | 0-0-2 | 0% | 0% | 2 | 0 |
| default | 1-0-1 | 50% | 50% | 2 | 0 |
| queen_of_spades | 1-0-1 | 50% | 50% | 2 | 0 |
| trophy | 1-0-1 | 50% | 50% | 2 | 0 |
| schooltime | 2-0-0 | 100% | 100% | 2 | 0 |

visible_portal dragon deaths: hit kelp 757, head-to-head 567, hit other body 301, no valid action/timeout 6, hit itself 3

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-182411-v4-visible-portal-ada92a/stress/summary.md

SHA-256: `c2dc84c73fecbe37fd14e153cf4b412feaec82cb64d3b333e3ef148b69685bb2`

# visible_portal

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 1-0-1 | 50% | 50% | 0-100% | -0 | 1 | 0 |
| **overall** | 1-0-1 | 50% | 50% | 0-100% | -0 | 1 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| new_dense_small | 1-0-1 | 50% | 50% | 2 | 0 |

visible_portal dragon deaths: hit kelp 751, head-to-head 512, hit other body 255

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-183910-v4-visible-portal-v2-fb319a/vs-v2/summary.md

SHA-256: `a020c3c237457dc11ae6f4d1fe2971730930a0d2624cd7a761804116b2229e4b`

# visible_portal

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 7-0-3 | 70% | 70% | 30-100% | +147 | 5 | 0 |
| **overall** | 7-0-3 | 70% | 70% | 30-100% | +147 | 5 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default | 0-0-2 | 0% | 0% | 2 | 0 |
| schooltime | 1-0-1 | 50% | 50% | 2 | 0 |
| Colosseum | 2-0-0 | 100% | 100% | 2 | 0 |
| queen_of_spades | 2-0-0 | 100% | 100% | 2 | 0 |
| trophy | 2-0-0 | 100% | 100% | 2 | 0 |

visible_portal dragon deaths: hit kelp 675, head-to-head 462, hit other body 306, no valid action/timeout 19, hit itself 17

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v2: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-184143-v4-portal-control-e3989f/vs-v2/summary.md

SHA-256: `56e4dbb6fe02bbb8ba7a20657b5fac57f9d92b55a4b88ba7a9959c67c8868249`

# additive

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| reference_v2 | 7-0-3 | 70% | 70% | 30-100% | +147 | 5 | 0 |
| **overall** | 7-0-3 | 70% | 70% | 30-100% | +147 | 5 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default | 0-0-2 | 0% | 0% | 2 | 0 |
| schooltime | 1-0-1 | 50% | 50% | 2 | 0 |
| Colosseum | 2-0-0 | 100% | 100% | 2 | 0 |
| queen_of_spades | 2-0-0 | 100% | 100% | 2 | 0 |
| trophy | 2-0-0 | 100% | 100% | 2 | 0 |

additive dragon deaths: hit kelp 675, head-to-head 462, hit other body 306, no valid action/timeout 19, hit itself 17

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for reference_v2: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-193023-v5-initial-4cdc22/vs-additive/summary.md

SHA-256: `e25ac04cc26dc0a4c17f5bfb7b87339ec895f29bffefeb543a9fdfd31793abc6`

# territory

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 2-0-6 | 25% | 25% | 0-50% | -191 | 4 | 0 |
| **overall** | 2-0-6 | 25% | 25% | 0-50% | -191 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold | 0-0-2 | 0% | 0% | 2 | 0 |
| Trauma | 0-0-2 | 0% | 0% | 2 | 0 |
| default | 1-0-1 | 50% | 50% | 2 | 0 |
| trophy | 1-0-1 | 50% | 50% | 2 | 0 |

territory dragon deaths: hit kelp 797, head-to-head 472, hit other body 180, no valid action/timeout 6, hit itself 3

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# king_guard

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 4-0-4 | 50% | 50% | 50-50% | -0 | 4 | 0 |
| **overall** | 4-0-4 | 50% | 50% | 50-50% | -0 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold | 1-0-1 | 50% | 50% | 2 | 0 |
| Trauma | 1-0-1 | 50% | 50% | 2 | 0 |
| default | 1-0-1 | 50% | 50% | 2 | 0 |
| trophy | 1-0-1 | 50% | 50% | 2 | 0 |

king_guard dragon deaths: hit kelp 290, head-to-head 278, hit other body 148, no valid action/timeout 2, hit itself 1

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# combined

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 2-0-6 | 25% | 25% | 0-50% | -191 | 4 | 0 |
| **overall** | 2-0-6 | 25% | 25% | 0-50% | -191 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold | 0-0-2 | 0% | 0% | 2 | 0 |
| Trauma | 0-0-2 | 0% | 0% | 2 | 0 |
| default | 1-0-1 | 50% | 50% | 2 | 0 |
| trophy | 1-0-1 | 50% | 50% | 2 | 0 |

combined dragon deaths: hit kelp 802, head-to-head 476, hit other body 177, hit itself 3, no valid action/timeout 2

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-193730-v5-initial-e256aa/vs-additive/summary.md

SHA-256: `4ca2847004bbf6625a2503ff996d0aca98e416a597a46ac8747f1f81f40ce1cf`

# territory

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 3-0-5 | 38% | 38% | 12-50% | -89 | 4 | 0 |
| **overall** | 3-0-5 | 38% | 38% | 12-50% | -89 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 0-0-2 | 0% | 0% | 2 | 0 |
| stronghold | 1-0-1 | 50% | 50% | 2 | 0 |
| default | 1-0-1 | 50% | 50% | 2 | 0 |
| trophy | 1-0-1 | 50% | 50% | 2 | 0 |

territory dragon deaths: hit kelp 357, head-to-head 282, hit other body 150, no valid action/timeout 9, hit itself 1

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# king_guard

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 4-0-4 | 50% | 50% | 50-50% | -0 | 4 | 0 |
| **overall** | 4-0-4 | 50% | 50% | 50-50% | -0 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold | 1-0-1 | 50% | 50% | 2 | 0 |
| Trauma | 1-0-1 | 50% | 50% | 2 | 0 |
| default | 1-0-1 | 50% | 50% | 2 | 0 |
| trophy | 1-0-1 | 50% | 50% | 2 | 0 |

king_guard dragon deaths: hit kelp 290, head-to-head 278, hit other body 148, no valid action/timeout 2, hit itself 1

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.

# combined

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 3-0-5 | 38% | 38% | 12-50% | -89 | 4 | 0 |
| **overall** | 3-0-5 | 38% | 38% | 12-50% | -89 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 0-0-2 | 0% | 0% | 2 | 0 |
| stronghold | 1-0-1 | 50% | 50% | 2 | 0 |
| default | 1-0-1 | 50% | 50% | 2 | 0 |
| trophy | 1-0-1 | 50% | 50% | 2 | 0 |

combined dragon deaths: hit kelp 364, head-to-head 278, hit other body 151, no valid action/timeout 8

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-194334-v5-export-ad159f/vs-additive/summary.md

SHA-256: `3464767a170a8503207f641032289e630a8b151f6287a4440ce9a0a8cf4fc53d`

# export_scout

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 4-0-4 | 50% | 50% | 0-100% | -0 | 4 | 0 |
| **overall** | 4-0-4 | 50% | 50% | 0-100% | -0 | 4 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold | 0-0-4 | 0% | 0% | 4 | 0 |
| Trauma | 4-0-0 | 100% | 100% | 4 | 0 |

export_scout dragon deaths: hit kelp 1176, head-to-head 632, hit other body 204, no valid action/timeout 6, hit itself 4

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-194815-v5-export-a2cb1a/vs-additive/summary.md

SHA-256: `047ee0db120bcf174332c5d06573fea52eea8ddc111d6595d62412730e87a581`

# export_scout

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 12-0-4 | 75% | 75% | 56-94% | +191 | 8 | 0 |
| **overall** | 12-0-4 | 75% | 75% | 56-94% | +191 | 8 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold | 4-0-4 | 50% | 50% | 8 | 0 |
| Trauma | 8-0-0 | 100% | 100% | 8 | 0 |

export_scout dragon deaths: hit kelp 1512, head-to-head 1000, hit other body 376, no valid action/timeout 4, hit itself 4

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-194928-v5-early-king-47a8ab/vs-additive/summary.md

SHA-256: `24fe647495ea99cff6993774c8ad89ab6a1bd0c34170d7a536890cd7cb61f731`

# early_king

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 14-0-10 | 58% | 58% | 33-83% | +58 | 12 | 0 |
| **overall** | 14-0-10 | 58% | 58% | 33-83% | +58 | 12 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold | 0-0-4 | 0% | 0% | 4 | 0 |
| trophy | 0-0-4 | 0% | 0% | 4 | 0 |
| big_empty | 2-0-2 | 50% | 50% | 4 | 0 |
| default | 4-0-0 | 100% | 100% | 4 | 0 |
| schooltime | 4-0-0 | 100% | 100% | 4 | 0 |
| Trauma | 4-0-0 | 100% | 100% | 4 | 0 |

early_king dragon deaths: hit kelp 1486, head-to-head 978, hit other body 686, hit itself 138, no valid action/timeout 16

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-215539-export_scout/summary.md

SHA-256: `38e459909c9fea1f91c41d7306161701d960c04582bf7b28a14c5438b0fcff44`

# export_scout evaluation

2026-09-24 21:55:39 - git 8e1000d+dirty - 2 games

code: export_scout a67ebf2b6eb44faa, v3 69382825b699723d

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| v3 | 2-0-0 | 100% | 100% | 0-100% | +1200 | 1 | 0 |
| **overall** | 2-0-0 | 100% | 100% | 0-100% | +1200 | 1 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 2-0-0 | 100% | 100% | 2 | 0 |

export_scout dragon deaths: hit kelp 281, head-to-head 92, hit other body 9

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-215614-export_scout/summary.md

SHA-256: `fca8cbee5e499d32f011d7d5cb38218e1284cb7fe239f260cdd1d3f2c05b20f0`

# export_scout evaluation

2026-09-24 21:56:14 - git 8e1000d+dirty - 2 games

code: export_scout a67ebf2b6eb44faa, nicked d6dd50765f54f638

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 0-0-2 | 0% | 0% | 0-100% | -1200 | 1 | 0 |
| **overall** | 0-0-2 | 0% | 0% | 0-100% | -1200 | 1 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 0-0-2 | 0% | 0% | 2 | 0 |

export_scout dragon deaths: hit kelp 264, head-to-head 91, hit other body 8

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for nicked: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-215724-additive/summary.md

SHA-256: `dbc0616782d0d12ed3c98a69d538f7ef753a24365c84df8065e3210c7e0e6ddf`

# additive evaluation

2026-09-24 21:57:25 - git 8e1000d+dirty - 2 games

code: additive bf33497158a49a7b, nicked d6dd50765f54f638

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 0-0-2 | 0% | 0% | 0-100% | -1200 | 1 | 0 |
| **overall** | 0-0-2 | 0% | 0% | 0-100% | -1200 | 1 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 0-0-2 | 0% | 0% | 2 | 0 |

additive dragon deaths: hit kelp 90, head-to-head 33, hit other body 3

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for nicked: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-220052-v5-feed-38e008/vs-additive/summary.md

SHA-256: `3b8db17a256b79cfc8e5b0c2a955dbf64ef2d812f099c26978276101c29ae394`

# feed_king

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 9-0-3 | 75% | 75% | 42-100% | +191 | 6 | 0 |
| **overall** | 9-0-3 | 75% | 75% | 42-100% | +191 | 6 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| trophy | 0-0-2 | 0% | 0% | 2 | 0 |
| big_empty | 1-0-1 | 50% | 50% | 2 | 0 |
| default | 2-0-0 | 100% | 100% | 2 | 0 |
| schooltime | 2-0-0 | 100% | 100% | 2 | 0 |
| stronghold | 2-0-0 | 100% | 100% | 2 | 0 |
| Trauma | 2-0-0 | 100% | 100% | 2 | 0 |

feed_king dragon deaths: hit kelp 748, head-to-head 482, hit other body 350, hit itself 67, no valid action/timeout 14

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-220052-v5-feed-38e008/vs-king/summary.md

SHA-256: `38445fffbabbc2004b8020a899a1c84dc6eeb34b9759d594aabf90f750204a1d`

# feed_king

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| early_king | 6-0-6 | 50% | 50% | 25-75% | -0 | 6 | 0 |
| **overall** | 6-0-6 | 50% | 50% | 25-75% | -0 | 6 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| schooltime | 0-0-2 | 0% | 0% | 2 | 0 |
| big_empty | 1-0-1 | 50% | 50% | 2 | 0 |
| default | 1-0-1 | 50% | 50% | 2 | 0 |
| Trauma | 1-0-1 | 50% | 50% | 2 | 0 |
| trophy | 1-0-1 | 50% | 50% | 2 | 0 |
| stronghold | 2-0-0 | 100% | 100% | 2 | 0 |

feed_king dragon deaths: hit kelp 719, head-to-head 432, hit other body 354, hit itself 74, no valid action/timeout 12

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for early_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-221046-v5-sonar-7b27e1/vs-additive/summary.md

SHA-256: `8176812b6f4be36c56f4791fcfda43131f35ee074342651ffea6744b91887a34`

# no_sonar

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 5-0-7 | 42% | 42% | 25-50% | -58 | 6 | 0 |
| **overall** | 5-0-7 | 42% | 42% | 25-50% | -58 | 6 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| schooltime | 0-0-2 | 0% | 0% | 2 | 0 |
| big_empty | 1-0-1 | 50% | 50% | 2 | 0 |
| default | 1-0-1 | 50% | 50% | 2 | 0 |
| stronghold | 1-0-1 | 50% | 50% | 2 | 0 |
| Trauma | 1-0-1 | 50% | 50% | 2 | 0 |
| trophy | 1-0-1 | 50% | 50% | 2 | 0 |

no_sonar dragon deaths: hit kelp 757, head-to-head 461, hit other body 356, hit itself 60, no valid action/timeout 6

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-221605-v5-king-safety-0c6649/vs-additive/summary.md

SHA-256: `cd22caf8342900b24a6e1c53e3cbfbb126a00d8d59957a7cc3bb557c9a6becdd`

# safe_king

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 5-0-7 | 42% | 42% | 17-67% | -58 | 6 | 0 |
| **overall** | 5-0-7 | 42% | 42% | 17-67% | -58 | 6 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold | 0-0-2 | 0% | 0% | 2 | 0 |
| trophy | 0-0-2 | 0% | 0% | 2 | 0 |
| big_empty | 1-0-1 | 50% | 50% | 2 | 0 |
| schooltime | 1-0-1 | 50% | 50% | 2 | 0 |
| Trauma | 1-0-1 | 50% | 50% | 2 | 0 |
| default | 2-0-0 | 100% | 100% | 2 | 0 |

safe_king dragon deaths: hit kelp 747, head-to-head 476, hit other body 367, hit itself 68, no valid action/timeout 4

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-221605-v5-king-safety-0c6649/vs-early_king/summary.md

SHA-256: `e2436b5481615c4a36fed087434296b1b6ab39d0b2778dd3c46ebdc8a4a9ff50`

# safe_king

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| early_king | 5-0-7 | 42% | 42% | 25-50% | -58 | 6 | 0 |
| **overall** | 5-0-7 | 42% | 42% | 25-50% | -58 | 6 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 0-0-2 | 0% | 0% | 2 | 0 |
| big_empty | 1-0-1 | 50% | 50% | 2 | 0 |
| default | 1-0-1 | 50% | 50% | 2 | 0 |
| schooltime | 1-0-1 | 50% | 50% | 2 | 0 |
| stronghold | 1-0-1 | 50% | 50% | 2 | 0 |
| trophy | 1-0-1 | 50% | 50% | 2 | 0 |

safe_king dragon deaths: hit kelp 732, head-to-head 450, hit other body 371, hit itself 81, no valid action/timeout 6

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for early_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-222647-v5-king-350-937025/vs-additive/summary.md

SHA-256: `2f909568d56359e68bb938a1ff8a46d49b1e579402b93750f0eea0669b7474cd`

# king_350

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 5-0-7 | 42% | 42% | 17-67% | -58 | 6 | 0 |
| **overall** | 5-0-7 | 42% | 42% | 17-67% | -58 | 6 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold | 0-0-2 | 0% | 0% | 2 | 0 |
| trophy | 0-0-2 | 0% | 0% | 2 | 0 |
| big_empty | 1-0-1 | 50% | 50% | 2 | 0 |
| schooltime | 1-0-1 | 50% | 50% | 2 | 0 |
| Trauma | 1-0-1 | 50% | 50% | 2 | 0 |
| default | 2-0-0 | 100% | 100% | 2 | 0 |

king_350 dragon deaths: hit kelp 733, head-to-head 466, hit other body 339, hit itself 76, no valid action/timeout 4

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-222647-v5-king-350-937025/vs-king_400/summary.md

SHA-256: `6b0395ca130b55f2edc25ca9e9c86c9c498608ed94a047b851f35d44a26db88c`

# king_350

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| king_400 | 7-0-5 | 58% | 58% | 33-83% | +58 | 6 | 0 |
| **overall** | 7-0-5 | 58% | 58% | 33-83% | +58 | 6 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| schooltime | 0-0-2 | 0% | 0% | 2 | 0 |
| default | 1-0-1 | 50% | 50% | 2 | 0 |
| stronghold | 1-0-1 | 50% | 50% | 2 | 0 |
| trophy | 1-0-1 | 50% | 50% | 2 | 0 |
| big_empty | 2-0-0 | 100% | 100% | 2 | 0 |
| Trauma | 2-0-0 | 100% | 100% | 2 | 0 |

king_350 dragon deaths: hit kelp 719, head-to-head 468, hit other body 339, hit itself 83, no valid action/timeout 5

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for king_400: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-223513-v5-king-350-holdout-8687c3/vs-king_400/summary.md

SHA-256: `7f087fc109e7a1189a3099eb019f9b04a7c6eb58b6066bc72dd4934dd8732720`

# king_350

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| king_400 | 5-0-5 | 50% | 50% | 50-50% | -0 | 5 | 0 |
| **overall** | 5-0-5 | 50% | 50% | 50-50% | -0 | 5 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| arena | 1-0-1 | 50% | 50% | 2 | 0 |
| Colosseum | 1-0-1 | 50% | 50% | 2 | 0 |
| default_small | 1-0-1 | 50% | 50% | 2 | 0 |
| queen_of_spades | 1-0-1 | 50% | 50% | 2 | 0 |
| Devil | 1-0-1 | 50% | 50% | 2 | 0 |

king_350 dragon deaths: head-to-head 1312, hit other body 605, hit kelp 500, hit itself 9, no valid action/timeout 4

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for king_400: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-223816-v5-combo-809e43/vs-additive/summary.md

SHA-256: `68d86b5214059e16276d70814da8dfd0136b575174aaa069baaba78c28b439d1`

# scout_king

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 2-0-2 | 50% | 50% | 0-100% | -0 | 2 | 0 |
| **overall** | 2-0-2 | 50% | 50% | 0-100% | -0 | 2 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold | 0-0-2 | 0% | 0% | 2 | 0 |
| Trauma | 2-0-0 | 100% | 100% | 2 | 0 |

scout_king dragon deaths: hit kelp 366, head-to-head 252, hit other body 91, no valid action/timeout 1, hit itself 1

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-223816-v5-combo-809e43/vs-nicked/summary.md

SHA-256: `088227cb9513de2ab85b03f1299d7709dc27db4a01d764afa2452bf6f429389c`

# scout_king

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 0-0-2 | 0% | 0% | 0-100% | -1200 | 1 | 0 |
| **overall** | 0-0-2 | 0% | 0% | 0-100% | -1200 | 1 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 0-0-2 | 0% | 0% | 2 | 0 |

scout_king dragon deaths: hit kelp 264, head-to-head 91, hit other body 8

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for nicked: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-233609-full-change-bb86e5/map_matrix.md

SHA-256: `f87305496c7b4613fd4ed8f0735dd994b25d5eae5715cd4a54f878b9b2a16396`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | additive | v3 | nicked |
|---|---|---|---|
| default_small | 2-0-0 | 2-0-0 | 0-0-2 |
| trophy | 0-0-2 | 1-0-1 | 0-0-2 |
| queen_of_spades | 1-0-1 | 1-0-1 | 0-0-2 |
| default | 2-0-0 | 2-0-0 | 0-0-2 |
| Devil | 1-0-1 | 0-0-2 | 0-0-2 |
| stronghold | 0-0-2 | 1-0-1 | 2-0-0 |
| Trauma | 2-0-0 | 2-0-0 | 0-0-2 |
| schooltime | 2-0-0 | 1-0-1 | 0-0-2 |
| big_empty | 1-0-1 | 2-0-0 | 0-0-2 |
| arena | 2-0-0 | 1-0-1 | 1-0-1 |
| Colosseum | 2-0-0 | 1-0-1 | 2-0-0 |


---

## results/20260924-233609-full-change-bb86e5/full/summary.md

SHA-256: `5eec740539f61038cbeaed603231cc7b47aeddddd3dba54689146f9d714d4eb6`

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


---

## results/20260924-235440-v5-portal-probe-b63cb1/diagnostic/summary.md

SHA-256: `fb15ae9202a1acab0734680d0f8930797cd468ff3780cb36c1d177faedbbc541`

# portal_push

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 0-0-6 | 0% | 0% | 0-0% | -1200 | 3 | 0 |
| **overall** | 0-0-6 | 0% | 0% | 0-0% | -1200 | 3 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 0-0-2 | 0% | 0% | 2 | 0 |
| default | 0-0-2 | 0% | 0% | 2 | 0 |
| queen_of_spades | 0-0-2 | 0% | 0% | 2 | 0 |

portal_push dragon deaths: hit kelp 383, head-to-head 216, hit other body 42

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for nicked: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260924-235840-full-change-a01a46/map_matrix.md

SHA-256: `961ad4cd5484a2f0fab161f9e2b9e4479c80d8724f73e66c2b80f8b6bcd82553`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | scout_king | additive | nicked |
|---|---|---|---|
| default_small | 1-0-1 | 2-0-0 | 0-0-2 |
| trophy | 2-0-0 | 1-0-1 | 0-0-2 |
| queen_of_spades | 1-0-1 | 1-0-1 | 0-0-2 |
| default | 2-0-0 | 2-0-0 | 0-0-2 |
| Devil | 1-0-1 | 1-0-1 | 0-0-2 |
| stronghold | 1-0-1 | 2-0-0 | 0-0-2 |
| Trauma | 0-0-2 | 0-0-2 | 0-0-2 |
| schooltime | 0-0-2 | 1-0-1 | 0-0-2 |
| big_empty | 1-0-1 | 1-0-1 | 0-0-2 |
| arena | 1-0-1 | 2-0-0 | 1-0-1 |
| Colosseum | 0-0-2 | 0-0-2 | 2-0-0 |


---

## results/20260924-235840-full-change-a01a46/completed/summary.md

SHA-256: `404b56db32ae5e2d81264e02feb4e4671b37ca279346b8ee83a56d2f6479dee4`

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


---

## results/20260925-001144-v5-trap-probe-047e50/diagnostic/summary.md

SHA-256: `6543be56cd348a9e4a5a1b3c3eda94b3ba5a32ae868190e163baf5e4d8458ed3`

# trap_guard

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 0-0-4 | 0% | 0% | 0-0% | -1200 | 2 | 0 |
| **overall** | 0-0-4 | 0% | 0% | 0-0% | -1200 | 2 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default_small | 0-0-2 | 0% | 0% | 2 | 0 |
| Trauma | 0-0-2 | 0% | 0% | 2 | 0 |

trap_guard dragon deaths: hit kelp 361, head-to-head 154, hit other body 25

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for nicked: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-001343-full-change-a0dc40/map_matrix.md

SHA-256: `0699d630545b9e716a35910ec18c9156748725b71ea9d35002313b2958e6fdb1`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | scout_king | additive | nicked |
|---|---|---|---|
| default_small | 1-0-1 | 0-0-2 | 0-0-2 |
| trophy | 0-0-2 | 0-0-2 | 0-0-2 |
| queen_of_spades | 2-0-0 | 1-0-1 | 0-0-2 |
| default | 1-0-1 | 1-0-1 | 0-0-2 |
| Devil | 2-0-0 | 2-0-0 | 0-0-2 |
| stronghold | 1-0-1 | 2-0-0 | 1-0-1 |
| Trauma | 2-0-0 | 2-0-0 | 0-0-2 |
| schooltime | 2-0-0 | 1-0-1 | 0-0-2 |
| big_empty | 0-0-2 | 1-0-1 | 0-0-2 |
| arena | 0-0-2 | 0-0-2 | 0-0-2 |
| Colosseum | 1-0-1 | 2-0-0 | 2-0-0 |


---

## results/20260925-001343-full-change-a0dc40/completed/summary.md

SHA-256: `056fb4f9449f9675b311ac269b6b0119873c5c9ee11b9c713a4ac6e5eacdd50f`

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


---

## results/20260925-112740-v5-economy-probe-6fd266/diagnostic/summary.md

SHA-256: `f02b0df9dd43d4004251fbccb6800232379ce0c2e1501dec871bc77620322b6c`

# economy

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 0-0-6 | 0% | 0% | 0-0% | -1200 | 3 | 0 |
| **overall** | 0-0-6 | 0% | 0% | 0-0% | -1200 | 3 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Default | 0-0-2 | 0% | 0% | 2 | 0 |
| schooltime | 0-0-2 | 0% | 0% | 2 | 0 |
| Big_Empty | 0-0-2 | 0% | 0% | 2 | 0 |

economy dragon deaths: hit kelp 417, head-to-head 372, hit other body 245, hit itself 47

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for nicked: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-113359-full-change-053960/map_matrix.md

SHA-256: `837c9cf1b622219bb211794692f37b40d8ef0e394573c22135e5e56851d668c6`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | scout_king | additive | nicked |
|---|---|---|---|
| default_small | 0-0-2 | 0-0-2 | 0-0-2 |
| trophy | 0-0-2 | 2-0-0 | 0-0-2 |
| queen_of_spades | 2-0-0 | 1-0-1 | 0-0-2 |
| default | 2-0-0 | 2-0-0 | 0-0-2 |
| Devil | 1-0-1 | 1-0-1 | 0-0-2 |
| stronghold | 0-0-2 | 0-0-2 | 0-0-2 |
| Trauma | 1-0-1 | 0-0-2 | 0-0-2 |
| schooltime | 1-0-1 | 0-0-2 | 0-0-2 |
| big_empty | 1-0-1 | 0-0-2 | 0-0-2 |
| arena | 1-0-1 | 2-0-0 | 0-0-2 |
| Colosseum | 2-0-0 | 0-0-2 | 1-0-1 |


---

## results/20260925-113359-full-change-053960/full/summary.md

SHA-256: `9aa136276016d265b33bb73c6780dcd1b07a6bec6ab84fd46610027c554877b6`

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


---

## results/20260925-114617-v5-queen-probe-733bcb/diagnostic/summary.md

SHA-256: `ccaafcd06f77236a46359338dc020b340ba6282c26cac17f20a4a3d5d3e1c1d7`

# queen_opening

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 0-0-2 | 0% | 0% | 0-100% | -1200 | 1 | 0 |
| **overall** | 0-0-2 | 0% | 0% | 0-100% | -1200 | 1 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades | 0-0-2 | 0% | 0% | 2 | 0 |

queen_opening dragon deaths: hit kelp 10, head-to-head 7

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for nicked: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-114822-v5-queen-probe-977acd/diagnostic/summary.md

SHA-256: `04b30f2e0e48ad6b4e2feca88d29d37f503b04ad457f5a338a89916a4934d2f1`

# queen_opening

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 0-0-2 | 0% | 0% | 0-100% | -1200 | 1 | 0 |
| **overall** | 0-0-2 | 0% | 0% | 0-100% | -1200 | 1 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades | 0-0-2 | 0% | 0% | 2 | 0 |

queen_opening dragon deaths: hit kelp 12, head-to-head 3

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for nicked: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-114947-full-change-08d46d/map_matrix.md

SHA-256: `d2ae6e3e87ae1399a0bd857a1e1573c5b87c1a1db1b05b631b3cde24ddcb7582`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | scout_king | additive | nicked |
|---|---|---|---|
| default_small | 1-0-1 | 2-0-0 | 0-0-2 |
| trophy | 1-0-1 | 0-0-2 | 0-0-2 |
| queen_of_spades | 0-0-2 | 0-0-2 | 0-0-2 |
| default | 1-0-1 | 2-0-0 | 0-0-2 |
| Devil | 1-0-1 | 1-0-1 | 0-0-2 |
| stronghold | 1-0-1 | 0-0-2 | 2-0-0 |
| Trauma | 1-0-1 | 2-0-0 | 0-0-2 |
| schooltime | 1-0-1 | 2-0-0 | 0-0-2 |
| big_empty | 1-0-1 | 1-0-1 | 0-0-2 |
| arena | 1-0-1 | 2-0-0 | 1-0-1 |
| Colosseum | 1-0-1 | 2-0-0 | 2-0-0 |


---

## results/20260925-114947-full-change-08d46d/full/summary.md

SHA-256: `2ba57536d5ceeb9305e256f1731fcb44985391daac7ff803883f0dc8ea4e4036`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 14-0-8 | 64% | 64% | 36-86% | +97 | 11 | 0 |
| nicked | 5-0-17 | 23% | 23% | 0-50% | -213 | 11 | 0 |
| scout_king | 10-0-12 | 45% | 45% | 36-50% | -32 | 11 | 0 |
| **overall** | 29-0-37 | 44% | 44% | 30-58% | -42 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades | 0-0-6 | 0% | 0% | 6 | 0 |
| trophy | 1-0-5 | 17% | 17% | 6 | 0 |
| Devil | 2-0-4 | 33% | 33% | 6 | 0 |
| big_empty | 2-0-4 | 33% | 33% | 6 | 0 |
| default_small | 3-0-3 | 50% | 50% | 6 | 0 |
| default | 3-0-3 | 50% | 50% | 6 | 0 |
| Trauma | 3-0-3 | 50% | 50% | 6 | 0 |
| stronghold | 3-0-3 | 50% | 50% | 6 | 0 |
| schooltime | 3-0-3 | 50% | 50% | 6 | 0 |
| arena | 4-0-2 | 67% | 67% | 6 | 0 |
| Colosseum | 5-0-1 | 83% | 83% | 6 | 0 |

candidate dragon deaths: head-to-head 5299, hit kelp 4524, hit other body 2744, hit itself 204, no valid action/timeout 31

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, scout_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-115752-v5-head-probe-5daac8/diagnostic/summary.md

SHA-256: `b536fd83d9daea72397cba48b92826e99e8b1d506d82d7b149ec2a19ab80e99d`

# head_guard

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 1-0-3 | 25% | 25% | 0-50% | -191 | 2 | 0 |
| **overall** | 1-0-3 | 25% | 25% | 0-50% | -191 | 2 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 0-0-2 | 0% | 0% | 2 | 0 |
| default_small | 1-0-1 | 50% | 50% | 2 | 0 |

head_guard dragon deaths: hit kelp 295, head-to-head 148, hit other body 64, no valid action/timeout 4, hit itself 1

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for nicked: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-115956-full-change-cb0cd7/map_matrix.md

SHA-256: `c56be2bdd4e6606452eb27e631f0ba3572becc324c48144be7afd15e2c4df734`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | scout_king | additive | nicked |
|---|---|---|---|
| default_small | 1-0-1 | 2-0-0 | 1-0-1 |
| trophy | 1-0-1 | 0-0-2 | 0-0-2 |
| queen_of_spades | 1-0-1 | 1-0-1 | 0-0-2 |
| default | 2-0-0 | 2-0-0 | 0-0-2 |
| Devil | 1-0-1 | 1-0-1 | 0-0-2 |
| stronghold | 0-0-2 | 1-0-1 | 1-0-1 |
| Trauma | 0-0-2 | 1-0-1 | 0-0-2 |
| schooltime | 1-0-1 | 2-0-0 | 0-0-2 |
| big_empty | 2-0-0 | 1-0-1 | 0-0-2 |
| arena | 1-0-1 | 1-0-1 | 0-0-2 |
| Colosseum | 2-0-0 | 2-0-0 | 2-0-0 |


---

## results/20260925-115956-full-change-cb0cd7/full/summary.md

SHA-256: `1cbee9cd0e0c9c7ff11c3c9439b4ec58b659e1706a7c2206f0630398aad0292b`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 14-0-8 | 64% | 64% | 45-82% | +97 | 11 | 0 |
| nicked | 4-0-18 | 18% | 18% | 0-41% | -261 | 11 | 0 |
| scout_king | 12-0-10 | 55% | 55% | 36-73% | +32 | 11 | 0 |
| **overall** | 30-0-36 | 45% | 45% | 33-59% | -32 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| trophy | 1-0-5 | 17% | 17% | 6 | 0 |
| Trauma | 1-0-5 | 17% | 17% | 6 | 0 |
| queen_of_spades | 2-0-4 | 33% | 33% | 6 | 0 |
| Devil | 2-0-4 | 33% | 33% | 6 | 0 |
| stronghold | 2-0-4 | 33% | 33% | 6 | 0 |
| arena | 2-0-4 | 33% | 33% | 6 | 0 |
| schooltime | 3-0-3 | 50% | 50% | 6 | 0 |
| big_empty | 3-0-3 | 50% | 50% | 6 | 0 |
| default_small | 4-0-2 | 67% | 67% | 6 | 0 |
| default | 4-0-2 | 67% | 67% | 6 | 0 |
| Colosseum | 6-0-0 | 100% | 100% | 6 | 0 |

candidate dragon deaths: head-to-head 5178, hit kelp 4567, hit other body 2832, hit itself 251, no valid action/timeout 35

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, scout_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-121905-v5-explore-probe-5971fb/diagnostic/summary.md

SHA-256: `0fb7e7c6cd6b8013e2d76b72d351af79174e207fef27a1823381ff33bf50215e`

# exploration

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 0-0-4 | 0% | 0% | 0-0% | -1200 | 2 | 0 |
| **overall** | 0-0-4 | 0% | 0% | 0-0% | -1200 | 2 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Default | 0-0-2 | 0% | 0% | 2 | 0 |
| queen_of_spades | 0-0-2 | 0% | 0% | 2 | 0 |

exploration dragon deaths: head-to-head 36, hit other body 21, hit kelp 9

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for nicked: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-122111-full-change-0499e5/map_matrix.md

SHA-256: `120b9e7a6cd840fbd41b1ca8d0ef75ea9af76a215f8002d4eabdd811b52fbfd5`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | scout_king | additive | nicked |
|---|---|---|---|
| default_small | 1-0-1 | 2-0-0 | 2-0-0 |
| trophy | 0-0-2 | 0-0-2 | 0-0-2 |
| queen_of_spades | 0-0-2 | 1-0-1 | 0-0-2 |
| default | 0-0-2 | 0-0-2 | 0-0-2 |
| Devil | 0-0-2 | 0-0-2 | 0-0-2 |
| stronghold | 0-0-2 | 2-0-0 | 0-0-2 |
| Trauma | 1-0-1 | 2-0-0 | 1-0-1 |
| schooltime | 1-0-1 | 2-0-0 | 0-0-2 |
| big_empty | 1-0-1 | 1-0-1 | 0-0-2 |
| arena | 2-0-0 | 2-0-0 | 0-0-2 |
| Colosseum | 1-0-1 | 0-0-2 | 2-0-0 |


---

## results/20260925-122111-full-change-0499e5/full/summary.md

SHA-256: `339c9ec7cce2075cf85d6c8edd28d7e577355f9706218b9d45bd3c09ec92e099`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 12-0-10 | 55% | 55% | 27-82% | +32 | 11 | 0 |
| nicked | 5-0-17 | 23% | 23% | 0-50% | -213 | 11 | 0 |
| scout_king | 7-0-15 | 32% | 32% | 14-50% | -132 | 11 | 0 |
| **overall** | 24-0-42 | 36% | 36% | 23-52% | -97 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| trophy | 0-0-6 | 0% | 0% | 6 | 0 |
| Devil | 0-0-6 | 0% | 0% | 6 | 0 |
| default | 0-0-6 | 0% | 0% | 6 | 0 |
| queen_of_spades | 1-0-5 | 17% | 17% | 6 | 0 |
| stronghold | 2-0-4 | 33% | 33% | 6 | 0 |
| big_empty | 2-0-4 | 33% | 33% | 6 | 0 |
| Colosseum | 3-0-3 | 50% | 50% | 6 | 0 |
| schooltime | 3-0-3 | 50% | 50% | 6 | 0 |
| Trauma | 4-0-2 | 67% | 67% | 6 | 0 |
| arena | 4-0-2 | 67% | 67% | 6 | 0 |
| default_small | 5-0-1 | 83% | 83% | 6 | 0 |

candidate dragon deaths: head-to-head 5070, hit kelp 4812, hit other body 2802, hit itself 262, no valid action/timeout 38

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, scout_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-122956-v5-population-probe-079b04/diagnostic/summary.md

SHA-256: `ee1dcbf1953b3988e3b327891fc0793814e500af254a26b56e4ad833d01bc92e`

# population

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 0-0-4 | 0% | 0% | 0-0% | -1200 | 2 | 0 |
| **overall** | 0-0-4 | 0% | 0% | 0-0% | -1200 | 2 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Big_Empty | 0-0-2 | 0% | 0% | 2 | 0 |
| schooltime | 0-0-2 | 0% | 0% | 2 | 0 |

population dragon deaths: hit kelp 384, head-to-head 154, hit other body 148, hit itself 48

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for nicked: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-123353-full-change-4c85a0/map_matrix.md

SHA-256: `3d52a5b1d6af4bb562933f12d1bd4563a49314c287525a0252262ebbe1ccb81f`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | scout_king | additive | nicked |
|---|---|---|---|
| default_small | 1-0-1 | 2-0-0 | 0-0-2 |
| trophy | 1-0-1 | 0-0-2 | 0-0-2 |
| queen_of_spades | 1-0-1 | 1-0-1 | 0-0-2 |
| default | 1-0-1 | 2-0-0 | 0-0-2 |
| Devil | 1-0-1 | 1-0-1 | 0-0-2 |
| stronghold | 1-0-1 | 0-0-2 | 2-0-0 |
| Trauma | 1-0-1 | 2-0-0 | 0-0-2 |
| schooltime | 2-0-0 | 0-0-2 | 0-0-2 |
| big_empty | 1-0-1 | 0-0-2 | 0-0-2 |
| arena | 1-0-1 | 2-0-0 | 1-0-1 |
| Colosseum | 1-0-1 | 2-0-0 | 2-0-0 |


---

## results/20260925-123353-full-change-4c85a0/full/summary.md

SHA-256: `36aa7a88e9d9eceb569bedb75a4aa23f2f22792a9a57daccc8e9ed86166c318b`

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


---

## results/20260925-132108-v6-g0-791c56/g0/summary.md

SHA-256: `2aff64052ff854747c0ab89704e5e4b3de89d3f98ec3b0a91d041dfa0b559d00`

# v6

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 6-0-4 | 60% | 60% | 30-90% | +70 | 5 | 0 |
| **overall** | 6-0-4 | 60% | 60% | 30-90% | +70 | 5 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades | 0-0-2 | 0% | 0% | 2 | 0 |
| default_small | 1-0-1 | 50% | 50% | 2 | 0 |
| trophy | 1-0-1 | 50% | 50% | 2 | 0 |
| Devil | 2-0-0 | 100% | 100% | 2 | 0 |
| big_empty | 2-0-0 | 100% | 100% | 2 | 0 |

v6 dragon deaths: head-to-head 665, hit kelp 547, hit other body 483, no valid action/timeout 253, hit itself 8

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for nicked: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-132931-full-change-982835/map_matrix.md

SHA-256: `3cd56a75e2b41323abd801f25da55fbc73c707e09b65869ce74ec69350bae6aa`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | scout_king | additive | nicked |
|---|---|---|---|
| default_small | 2-0-0 | 2-0-0 | 1-0-1 |
| trophy | 2-0-0 | 2-0-0 | 1-0-1 |
| queen_of_spades | 2-0-0 | 2-0-0 | 0-0-2 |
| default | 2-0-0 | 2-0-0 | 2-0-0 |
| Devil | 2-0-0 | 1-0-1 | 1-0-1 |
| stronghold | 0-0-2 | 0-0-2 | 0-0-2 |
| Trauma | 0-0-2 | 0-0-2 | 0-0-2 |
| schooltime | 2-0-0 | 2-0-0 | 1-0-1 |
| big_empty | 2-0-0 | 2-0-0 | 2-0-0 |
| arena | 2-0-0 | 2-0-0 | 2-0-0 |
| Colosseum | 1-0-1 | 2-0-0 | 2-0-0 |


---

## results/20260925-132931-full-change-982835/full/summary.md

SHA-256: `625511f24283e9042173f25bf1c026ddfec8f3af96e11a071178716de6cbb1c1`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 17-0-5 | 77% | 77% | 50-95% | +213 | 11 | 0 |
| nicked | 12-0-10 | 55% | 55% | 27-77% | +32 | 11 | 0 |
| scout_king | 17-0-5 | 77% | 77% | 55-100% | +213 | 11 | 0 |
| **overall** | 46-0-20 | 70% | 70% | 56-83% | +145 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 0-0-6 | 0% | 0% | 6 | 0 |
| stronghold | 0-0-6 | 0% | 0% | 6 | 0 |
| queen_of_spades | 4-0-2 | 67% | 67% | 6 | 0 |
| Devil | 4-0-2 | 67% | 67% | 6 | 0 |
| default_small | 5-0-1 | 83% | 83% | 6 | 0 |
| trophy | 5-0-1 | 83% | 83% | 6 | 0 |
| Colosseum | 5-0-1 | 83% | 83% | 6 | 0 |
| schooltime | 5-0-1 | 83% | 83% | 6 | 0 |
| default | 6-0-0 | 100% | 100% | 6 | 0 |
| arena | 6-0-0 | 100% | 100% | 6 | 0 |
| big_empty | 6-0-0 | 100% | 100% | 6 | 0 |

candidate dragon deaths: head-to-head 3034, hit kelp 2901, hit other body 2484, no valid action/timeout 1960, hit itself 20

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, scout_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-165427-full-change-6aff76/map_matrix.md

SHA-256: `12e51b305315324606fdb4633f3c15e32d72e0c840a2f2879e98f71a1d64dba8`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | scout_king | additive | nicked |
|---|---|---|---|
| default_small | 2-0-0 | 2-0-0 | 1-0-1 |
| trophy | 1-0-1 | 2-0-0 | 1-0-1 |
| queen_of_spades | 2-0-0 | 2-0-0 | 0-0-2 |
| default | 2-0-0 | 2-0-0 | 1-0-1 |
| Devil | 2-0-0 | 1-0-1 | 2-0-0 |
| stronghold | 0-0-2 | 0-0-2 | 0-0-2 |
| Trauma | 0-0-2 | 0-0-2 | 0-0-2 |
| schooltime | 2-0-0 | 2-0-0 | 1-0-1 |
| big_empty | 2-0-0 | 2-0-0 | 2-0-0 |
| arena | 2-0-0 | 2-0-0 | 2-0-0 |
| Colosseum | 2-0-0 | 2-0-0 | 2-0-0 |


---

## results/20260925-165427-full-change-6aff76/full/summary.md

SHA-256: `01732f6ea9743ea32c03e4cac3d90205b3a23aaa50ad0181d3a0d3d41ba5717b`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 17-0-5 | 77% | 77% | 55-100% | +213 | 11 | 0 |
| nicked | 12-0-10 | 55% | 55% | 32-77% | +32 | 11 | 0 |
| scout_king | 17-0-5 | 77% | 77% | 55-100% | +213 | 11 | 0 |
| **overall** | 46-0-20 | 70% | 70% | 56-83% | +145 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 0-0-6 | 0% | 0% | 6 | 0 |
| stronghold | 0-0-6 | 0% | 0% | 6 | 0 |
| queen_of_spades | 4-0-2 | 67% | 67% | 6 | 0 |
| trophy | 4-0-2 | 67% | 67% | 6 | 0 |
| default_small | 5-0-1 | 83% | 83% | 6 | 0 |
| Devil | 5-0-1 | 83% | 83% | 6 | 0 |
| default | 5-0-1 | 83% | 83% | 6 | 0 |
| schooltime | 5-0-1 | 83% | 83% | 6 | 0 |
| arena | 6-0-0 | 100% | 100% | 6 | 0 |
| Colosseum | 6-0-0 | 100% | 100% | 6 | 0 |
| big_empty | 6-0-0 | 100% | 100% | 6 | 0 |

candidate dragon deaths: head-to-head 3455, hit kelp 3128, hit other body 2836, no valid action/timeout 2269, hit itself 10

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, scout_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-170438-full-change-1b70b0/map_matrix.md

SHA-256: `a30ef767fa60add452ce14ac903efdb87b14ba90aabb7138a21e7729f6902129`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | scout_king | additive | nicked |
|---|---|---|---|
| default_small | 2-0-0 | 2-0-0 | 1-0-1 |
| trophy | 1-0-1 | 2-0-0 | 2-0-0 |
| queen_of_spades | 2-0-0 | 2-0-0 | 0-0-2 |
| default | 2-0-0 | 2-0-0 | 0-0-2 |
| Devil | 2-0-0 | 1-0-1 | 2-0-0 |
| stronghold | 0-0-2 | 0-0-2 | 0-0-2 |
| Trauma | 0-0-2 | 1-0-1 | 0-0-2 |
| schooltime | 2-0-0 | 2-0-0 | 2-0-0 |
| big_empty | 2-0-0 | 2-0-0 | 2-0-0 |
| arena | 2-0-0 | 2-0-0 | 2-0-0 |
| Colosseum | 2-0-0 | 2-0-0 | 2-0-0 |


---

## results/20260925-170438-full-change-1b70b0/full/summary.md

SHA-256: `2a8b1176ca8f7dd1ca784b44f20b095ee1a7a00919220176702c9c5408d2e92e`

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


---

## results/20260925-172503-full-change-de9339/map_matrix.md

SHA-256: `c77ecdedc98001290f0a5c7bc8b39bdba0225394a89ccde3d025efc74bf4ae87`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | scout_king | additive | nicked |
|---|---|---|---|
| default_small | 2-0-0 | 2-0-0 | 1-0-1 |
| trophy | 1-0-1 | 2-0-0 | 1-0-1 |
| queen_of_spades | 2-0-0 | 2-0-0 | 0-0-2 |
| default | 2-0-0 | 2-0-0 | 1-0-1 |
| Devil | 2-0-0 | 1-0-1 | 2-0-0 |
| stronghold | 0-0-2 | 0-0-2 | 0-0-2 |
| Trauma | 0-0-2 | 0-0-2 | 0-0-2 |
| schooltime | 2-0-0 | 2-0-0 | 2-0-0 |
| big_empty | 2-0-0 | 2-0-0 | 2-0-0 |
| arena | 2-0-0 | 2-0-0 | 2-0-0 |
| Colosseum | 2-0-0 | 2-0-0 | 2-0-0 |


---

## results/20260925-172503-full-change-de9339/full/summary.md

SHA-256: `a46adba1c4c1bbb43be5d955ee81377503ab47b1dfac5cc9e12861262dbc156c`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 17-0-5 | 77% | 77% | 55-100% | +213 | 11 | 0 |
| nicked | 13-0-9 | 59% | 59% | 36-82% | +64 | 11 | 0 |
| scout_king | 17-0-5 | 77% | 77% | 55-100% | +213 | 11 | 0 |
| **overall** | 47-0-19 | 71% | 71% | 58-85% | +157 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 0-0-6 | 0% | 0% | 6 | 0 |
| stronghold | 0-0-6 | 0% | 0% | 6 | 0 |
| queen_of_spades | 4-0-2 | 67% | 67% | 6 | 0 |
| trophy | 4-0-2 | 67% | 67% | 6 | 0 |
| default_small | 5-0-1 | 83% | 83% | 6 | 0 |
| default | 5-0-1 | 83% | 83% | 6 | 0 |
| Devil | 5-0-1 | 83% | 83% | 6 | 0 |
| arena | 6-0-0 | 100% | 100% | 6 | 0 |
| Colosseum | 6-0-0 | 100% | 100% | 6 | 0 |
| schooltime | 6-0-0 | 100% | 100% | 6 | 0 |
| big_empty | 6-0-0 | 100% | 100% | 6 | 0 |

candidate dragon deaths: head-to-head 3506, hit kelp 3026, hit other body 2838, no valid action/timeout 2186, hit itself 18

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, scout_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-174256-full-change-ac5a2a/map_matrix.md

SHA-256: `bc5c56a18e25a6f3335a1ff5d652f04f18ce228381959140abc8a58094e92943`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | scout_king | additive | nicked |
|---|---|---|---|
| default_small | 2-0-0 | 2-0-0 | 1-0-1 |
| trophy | 2-0-0 | 2-0-0 | 2-0-0 |
| queen_of_spades | 1-0-1 | 1-0-1 | 0-0-2 |
| default | 2-0-0 | 2-0-0 | 0-0-2 |
| Devil | 2-0-0 | 2-0-0 | 2-0-0 |
| stronghold | 0-0-2 | 0-0-2 | 0-0-2 |
| Trauma | 0-0-2 | 1-0-1 | 0-0-2 |
| schooltime | 2-0-0 | 2-0-0 | 1-0-1 |
| big_empty | 2-0-0 | 2-0-0 | 1-0-1 |
| arena | 2-0-0 | 2-0-0 | 2-0-0 |
| Colosseum | 2-0-0 | 2-0-0 | 2-0-0 |


---

## results/20260925-174256-full-change-ac5a2a/full/summary.md

SHA-256: `a1e73b12c493993f143d60922bfb29e4646f6dd7b475878e00a784b25aba2bab`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 18-0-4 | 82% | 82% | 59-100% | +261 | 11 | 0 |
| nicked | 11-0-11 | 50% | 50% | 27-73% | -0 | 11 | 0 |
| scout_king | 17-0-5 | 77% | 77% | 50-100% | +213 | 11 | 0 |
| **overall** | 46-0-20 | 70% | 70% | 55-83% | +145 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold | 0-0-6 | 0% | 0% | 6 | 0 |
| Trauma | 1-0-5 | 17% | 17% | 6 | 0 |
| queen_of_spades | 2-0-4 | 33% | 33% | 6 | 0 |
| default | 4-0-2 | 67% | 67% | 6 | 0 |
| default_small | 5-0-1 | 83% | 83% | 6 | 0 |
| schooltime | 5-0-1 | 83% | 83% | 6 | 0 |
| big_empty | 5-0-1 | 83% | 83% | 6 | 0 |
| Devil | 6-0-0 | 100% | 100% | 6 | 0 |
| trophy | 6-0-0 | 100% | 100% | 6 | 0 |
| arena | 6-0-0 | 100% | 100% | 6 | 0 |
| Colosseum | 6-0-0 | 100% | 100% | 6 | 0 |

candidate dragon deaths: head-to-head 3761, hit other body 3203, hit kelp 3128, no valid action/timeout 2082, hit itself 10

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, scout_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-182609-full-change-a85586/map_matrix.md

SHA-256: `0fedeb09abbe6ce8b903dbd18bbf3e8e75c31eb45f1f956c70b5e96827820610`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | scout_king | additive | nicked |
|---|---|---|---|
| default_small | 0-0-2 | 0-0-2 | 0-0-2 |
| trophy | 0-0-2 | 0-0-2 | 0-0-2 |
| queen_of_spades | 0-0-2 | 0-0-2 | 0-0-2 |
| default | 0-0-2 | 0-0-2 | 0-0-2 |
| Devil | 0-0-2 | 0-0-2 | 0-0-2 |
| stronghold | 1-0-1 | 0-0-2 | 0-0-2 |
| Trauma | 0-0-2 | 0-0-2 | 0-0-2 |
| schooltime | 0-0-2 | 0-0-2 | 0-0-2 |
| big_empty | 0-0-2 | 0-0-2 | 0-0-2 |
| arena | 1-0-1 | 1-0-1 | 0-0-2 |
| Colosseum | 0-0-2 | 0-0-2 | 0-0-2 |


---

## results/20260925-182609-full-change-a85586/full/summary.md

SHA-256: `4408cf3e88789d2792fe9d254481a8ace5ff15a77890cf90c50d301699927a8a`

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


---

## results/20260925-182711-full-change-1505bb/map_matrix.md

SHA-256: `714b2cd6865c68976c7174d640d5a2702910a9434a595a7cd7458094275c94ba`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | scout_king | additive | nicked |
|---|---|---|---|
| default_small | 0-0-2 | 0-0-2 | 0-0-2 |
| trophy | 0-0-2 | 0-0-2 | 0-0-2 |
| queen_of_spades | 0-0-2 | 0-0-2 | 0-0-2 |
| default | 0-0-2 | 0-0-2 | 0-0-2 |
| Devil | 0-0-2 | 0-0-2 | 0-0-2 |
| stronghold | 0-0-2 | 0-0-2 | 0-0-2 |
| Trauma | 0-0-2 | 0-0-2 | 0-0-2 |
| schooltime | 0-0-2 | 0-0-2 | 0-0-2 |
| big_empty | 0-0-2 | 0-0-2 | 0-0-2 |
| arena | 1-0-1 | 1-0-1 | 0-0-2 |
| Colosseum | 0-0-2 | 0-0-2 | 0-0-2 |


---

## results/20260925-182711-full-change-1505bb/full/summary.md

SHA-256: `107841adf0d94ca79fcff3adac1b43f8a6525e422420b5b373f4670c40ae79d7`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 1-0-21 | 5% | 5% | 0-14% | -529 | 11 | 0 |
| nicked | 0-0-22 | 0% | 0% | 0-0% | -1200 | 11 | 0 |
| scout_king | 1-0-21 | 5% | 5% | 0-14% | -529 | 11 | 0 |
| **overall** | 2-0-64 | 3% | 3% | 0-8% | -602 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades | 0-0-6 | 0% | 0% | 6 | 0 |
| default_small | 0-0-6 | 0% | 0% | 6 | 0 |
| Devil | 0-0-6 | 0% | 0% | 6 | 0 |
| Trauma | 0-0-6 | 0% | 0% | 6 | 0 |
| trophy | 0-0-6 | 0% | 0% | 6 | 0 |
| default | 0-0-6 | 0% | 0% | 6 | 0 |
| stronghold | 0-0-6 | 0% | 0% | 6 | 0 |
| Colosseum | 0-0-6 | 0% | 0% | 6 | 0 |
| schooltime | 0-0-6 | 0% | 0% | 6 | 0 |
| big_empty | 0-0-6 | 0% | 0% | 6 | 0 |
| arena | 2-0-4 | 33% | 33% | 6 | 0 |

candidate dragon deaths: head-to-head 1596, hit other body 1292, hit kelp 887, no valid action/timeout 237

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, scout_king: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-184725-full-change-858372/map_matrix.md

SHA-256: `c815dbf24954a8516df51ead0208ee423d321e69dcbeb108d8a9d3f8a11358d9`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | scout_king | additive | nicked |
|---|---|---|---|
| default_small | 2-0-0 | 2-0-0 | 1-0-1 |
| trophy | 1-0-1 | 2-0-0 | 1-0-1 |
| queen_of_spades | 1-0-1 | 1-0-1 | 0-0-2 |
| default | 2-0-0 | 2-0-0 | 1-0-1 |
| Devil | 2-0-0 | 2-0-0 | 2-0-0 |
| stronghold | 0-0-2 | 0-0-2 | 0-0-2 |
| Trauma | 0-0-2 | 0-0-2 | 0-0-2 |
| schooltime | 2-0-0 | 2-0-0 | 2-0-0 |
| big_empty | 2-0-0 | 2-0-0 | 1-0-1 |
| arena | 2-0-0 | 2-0-0 | 2-0-0 |
| Colosseum | 2-0-0 | 2-0-0 | 2-0-0 |


---

## results/20260925-184725-full-change-858372/full/summary.md

SHA-256: `a963e943b87392f85bd1232d953ea22503e552db197d111d81ab088cc475a5bf`

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


---

## results/20260925-190333-full-change-62d036/map_matrix.md

SHA-256: `93f81afcf583f082c58da759131e5107361614d8aec2cf4438a4df21cc4cef70`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | v3 | ctmes | nicked_v44 |
|---|---|---|---|
| default_small | 2-0-0 | 2-0-0 | 2-0-0 |
| trophy | 1-0-1 | 1-0-1 | 0-0-2 |
| queen_of_spades | 1-0-1 | 2-0-0 | 0-0-2 |
| default | 2-0-0 | 2-0-0 | 1-0-1 |
| Devil | 2-0-0 | 2-0-0 | 2-0-0 |
| stronghold | 0-0-2 | 0-0-2 | 0-0-2 |
| Trauma | 0-0-2 | 0-0-2 | 0-0-2 |
| schooltime | 2-0-0 | 2-0-0 | 0-0-2 |
| big_empty | 2-0-0 | 2-0-0 | 0-0-2 |
| arena | 2-0-0 | 2-0-0 | 0-0-2 |
| Colosseum | 2-0-0 | 2-0-0 | 2-0-0 |


---

## results/20260925-190333-full-change-62d036/full/summary.md

SHA-256: `e41de067be47daf056e83a4f5f623f82269dd33a87c1af0e206478c26c2618ec`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| ctmes | 17-0-5 | 77% | 77% | 50-100% | +213 | 11 | 0 |
| nicked_v44 | 7-0-15 | 32% | 32% | 9-59% | -132 | 11 | 0 |
| v3 | 16-0-6 | 73% | 73% | 50-91% | +170 | 11 | 0 |
| **overall** | 40-0-26 | 61% | 61% | 45-77% | +75 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 0-0-6 | 0% | 0% | 6 | 0 |
| stronghold | 0-0-6 | 0% | 0% | 6 | 0 |
| trophy | 2-0-4 | 33% | 33% | 6 | 0 |
| queen_of_spades | 3-0-3 | 50% | 50% | 6 | 0 |
| arena | 4-0-2 | 67% | 67% | 6 | 0 |
| schooltime | 4-0-2 | 67% | 67% | 6 | 0 |
| big_empty | 4-0-2 | 67% | 67% | 6 | 0 |
| default | 5-0-1 | 83% | 83% | 6 | 0 |
| default_small | 6-0-0 | 100% | 100% | 6 | 0 |
| Devil | 6-0-0 | 100% | 100% | 6 | 0 |
| Colosseum | 6-0-0 | 100% | 100% | 6 | 0 |

candidate dragon deaths: hit kelp 3116, head-to-head 3011, hit other body 2610, no valid action/timeout 2445, hit itself 5

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for ctmes, nicked_v44, v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-191302-full-change-a71535/map_matrix.md

SHA-256: `51e2eaa5ad19e1f6e36158859aec9f1971ef2435b90135fdbfa32ae55deda881`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | v6-fair-search-bot | additive | nicked | v3 | ctmes | nicked_v44 |
|---|---|---|---|---|---|---|
| default_small | 2-0-0 | 2-0-0 | 1-0-1 | 2-0-0 | 2-0-0 | 2-0-0 |
| trophy | 1-0-1 | 2-0-0 | 2-0-0 | 2-0-0 | 1-0-1 | 0-0-2 |
| queen_of_spades | 2-0-0 | 2-0-0 | 0-0-2 | 2-0-0 | 2-0-0 | 0-0-2 |
| default | 1-0-1 | 2-0-0 | 2-0-0 | 2-0-0 | 2-0-0 | 1-0-1 |
| Devil | 1-0-1 | 2-0-0 | 2-0-0 | 2-0-0 | 2-0-0 | 2-0-0 |
| stronghold | 2-0-0 | 2-0-0 | 2-0-0 | 2-0-0 | 2-0-0 | 1-0-1 |
| Trauma | 2-0-0 | 1-0-1 | 0-0-2 | 1-0-1 | 2-0-0 | 0-0-2 |
| schooltime | 1-0-1 | 2-0-0 | 2-0-0 | 2-0-0 | 2-0-0 | 0-0-2 |
| big_empty | 1-0-1 | 2-0-0 | 1-0-1 | 2-0-0 | 2-0-0 | 0-0-2 |
| arena | 1-0-1 | 2-0-0 | 2-0-0 | 2-0-0 | 2-0-0 | 0-0-2 |
| Colosseum | 2-0-0 | 2-0-0 | 2-0-0 | 2-0-0 | 2-0-0 | 2-0-0 |


---

## results/20260925-191302-full-change-a71535/full/summary.md

SHA-256: `b9fb3971121d9f8b2e82a4988c5b2ad4a4a18f8738e089c660f0e51aaa5cea0f`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 21-0-1 | 95% | 95% | 86-100% | +529 | 11 | 0 |
| ctmes | 21-0-1 | 95% | 95% | 86-100% | +529 | 11 | 0 |
| nicked | 16-0-6 | 73% | 73% | 45-95% | +170 | 11 | 0 |
| nicked_v44 | 8-0-14 | 36% | 36% | 14-64% | -97 | 11 | 0 |
| v3 | 21-0-1 | 95% | 95% | 86-100% | +529 | 11 | 0 |
| v6-fair-search-bot | 16-0-6 | 73% | 73% | 59-86% | +170 | 11 | 0 |
| **overall** | 103-0-29 | 78% | 78% | 69-86% | +220 | 66 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 6-0-6 | 50% | 50% | 12 | 0 |
| queen_of_spades | 8-0-4 | 67% | 67% | 12 | 0 |
| trophy | 8-0-4 | 67% | 67% | 12 | 0 |
| big_empty | 8-0-4 | 67% | 67% | 12 | 0 |
| arena | 9-0-3 | 75% | 75% | 12 | 0 |
| schooltime | 9-0-3 | 75% | 75% | 12 | 0 |
| default | 10-0-2 | 83% | 83% | 12 | 0 |
| default_small | 11-0-1 | 92% | 92% | 12 | 0 |
| Devil | 11-0-1 | 92% | 92% | 12 | 0 |
| stronghold | 11-0-1 | 92% | 92% | 12 | 0 |
| Colosseum | 12-0-0 | 100% | 100% | 12 | 0 |

candidate dragon deaths: head-to-head 6706, hit kelp 5979, hit other body 5452, no valid action/timeout 3278, hit itself 9

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, ctmes, nicked, nicked_v44, v3, v6-fair-search-bot: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-204545-full-change-13b847/map_matrix.md

SHA-256: `1af51a015f0fcf6202c3f3aca5f1fc0b1f13f42aa86579ecc81f6adb314cd09c`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | v6 | additive | nicked |
|---|---|---|---|
| default_small | 1-0-1 | 2-0-0 | 1-0-1 |
| trophy | 1-0-1 | 2-0-0 | 2-0-0 |
| queen_of_spades | 1-0-1 | 2-0-0 | 0-0-2 |
| default | 1-0-1 | 2-0-0 | 2-0-0 |
| Devil | 1-0-1 | 2-0-0 | 2-0-0 |
| stronghold | 2-0-0 | 2-0-0 | 2-0-0 |
| Trauma | 1-0-1 | 1-0-1 | 0-0-2 |
| schooltime | 1-0-1 | 2-0-0 | 0-0-2 |
| big_empty | 1-0-1 | 2-0-0 | 1-0-1 |
| arena | 1-0-1 | 2-0-0 | 2-0-0 |
| Colosseum | 1-0-1 | 2-0-0 | 2-0-0 |


---

## results/20260925-204545-full-change-13b847/full/summary.md

SHA-256: `f362c6c5419718ac7710d960f9dfc3bc37199191bb45bd4fb229859e8d04df82`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 21-0-1 | 95% | 95% | 86-100% | +529 | 11 | 0 |
| nicked | 14-0-8 | 64% | 64% | 41-86% | +97 | 11 | 0 |
| v6 | 12-0-10 | 55% | 55% | 50-64% | +32 | 11 | 0 |
| **overall** | 47-0-19 | 71% | 71% | 59-82% | +157 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 2-0-4 | 33% | 33% | 6 | 0 |
| queen_of_spades | 3-0-3 | 50% | 50% | 6 | 0 |
| schooltime | 3-0-3 | 50% | 50% | 6 | 0 |
| default_small | 4-0-2 | 67% | 67% | 6 | 0 |
| big_empty | 4-0-2 | 67% | 67% | 6 | 0 |
| trophy | 5-0-1 | 83% | 83% | 6 | 0 |
| default | 5-0-1 | 83% | 83% | 6 | 0 |
| Devil | 5-0-1 | 83% | 83% | 6 | 0 |
| arena | 5-0-1 | 83% | 83% | 6 | 0 |
| Colosseum | 5-0-1 | 83% | 83% | 6 | 0 |
| stronghold | 6-0-0 | 100% | 100% | 6 | 0 |

candidate dragon deaths: head-to-head 3603, hit kelp 2967, hit other body 2751, no valid action/timeout 1431, hit itself 11

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, v6: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-204546-full-change-911c3e/map_matrix.md

SHA-256: `3048b074c24051abe39c0d9e555b29066303717e9a501fba3dfa9492c92aff5f`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | v6 | additive | nicked |
|---|---|---|---|
| default_small | 1-0-1 | 2-0-0 | 1-0-1 |
| trophy | 1-0-1 | 2-0-0 | 0-0-2 |
| queen_of_spades | 2-0-0 | 2-0-0 | 0-0-2 |
| default | 1-0-1 | 2-0-0 | 2-0-0 |
| Devil | 1-0-1 | 2-0-0 | 2-0-0 |
| stronghold | 1-0-1 | 2-0-0 | 2-0-0 |
| Trauma | 1-0-1 | 1-0-1 | 0-0-2 |
| schooltime | 1-0-1 | 2-0-0 | 1-0-1 |
| big_empty | 1-0-1 | 2-0-0 | 1-0-1 |
| arena | 1-0-1 | 2-0-0 | 2-0-0 |
| Colosseum | 0-0-2 | 2-0-0 | 2-0-0 |


---

## results/20260925-204546-full-change-911c3e/full/summary.md

SHA-256: `b50c0ab3681944557f8e9b93e13497b368d2d000ac9d85d91e325a4df58673c6`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 21-0-1 | 95% | 95% | 86-100% | +529 | 11 | 0 |
| nicked | 13-0-9 | 59% | 59% | 32-82% | +64 | 11 | 0 |
| v6 | 11-0-11 | 50% | 50% | 36-64% | -0 | 11 | 0 |
| **overall** | 45-0-21 | 68% | 68% | 56-80% | +132 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 2-0-4 | 33% | 33% | 6 | 0 |
| trophy | 3-0-3 | 50% | 50% | 6 | 0 |
| default_small | 4-0-2 | 67% | 67% | 6 | 0 |
| queen_of_spades | 4-0-2 | 67% | 67% | 6 | 0 |
| schooltime | 4-0-2 | 67% | 67% | 6 | 0 |
| Colosseum | 4-0-2 | 67% | 67% | 6 | 0 |
| big_empty | 4-0-2 | 67% | 67% | 6 | 0 |
| default | 5-0-1 | 83% | 83% | 6 | 0 |
| Devil | 5-0-1 | 83% | 83% | 6 | 0 |
| stronghold | 5-0-1 | 83% | 83% | 6 | 0 |
| arena | 5-0-1 | 83% | 83% | 6 | 0 |

candidate dragon deaths: head-to-head 3786, hit kelp 3297, hit other body 2938, no valid action/timeout 1485, hit itself 9

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, v6: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-210223-full-change-d2d318/map_matrix.md

SHA-256: `5e7bbf16b885aa15145d2bb13d8f2e9073e43ad3ac0f78426502feffa83fac47`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | v6 | additive | nicked | nicked_v44 |
|---|---|---|---|---|
| default_small | 0-0-2 | 2-0-0 | 2-0-0 | 1-0-1 |
| trophy | 1-0-1 | 2-0-0 | 2-0-0 | 0-0-2 |
| queen_of_spades | 1-0-1 | 2-0-0 | 0-0-2 | 0-0-2 |
| default | 1-0-1 | 2-0-0 | 2-0-0 | 2-0-0 |
| Devil | 2-0-0 | 2-0-0 | 2-0-0 | 2-0-0 |
| stronghold | 1-0-1 | 2-0-0 | 2-0-0 | 0-0-2 |
| Trauma | 2-0-0 | 1-0-1 | 1-0-1 | 0-0-2 |
| schooltime | 0-0-2 | 2-0-0 | 1-0-1 | 0-0-2 |
| big_empty | 0-0-2 | 2-0-0 | 0-0-2 | 0-0-2 |
| arena | 2-0-0 | 2-0-0 | 2-0-0 | 1-0-1 |
| Colosseum | 1-0-1 | 2-0-0 | 2-0-0 | 1-0-1 |


---

## results/20260925-210223-full-change-d2d318/full/summary.md

SHA-256: `9a456009568b5718e13d1debd2cb1992b43bea4ae968c2a1c9bec350677ed9b9`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 21-0-1 | 95% | 95% | 86-100% | +529 | 11 | 0 |
| nicked | 16-0-6 | 73% | 73% | 50-95% | +170 | 11 | 0 |
| nicked_v44 | 7-0-15 | 32% | 32% | 9-55% | -132 | 11 | 0 |
| v6 | 11-0-11 | 50% | 50% | 32-73% | -0 | 11 | 0 |
| **overall** | 55-0-33 | 62% | 62% | 50-75% | +89 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| big_empty | 2-0-6 | 25% | 25% | 8 | 0 |
| queen_of_spades | 3-0-5 | 38% | 38% | 8 | 0 |
| schooltime | 3-0-5 | 38% | 38% | 8 | 0 |
| Trauma | 4-0-4 | 50% | 50% | 8 | 0 |
| default_small | 5-0-3 | 62% | 62% | 8 | 0 |
| trophy | 5-0-3 | 62% | 62% | 8 | 0 |
| stronghold | 5-0-3 | 62% | 62% | 8 | 0 |
| Colosseum | 6-0-2 | 75% | 75% | 8 | 0 |
| default | 7-0-1 | 88% | 88% | 8 | 0 |
| arena | 7-0-1 | 88% | 88% | 8 | 0 |
| Devil | 8-0-0 | 100% | 100% | 8 | 0 |

candidate dragon deaths: head-to-head 3979, hit kelp 2209, hit other body 1876, no valid action/timeout 1040, hit itself 7

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, nicked_v44, v6: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-210224-full-change-4838d6/map_matrix.md

SHA-256: `f1bed5f28fb5b527743859398f33d3dfe8cc787ab79dc1e8664ef72adc366af7`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | v6 | additive | nicked | nicked_v44 |
|---|---|---|---|---|
| default_small | 0-0-2 | 2-0-0 | 2-0-0 | 2-0-0 |
| trophy | 2-0-0 | 2-0-0 | 2-0-0 | 1-0-1 |
| queen_of_spades | 2-0-0 | 2-0-0 | 0-0-2 | 0-0-2 |
| default | 0-0-2 | 2-0-0 | 2-0-0 | 0-0-2 |
| Devil | 2-0-0 | 2-0-0 | 2-0-0 | 1-0-1 |
| stronghold | 0-0-2 | 2-0-0 | 2-0-0 | 0-0-2 |
| Trauma | 1-0-1 | 1-0-1 | 1-0-1 | 0-0-2 |
| schooltime | 2-0-0 | 2-0-0 | 1-0-1 | 0-0-2 |
| big_empty | 1-0-1 | 2-0-0 | 1-0-1 | 0-0-2 |
| arena | 1-0-1 | 2-0-0 | 2-0-0 | 0-0-2 |
| Colosseum | 1-0-1 | 2-0-0 | 2-0-0 | 2-0-0 |


---

## results/20260925-210224-full-change-4838d6/full/summary.md

SHA-256: `a5f33bb1690cf3ff95c3d2377b07de899956a05fe0bc643d608c1f62bfbc7218`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 21-0-1 | 95% | 95% | 86-100% | +529 | 11 | 0 |
| nicked | 17-0-5 | 77% | 77% | 55-95% | +213 | 11 | 0 |
| nicked_v44 | 6-0-16 | 27% | 27% | 5-50% | -170 | 11 | 0 |
| v6 | 12-0-10 | 55% | 55% | 32-77% | +32 | 11 | 0 |
| **overall** | 56-0-32 | 64% | 64% | 52-76% | +97 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 3-0-5 | 38% | 38% | 8 | 0 |
| queen_of_spades | 4-0-4 | 50% | 50% | 8 | 0 |
| default | 4-0-4 | 50% | 50% | 8 | 0 |
| stronghold | 4-0-4 | 50% | 50% | 8 | 0 |
| big_empty | 4-0-4 | 50% | 50% | 8 | 0 |
| schooltime | 5-0-3 | 62% | 62% | 8 | 0 |
| arena | 5-0-3 | 62% | 62% | 8 | 0 |
| default_small | 6-0-2 | 75% | 75% | 8 | 0 |
| trophy | 7-0-1 | 88% | 88% | 8 | 0 |
| Devil | 7-0-1 | 88% | 88% | 8 | 0 |
| Colosseum | 7-0-1 | 88% | 88% | 8 | 0 |

candidate dragon deaths: head-to-head 4824, hit kelp 4437, hit other body 3782, no valid action/timeout 2114, hit itself 10

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, nicked_v44, v6: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-210224-full-change-b3cbea/map_matrix.md

SHA-256: `c70df4390208691ba1cd88586f927f13ea8762e30fc88d5fdae8d3fc629c9591`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | v6 | additive | nicked | nicked_v44 |
|---|---|---|---|---|
| default_small | 2-0-0 | 2-0-0 | 1-0-1 | 1-0-1 |
| trophy | 1-0-1 | 2-0-0 | 1-0-1 | 0-0-2 |
| queen_of_spades | 0-0-2 | 2-0-0 | 0-0-2 | 0-0-2 |
| default | 2-0-0 | 2-0-0 | 1-0-1 | 1-0-1 |
| Devil | 2-0-0 | 2-0-0 | 2-0-0 | 2-0-0 |
| stronghold | 0-0-2 | 2-0-0 | 2-0-0 | 0-0-2 |
| Trauma | 2-0-0 | 1-0-1 | 1-0-1 | 0-0-2 |
| schooltime | 1-0-1 | 2-0-0 | 2-0-0 | 1-0-1 |
| big_empty | 0-0-2 | 2-0-0 | 0-0-2 | 0-0-2 |
| arena | 2-0-0 | 2-0-0 | 2-0-0 | 1-0-1 |
| Colosseum | 1-0-1 | 2-0-0 | 2-0-0 | 1-0-1 |


---

## results/20260925-210224-full-change-b3cbea/full/summary.md

SHA-256: `12d31c93aa0e545e4b41c692ab3286f42782cfd6124c8408485544e34a7ae441`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 21-0-1 | 95% | 95% | 86-100% | +529 | 11 | 0 |
| nicked | 14-0-8 | 64% | 64% | 41-86% | +97 | 11 | 0 |
| nicked_v44 | 7-0-15 | 32% | 32% | 14-50% | -132 | 11 | 0 |
| v6 | 13-0-9 | 59% | 59% | 36-82% | +64 | 11 | 0 |
| **overall** | 55-0-33 | 62% | 62% | 50-74% | +89 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades | 2-0-6 | 25% | 25% | 8 | 0 |
| big_empty | 2-0-6 | 25% | 25% | 8 | 0 |
| trophy | 4-0-4 | 50% | 50% | 8 | 0 |
| Trauma | 4-0-4 | 50% | 50% | 8 | 0 |
| stronghold | 4-0-4 | 50% | 50% | 8 | 0 |
| default_small | 6-0-2 | 75% | 75% | 8 | 0 |
| default | 6-0-2 | 75% | 75% | 8 | 0 |
| schooltime | 6-0-2 | 75% | 75% | 8 | 0 |
| Colosseum | 6-0-2 | 75% | 75% | 8 | 0 |
| arena | 7-0-1 | 88% | 88% | 8 | 0 |
| Devil | 8-0-0 | 100% | 100% | 8 | 0 |

candidate dragon deaths: head-to-head 3945, hit kelp 2128, hit other body 1775, no valid action/timeout 1076, hit itself 8

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, nicked_v44, v6: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-212726-full-change-52675f/map_matrix.md

SHA-256: `2a6d73909ac455c757936c0c8b74bd768d5a8792719b4908e8871b5ea0694c4c`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | v6 | additive | nicked | nicked_v44 |
|---|---|---|---|---|
| default_small | 1-0-1 | 2-0-0 | 1-0-1 | 1-0-1 |
| trophy | 2-0-0 | 2-0-0 | 2-0-0 | 1-0-1 |
| queen_of_spades | 2-0-0 | 2-0-0 | 0-0-2 | 1-0-1 |
| default | 0-0-2 | 2-0-0 | 2-0-0 | 0-0-2 |
| Devil | 1-0-1 | 2-0-0 | 2-0-0 | 2-0-0 |
| stronghold | 2-0-0 | 2-0-0 | 2-0-0 | 0-0-2 |
| Trauma | 2-0-0 | 1-0-1 | 1-0-1 | 0-0-2 |
| schooltime | 1-0-1 | 2-0-0 | 1-0-1 | 0-0-2 |
| big_empty | 1-0-1 | 2-0-0 | 2-0-0 | 0-0-2 |
| arena | 2-0-0 | 2-0-0 | 2-0-0 | 0-0-2 |
| Colosseum | 1-0-1 | 2-0-0 | 2-0-0 | 2-0-0 |


---

## results/20260925-212726-full-change-52675f/completed/summary.md

SHA-256: `7f29f8a03436c48d0cf5ddc57aaa63819991eea650b1fcd26675dd397db583c3`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 21-0-1 | 95% | 95% | 86-100% | +529 | 11 | 0 |
| nicked | 17-0-5 | 77% | 77% | 59-95% | +213 | 11 | 0 |
| nicked_v44 | 7-0-15 | 32% | 32% | 9-55% | -132 | 11 | 0 |
| v6 | 15-0-7 | 68% | 68% | 50-86% | +132 | 11 | 0 |
| **overall** | 60-0-28 | 68% | 68% | 57-80% | +132 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 4-0-4 | 50% | 50% | 8 | 0 |
| default | 4-0-4 | 50% | 50% | 8 | 0 |
| schooltime | 4-0-4 | 50% | 50% | 8 | 0 |
| big_empty | 5-0-3 | 62% | 62% | 8 | 0 |
| default_small | 5-0-3 | 62% | 62% | 8 | 0 |
| queen_of_spades | 5-0-3 | 62% | 62% | 8 | 0 |
| arena | 6-0-2 | 75% | 75% | 8 | 0 |
| stronghold | 6-0-2 | 75% | 75% | 8 | 0 |
| Colosseum | 7-0-1 | 88% | 88% | 8 | 0 |
| Devil | 7-0-1 | 88% | 88% | 8 | 0 |
| trophy | 7-0-1 | 88% | 88% | 8 | 0 |

candidate dragon deaths: head-to-head 4234, hit kelp 3481, hit other body 2602, no valid action/timeout 1609, hit itself 5

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, nicked_v44, v6: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-212727-full-change-b01abd/map_matrix.md

SHA-256: `0e0f986790c631c0cdd7ea1d9674c26b6315affd57bf66bb4630216b0fc30355`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | v6 | additive | nicked | nicked_v44 |
|---|---|---|---|---|
| default_small | 2-0-0 | 2-0-0 | 1-0-1 | 0-0-2 |
| trophy | 2-0-0 | 2-0-0 | 2-0-0 | 0-0-2 |
| queen_of_spades | 2-0-0 | 2-0-0 | 0-0-2 | 1-0-1 |
| default | 1-0-1 | 2-0-0 | 2-0-0 | 1-0-1 |
| Devil | 1-0-1 | 2-0-0 | 2-0-0 | 2-0-0 |
| stronghold | 1-0-1 | 2-0-0 | 2-0-0 | 1-0-1 |
| Trauma | 1-0-1 | 2-0-0 | 2-0-0 | 0-0-2 |
| schooltime | 2-0-0 | 2-0-0 | 1-0-1 | 0-0-2 |
| big_empty | 2-0-0 | 2-0-0 | 2-0-0 | 0-0-2 |
| arena | 1-0-1 | 2-0-0 | 2-0-0 | 1-0-1 |
| Colosseum | 1-0-1 | 2-0-0 | 2-0-0 | 2-0-0 |


---

## results/20260925-212727-full-change-b01abd/full/summary.md

SHA-256: `814f40acb00140d86d268a021674aee4fbf91458b292bb24cb53e76396e62515`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 22-0-0 | 100% | 100% | 100-100% | +1200 | 11 | 0 |
| nicked | 18-0-4 | 82% | 82% | 64-100% | +261 | 11 | 0 |
| nicked_v44 | 8-0-14 | 36% | 36% | 18-59% | -97 | 11 | 0 |
| v6 | 16-0-6 | 73% | 73% | 59-86% | +170 | 11 | 0 |
| **overall** | 64-0-24 | 73% | 73% | 62-83% | +170 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default_small | 5-0-3 | 62% | 62% | 8 | 0 |
| queen_of_spades | 5-0-3 | 62% | 62% | 8 | 0 |
| Trauma | 5-0-3 | 62% | 62% | 8 | 0 |
| schooltime | 5-0-3 | 62% | 62% | 8 | 0 |
| trophy | 6-0-2 | 75% | 75% | 8 | 0 |
| default | 6-0-2 | 75% | 75% | 8 | 0 |
| stronghold | 6-0-2 | 75% | 75% | 8 | 0 |
| arena | 6-0-2 | 75% | 75% | 8 | 0 |
| big_empty | 6-0-2 | 75% | 75% | 8 | 0 |
| Devil | 7-0-1 | 88% | 88% | 8 | 0 |
| Colosseum | 7-0-1 | 88% | 88% | 8 | 0 |

candidate dragon deaths: head-to-head 4261, hit kelp 3416, hit other body 2543, no valid action/timeout 1915, hit itself 9

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, nicked, nicked_v44, v6: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-214042-full-change-ba75fb/map_matrix.md

SHA-256: `1e3400492658d56978665bd22a9e031f6a514f8ffe30b467ce9eccb41313e6dc`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | v3 | ctmes |
|---|---|---|
| default_small | 2-0-0 | 2-0-0 |
| trophy | 2-0-0 | 2-0-0 |
| queen_of_spades | 2-0-0 | 1-0-1 |
| default | 2-0-0 | 2-0-0 |
| Devil | 2-0-0 | 2-0-0 |
| stronghold | 2-0-0 | 1-0-1 |
| Trauma | 2-0-0 | 2-0-0 |
| schooltime | 2-0-0 | 2-0-0 |
| big_empty | 2-0-0 | 2-0-0 |
| arena | 2-0-0 | 2-0-0 |
| Colosseum | 2-0-0 | 2-0-0 |


---

## results/20260925-214042-full-change-ba75fb/full/summary.md

SHA-256: `1b1b00fe943bd5bb8de5f0188fb82a8ebefa9ae0cd8651fdae7197f3e7528768`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| ctmes | 20-0-2 | 91% | 91% | 77-100% | +400 | 11 | 0 |
| v3 | 22-0-0 | 100% | 100% | 100-100% | +1200 | 11 | 0 |
| **overall** | 42-0-2 | 95% | 95% | 89-100% | +529 | 22 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades | 3-0-1 | 75% | 75% | 4 | 0 |
| stronghold | 3-0-1 | 75% | 75% | 4 | 0 |
| default_small | 4-0-0 | 100% | 100% | 4 | 0 |
| trophy | 4-0-0 | 100% | 100% | 4 | 0 |
| default | 4-0-0 | 100% | 100% | 4 | 0 |
| Devil | 4-0-0 | 100% | 100% | 4 | 0 |
| Trauma | 4-0-0 | 100% | 100% | 4 | 0 |
| schooltime | 4-0-0 | 100% | 100% | 4 | 0 |
| arena | 4-0-0 | 100% | 100% | 4 | 0 |
| Colosseum | 4-0-0 | 100% | 100% | 4 | 0 |
| big_empty | 4-0-0 | 100% | 100% | 4 | 0 |

candidate dragon deaths: head-to-head 1818, hit kelp 1676, hit other body 1323, no valid action/timeout 906, hit itself 7

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for ctmes, v3: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-232832-full-change-b0a387/map_matrix.md

SHA-256: `b7b63ef2818f43576268eee7c8cf081ee4f07fdcbc382a504d9a8d806781b3f9`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | v61b-goal-bot | additive | nicked | nicked_v44 | v3 | ctmes |
|---|---|---|---|---|---|---|
| default_small | 0-0-2 | 2-0-0 | 1-0-1 | 2-0-0 | 2-0-0 | 2-0-0 |
| trophy | 1-0-1 | 2-0-0 | 2-0-0 | 1-0-1 | 2-0-0 | 2-0-0 |
| queen_of_spades | 2-0-0 | 2-0-0 | 0-0-2 | 0-0-2 | 2-0-0 | 2-0-0 |
| default | 0-0-2 | 2-0-0 | 2-0-0 | 1-0-1 | 2-0-0 | 2-0-0 |
| Devil | 2-0-0 | 2-0-0 | 2-0-0 | 2-0-0 | 2-0-0 | 2-0-0 |
| stronghold | 0-0-2 | 2-0-0 | 2-0-0 | 0-0-2 | 2-0-0 | 2-0-0 |
| Trauma | 1-0-1 | 2-0-0 | 0-0-2 | 1-0-1 | 2-0-0 | 2-0-0 |
| schooltime | 2-0-0 | 2-0-0 | 1-0-1 | 0-0-2 | 2-0-0 | 1-0-1 |
| big_empty | 2-0-0 | 2-0-0 | 0-0-2 | 0-0-2 | 2-0-0 | 2-0-0 |
| arena | 1-0-1 | 2-0-0 | 2-0-0 | 0-0-2 | 2-0-0 | 2-0-0 |
| Colosseum | 1-0-1 | 2-0-0 | 2-0-0 | 2-0-0 | 2-0-0 | 2-0-0 |


---

## results/20260925-232832-full-change-b0a387/full/summary.md

SHA-256: `c324461693567df24edde06dda6943ea576c90f3a06bce9f0363fda01345f96f`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| additive | 22-0-0 | 100% | 100% | 100-100% | +1200 | 11 | 0 |
| ctmes | 21-0-1 | 95% | 95% | 86-100% | +529 | 11 | 0 |
| nicked | 14-0-8 | 64% | 64% | 36-86% | +97 | 11 | 0 |
| nicked_v44 | 9-0-13 | 41% | 41% | 18-64% | -64 | 11 | 0 |
| v3 | 22-0-0 | 100% | 100% | 100-100% | +1200 | 11 | 0 |
| v61b-goal-bot | 12-0-10 | 55% | 55% | 32-77% | +32 | 11 | 0 |
| **overall** | 100-0-32 | 76% | 76% | 67-85% | +198 | 66 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades | 8-0-4 | 67% | 67% | 12 | 0 |
| Trauma | 8-0-4 | 67% | 67% | 12 | 0 |
| stronghold | 8-0-4 | 67% | 67% | 12 | 0 |
| schooltime | 8-0-4 | 67% | 67% | 12 | 0 |
| big_empty | 8-0-4 | 67% | 67% | 12 | 0 |
| default_small | 9-0-3 | 75% | 75% | 12 | 0 |
| default | 9-0-3 | 75% | 75% | 12 | 0 |
| arena | 9-0-3 | 75% | 75% | 12 | 0 |
| trophy | 10-0-2 | 83% | 83% | 12 | 0 |
| Colosseum | 11-0-1 | 92% | 92% | 12 | 0 |
| Devil | 12-0-0 | 100% | 100% | 12 | 0 |

candidate dragon deaths: head-to-head 6458, hit kelp 5106, hit other body 4024, no valid action/timeout 2873, hit itself 9

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for additive, ctmes, nicked, nicked_v44, v3, v61b-goal-bot: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-235406-full-change-d94b9b/map_matrix.md

SHA-256: `2566868080d25f90a83862dd5fc54215f241b2aab4f6244cdc6265820183ebd7`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | v7-base-bot | nicked |
|---|---|---|
| default_small | 1-0-1 | 1-0-1 |
| trophy | 1-0-1 | 1-0-1 |
| queen_of_spades | 0-0-2 | 0-0-2 |
| default | 1-0-1 | 2-0-0 |
| Devil | 0-0-2 | 2-0-0 |
| stronghold | 1-0-1 | 2-0-0 |
| Trauma | 1-0-1 | 2-0-0 |
| schooltime | 0-0-2 | 1-0-1 |
| big_empty | 1-0-1 | 2-0-0 |
| arena | 1-0-1 | 2-0-0 |
| Colosseum | 1-0-1 | 2-0-0 |


---

## results/20260925-235406-full-change-d94b9b/full/summary.md

SHA-256: `dab013796839dfd8fa11814afc7a0c50f5b6bcdf165d7a0bb5ca7ea21be7f84d`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 17-0-5 | 77% | 77% | 59-95% | +213 | 11 | 0 |
| v7-base-bot | 8-0-14 | 36% | 36% | 23-50% | -97 | 11 | 0 |
| **overall** | 25-0-19 | 57% | 57% | 43-70% | +48 | 22 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades | 0-0-4 | 0% | 0% | 4 | 0 |
| schooltime | 1-0-3 | 25% | 25% | 4 | 0 |
| default_small | 2-0-2 | 50% | 50% | 4 | 0 |
| trophy | 2-0-2 | 50% | 50% | 4 | 0 |
| Devil | 2-0-2 | 50% | 50% | 4 | 0 |
| default | 3-0-1 | 75% | 75% | 4 | 0 |
| stronghold | 3-0-1 | 75% | 75% | 4 | 0 |
| Trauma | 3-0-1 | 75% | 75% | 4 | 0 |
| big_empty | 3-0-1 | 75% | 75% | 4 | 0 |
| arena | 3-0-1 | 75% | 75% | 4 | 0 |
| Colosseum | 3-0-1 | 75% | 75% | 4 | 0 |

candidate dragon deaths: head-to-head 2164, hit kelp 1261, hit other body 990, no valid action/timeout 495, hit itself 2

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for nicked, v7-base-bot: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-235406-full-change-ecd2b0/map_matrix.md

SHA-256: `54ba4b0ed1edf81a64bae522faaa8de765b99250e4d60679f7baa4aa98c0d45b`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | v7-base-bot | nicked |
|---|---|---|
| default_small | 1-0-1 | 1-0-1 |
| trophy | 1-0-1 | 2-0-0 |
| queen_of_spades | 0-0-2 | 0-0-2 |
| default | 0-0-2 | 1-0-1 |
| Devil | 1-0-1 | 2-0-0 |
| stronghold | 2-0-0 | 2-0-0 |
| Trauma | 1-0-1 | 0-0-2 |
| schooltime | 1-0-1 | 2-0-0 |
| big_empty | 1-0-1 | 1-0-1 |
| arena | 1-0-1 | 2-0-0 |
| Colosseum | 1-0-1 | 2-0-0 |


---

## results/20260925-235406-full-change-ecd2b0/full/summary.md

SHA-256: `360b5ebb6de291d167bac96e853ded82dc8c4932f0a7af10508dfb4f5aa5dd6d`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 15-0-7 | 68% | 68% | 45-91% | +132 | 11 | 0 |
| v7-base-bot | 10-0-12 | 45% | 45% | 32-59% | -32 | 11 | 0 |
| **overall** | 25-0-19 | 57% | 57% | 43-70% | +48 | 22 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades | 0-0-4 | 0% | 0% | 4 | 0 |
| default | 1-0-3 | 25% | 25% | 4 | 0 |
| Trauma | 1-0-3 | 25% | 25% | 4 | 0 |
| default_small | 2-0-2 | 50% | 50% | 4 | 0 |
| big_empty | 2-0-2 | 50% | 50% | 4 | 0 |
| trophy | 3-0-1 | 75% | 75% | 4 | 0 |
| Devil | 3-0-1 | 75% | 75% | 4 | 0 |
| schooltime | 3-0-1 | 75% | 75% | 4 | 0 |
| arena | 3-0-1 | 75% | 75% | 4 | 0 |
| Colosseum | 3-0-1 | 75% | 75% | 4 | 0 |
| stronghold | 4-0-0 | 100% | 100% | 4 | 0 |

candidate dragon deaths: head-to-head 2363, hit kelp 1359, hit other body 1149, no valid action/timeout 646, hit itself 1

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for nicked, v7-base-bot: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-235407-full-change-165aad/map_matrix.md

SHA-256: `bf87edb8eee09355e5b678159c1a3bd362004bbee43700f7a965f17d6e92fdff`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | v7-base-bot | nicked |
|---|---|---|
| default_small | 0-0-2 | 2-0-0 |
| trophy | 1-0-1 | 1-0-1 |
| queen_of_spades | 1-0-1 | 0-0-2 |
| default | 1-0-1 | 2-0-0 |
| Devil | 0-0-2 | 1-0-1 |
| stronghold | 1-0-1 | 2-0-0 |
| Trauma | 1-0-1 | 2-0-0 |
| schooltime | 0-0-2 | 2-0-0 |
| big_empty | 1-0-1 | 1-0-1 |
| arena | 0-0-2 | 2-0-0 |
| Colosseum | 0-0-2 | 2-0-0 |


---

## results/20260925-235407-full-change-165aad/full/summary.md

SHA-256: `c8dbd2ee8c3667b450b7a77b025e495de31b849d80736e12eee5da640245c050`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 17-0-5 | 77% | 77% | 59-95% | +213 | 11 | 0 |
| v7-base-bot | 6-0-16 | 27% | 27% | 14-41% | -170 | 11 | 0 |
| **overall** | 23-0-21 | 52% | 52% | 36-68% | +16 | 22 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades | 1-0-3 | 25% | 25% | 4 | 0 |
| Devil | 1-0-3 | 25% | 25% | 4 | 0 |
| default_small | 2-0-2 | 50% | 50% | 4 | 0 |
| trophy | 2-0-2 | 50% | 50% | 4 | 0 |
| schooltime | 2-0-2 | 50% | 50% | 4 | 0 |
| big_empty | 2-0-2 | 50% | 50% | 4 | 0 |
| arena | 2-0-2 | 50% | 50% | 4 | 0 |
| Colosseum | 2-0-2 | 50% | 50% | 4 | 0 |
| default | 3-0-1 | 75% | 75% | 4 | 0 |
| stronghold | 3-0-1 | 75% | 75% | 4 | 0 |
| Trauma | 3-0-1 | 75% | 75% | 4 | 0 |

candidate dragon deaths: head-to-head 1938, hit kelp 1068, hit other body 908, no valid action/timeout 491, hit itself 2

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for nicked, v7-base-bot: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260925-235407-full-change-6fe318/map_matrix.md

SHA-256: `759fd6324b5a6acbdbe4a3d78f144ddb03815fe6a12adbbfedb208ce278b3076`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | v7-base-bot | nicked |
|---|---|---|
| default_small | 0-0-2 | 1-0-1 |
| trophy | 1-0-1 | 0-0-2 |
| queen_of_spades | 1-0-1 | 0-0-2 |
| default | 0-0-2 | 2-0-0 |
| Devil | 1-0-1 | 1-0-1 |
| stronghold | 1-0-1 | 2-0-0 |
| Trauma | 1-0-1 | 0-0-2 |
| schooltime | 2-0-0 | 1-0-1 |
| big_empty | 0-0-2 | 0-0-2 |
| arena | 0-0-2 | 2-0-0 |
| Colosseum | 1-0-1 | 2-0-0 |


---

## results/20260925-235407-full-change-6fe318/full/summary.md

SHA-256: `0635b0f3116bd06ed6125bc977d1a03769a98b21551ce3fb27ed2410d083212e`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 11-0-11 | 50% | 50% | 27-77% | -0 | 11 | 0 |
| v7-base-bot | 8-0-14 | 36% | 36% | 18-55% | -97 | 11 | 0 |
| **overall** | 19-0-25 | 43% | 43% | 27-57% | -48 | 22 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| big_empty | 0-0-4 | 0% | 0% | 4 | 0 |
| default_small | 1-0-3 | 25% | 25% | 4 | 0 |
| trophy | 1-0-3 | 25% | 25% | 4 | 0 |
| queen_of_spades | 1-0-3 | 25% | 25% | 4 | 0 |
| Trauma | 1-0-3 | 25% | 25% | 4 | 0 |
| default | 2-0-2 | 50% | 50% | 4 | 0 |
| Devil | 2-0-2 | 50% | 50% | 4 | 0 |
| arena | 2-0-2 | 50% | 50% | 4 | 0 |
| stronghold | 3-0-1 | 75% | 75% | 4 | 0 |
| schooltime | 3-0-1 | 75% | 75% | 4 | 0 |
| Colosseum | 3-0-1 | 75% | 75% | 4 | 0 |

candidate dragon deaths: head-to-head 2311, hit kelp 1200, hit other body 1109, no valid action/timeout 521

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for nicked, v7-base-bot: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260926-145349-full-change-516b69/map_matrix.md

SHA-256: `1d5ccc5beadc65cfab89d82b2ac5bb0e52b9152440ddde738346f0d295e64367`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | nicked_v44 | ctmes | v6 | v7-base-bot |
|---|---|---|---|---|
| default_small | 2-0-0 | 2-0-0 | 2-0-0 | 1-0-1 |
| trophy | 0-0-2 | 2-0-0 | 2-0-0 | 1-0-1 |
| queen_of_spades | 0-0-2 | 1-0-1 | 1-0-1 | 1-0-1 |
| default | 1-0-1 | 2-0-0 | 2-0-0 | 1-0-1 |
| Devil | 2-0-0 | 2-0-0 | 2-0-0 | 0-0-2 |
| stronghold | 0-0-2 | 2-0-0 | 2-0-0 | 1-0-1 |
| Trauma | 1-0-1 | 0-0-2 | 1-0-1 | 0-0-2 |
| schooltime | 1-0-1 | 2-0-0 | 1-0-1 | 1-0-1 |
| big_empty | 0-0-2 | 2-0-0 | 2-0-0 | 2-0-0 |
| arena | 1-0-1 | 2-0-0 | 2-0-0 | 1-0-1 |
| Colosseum | 2-0-0 | 2-0-0 | 2-0-0 | 1-0-1 |


---

## results/20260926-145349-full-change-516b69/full/summary.md

SHA-256: `0b00c609e6873f9c530f0d901c506d4cfc3b08a644e9724b716ad314bb75844f`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| ctmes | 19-0-3 | 86% | 86% | 64-100% | +321 | 11 | 0 |
| nicked_v44 | 10-0-12 | 45% | 45% | 23-68% | -32 | 11 | 0 |
| v6 | 19-0-3 | 86% | 86% | 73-100% | +321 | 11 | 0 |
| v7-base-bot | 10-0-12 | 45% | 45% | 32-59% | -32 | 11 | 0 |
| **overall** | 58-0-30 | 66% | 66% | 55-76% | +115 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 2-0-6 | 25% | 25% | 8 | 0 |
| queen_of_spades | 3-0-5 | 38% | 38% | 8 | 0 |
| trophy | 5-0-3 | 62% | 62% | 8 | 0 |
| stronghold | 5-0-3 | 62% | 62% | 8 | 0 |
| schooltime | 5-0-3 | 62% | 62% | 8 | 0 |
| Devil | 6-0-2 | 75% | 75% | 8 | 0 |
| default | 6-0-2 | 75% | 75% | 8 | 0 |
| arena | 6-0-2 | 75% | 75% | 8 | 0 |
| big_empty | 6-0-2 | 75% | 75% | 8 | 0 |
| default_small | 7-0-1 | 88% | 88% | 8 | 0 |
| Colosseum | 7-0-1 | 88% | 88% | 8 | 0 |

candidate dragon deaths: head-to-head 3973, hit kelp 2417, hit other body 2367, no valid action/timeout 1241, hit itself 17

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for ctmes, nicked_v44, v6, v7-base-bot: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260926-145350-full-change-c39295/map_matrix.md

SHA-256: `467cc57ad152270a262af983a844ca7572cccaa3d604110622e6e4d9392215a2`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | nicked_v44 | ctmes | v6 | v7-base-bot |
|---|---|---|---|---|
| default_small | 0-0-2 | 2-0-0 | 2-0-0 | 0-0-2 |
| trophy | 2-0-0 | 2-0-0 | 2-0-0 | 0-0-2 |
| queen_of_spades | 0-0-2 | 2-0-0 | 2-0-0 | 2-0-0 |
| default | 1-0-1 | 1-0-1 | 1-0-1 | 1-0-1 |
| Devil | 2-0-0 | 2-0-0 | 1-0-1 | 1-0-1 |
| stronghold | 0-0-2 | 1-0-1 | 0-0-2 | 0-0-2 |
| Trauma | 0-0-2 | 2-0-0 | 1-0-1 | 1-0-1 |
| schooltime | 1-0-1 | 2-0-0 | 0-0-2 | 1-0-1 |
| big_empty | 1-0-1 | 2-0-0 | 2-0-0 | 2-0-0 |
| arena | 0-0-2 | 2-0-0 | 1-0-1 | 1-0-1 |
| Colosseum | 2-0-0 | 2-0-0 | 2-0-0 | 1-0-1 |


---

## results/20260926-145350-full-change-c39295/full/summary.md

SHA-256: `6676bbdadb64c1ad5ec680955cc65ccfcdcb7c3a9f71cf30c383bb06d9cf584c`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| ctmes | 20-0-2 | 91% | 91% | 77-100% | +400 | 11 | 0 |
| nicked_v44 | 9-0-13 | 41% | 41% | 18-68% | -64 | 11 | 0 |
| v6 | 14-0-8 | 64% | 64% | 41-86% | +97 | 11 | 0 |
| v7-base-bot | 10-0-12 | 45% | 45% | 27-64% | -32 | 11 | 0 |
| **overall** | 53-0-35 | 60% | 60% | 49-73% | +72 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold | 1-0-7 | 12% | 12% | 8 | 0 |
| default_small | 4-0-4 | 50% | 50% | 8 | 0 |
| default | 4-0-4 | 50% | 50% | 8 | 0 |
| Trauma | 4-0-4 | 50% | 50% | 8 | 0 |
| arena | 4-0-4 | 50% | 50% | 8 | 0 |
| schooltime | 4-0-4 | 50% | 50% | 8 | 0 |
| queen_of_spades | 6-0-2 | 75% | 75% | 8 | 0 |
| trophy | 6-0-2 | 75% | 75% | 8 | 0 |
| Devil | 6-0-2 | 75% | 75% | 8 | 0 |
| Colosseum | 7-0-1 | 88% | 88% | 8 | 0 |
| big_empty | 7-0-1 | 88% | 88% | 8 | 0 |

candidate dragon deaths: head-to-head 5111, hit kelp 3639, hit other body 3019, no valid action/timeout 1357, hit itself 8

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for ctmes, nicked_v44, v6, v7-base-bot: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260926-145351-full-change-5e66de/map_matrix.md

SHA-256: `45361ca88524a97ec19ead5f50cbe90bfb827b84e2bdd97d4fd9da1642b64ddf`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | nicked_v44 | ctmes | v6 | v7-base-bot |
|---|---|---|---|---|
| default_small | 1-0-1 | 2-0-0 | 2-0-0 | 2-0-0 |
| trophy | 0-0-2 | 2-0-0 | 1-0-1 | 1-0-1 |
| queen_of_spades | 1-0-1 | 2-0-0 | 1-0-1 | 0-0-2 |
| default | 1-0-1 | 0-0-2 | 0-0-2 | 0-0-2 |
| Devil | 2-0-0 | 2-0-0 | 2-0-0 | 2-0-0 |
| stronghold | 1-0-1 | 1-0-1 | 1-0-1 | 0-0-2 |
| Trauma | 0-0-2 | 1-0-1 | 2-0-0 | 2-0-0 |
| schooltime | 1-0-1 | 2-0-0 | 1-0-1 | 1-0-1 |
| big_empty | 0-0-2 | 0-0-2 | 1-0-1 | 1-0-1 |
| arena | 1-0-1 | 2-0-0 | 2-0-0 | 1-1-0 |
| Colosseum | 2-0-0 | 2-0-0 | 2-0-0 | 1-0-1 |


---

## results/20260926-145351-full-change-5e66de/full/summary.md

SHA-256: `35ee88a85cbb032adac08829315bf8239824f53c05f737011b3936a5ddf0fea4`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| ctmes | 16-0-6 | 73% | 73% | 50-91% | +170 | 11 | 0 |
| nicked_v44 | 10-0-12 | 45% | 45% | 27-64% | -32 | 11 | 0 |
| v6 | 15-0-7 | 68% | 68% | 50-86% | +132 | 11 | 0 |
| v7-base-bot | 11-1-10 | 50% | 52% | 30-75% | +16 | 11 | 0 |
| **overall** | 52-1-35 | 59% | 60% | 48-71% | +68 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default | 1-0-7 | 12% | 12% | 8 | 0 |
| big_empty | 2-0-6 | 25% | 25% | 8 | 0 |
| stronghold | 3-0-5 | 38% | 38% | 8 | 0 |
| queen_of_spades | 4-0-4 | 50% | 50% | 8 | 0 |
| trophy | 4-0-4 | 50% | 50% | 8 | 0 |
| Trauma | 5-0-3 | 62% | 62% | 8 | 0 |
| schooltime | 5-0-3 | 62% | 62% | 8 | 0 |
| arena | 6-1-1 | 75% | 81% | 8 | 0 |
| default_small | 7-0-1 | 88% | 88% | 8 | 0 |
| Colosseum | 7-0-1 | 88% | 88% | 8 | 0 |
| Devil | 8-0-0 | 100% | 100% | 8 | 0 |

candidate dragon deaths: head-to-head 4565, hit other body 3155, hit kelp 3003, no valid action/timeout 849, hit itself 8

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for ctmes, nicked_v44, v6, v7-base-bot: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260926-145351-full-change-bbba46/map_matrix.md

SHA-256: `04ddbb249f8e999273bfe8fba7a8d2f201b85b6efdb7aa859e96f2339eeb72b4`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | nicked_v44 | ctmes | v6 | v7-base-bot |
|---|---|---|---|---|
| default_small | 2-0-0 | 2-0-0 | 2-0-0 | 1-0-1 |
| trophy | 2-0-0 | 2-0-0 | 1-0-1 | 1-0-1 |
| queen_of_spades | 1-0-1 | 1-0-1 | 1-0-1 | 1-0-1 |
| default | 1-0-1 | 1-0-1 | 2-0-0 | 0-0-2 |
| Devil | 2-0-0 | 2-0-0 | 1-0-1 | 2-0-0 |
| stronghold | 2-0-0 | 2-0-0 | 0-0-2 | 1-0-1 |
| Trauma | 0-0-2 | 2-0-0 | 2-0-0 | 1-0-1 |
| schooltime | 1-0-1 | 2-0-0 | 1-0-1 | 2-0-0 |
| big_empty | 0-0-2 | 2-0-0 | 1-0-1 | 1-0-1 |
| arena | 1-0-1 | 2-0-0 | 2-0-0 | 2-0-0 |
| Colosseum | 2-0-0 | 2-0-0 | 2-0-0 | 0-0-2 |


---

## results/20260926-145351-full-change-bbba46/full/summary.md

SHA-256: `4acc7e48dd8d8ca9c2a2fed61fbcc35b309e466bfe7e82627e9b26c79b9f718a`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| ctmes | 20-0-2 | 91% | 91% | 77-100% | +400 | 11 | 0 |
| nicked_v44 | 14-0-8 | 64% | 64% | 41-86% | +97 | 11 | 0 |
| v6 | 15-0-7 | 68% | 68% | 50-86% | +132 | 11 | 0 |
| v7-base-bot | 12-0-10 | 55% | 55% | 36-73% | +32 | 11 | 0 |
| **overall** | 61-0-27 | 69% | 69% | 59-80% | +142 | 44 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades | 4-0-4 | 50% | 50% | 8 | 0 |
| default | 4-0-4 | 50% | 50% | 8 | 0 |
| big_empty | 4-0-4 | 50% | 50% | 8 | 0 |
| Trauma | 5-0-3 | 62% | 62% | 8 | 0 |
| stronghold | 5-0-3 | 62% | 62% | 8 | 0 |
| trophy | 6-0-2 | 75% | 75% | 8 | 0 |
| Colosseum | 6-0-2 | 75% | 75% | 8 | 0 |
| schooltime | 6-0-2 | 75% | 75% | 8 | 0 |
| default_small | 7-0-1 | 88% | 88% | 8 | 0 |
| Devil | 7-0-1 | 88% | 88% | 8 | 0 |
| arena | 7-0-1 | 88% | 88% | 8 | 0 |

candidate dragon deaths: head-to-head 4828, hit kelp 3136, hit other body 3043, no valid action/timeout 1045, hit itself 20

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for ctmes, nicked_v44, v6, v7-base-bot: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260926-151434-full-change-8bec11/map_matrix.md

SHA-256: `24663fef2ee53727e91277917f500b33a295e55d75c4b77a478120ec52584a99`

# candidate: every official map, both sides

Each cell is candidate W-D-L across its two sides. A 1-0-1 cell
may reflect side advantage rather than a policy improvement.

| map | nicked_v44 | ctmes | v6 |
|---|---|---|---|
| default_small | 2-0-0 | 2-0-0 | 2-0-0 |
| trophy | 1-0-1 | 2-0-0 | 2-0-0 |
| queen_of_spades | 0-0-2 | 2-0-0 | 1-0-1 |
| default | 1-0-1 | 2-0-0 | 1-0-1 |
| Devil | 2-0-0 | 2-0-0 | 1-0-1 |
| stronghold | 0-0-2 | 2-0-0 | 1-0-1 |
| Trauma | 1-0-1 | 2-0-0 | 2-0-0 |
| schooltime | 0-0-2 | 1-0-1 | 1-0-1 |
| big_empty | 0-0-2 | 2-0-0 | 1-0-1 |
| arena | 0-0-2 | 2-0-0 | 2-0-0 |
| Colosseum | 2-0-0 | 2-0-0 | 2-0-0 |


---

## results/20260926-151434-full-change-8bec11/full/summary.md

SHA-256: `93cf976aeb9886b19368769f10477d1ce68b3e9726c967192e964c2522867de8`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| ctmes | 21-0-1 | 95% | 95% | 86-100% | +529 | 11 | 0 |
| nicked_v44 | 9-0-13 | 41% | 41% | 18-64% | -64 | 11 | 0 |
| v6 | 16-0-6 | 73% | 73% | 59-86% | +170 | 11 | 0 |
| **overall** | 46-0-20 | 70% | 70% | 56-82% | +145 | 33 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| schooltime | 2-0-4 | 33% | 33% | 6 | 0 |
| queen_of_spades | 3-0-3 | 50% | 50% | 6 | 0 |
| stronghold | 3-0-3 | 50% | 50% | 6 | 0 |
| big_empty | 3-0-3 | 50% | 50% | 6 | 0 |
| default | 4-0-2 | 67% | 67% | 6 | 0 |
| arena | 4-0-2 | 67% | 67% | 6 | 0 |
| trophy | 5-0-1 | 83% | 83% | 6 | 0 |
| Devil | 5-0-1 | 83% | 83% | 6 | 0 |
| Trauma | 5-0-1 | 83% | 83% | 6 | 0 |
| default_small | 6-0-0 | 100% | 100% | 6 | 0 |
| Colosseum | 6-0-0 | 100% | 100% | 6 | 0 |

candidate dragon deaths: head-to-head 3116, hit kelp 2404, hit other body 1930, no valid action/timeout 1200, hit itself 4

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).
Fewer than 20 blocks for ctmes, nicked_v44, v6: those intervals understate the uncertainty (a result that never varied gets a zero-width interval); add maps or seeds before trusting them.


---

## results/20260926-163332-full-change-f35783/map_matrix.md

SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`



---

## results/20260926-163332-full-change-f35783/full/summary.md

SHA-256: `8a2963931ac5fb1ba229eac505dd4a407d81067579c6a07f395191a945100577`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| ctmes | 60-0-6 | 91% | 91% | 83-97% | +400 | 33 | 0 |
| nicked_v44 | 29-0-37 | 44% | 44% | 29-59% | -42 | 33 | 0 |
| v6 | 42-0-24 | 64% | 64% | 52-76% | +97 | 33 | 0 |
| v7-base-bot | 30-0-36 | 45% | 45% | 33-59% | -32 | 33 | 0 |
| **overall** | 161-0-103 | 61% | 61% | 54-67% | +78 | 132 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default | 9-0-15 | 38% | 38% | 24 | 0 |
| stronghold | 12-0-12 | 50% | 50% | 24 | 0 |
| schooltime | 12-0-12 | 50% | 50% | 24 | 0 |
| big_empty | 12-0-12 | 50% | 50% | 24 | 0 |
| trophy | 13-0-11 | 54% | 54% | 24 | 0 |
| queen_of_spades | 14-0-10 | 58% | 58% | 24 | 0 |
| Trauma | 15-0-9 | 62% | 62% | 24 | 0 |
| arena | 15-0-9 | 62% | 62% | 24 | 0 |
| Colosseum | 18-0-6 | 75% | 75% | 24 | 0 |
| default_small | 19-0-5 | 79% | 79% | 24 | 0 |
| Devil | 22-0-2 | 92% | 92% | 24 | 0 |

candidate dragon deaths: head-to-head 13979, hit kelp 10201, hit other body 9097, no valid action/timeout 3252, hit itself 50

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260926-163333-full-change-c38170/map_matrix.md

SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`



---

## results/20260926-163333-full-change-c38170/full/summary.md

SHA-256: `78b1e95c5a3478c7b3297939de8b0b73ac2ad8366c4103745c550a3a3ddfbe13`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| ctmes | 59-0-7 | 89% | 89% | 82-95% | +370 | 33 | 0 |
| nicked_v44 | 32-0-34 | 48% | 48% | 36-62% | -11 | 33 | 0 |
| v6 | 43-0-23 | 65% | 65% | 55-76% | +109 | 33 | 0 |
| **overall** | 134-0-64 | 68% | 68% | 61-75% | +128 | 99 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 7-0-11 | 39% | 39% | 18 | 0 |
| default | 8-0-10 | 44% | 44% | 18 | 0 |
| big_empty | 8-0-10 | 44% | 44% | 18 | 0 |
| stronghold | 10-0-8 | 56% | 56% | 18 | 0 |
| queen_of_spades | 12-0-6 | 67% | 67% | 18 | 0 |
| schooltime | 13-0-5 | 72% | 72% | 18 | 0 |
| default_small | 14-0-4 | 78% | 78% | 18 | 0 |
| trophy | 15-0-3 | 83% | 83% | 18 | 0 |
| arena | 15-0-3 | 83% | 83% | 18 | 0 |
| Colosseum | 15-0-3 | 83% | 83% | 18 | 0 |
| Devil | 17-0-1 | 94% | 94% | 18 | 0 |

candidate dragon deaths: head-to-head 9324, hit kelp 7014, hit other body 5760, no valid action/timeout 3375, hit itself 8

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260926-183834-full-change-162756/full/summary.md

SHA-256: `2dd35c709bbacb3a7ada7bc78f76ef58bc464ebd547146c39fc969979c7166b3`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 16-0-28 | 36% | 36% | 18-55% | -97 | 22 | 0 |
| nicked_v44 | 10-0-34 | 23% | 23% | 9-39% | -213 | 22 | 0 |
| v7-base | 12-0-32 | 27% | 27% | 14-43% | -170 | 22 | 0 |
| **overall** | 38-0-94 | 29% | 29% | 20-38% | -157 | 66 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| trophy | 0-0-12 | 0% | 0% | 12 | 0 |
| stronghold | 0-0-12 | 0% | 0% | 12 | 0 |
| Trauma | 1-0-11 | 8% | 8% | 12 | 0 |
| Devil | 2-0-10 | 17% | 17% | 12 | 0 |
| schooltime | 3-0-9 | 25% | 25% | 12 | 0 |
| default_small | 4-0-8 | 33% | 33% | 12 | 0 |
| arena | 4-0-8 | 33% | 33% | 12 | 0 |
| big_empty | 4-0-8 | 33% | 33% | 12 | 0 |
| default | 6-0-6 | 50% | 50% | 12 | 0 |
| queen_of_spades | 7-0-5 | 58% | 58% | 12 | 0 |
| Colosseum | 7-0-5 | 58% | 58% | 12 | 0 |

candidate dragon deaths: head-to-head 4389, hit other body 3236, hit itself 2990, hit kelp 2515

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260926-183834-full-change-3fe65d/full/summary.md

SHA-256: `94cfd0ba59b4ce7a191ccb7a4fdac202bf15154afc80093b601426a9f3b41ba3`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 17-0-27 | 39% | 39% | 20-59% | -80 | 22 | 0 |
| nicked_v44 | 12-0-32 | 27% | 27% | 14-41% | -170 | 22 | 0 |
| v7-base | 10-0-34 | 23% | 23% | 9-39% | -213 | 22 | 0 |
| **overall** | 39-0-93 | 30% | 30% | 20-39% | -151 | 66 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| stronghold | 0-0-12 | 0% | 0% | 12 | 0 |
| trophy | 1-0-11 | 8% | 8% | 12 | 0 |
| Trauma | 1-0-11 | 8% | 8% | 12 | 0 |
| Devil | 2-0-10 | 17% | 17% | 12 | 0 |
| big_empty | 2-0-10 | 17% | 17% | 12 | 0 |
| queen_of_spades | 3-0-9 | 25% | 25% | 12 | 0 |
| schooltime | 3-0-9 | 25% | 25% | 12 | 0 |
| default_small | 6-0-6 | 50% | 50% | 12 | 0 |
| arena | 6-0-6 | 50% | 50% | 12 | 0 |
| default | 7-0-5 | 58% | 58% | 12 | 0 |
| Colosseum | 8-0-4 | 67% | 67% | 12 | 0 |

candidate dragon deaths: head-to-head 5108, hit other body 3342, hit itself 2875, hit kelp 2388

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260926-183835-full-change-bb2dcf/full/summary.md

SHA-256: `f5183fae59a3b7bb7857adb1ed963266ec82ef23d5b731f5f076f83d337236af`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 16-0-28 | 36% | 36% | 18-55% | -97 | 22 | 0 |
| nicked_v44 | 6-0-38 | 14% | 14% | 2-27% | -321 | 22 | 0 |
| v7-base | 9-0-35 | 20% | 20% | 7-34% | -236 | 22 | 0 |
| **overall** | 31-0-101 | 23% | 23% | 14-33% | -205 | 66 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| trophy | 0-0-12 | 0% | 0% | 12 | 0 |
| stronghold | 0-0-12 | 0% | 0% | 12 | 0 |
| Trauma | 0-0-12 | 0% | 0% | 12 | 0 |
| Devil | 1-0-11 | 8% | 8% | 12 | 0 |
| big_empty | 1-0-11 | 8% | 8% | 12 | 0 |
| default_small | 3-0-9 | 25% | 25% | 12 | 0 |
| arena | 3-0-9 | 25% | 25% | 12 | 0 |
| queen_of_spades | 4-0-8 | 33% | 33% | 12 | 0 |
| default | 5-0-7 | 42% | 42% | 12 | 0 |
| schooltime | 5-0-7 | 42% | 42% | 12 | 0 |
| Colosseum | 9-0-3 | 75% | 75% | 12 | 0 |

candidate dragon deaths: head-to-head 5275, hit other body 4186, hit itself 3569, hit kelp 2783

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260926-183836-full-change-d496cd/full/summary.md

SHA-256: `87d2dc2a708379a2a9af0a7c7dfd49c1b5a19ddd411756a66399318f0155aeb5`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 5-0-39 | 11% | 11% | 0-25% | -357 | 22 | 0 |
| nicked_v44 | 2-0-42 | 5% | 5% | 0-11% | -529 | 22 | 0 |
| v7-base | 4-0-40 | 9% | 9% | 2-18% | -400 | 22 | 0 |
| **overall** | 11-0-121 | 8% | 8% | 3-14% | -417 | 66 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default_small | 0-0-12 | 0% | 0% | 12 | 0 |
| trophy | 0-0-12 | 0% | 0% | 12 | 0 |
| queen_of_spades | 0-0-12 | 0% | 0% | 12 | 0 |
| default | 0-0-12 | 0% | 0% | 12 | 0 |
| Devil | 0-0-12 | 0% | 0% | 12 | 0 |
| schooltime | 0-0-12 | 0% | 0% | 12 | 0 |
| arena | 0-0-12 | 0% | 0% | 12 | 0 |
| Colosseum | 0-0-12 | 0% | 0% | 12 | 0 |
| big_empty | 0-0-12 | 0% | 0% | 12 | 0 |
| Trauma | 3-0-9 | 25% | 25% | 12 | 0 |
| stronghold | 8-0-4 | 67% | 67% | 12 | 0 |

candidate dragon deaths: head-to-head 143, hit other body 137, hit itself 79, hit kelp 53

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260926-183837-full-change-60b9a8/full/summary.md

SHA-256: `457c2797c518e99d4b5e23d091c6e091add41fa98a70b00ca7ad0049f6d78077`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked | 1-0-43 | 2% | 2% | 0-7% | -653 | 22 | 0 |
| nicked_v44 | 0-0-44 | 0% | 0% | 0-0% | -1200 | 22 | 0 |
| v7-base | 1-0-43 | 2% | 2% | 0-7% | -653 | 22 | 0 |
| **overall** | 2-0-130 | 2% | 2% | 0-4% | -725 | 66 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default_small | 0-0-12 | 0% | 0% | 12 | 0 |
| queen_of_spades | 0-0-12 | 0% | 0% | 12 | 0 |
| trophy | 0-0-12 | 0% | 0% | 12 | 0 |
| Devil | 0-0-12 | 0% | 0% | 12 | 0 |
| default | 0-0-12 | 0% | 0% | 12 | 0 |
| schooltime | 0-0-12 | 0% | 0% | 12 | 0 |
| arena | 0-0-12 | 0% | 0% | 12 | 0 |
| Colosseum | 0-0-12 | 0% | 0% | 12 | 0 |
| big_empty | 0-0-12 | 0% | 0% | 12 | 0 |
| stronghold | 1-0-11 | 8% | 8% | 12 | 0 |
| Trauma | 1-0-11 | 8% | 8% | 12 | 0 |

candidate dragon deaths: hit other body 1488, head-to-head 1464, hit itself 928, hit kelp 785

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260926-204339-ablate-af847f/report.md

SHA-256: `be3674c34f899ae13141829d41eba5ad4c580e393921190d6bced73e4a8455c0`

# Ablation report: 20260926-204339-ablate-af847f

1 seeds, opponents splitter; 11 official + 0 extra maps, both sides. Objective: margin. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.717, wins 22/22; by opponent: splitter +0.717

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs splitter | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|
| no_hub | -0.044 [-0.197, +0.055] | neutral | +0.019 | -0.015 [-0.101, +0.041] | neutral | -0.015 | -0.015 | - | 22/22 |
| no_food | -0.038 [-0.114, +0.029] | neutral | -0.023 | -0.031 [-0.077, +0.008] | neutral | -0.031 | -0.031 | - | 21/22 |

Noise: observed CI half-width 0.057 with 1 seed(s); run with 2+ seeds for a per-cell estimate.


---

## results/20260926-204722-ablate-903314/report.md

SHA-256: `53be85fe513190555621026fa228ec180fb4d4fcf99b5be5533a12160203379c`

# Ablation report: 20260926-204722-ablate-903314

6 seeds, opponents nicked; 11 official + 4 extra maps, both sides. Delta = variant margin minus base margin on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.147, wins 128/180; by opponent: nicked +0.147

| variant | delta all [95% CI] | verdict | vs nicked | official | extra | wins |
|---|---|---|---|---|---|---|

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.332 over 30 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.332^2 / (30 * K)): K=2: 0.119, K=3: 0.097, K=4: 0.084, K=6: 0.069, K=8: 0.059


---

## results/20260926-214429-ablate-346278/report.md

SHA-256: `57fd499449e30de35d78d69900ae3aa5c21c351f66db089443f0352f4fefc5c8`

# Ablation report: 20260926-214429-ablate-346278

4 seeds, opponents v7-base-bot, nicked; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.134, wins 141/240; by opponent: v7-base-bot +0.000, nicked +0.267

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs v7-base-bot | vs nicked | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|
| no_food | -0.255 [-0.376, -0.137] | essential | -0.235 | -0.248 [-0.355, -0.143] | essential | -0.309 | -0.188 | -0.282 | -0.155 | 103/240 |
| no_spawn | -0.123 [-0.218, -0.014] | essential | -0.099 | -0.115 [-0.205, -0.026] | essential | -0.168 | -0.063 | -0.150 | -0.020 | 123/240 |
| no_explore | +0.008 [-0.109, +0.117] | neutral | -0.010 | +0.002 [-0.080, +0.078] | neutral | +0.039 | -0.034 | +0.044 | -0.113 | 142/240 |
| no_trap | +0.131 [+0.024, +0.231] | harmful (drop) | -0.066 | +0.065 [-0.013, +0.147] | neutral | +0.123 | +0.007 | -0.025 | +0.315 | 154/240 |
| no_deadend | -0.029 [-0.123, +0.063] | neutral | -0.052 | -0.037 [-0.112, +0.037] | neutral | -0.076 | +0.002 | -0.065 | +0.041 | 134/240 |
| no_headsafe | -0.017 [-0.101, +0.078] | neutral | -0.024 | -0.019 [-0.089, +0.059] | neutral | -0.077 | +0.039 | -0.022 | -0.011 | 139/240 |
| no_revisit | +0.055 [-0.059, +0.171] | neutral | -0.005 | +0.035 [-0.052, +0.121] | neutral | -0.039 | +0.109 | +0.004 | +0.121 | 147/240 |
| no_fan | -0.016 [-0.114, +0.083] | neutral | +0.085 | +0.018 [-0.055, +0.094] | neutral | +0.063 | -0.027 | +0.047 | -0.061 | 146/240 |
| no_straight | -0.004 [-0.100, +0.102] | neutral | -0.001 | -0.003 [-0.080, +0.076] | neutral | -0.019 | +0.013 | -0.043 | +0.107 | 141/240 |
| no_portal | -0.006 [-0.080, +0.065] | neutral | -0.022 | -0.012 [-0.066, +0.041] | neutral | -0.003 | -0.020 | -0.003 | -0.035 | 139/240 |
| no_v3model | -0.355 [-0.463, -0.252] | essential | -0.271 | -0.327 [-0.415, -0.240] | essential | -0.320 | -0.334 | -0.381 | -0.179 | 92/240 |
| no_attack | -0.029 [-0.130, +0.066] | neutral | -0.195 | -0.085 [-0.165, -0.002] | essential | -0.173 | +0.004 | -0.117 | +0.004 | 130/240 |
| no_hunt | +0.028 [-0.045, +0.100] | neutral | +0.023 | +0.026 [-0.043, +0.093] | neutral | +0.021 | +0.032 | +0.011 | +0.069 | 146/240 |
| no_defend | +0.025 [-0.020, +0.068] | neutral | +0.118 | +0.056 [+0.016, +0.098] | harmful (drop) | +0.092 | +0.019 | +0.063 | +0.034 | 153/240 |
| no_hub | -0.115 [-0.200, -0.033] | essential | +0.051 | -0.060 [-0.130, +0.015] | neutral | -0.081 | -0.039 | -0.040 | -0.115 | 130/240 |
| no_goal | +0.037 [-0.094, +0.174] | neutral | +0.012 | +0.029 [-0.077, +0.138] | neutral | +0.047 | +0.011 | +0.019 | +0.056 | 147/240 |
| no_feed | -0.038 [-0.097, +0.025] | neutral | -0.086 | -0.054 [-0.110, +0.001] | neutral | -0.048 | -0.060 | -0.045 | -0.077 | 130/240 |
| no_protect | +0.017 [-0.038, +0.069] | neutral | +0.000 | +0.011 [-0.025, +0.047] | neutral | -0.043 | +0.066 | +0.004 | +0.030 | 143/240 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.649 over 60 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.649^2 / (60 * K)): K=2: 0.164, K=3: 0.134, K=4: 0.116, K=6: 0.095, K=8: 0.082


---

## results/20260927-021008-ablate-5c0197/report.md

SHA-256: `c914861cab0171bcba2dcbefbf5f6580fe3f2bb007e686a997cc5cc850446484`

# Ablation report: 20260927-021008-ablate-5c0197

4 seeds, opponents v7-base-bot, nicked; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.165, wins 147/240; by opponent: v7-base-bot +0.000, nicked +0.331

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs v7-base-bot | vs nicked | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|
| drop_harmful | +0.131 [+0.051, +0.210] | harmful (drop) | -0.022 | +0.080 [+0.018, +0.148] | harmful (drop) | +0.104 | +0.057 | +0.018 | +0.250 | 161/240 |
| lean | +0.098 [-0.057, +0.248] | neutral | +0.007 | +0.068 [-0.050, +0.177] | neutral | +0.122 | +0.013 | -0.000 | +0.254 | 159/240 |
| simplified | +0.005 [-0.143, +0.148] | neutral | +0.109 | +0.040 [-0.085, +0.149] | neutral | +0.097 | -0.018 | -0.048 | +0.280 | 156/240 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.645 over 60 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.645^2 / (60 * K)): K=2: 0.163, K=3: 0.133, K=4: 0.115, K=6: 0.094, K=8: 0.082


---

## results/20260927-061647-full-change-fc188d/full/summary.md

SHA-256: `bc5d95567a57426bd7df5bef018bad79bcdc986a5626a98172a82326c7387adc`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| cpp_leviathan3 | 59-0-31 | 66% | 66% | 53-77% | +112 | 45 | 0 |
| ctmes | 87-0-3 | 97% | 97% | 92-100% | +585 | 45 | 0 |
| nicked_v44 | 41-0-49 | 46% | 46% | 32-59% | -31 | 45 | 0 |
| v6 | 65-0-25 | 72% | 72% | 62-81% | +166 | 45 | 0 |
| **overall** | 252-0-108 | 70% | 70% | 64-76% | +147 | 180 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| queen_of_spades | 8-0-16 | 33% | 33% | 24 | 0 |
| Slithery_Fight | 9-0-15 | 38% | 38% | 24 | 0 |
| default | 12-0-12 | 50% | 50% | 24 | 0 |
| big_empty | 13-0-11 | 54% | 54% | 24 | 0 |
| Portals | 16-0-8 | 67% | 67% | 24 | 0 |
| stronghold | 17-0-7 | 71% | 71% | 24 | 0 |
| schooltime | 17-0-7 | 71% | 71% | 24 | 0 |
| Trauma | 18-0-6 | 75% | 75% | 24 | 0 |
| Prisoners_Dilemma | 18-0-6 | 75% | 75% | 24 | 0 |
| default_small | 19-0-5 | 79% | 79% | 24 | 0 |
| trophy | 19-0-5 | 79% | 79% | 24 | 0 |
| Colosseum | 20-0-4 | 83% | 83% | 24 | 0 |
| Devil | 21-0-3 | 88% | 88% | 24 | 0 |
| arena | 22-0-2 | 92% | 92% | 24 | 0 |
| Autarky | 23-0-1 | 96% | 96% | 24 | 0 |

candidate dragon deaths: hit kelp 59725, head-to-head 18595, hit other body 12234, no valid action/timeout 10256, hit itself 37

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260927-061649-full-change-db2585/full/summary.md

SHA-256: `cdf16b598c53c76933b5fcf99d3cd2115134fc9cf3a4015f8ee1454c57988069`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| cpp_leviathan3 | 60-0-30 | 67% | 67% | 56-78% | +120 | 45 | 0 |
| ctmes | 83-0-7 | 92% | 92% | 87-97% | +430 | 45 | 0 |
| nicked_v44 | 43-0-47 | 48% | 48% | 36-60% | -15 | 45 | 0 |
| v6 | 58-0-32 | 64% | 64% | 53-74% | +103 | 45 | 0 |
| **overall** | 244-0-116 | 68% | 68% | 62-73% | +129 | 180 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| default | 8-0-16 | 33% | 33% | 24 | 0 |
| Trauma | 11-0-13 | 46% | 46% | 24 | 0 |
| Slithery_Fight | 11-0-13 | 46% | 46% | 24 | 0 |
| Portals | 11-0-13 | 46% | 46% | 24 | 0 |
| big_empty | 13-0-11 | 54% | 54% | 24 | 0 |
| queen_of_spades | 15-0-9 | 62% | 62% | 24 | 0 |
| stronghold | 16-0-8 | 67% | 67% | 24 | 0 |
| Prisoners_Dilemma | 17-0-7 | 71% | 71% | 24 | 0 |
| default_small | 19-0-5 | 79% | 79% | 24 | 0 |
| schooltime | 19-0-5 | 79% | 79% | 24 | 0 |
| Colosseum | 19-0-5 | 79% | 79% | 24 | 0 |
| arena | 20-0-4 | 83% | 83% | 24 | 0 |
| trophy | 21-0-3 | 88% | 88% | 24 | 0 |
| Autarky | 21-0-3 | 88% | 88% | 24 | 0 |
| Devil | 23-0-1 | 96% | 96% | 24 | 0 |

candidate dragon deaths: hit kelp 26000, head-to-head 14668, hit other body 10416, no valid action/timeout 8921, hit itself 19

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260927-190107-ablate-6028c1/report.md

SHA-256: `c7d2bc6ccae9997daa96da6fdf55085a3b53014d70e77e3e45cbf39c9764a1e7`

# Ablation report: 20260927-190107-ablate-6028c1

3 seeds, opponents v7-base-bot, cpp_nicked_v75, cpp_leviathan3; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.143, wins 156/270; by opponent: v7-base-bot +0.294, cpp_nicked_v75 -0.187, cpp_leviathan3 +0.321

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs v7-base-bot | vs cpp_nicked_v75 | vs cpp_leviathan3 | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|
| age | +0.068 [-0.011, +0.148] | neutral | -0.075 | +0.020 [-0.043, +0.088] | neutral | -0.046 | +0.008 | +0.100 | +0.002 | +0.070 | 160/270 |
| vor | +0.016 [-0.080, +0.109] | neutral | -0.025 | +0.002 [-0.072, +0.072] | neutral | +0.036 | -0.045 | +0.016 | -0.003 | +0.018 | 158/270 |
| age_vor | +0.066 [-0.037, +0.177] | neutral | -0.069 | +0.021 [-0.062, +0.113] | neutral | +0.083 | -0.043 | +0.022 | +0.036 | -0.021 | 159/270 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.568 over 90 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.568^2 / (90 * K)): K=2: 0.117, K=3: 0.096, K=4: 0.083, K=6: 0.068, K=8: 0.059


---

## results/20260927-231030-full-change-1f35bb/full/summary.md

SHA-256: `9193d04a6f24c48f025581ed1b6d4cdbb4e8bce419e27ff1c9f9f3dfae3e4fab`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked_lab | 37-0-53 | 41% | 41% | 31-51% | -62 | 45 | 0 |
| nicked_v44 | 42-0-48 | 47% | 47% | 33-59% | -23 | 45 | 0 |
| v6 | 74-0-16 | 82% | 82% | 73-90% | +266 | 45 | 0 |
| **overall** | 153-0-117 | 57% | 57% | 50-63% | +47 | 135 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 4-0-14 | 22% | 22% | 18 | 0 |
| Slithery_Fight | 5-0-13 | 28% | 28% | 18 | 0 |
| big_empty | 6-0-12 | 33% | 33% | 18 | 0 |
| trophy | 7-0-11 | 39% | 39% | 18 | 0 |
| queen_of_spades | 8-0-10 | 44% | 44% | 18 | 0 |
| stronghold | 9-0-9 | 50% | 50% | 18 | 0 |
| schooltime | 9-0-9 | 50% | 50% | 18 | 0 |
| Portals | 9-0-9 | 50% | 50% | 18 | 0 |
| arena | 11-0-7 | 61% | 61% | 18 | 0 |
| default_small | 12-0-6 | 67% | 67% | 18 | 0 |
| default | 12-0-6 | 67% | 67% | 18 | 0 |
| Devil | 13-0-5 | 72% | 72% | 18 | 0 |
| Prisoners_Dilemma | 14-0-4 | 78% | 78% | 18 | 0 |
| Colosseum | 16-0-2 | 89% | 89% | 18 | 0 |
| Autarky | 18-0-0 | 100% | 100% | 18 | 0 |

candidate dragon deaths: hit kelp 38475, head-to-head 16314, hit other body 7972, no valid action/timeout 6510, hit itself 17

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260927-231031-full-change-51b4d9/full/summary.md

SHA-256: `fc6fb79da9fb1d6295ec98633ee91fa3219f265953341857ee328baf8ef82cee`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked_lab | 23-0-67 | 26% | 26% | 16-37% | -186 | 45 | 0 |
| nicked_v44 | 43-0-47 | 48% | 48% | 36-60% | -15 | 45 | 0 |
| v6 | 58-0-32 | 64% | 64% | 54-74% | +103 | 45 | 0 |
| **overall** | 124-0-146 | 46% | 46% | 39-53% | -28 | 135 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Slithery_Fight | 2-0-16 | 11% | 11% | 18 | 0 |
| Trauma | 4-0-14 | 22% | 22% | 18 | 0 |
| default | 5-0-13 | 28% | 28% | 18 | 0 |
| Portals | 5-0-13 | 28% | 28% | 18 | 0 |
| queen_of_spades | 6-0-12 | 33% | 33% | 18 | 0 |
| stronghold | 6-0-12 | 33% | 33% | 18 | 0 |
| schooltime | 7-0-11 | 39% | 39% | 18 | 0 |
| big_empty | 7-0-11 | 39% | 39% | 18 | 0 |
| trophy | 9-0-9 | 50% | 50% | 18 | 0 |
| default_small | 11-0-7 | 61% | 61% | 18 | 0 |
| Colosseum | 11-0-7 | 61% | 61% | 18 | 0 |
| Prisoners_Dilemma | 11-0-7 | 61% | 61% | 18 | 0 |
| arena | 12-0-6 | 67% | 67% | 18 | 0 |
| Autarky | 13-0-5 | 72% | 72% | 18 | 0 |
| Devil | 15-0-3 | 83% | 83% | 18 | 0 |

candidate dragon deaths: hit kelp 17329, head-to-head 12517, hit other body 6010, no valid action/timeout 5392, hit itself 7

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260928-044431-full-change-62591f/full/summary.md

SHA-256: `73060455a6010bd88f4f411584dbc066b53a084fc8fcfc63a6ad7923f70c0246`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked_lab | 33-0-57 | 37% | 37% | 26-48% | -95 | 45 | 0 |
| nicked_v44 | 48-0-42 | 53% | 53% | 41-66% | +23 | 45 | 0 |
| v6 | 72-0-18 | 80% | 80% | 71-88% | +241 | 45 | 0 |
| **overall** | 153-0-117 | 57% | 57% | 50-63% | +47 | 135 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Slithery_Fight | 3-0-15 | 17% | 17% | 18 | 0 |
| Trauma | 6-0-12 | 33% | 33% | 18 | 0 |
| big_empty | 6-0-12 | 33% | 33% | 18 | 0 |
| trophy | 7-0-11 | 39% | 39% | 18 | 0 |
| stronghold | 7-0-11 | 39% | 39% | 18 | 0 |
| queen_of_spades | 9-0-9 | 50% | 50% | 18 | 0 |
| schooltime | 11-0-7 | 61% | 61% | 18 | 0 |
| Portals | 11-0-7 | 61% | 61% | 18 | 0 |
| arena | 12-0-6 | 67% | 67% | 18 | 0 |
| Prisoners_Dilemma | 12-0-6 | 67% | 67% | 18 | 0 |
| default_small | 13-0-5 | 72% | 72% | 18 | 0 |
| default | 13-0-5 | 72% | 72% | 18 | 0 |
| Devil | 13-0-5 | 72% | 72% | 18 | 0 |
| Colosseum | 14-0-4 | 78% | 78% | 18 | 0 |
| Autarky | 16-0-2 | 89% | 89% | 18 | 0 |

candidate dragon deaths: hit kelp 39440, head-to-head 16491, hit other body 8077, no valid action/timeout 6817, hit itself 30

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260928-044432-full-change-5fc479/full/summary.md

SHA-256: `00c53efd406dce1de859c94d2403b0c2c1ee4d73c8864aaa0dfa860f6218ca0e`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| nicked_lab | 37-0-53 | 41% | 41% | 31-51% | -62 | 45 | 0 |
| nicked_v44 | 42-0-48 | 47% | 47% | 34-60% | -23 | 45 | 0 |
| v6 | 74-0-16 | 82% | 82% | 73-90% | +266 | 45 | 0 |
| **overall** | 153-0-117 | 57% | 57% | 50-64% | +47 | 135 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 4-0-14 | 22% | 22% | 18 | 0 |
| Slithery_Fight | 5-0-13 | 28% | 28% | 18 | 0 |
| big_empty | 6-0-12 | 33% | 33% | 18 | 0 |
| trophy | 7-0-11 | 39% | 39% | 18 | 0 |
| queen_of_spades | 8-0-10 | 44% | 44% | 18 | 0 |
| stronghold | 9-0-9 | 50% | 50% | 18 | 0 |
| schooltime | 9-0-9 | 50% | 50% | 18 | 0 |
| Portals | 9-0-9 | 50% | 50% | 18 | 0 |
| arena | 11-0-7 | 61% | 61% | 18 | 0 |
| default_small | 12-0-6 | 67% | 67% | 18 | 0 |
| default | 12-0-6 | 67% | 67% | 18 | 0 |
| Devil | 13-0-5 | 72% | 72% | 18 | 0 |
| Prisoners_Dilemma | 14-0-4 | 78% | 78% | 18 | 0 |
| Colosseum | 16-0-2 | 89% | 89% | 18 | 0 |
| Autarky | 18-0-0 | 100% | 100% | 18 | 0 |

candidate dragon deaths: hit kelp 38475, head-to-head 16314, hit other body 7972, no valid action/timeout 6510, hit itself 17

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260928-140413-ablate-2970a3/report.md

SHA-256: `d98c03a6e5b20067b3cd0723de13ef96ccb497429bdcfd2d14db54ca7c79fb7d`

# Ablation report: 20260928-140413-ablate-2970a3

3 seeds, opponents cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.152, wins 210/360; by opponent: cpp_nicked_v75 -0.363, cpp_leviathan3 +0.449, v7-base-bot +0.281, nicked_v44 +0.241

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| kb | +0.027 [-0.022, +0.075] | neutral | +0.008 | +0.021 [-0.012, +0.052] | neutral | +0.001 | +0.038 | +0.060 | -0.016 | -0.007 | +0.098 | 218/360 |
| kbbig | +0.059 [-0.004, +0.126] | neutral | +0.136 | +0.085 [+0.032, +0.138] | harmful (drop) | +0.035 | +0.105 | +0.104 | +0.095 | +0.052 | +0.173 | 237/360 |
| dead | -0.008 [-0.086, +0.068] | neutral | +0.008 | -0.003 [-0.054, +0.048] | neutral | -0.014 | -0.027 | -0.042 | +0.073 | +0.043 | -0.127 | 213/360 |
| all | +0.002 [-0.082, +0.087] | neutral | +0.136 | +0.047 [-0.024, +0.110] | neutral | +0.029 | -0.010 | +0.048 | +0.121 | +0.093 | -0.079 | 228/360 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.581 over 120 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.581^2 / (120 * K)): K=2: 0.104, K=3: 0.085, K=4: 0.073, K=6: 0.060, K=8: 0.052


---

## results/20260928-174742-ablate-8cf646/report.md

SHA-256: `d4136a1c72fe52d39a57c130a88518a858443a0a2391e9607e0da4e9e138a6f2`

# Ablation report: 20260928-174742-ablate-8cf646

3 seeds, opponents cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.273, wins 247/360; by opponent: cpp_nicked_v75 -0.155, cpp_leviathan3 +0.566, v7-base-bot +0.331, nicked_v44 +0.349

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| room8 | -0.092 [-0.179, -0.004] | essential | -0.023 | -0.069 [-0.130, -0.012] | essential | -0.019 | -0.127 | -0.057 | -0.073 | -0.086 | -0.023 | 229/360 |
| room16 | -0.059 [-0.106, -0.010] | essential | +0.068 | -0.017 [-0.058, +0.023] | neutral | -0.015 | -0.042 | +0.001 | -0.011 | -0.006 | -0.048 | 242/360 |
| dead60 | -0.073 [-0.150, +0.006] | neutral | +0.008 | -0.046 [-0.100, +0.005] | neutral | -0.043 | -0.064 | -0.021 | -0.057 | -0.038 | -0.069 | 234/360 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.559 over 120 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.559^2 / (120 * K)): K=2: 0.100, K=3: 0.082, K=4: 0.071, K=6: 0.058, K=8: 0.050


---

## results/20260928-180616-ablate-22301c/report.md

SHA-256: `53bff0d5831b2da265db7767e7bba90a57021c7d8c45d4b4e90242013ac98552`

# Ablation report: 20260928-180616-ablate-22301c

3 seeds, opponents cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.273, wins 247/360; by opponent: cpp_nicked_v75 -0.155, cpp_leviathan3 +0.566, v7-base-bot +0.331, nicked_v44 +0.349

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| brief | -0.012 [-0.043, +0.017] | neutral | +0.010 | -0.005 [-0.027, +0.015] | neutral | +0.018 | -0.012 | -0.011 | -0.013 | -0.007 | +0.002 | 247/360 |
| brief_room8 | -0.127 [-0.204, -0.053] | essential | -0.023 | -0.092 [-0.149, -0.041] | essential | -0.001 | -0.167 | -0.059 | -0.142 | -0.097 | -0.078 | 221/360 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.559 over 120 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.559^2 / (120 * K)): K=2: 0.100, K=3: 0.082, K=4: 0.071, K=6: 0.058, K=8: 0.050


---

## results/20260928-224114-full-change-f05cec/full/summary.md

SHA-256: `18f47b89658c6dfb95e0cb75558e93c0795833545b0e34002b7478ebf5550873`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| ctmes | 88-0-2 | 98% | 98% | 94-100% | +657 | 45 | 0 |
| nicked_lab | 38-0-52 | 42% | 42% | 32-52% | -54 | 45 | 0 |
| v6 | 81-0-9 | 90% | 90% | 83-96% | +382 | 45 | 0 |
| **overall** | 207-0-63 | 77% | 77% | 71-82% | +207 | 135 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| trophy | 12-0-6 | 67% | 67% | 18 | 0 |
| Trauma | 12-0-6 | 67% | 67% | 18 | 0 |
| default_small | 13-0-5 | 72% | 72% | 18 | 0 |
| Devil | 13-0-5 | 72% | 72% | 18 | 0 |
| schooltime | 13-0-5 | 72% | 72% | 18 | 0 |
| arena | 13-0-5 | 72% | 72% | 18 | 0 |
| big_empty | 13-0-5 | 72% | 72% | 18 | 0 |
| Slithery_Fight | 13-0-5 | 72% | 72% | 18 | 0 |
| queen_of_spades | 14-0-4 | 78% | 78% | 18 | 0 |
| default | 14-0-4 | 78% | 78% | 18 | 0 |
| stronghold | 14-0-4 | 78% | 78% | 18 | 0 |
| Prisoners_Dilemma | 14-0-4 | 78% | 78% | 18 | 0 |
| Colosseum | 16-0-2 | 89% | 89% | 18 | 0 |
| Portals | 16-0-2 | 89% | 89% | 18 | 0 |
| Autarky | 17-0-1 | 94% | 94% | 18 | 0 |

candidate dragon deaths: hit kelp 39523, head-to-head 14808, hit other body 7490, no valid action/timeout 7224, hit itself 12

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260928-224115-full-change-345748/full/summary.md

SHA-256: `ea703629edc6d1c2fec63c8de7be421a5d5a4392483199daf83894b7bb1c4d9d`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| ctmes | 87-0-3 | 97% | 97% | 92-100% | +585 | 45 | 0 |
| nicked_lab | 37-0-53 | 41% | 41% | 31-51% | -62 | 45 | 0 |
| v6 | 74-0-16 | 82% | 82% | 73-90% | +266 | 45 | 0 |
| **overall** | 198-0-72 | 73% | 73% | 67-79% | +176 | 135 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| Trauma | 9-0-9 | 50% | 50% | 18 | 0 |
| big_empty | 10-0-8 | 56% | 56% | 18 | 0 |
| Slithery_Fight | 11-0-7 | 61% | 61% | 18 | 0 |
| trophy | 12-0-6 | 67% | 67% | 18 | 0 |
| stronghold | 12-0-6 | 67% | 67% | 18 | 0 |
| schooltime | 12-0-6 | 67% | 67% | 18 | 0 |
| arena | 13-0-5 | 72% | 72% | 18 | 0 |
| default_small | 14-0-4 | 78% | 78% | 18 | 0 |
| queen_of_spades | 14-0-4 | 78% | 78% | 18 | 0 |
| Devil | 14-0-4 | 78% | 78% | 18 | 0 |
| default | 14-0-4 | 78% | 78% | 18 | 0 |
| Prisoners_Dilemma | 14-0-4 | 78% | 78% | 18 | 0 |
| Portals | 15-0-3 | 83% | 83% | 18 | 0 |
| Colosseum | 16-0-2 | 89% | 89% | 18 | 0 |
| Autarky | 18-0-0 | 100% | 100% | 18 | 0 |

candidate dragon deaths: hit kelp 40370, head-to-head 14954, hit other body 7720, no valid action/timeout 6765, hit itself 12

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260929-001450-ablate-0e245d/report.md

SHA-256: `d79c6cfccba76ab8d6b1c5ddc7e2c0b9b8e12f4653267b85da6bb1bcde75becd`

# Ablation report: 20260929-001450-ablate-0e245d

3 seeds, opponents cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44; 11 official + 14 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.209, wins 386/600; by opponent: cpp_nicked_v75 -0.238, cpp_leviathan3 +0.462, v7-base-bot +0.409, nicked_v44 +0.202

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hubbook_off | -0.086 [-0.165, -0.008] | essential | +0.001 | -0.034 [-0.088, +0.022] | neutral | -0.130 | -0.048 | +0.019 | +0.024 | -0.103 | +0.021 | 371/600 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.552 over 200 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.552^2 / (200 * K)): K=2: 0.076, K=3: 0.062, K=4: 0.054, K=6: 0.044, K=8: 0.038


---

## results/20260929-005706-ablate-39e66c/report.md

SHA-256: `56ddf8ec24f535436175178d71b306977cbc947a907903fa32ffc98ea68c5f7e`

# Ablation report: 20260929-005706-ablate-39e66c

3 seeds, opponents cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44; 11 official + 14 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.209, wins 386/600; by opponent: cpp_nicked_v75 -0.238, cpp_leviathan3 +0.462, v7-base-bot +0.409, nicked_v44 +0.202

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hub_observe | -0.104 [-0.175, -0.041] | essential | +0.007 | -0.038 [-0.093, +0.019] | neutral | -0.081 | -0.087 | -0.050 | +0.068 | -0.088 | +0.002 | 367/600 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.552 over 200 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.552^2 / (200 * K)): K=2: 0.076, K=3: 0.062, K=4: 0.054, K=6: 0.044, K=8: 0.038


---

## results/20260929-071650-full-change-8cfa1b/full/summary.md

SHA-256: `5f6bf024c7226bdc896d574ef76532b1ab8eacbb742b0a8656dc4899a11c966a`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| ctmes | 87-0-3 | 97% | 97% | 92-100% | +585 | 45 | 0 |
| nicked_lab | 40-0-50 | 44% | 44% | 33-56% | -39 | 45 | 0 |
| v6 | 78-0-12 | 87% | 87% | 79-93% | +325 | 45 | 0 |
| **overall** | 205-0-65 | 76% | 76% | 70-82% | +200 | 135 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| trophy | 10-0-8 | 56% | 56% | 18 | 0 |
| Trauma | 10-0-8 | 56% | 56% | 18 | 0 |
| Devil | 11-0-7 | 61% | 61% | 18 | 0 |
| queen_of_spades | 12-0-6 | 67% | 67% | 18 | 0 |
| Prisoners_Dilemma | 12-0-6 | 67% | 67% | 18 | 0 |
| default_small | 13-0-5 | 72% | 72% | 18 | 0 |
| Colosseum | 13-0-5 | 72% | 72% | 18 | 0 |
| schooltime | 14-0-4 | 78% | 78% | 18 | 0 |
| arena | 14-0-4 | 78% | 78% | 18 | 0 |
| Slithery_Fight | 14-0-4 | 78% | 78% | 18 | 0 |
| stronghold | 15-0-3 | 83% | 83% | 18 | 0 |
| big_empty | 15-0-3 | 83% | 83% | 18 | 0 |
| default | 17-0-1 | 94% | 94% | 18 | 0 |
| Portals | 17-0-1 | 94% | 94% | 18 | 0 |
| Autarky | 18-0-0 | 100% | 100% | 18 | 0 |

candidate dragon deaths: hit kelp 37993, head-to-head 13737, hit other body 7574, no valid action/timeout 6387, hit itself 23

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260929-071651-full-change-5060a9/full/summary.md

SHA-256: `3a9fa87599d78e8bc454760ff13e84f3413027a0e2aaf284a016ed73543fe1d6`

# candidate

| opponent | W-D-L | win rate | score | score 95% CI | Elo diff | blocks | errors |
|---|---|---|---|---|---|---|---|
| ctmes | 88-0-2 | 98% | 98% | 94-100% | +657 | 45 | 0 |
| nicked_lab | 38-0-52 | 42% | 42% | 33-52% | -54 | 45 | 0 |
| v6 | 81-0-9 | 90% | 90% | 83-96% | +382 | 45 | 0 |
| **overall** | 207-0-63 | 77% | 77% | 71-82% | +207 | 135 | 0 |

| map | W-D-L | win rate | score | games | errors |
|---|---|---|---|---|---|
| trophy | 12-0-6 | 67% | 67% | 18 | 0 |
| Trauma | 12-0-6 | 67% | 67% | 18 | 0 |
| default_small | 13-0-5 | 72% | 72% | 18 | 0 |
| Devil | 13-0-5 | 72% | 72% | 18 | 0 |
| schooltime | 13-0-5 | 72% | 72% | 18 | 0 |
| arena | 13-0-5 | 72% | 72% | 18 | 0 |
| big_empty | 13-0-5 | 72% | 72% | 18 | 0 |
| Slithery_Fight | 13-0-5 | 72% | 72% | 18 | 0 |
| queen_of_spades | 14-0-4 | 78% | 78% | 18 | 0 |
| default | 14-0-4 | 78% | 78% | 18 | 0 |
| stronghold | 14-0-4 | 78% | 78% | 18 | 0 |
| Prisoners_Dilemma | 14-0-4 | 78% | 78% | 18 | 0 |
| Colosseum | 16-0-2 | 89% | 89% | 18 | 0 |
| Portals | 16-0-2 | 89% | 89% | 18 | 0 |
| Autarky | 17-0-1 | 94% | 94% | 18 | 0 |

candidate dragon deaths: hit kelp 39523, head-to-head 14808, hit other body 7490, no valid action/timeout 7224, hit itself 12

Score counts a draw as half a win; win rate counts wins only. CI: percentile bootstrap over opponent+map+seed blocks (both sides kept together).


---

## results/20260929-074209-ablate-87a257/report.md

SHA-256: `2c200e4a2cb7bcde9237be85e5923aac4234dcb7dfc1dcd19e92f7314fa3ff87`

# Ablation report: 20260929-074209-ablate-87a257

3 seeds, opponents cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.131, wins 212/360; by opponent: cpp_nicked_v75 -0.338, cpp_leviathan3 +0.311, v7-base-bot +0.325, nicked_v44 +0.226

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v11 | +0.105 [+0.008, +0.191] | harmful (drop) | -0.065 | +0.048 [-0.025, +0.123] | neutral | -0.059 | +0.152 | +0.032 | +0.067 | -0.004 | +0.192 | 232/360 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.628 over 120 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.628^2 / (120 * K)): K=2: 0.112, K=3: 0.092, K=4: 0.079, K=6: 0.065, K=8: 0.056


---

## results/20260929-092956-ablate-1fdc1e/report.md

SHA-256: `4719a5206037209cae4b12c4bfdd0131e74689871da74a03fd045ff1047141b2`

# Ablation report: 20260929-092956-ablate-1fdc1e

3 seeds, opponents cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.119, wins 258/450; by opponent: cpp_nicked_v75 -0.210, cpp_leviathan3 +0.408, v7-base-bot +0.335, nicked_v44 +0.229, nicked_lab -0.169

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fpr80 | -0.008 [-0.063, +0.046] | neutral | +0.010 | -0.002 [-0.045, +0.039] | neutral | +0.014 | +0.065 | -0.009 | +0.032 | -0.112 | -0.008 | +0.013 | 260/450 |
| anchor80 | -0.008 [-0.068, +0.053] | neutral | +0.029 | +0.004 [-0.040, +0.050] | neutral | -0.029 | +0.052 | +0.013 | +0.096 | -0.112 | +0.011 | -0.014 | 262/450 |
| anchor150 | +0.015 [-0.046, +0.068] | neutral | +0.010 | +0.014 [-0.028, +0.052] | neutral | -0.046 | +0.025 | +0.049 | +0.012 | +0.028 | -0.012 | +0.086 | 265/450 |
| anchor80_r20 | -0.020 [-0.084, +0.042] | neutral | +0.026 | -0.005 [-0.051, +0.040] | neutral | +0.006 | +0.003 | +0.033 | +0.026 | -0.090 | -0.009 | +0.007 | 258/450 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.587 over 150 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.587^2 / (150 * K)): K=2: 0.094, K=3: 0.077, K=4: 0.066, K=6: 0.054, K=8: 0.047


---

## results/20260929-093158-ablate-933dc7/report.md

SHA-256: `0a7416bb95fcb4c368723676ac5605973cfa670b5d6a91d3ff3a3e8c93c79761`

# Ablation report: 20260929-093158-ablate-933dc7

3 seeds, opponents cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.119, wins 258/450; by opponent: cpp_nicked_v75 -0.210, cpp_leviathan3 +0.408, v7-base-bot +0.335, nicked_v44 +0.229, nicked_lab -0.169

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hubfar | +0.047 [-0.024, +0.130] | neutral | +0.039 | +0.044 [-0.011, +0.101] | neutral | +0.093 | +0.003 | -0.049 | +0.070 | +0.105 | +0.032 | +0.078 | 275/450 |
| hubfar2 | +0.040 [-0.026, +0.104] | neutral | +0.026 | +0.035 [-0.010, +0.079] | neutral | +0.071 | +0.023 | +0.010 | +0.055 | +0.016 | +0.018 | +0.081 | 270/450 |
| goal0 | +0.023 [-0.062, +0.110] | neutral | -0.017 | +0.010 [-0.059, +0.075] | neutral | -0.061 | -0.026 | +0.016 | +0.086 | +0.034 | -0.031 | +0.122 | 268/450 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.587 over 150 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.587^2 / (150 * K)): K=2: 0.094, K=3: 0.077, K=4: 0.066, K=6: 0.054, K=8: 0.047


---

## results/20260929-121639-ablate-d99145/report.md

SHA-256: `e20f8075388e4d9b0e8eb288f120696d97ad2456565f6a62cdeb159fed50376a`

# Ablation report: 20260929-121639-ablate-d99145

3 seeds, opponents cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v6; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.237, wins 359/540; by opponent: cpp_nicked_v75 -0.202, cpp_leviathan3 +0.507, v7-base-bot +0.407, nicked_v44 +0.306, nicked_lab -0.097, v6 +0.500

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v6 | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hubfar | -0.048 [-0.137, +0.040] | neutral | -0.071 | -0.056 [-0.136, +0.017] | neutral | -0.127 | -0.075 | -0.146 | -0.070 | +0.024 | +0.058 | -0.040 | -0.099 | 338/540 |
| hubfar_strong | -0.041 [-0.117, +0.039] | neutral | -0.091 | -0.058 [-0.136, +0.014] | neutral | -0.127 | -0.068 | -0.081 | -0.093 | -0.007 | +0.030 | -0.059 | -0.053 | 336/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.579 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.579^2 / (180 * K)): K=2: 0.085, K=3: 0.069, K=4: 0.060, K=6: 0.049, K=8: 0.042


---

## results/20260929-134853-ablate-5617dc/report.md

SHA-256: `72f082e5ae129d57e87221fea2dac17afa1a13cbac3658577a8bcfc1f3ef831f`

# Ablation report: 20260929-134853-ablate-5617dc

3 seeds, opponents cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v6; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.170, wins 335/540; by opponent: cpp_nicked_v75 -0.344, cpp_leviathan3 +0.466, v7-base-bot +0.237, nicked_v44 +0.308, nicked_lab -0.147, v6 +0.500

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v6 | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| book | +0.150 [+0.073, +0.236] | harmful (drop) | +0.065 | +0.122 [+0.054, +0.191] | harmful (drop) | +0.259 | +0.035 | +0.116 | +0.146 | +0.113 | +0.061 | +0.166 | +0.000 | 378/540 |
| bookgrad15 | -0.156 [-0.312, +0.005] | neutral | +0.050 | -0.087 [-0.206, +0.022] | neutral | +0.059 | -0.261 | -0.114 | -0.159 | +0.091 | -0.141 | -0.155 | +0.099 | 309/540 |
| bookgrad8 | +0.010 [-0.126, +0.141] | neutral | +0.057 | +0.026 [-0.074, +0.121] | neutral | +0.154 | -0.132 | +0.033 | +0.004 | +0.164 | -0.068 | -0.013 | +0.134 | 347/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.568 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.568^2 / (180 * K)): K=2: 0.083, K=3: 0.068, K=4: 0.059, K=6: 0.048, K=8: 0.041


---

## results/20260929-152611-ablate-5cb6f9/report.md

SHA-256: `1fe39ea07e17204edf1e4155e13857d86f033c225795cae87c6d08e3c082a78d`

# Ablation report: 20260929-152611-ablate-5cb6f9

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.010, wins 280/540; by opponent: cpp_nicked_v92 -0.525, cpp_nicked_v75 -0.366, cpp_leviathan3 +0.472, v7-base-bot +0.365, nicked_v44 +0.258, nicked_lab -0.144

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| book | +0.118 [+0.033, +0.203] | harmful (drop) | +0.034 | +0.090 [+0.019, +0.164] | harmful (drop) | +0.027 | +0.164 | +0.089 | +0.066 | +0.071 | +0.124 | +0.123 | +0.000 | 316/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.575 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.575^2 / (180 * K)): K=2: 0.084, K=3: 0.069, K=4: 0.059, K=6: 0.049, K=8: 0.042


---

## results/20260929-163912-ablate-263928/report.md

SHA-256: `45e8bf7934580fcb7ea88cf67f5c576a2b23d9ceb2fb8986275878ef5482b9b0`

# Ablation report: 20260929-163912-ablate-263928

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.149, wins 325/540; by opponent: cpp_nicked_v92 -0.415, cpp_nicked_v75 -0.068, cpp_leviathan3 +0.499, v7-base-bot +0.470, nicked_v44 +0.462, nicked_lab -0.054

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pf16 | -0.013 [-0.029, +0.000] | neutral | +0.000 | -0.009 [-0.019, +0.001] | neutral | -0.012 | -0.018 | -0.008 | +0.001 | -0.015 | -0.002 | -0.006 | -0.016 | 321/540 |
| pf16r5 | -0.006 [-0.022, +0.009] | neutral | +0.000 | -0.004 [-0.015, +0.006] | neutral | -0.013 | -0.018 | +0.004 | +0.003 | -0.013 | +0.013 | -0.006 | +0.001 | 323/540 |
| pf10r5 | -0.005 [-0.021, +0.011] | neutral | -0.012 | -0.007 [-0.020, +0.004] | neutral | +0.017 | -0.032 | -0.001 | -0.016 | -0.013 | +0.001 | -0.004 | -0.016 | 322/540 |
| shift40 | +0.026 [-0.007, +0.064] | neutral | +0.056 | +0.036 [+0.011, +0.064] | harmful (drop) | +0.022 | +0.080 | +0.011 | +0.023 | +0.002 | +0.079 | +0.037 | +0.035 | 344/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.624 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.624^2 / (180 * K)): K=2: 0.091, K=3: 0.074, K=4: 0.064, K=6: 0.053, K=8: 0.046


---

## results/20260929-182640-ablate-e2493c/report.md

SHA-256: `8c3286b4ed28f6d56a759364d8e54f788b63a802be4ee57b2b841b1928a75c57`

# Ablation report: 20260929-182640-ablate-e2493c

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.167, wins 329/540; by opponent: cpp_nicked_v92 -0.417, cpp_nicked_v75 -0.089, cpp_leviathan3 +0.590, v7-base-bot +0.447, nicked_v44 +0.478, nicked_lab -0.005

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| shift40 | +0.004 [-0.027, +0.036] | neutral | +0.079 | +0.029 [-0.000, +0.061] | neutral | +0.024 | +0.053 | -0.024 | +0.039 | +0.032 | +0.049 | +0.031 | +0.022 | 344/540 |
| plen4 | -0.185 [-0.269, -0.106] | essential | -0.030 | -0.133 [-0.197, -0.077] | essential | -0.133 | -0.199 | -0.082 | -0.101 | -0.160 | -0.124 | -0.147 | -0.095 | 285/540 |
| plen4pf16r5 | -0.302 [-0.403, -0.201] | essential | -0.138 | -0.248 [-0.335, -0.164] | essential | -0.228 | -0.236 | -0.269 | -0.292 | -0.357 | -0.103 | -0.276 | -0.170 | 250/540 |
| plen4pf16r5s40 | -0.324 [-0.430, -0.226] | essential | -0.120 | -0.256 [-0.349, -0.167] | essential | -0.212 | -0.251 | -0.283 | -0.313 | -0.344 | -0.134 | -0.280 | -0.191 | 247/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.547 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.547^2 / (180 * K)): K=2: 0.080, K=3: 0.065, K=4: 0.057, K=6: 0.046, K=8: 0.040


---

## results/20260930-073741-ablate-f5f4ba/report.md

SHA-256: `04f5f320c6a4959d75392f497debd86798083e27b1a028798b7829298017dae6`

# Ablation report: 20260930-073741-ablate-f5f4ba

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.169, wins 339/540; by opponent: cpp_nicked_v92 -0.315, cpp_nicked_v75 -0.104, cpp_leviathan3 +0.441, v7-base-bot +0.505, nicked_v44 +0.395, nicked_lab +0.093

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hubsep | +0.011 [-0.016, +0.040] | neutral | +0.000 | +0.008 [-0.012, +0.027] | neutral | +0.001 | +0.032 | -0.020 | +0.006 | +0.044 | -0.016 | +0.000 | +0.029 | 342/540 |
| v3portal | -0.043 [-0.095, +0.006] | neutral | +0.036 | -0.017 [-0.059, +0.024] | neutral | -0.036 | -0.045 | -0.018 | -0.070 | +0.028 | +0.041 | -0.019 | -0.010 | 330/540 |
| both | -0.033 [-0.093, +0.030] | neutral | +0.036 | -0.010 [-0.059, +0.037] | neutral | -0.019 | -0.010 | -0.041 | -0.072 | +0.047 | +0.037 | -0.019 | +0.016 | 332/540 |
| v12tune | -0.091 [-0.192, +0.002] | neutral | -0.007 | -0.063 [-0.147, +0.020] | neutral | -0.185 | +0.061 | -0.024 | -0.157 | -0.004 | -0.069 | -0.110 | +0.067 | 317/540 |
| v12gen5 | -0.087 [-0.175, +0.001] | neutral | +0.069 | -0.035 [-0.108, +0.042] | neutral | -0.100 | -0.032 | +0.097 | -0.062 | +0.034 | -0.149 | -0.071 | +0.062 | 324/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.618 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.618^2 / (180 * K)): K=2: 0.090, K=3: 0.074, K=4: 0.064, K=6: 0.052, K=8: 0.045


---

## results/20260930-095351-ablate-907fbc/report.md

SHA-256: `d3d939bae3abd693bada1c9dcbd90c109aca1a2609b3b2039c229164531e44e6`

# Ablation report: 20260930-095351-ablate-907fbc

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.107, wins 314/540; by opponent: cpp_nicked_v92 -0.406, cpp_nicked_v75 -0.166, cpp_leviathan3 +0.456, v7-base-bot +0.458, nicked_v44 +0.355, nicked_lab -0.054

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| kb2 | +0.033 [+0.009, +0.060] | harmful (drop) | -0.012 | +0.018 [-0.008, +0.045] | neutral | -0.034 | +0.012 | +0.087 | +0.011 | -0.001 | +0.035 | +0.013 | +0.032 | 323/540 |
| kb2hub | +0.041 [+0.003, +0.085] | harmful (drop) | -0.012 | +0.023 [-0.009, +0.058] | neutral | -0.017 | +0.028 | +0.078 | +0.062 | +0.020 | -0.032 | +0.013 | +0.050 | 324/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.605 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.605^2 / (180 * K)): K=2: 0.088, K=3: 0.072, K=4: 0.062, K=6: 0.051, K=8: 0.044


---

## results/20260930-110033-ablate-a99756/report.md

SHA-256: `fab55fdad3aae08f40104bdef5222f5524936661f1d76453be33318ea0ee32b7`

# Ablation report: 20260930-110033-ablate-a99756

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.076, wins 303/540; by opponent: cpp_nicked_v92 -0.532, cpp_nicked_v75 -0.287, cpp_leviathan3 +0.451, v7-base-bot +0.472, nicked_v44 +0.333, nicked_lab +0.020

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| kb2 | +0.017 [-0.020, +0.060] | neutral | -0.008 | +0.009 [-0.021, +0.040] | neutral | -0.026 | +0.022 | +0.053 | +0.015 | +0.049 | -0.059 | -0.001 | +0.036 | 308/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.556 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.556^2 / (180 * K)): K=2: 0.081, K=3: 0.066, K=4: 0.057, K=6: 0.047, K=8: 0.041


---

## results/20260930-114529-ablate-214862/report.md

SHA-256: `53b1b9ec4791ad3186ea7310e181be7ee3dc3bc8625e70036e676b91bc8ba492`

# Ablation report: 20260930-114529-ablate-214862

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.151, wins 329/540; by opponent: cpp_nicked_v92 -0.306, cpp_nicked_v75 -0.140, cpp_leviathan3 +0.538, v7-base-bot +0.522, nicked_v44 +0.350, nicked_lab -0.058

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| reach4 | +0.030 [-0.014, +0.078] | neutral | -0.032 | +0.009 [-0.024, +0.045] | neutral | -0.029 | +0.049 | +0.002 | +0.015 | +0.016 | +0.003 | -0.005 | +0.050 | 333/540 |
| reach6 | +0.004 [-0.039, +0.051] | neutral | -0.032 | -0.008 [-0.043, +0.026] | neutral | -0.048 | -0.012 | +0.008 | +0.018 | +0.001 | -0.011 | -0.025 | +0.041 | 325/540 |
| kb2reach4 | +0.022 [-0.017, +0.064] | neutral | -0.057 | -0.005 [-0.037, +0.030] | neutral | -0.058 | +0.014 | +0.003 | +0.005 | +0.016 | -0.007 | -0.021 | +0.041 | 326/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.620 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.620^2 / (180 * K)): K=2: 0.091, K=3: 0.074, K=4: 0.064, K=6: 0.052, K=8: 0.045


---

## results/20260930-131507-ablate-bfe34e/report.md

SHA-256: `5311cb1527c4ffb1053dc1be22c915bca4929d1bd361b5fb35b77fa0ce0a346e`

# Ablation report: 20260930-131507-ablate-bfe34e

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.132, wins 327/540; by opponent: cpp_nicked_v92 -0.349, cpp_nicked_v75 -0.167, cpp_leviathan3 +0.526, v7-base-bot +0.418, nicked_v44 +0.333, nicked_lab +0.030

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| kgrad10 | -0.011 [-0.038, +0.020] | neutral | -0.028 | -0.016 [-0.048, +0.015] | neutral | -0.034 | -0.051 | -0.000 | -0.005 | -0.008 | -0.000 | -0.023 | +0.003 | 318/540 |
| kgrad25 | -0.022 [-0.058, +0.014] | neutral | -0.012 | -0.018 [-0.047, +0.010] | neutral | -0.005 | -0.052 | -0.007 | -0.010 | -0.011 | -0.026 | -0.028 | +0.007 | 319/540 |
| kgrad25kb2 | -0.013 [-0.046, +0.018] | neutral | -0.037 | -0.021 [-0.050, +0.004] | neutral | -0.030 | -0.025 | -0.002 | +0.001 | -0.002 | -0.070 | -0.031 | +0.005 | 316/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.610 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.610^2 / (180 * K)): K=2: 0.089, K=3: 0.073, K=4: 0.063, K=6: 0.051, K=8: 0.045


---

## results/20260930-144847-ablate-27e8a7/report.md

SHA-256: `1206e94e3d4e24876f5efe7c97639fb01e108f64a99ec9a72269ebd7f14b6ebf`

# Ablation report: 20260930-144847-ablate-27e8a7

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.215, wins 348/540; by opponent: cpp_nicked_v92 -0.299, cpp_nicked_v75 -0.073, cpp_leviathan3 +0.563, v7-base-bot +0.415, nicked_v44 +0.509, nicked_lab +0.178

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sum64 | +0.014 [-0.019, +0.044] | neutral | +0.011 | +0.013 [-0.016, +0.043] | neutral | +0.047 | +0.028 | +0.024 | +0.025 | -0.053 | +0.008 | +0.007 | +0.029 | 355/540 |
| sum12 | +0.034 [-0.003, +0.070] | neutral | +0.017 | +0.028 [+0.001, +0.056] | harmful (drop) | +0.027 | +0.071 | +0.060 | +0.014 | -0.035 | +0.035 | +0.021 | +0.048 | 362/540 |
| sum64early | -0.002 [-0.064, +0.053] | neutral | -0.005 | -0.003 [-0.045, +0.032] | neutral | +0.058 | +0.067 | -0.030 | -0.014 | -0.107 | +0.007 | -0.013 | +0.025 | 349/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.587 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.587^2 / (180 * K)): K=2: 0.086, K=3: 0.070, K=4: 0.061, K=6: 0.050, K=8: 0.043


---

## results/20260930-161837-ablate-05467d/report.md

SHA-256: `4a7c9dd45d89caf4d0f717dad31ea3a54710a96e53ad79f2318b9d9e49100a35`

# Ablation report: 20260930-161837-ablate-05467d

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.127, wins 323/540; by opponent: cpp_nicked_v92 -0.506, cpp_nicked_v75 -0.105, cpp_leviathan3 +0.535, v7-base-bot +0.472, nicked_v44 +0.441, nicked_lab -0.075

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sum12 | -0.017 [-0.050, +0.024] | neutral | +0.009 | -0.008 [-0.035, +0.019] | neutral | +0.049 | -0.051 | +0.027 | -0.036 | -0.031 | -0.007 | -0.017 | +0.016 | 322/540 |
| sum64 | -0.030 [-0.064, +0.008] | neutral | -0.003 | -0.021 [-0.049, +0.007] | neutral | +0.038 | -0.054 | +0.030 | -0.049 | -0.068 | -0.024 | -0.038 | +0.026 | 316/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.589 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.589^2 / (180 * K)): K=2: 0.086, K=3: 0.070, K=4: 0.061, K=6: 0.050, K=8: 0.043


---

## results/20260930-182348-ablate-81c0bb/report.md

SHA-256: `c64afe371ad7ff15dfb14cc524cf4edd2f70d89ef27175b5692555f9e6e77e01`

# Ablation report: 20260930-182348-ablate-81c0bb

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.198, wins 347/540; by opponent: cpp_nicked_v92 -0.314, cpp_nicked_v75 +0.045, cpp_leviathan3 +0.525, v7-base-bot +0.471, nicked_v44 +0.423, nicked_lab +0.040

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r4 | -0.044 [-0.149, +0.060] | neutral | +0.021 | -0.022 [-0.113, +0.069] | neutral | -0.043 | -0.041 | -0.006 | -0.102 | -0.032 | +0.091 | -0.006 | -0.067 | 333/540 |
| r4eq | -0.053 [-0.148, +0.036] | neutral | -0.068 | -0.058 [-0.156, +0.037] | neutral | -0.038 | -0.141 | -0.087 | -0.092 | -0.072 | +0.080 | -0.050 | -0.083 | 326/540 |
| r4lo | -0.175 [-0.283, -0.078] | essential | -0.173 | -0.174 [-0.287, -0.076] | essential | -0.160 | -0.326 | -0.131 | -0.227 | -0.134 | -0.069 | -0.188 | -0.136 | 291/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.606 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.606^2 / (180 * K)): K=2: 0.089, K=3: 0.072, K=4: 0.063, K=6: 0.051, K=8: 0.044


---

## results/20260930-195605-ablate-983951/report.md

SHA-256: `591fa833280e522dd2befa35e57ffa444eb3d3a4ae33278b25f6cf2483ec0f7e`

# Ablation report: 20260930-195605-ablate-983951

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.178, wins 343/540; by opponent: cpp_nicked_v92 -0.382, cpp_nicked_v75 -0.097, cpp_leviathan3 +0.636, v7-base-bot +0.394, nicked_v44 +0.466, nicked_lab +0.052

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sonarhub | -0.011 [-0.065, +0.042] | neutral | +0.000 | -0.007 [-0.040, +0.028] | neutral | +0.027 | +0.005 | -0.014 | +0.014 | -0.038 | -0.038 | +0.000 | -0.027 | 337/540 |
| sonarhub_whub3 | -0.193 [-0.318, -0.069] | essential | -0.043 | -0.143 [-0.228, -0.061] | essential | -0.033 | -0.148 | -0.148 | -0.151 | -0.219 | -0.159 | -0.171 | -0.066 | 293/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.594 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.594^2 / (180 * K)): K=2: 0.087, K=3: 0.071, K=4: 0.061, K=6: 0.050, K=8: 0.043


---

## results/20260930-210927-ablate-9aaef8/report.md

SHA-256: `5c330c1f944f718a470b46546796e0a0bd4eafdff694bfe6f5191bfc51125bf9`

# Ablation report: 20260930-210927-ablate-9aaef8

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.161, wins 333/540; by opponent: cpp_nicked_v92 -0.514, cpp_nicked_v75 -0.016, cpp_leviathan3 +0.517, v7-base-bot +0.417, nicked_v44 +0.420, nicked_lab +0.140

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sh_age15 | -0.014 [-0.052, +0.021] | neutral | +0.000 | -0.009 [-0.034, +0.013] | neutral | -0.000 | -0.070 | +0.046 | -0.001 | +0.019 | -0.048 | +0.000 | -0.034 | 331/540 |
| sh_age30 | +0.026 [+0.001, +0.054] | harmful (drop) | +0.000 | +0.017 [+0.001, +0.036] | harmful (drop) | +0.036 | -0.007 | +0.049 | +0.030 | -0.013 | +0.008 | +0.000 | +0.064 | 340/540 |
| sh_age60 | +0.028 [-0.001, +0.066] | neutral | +0.000 | +0.019 [-0.001, +0.041] | neutral | -0.008 | +0.022 | +0.039 | +0.015 | +0.022 | +0.022 | +0.000 | +0.070 | 342/540 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.611 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.611^2 / (180 * K)): K=2: 0.089, K=3: 0.073, K=4: 0.063, K=6: 0.052, K=8: 0.045


---

## results/20260930-224324-ablate-a110d4/report.md

SHA-256: `2251e9e9c02c4340326a04ecd272fa28319d8587b63ea55482bd240e5ace9675`

# Ablation report: 20260930-224324-ablate-a110d4

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 14 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.142, wins 542/900; by opponent: cpp_nicked_v92 -0.481, cpp_nicked_v75 -0.123, cpp_leviathan3 +0.553, v7-base-bot +0.415, nicked_v44 +0.413, nicked_lab +0.075

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sh_age30 | +0.038 [-0.004, +0.085] | neutral | +0.037 | +0.038 [+0.010, +0.065] | harmful (drop) | +0.060 | +0.033 | -0.019 | +0.089 | +0.055 | +0.008 | +0.000 | +0.067 | 563/900 |
| sh_age60 | +0.026 [-0.013, +0.069] | neutral | +0.015 | +0.020 [-0.002, +0.044] | neutral | +0.006 | +0.029 | -0.009 | +0.093 | +0.038 | -0.038 | +0.000 | +0.035 | 552/900 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.574 over 300 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.574^2 / (300 * K)): K=2: 0.065, K=3: 0.053, K=4: 0.046, K=6: 0.038, K=8: 0.033


---

## results/20261001-141248-ablate-4e9237/report.md

SHA-256: `9f7b5b4d63d4c8b06cee180fbbe8e5fa1017b0777c364a460a495220f640cc21`

# Ablation report: 20261001-141248-ablate-4e9237

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 11 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.090, wins 270/528; by opponent: cpp_nicked_v92 -0.277, cpp_nicked_v75 -0.079, cpp_leviathan3 +0.298, v7-base-bot +0.305, nicked_v44 +0.334, nicked_lab -0.039

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| mv_t05 | -0.352 [-0.557, -0.161] | essential | -0.179 | -0.258 [-0.367, -0.156] | essential | -0.246 | -0.251 | -0.213 | -0.194 | -0.361 | -0.282 | -0.415 | -0.100 | 184/528 |
| mv_t1 | -0.163 [-0.314, -0.016] | essential | -0.036 | -0.094 [-0.177, -0.015] | essential | -0.066 | -0.138 | -0.011 | -0.139 | -0.029 | -0.181 | -0.191 | +0.003 | 234/528 |
| mv_t2 | -0.014 [-0.104, +0.080] | neutral | +0.009 | -0.001 [-0.049, +0.052] | neutral | +0.028 | -0.037 | +0.098 | -0.042 | -0.007 | -0.048 | +0.009 | -0.011 | 263/528 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.440 over 264 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.440^2 / (264 * K)): K=2: 0.053, K=3: 0.043, K=4: 0.038, K=6: 0.031, K=8: 0.027


---

## results/20261001-152839-ablate-fec4b0/report.md

SHA-256: `25e5fc2c351331b6704898b5fe1936c19ffdad01e1c04afb960817c4824172b8`

# Ablation report: 20261001-152839-ablate-fec4b0

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 7 extra maps, both sides. Objective: aligned. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.124, wins 226/432; by opponent: cpp_nicked_v92 -0.148, cpp_nicked_v75 -0.016, cpp_leviathan3 +0.345, v7-base-bot +0.167, nicked_v44 +0.370, nicked_lab +0.023

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v7_weights | +0.011 [-0.202, +0.206] | neutral | -0.065 | -0.040 [-0.131, +0.054] | neutral | -0.031 | -0.095 | -0.098 | -0.002 | +0.055 | -0.068 | -0.073 | +0.013 | 214/432 |
| v7_v3 | -0.115 [-0.299, +0.077] | neutral | -0.005 | -0.042 [-0.125, +0.037] | neutral | -0.115 | -0.025 | +0.010 | +0.037 | -0.110 | -0.047 | -0.077 | +0.013 | 199/432 |
| v7_food | -0.017 [-0.143, +0.096] | neutral | -0.005 | -0.009 [-0.061, +0.045] | neutral | +0.058 | -0.016 | -0.024 | +0.114 | -0.077 | -0.107 | -0.038 | +0.038 | 222/432 |
| v7_safety | +0.120 [+0.039, +0.194] | harmful (drop) | +0.000 | +0.040 [-0.004, +0.084] | neutral | -0.037 | +0.004 | +0.074 | +0.059 | +0.084 | +0.057 | +0.058 | +0.013 | 237/432 |
| v7_fight | +0.018 [-0.070, +0.115] | neutral | +0.013 | +0.015 [-0.027, +0.055] | neutral | -0.024 | -0.015 | -0.031 | +0.038 | +0.032 | +0.089 | +0.013 | +0.017 | 229/432 |
| v7_explore | +0.011 [-0.126, +0.166] | neutral | +0.023 | +0.019 [-0.038, +0.080] | neutral | -0.015 | -0.055 | +0.077 | +0.043 | +0.055 | +0.008 | +0.027 | +0.006 | 223/432 |
| no_kb_feed | -0.083 [-0.170, -0.012] | essential | -0.056 | -0.065 [-0.114, -0.024] | essential | -0.099 | -0.146 | -0.004 | -0.050 | -0.059 | -0.033 | -0.107 | +0.000 | 200/432 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.491 over 216 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.491^2 / (216 * K)): K=2: 0.066, K=3: 0.053, K=4: 0.046, K=6: 0.038, K=8: 0.033


---

## results/20261001-203651-ablate-9c6006/report.md

SHA-256: `b409cb9036cada73bd4e0b97902e4f5ee45e876c05925a581a35a2bb4f1f4767`

# Ablation report: 20261001-203651-ablate-9c6006

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.111, wins 200/360; by opponent: cpp_nicked_v92 -0.667, cpp_nicked_v75 -0.067, cpp_leviathan3 +0.700, v7-base-bot +0.233, nicked_v44 +0.367, nicked_lab +0.100

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| q_on | -0.058 [-0.233, +0.108] | neutral | -0.750 | -0.289 [-0.489, -0.094] | essential | -0.200 | -0.433 | -0.433 | -0.033 | -0.300 | -0.333 | -0.333 | -0.167 | 148/360 |
| q_nosplit | -0.067 [-0.217, +0.083] | neutral | -0.750 | -0.294 [-0.489, -0.111] | essential | -0.100 | -0.533 | -0.367 | -0.100 | -0.400 | -0.267 | -0.356 | -0.125 | 147/360 |
| q_late | -0.058 [-0.267, +0.150] | neutral | -0.583 | -0.233 [-0.411, -0.044] | essential | +0.067 | -0.400 | -0.367 | +0.000 | -0.267 | -0.433 | -0.197 | -0.333 | 158/360 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.894 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.894^2 / (180 * K)): K=2: 0.131, K=3: 0.107, K=4: 0.092, K=6: 0.075, K=8: 0.065


---

## results/20261001-204841-ablate-1c9d1d/report.md

SHA-256: `5f475dd7b43282f5f8d9ce9d05e96d92182a22ee20ec050e5685c16831fd1b29`

# Ablation report: 20261001-204841-ablate-1c9d1d

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.200, wins 216/360; by opponent: cpp_nicked_v92 -0.467, cpp_nicked_v75 +0.033, cpp_leviathan3 +0.667, v7-base-bot +0.533, nicked_v44 +0.433, nicked_lab +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| q_ms | -0.075 [-0.267, +0.133] | neutral | -0.533 | -0.228 [-0.422, -0.022] | essential | -0.167 | -0.367 | -0.167 | -0.367 | -0.167 | -0.133 | -0.227 | -0.229 | 175/360 |
| q_ms_s7 | -0.625 [-0.850, -0.400] | essential | -0.683 | -0.644 [-0.844, -0.417] | essential | -0.333 | -0.800 | -0.733 | -0.767 | -0.567 | -0.667 | -0.667 | -0.583 | 100/360 |
| q_ms_s11 | -0.692 [-0.933, -0.433] | essential | -0.833 | -0.739 [-0.967, -0.494] | essential | -0.467 | -0.933 | -0.467 | -1.000 | -0.833 | -0.733 | -0.795 | -0.583 | 83/360 |
| q_s7 | -0.633 [-0.875, -0.375] | essential | -0.900 | -0.722 [-0.922, -0.517] | essential | -0.433 | -0.800 | -0.700 | -0.967 | -0.733 | -0.700 | -0.788 | -0.542 | 86/360 |
| ms_s7 | -0.517 [-0.758, -0.275] | essential | -0.467 | -0.500 [-0.744, -0.239] | essential | -0.167 | -0.767 | -0.367 | -0.667 | -0.400 | -0.633 | -0.576 | -0.292 | 126/360 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.803 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.803^2 / (180 * K)): K=2: 0.117, K=3: 0.096, K=4: 0.083, K=6: 0.068, K=8: 0.059


---

## results/20261001-213229-ablate-a8b26d/report.md

SHA-256: `fb6faf84c0522c53be052365a722bd752f34b1f32c01b22b50071ec1cc3b3dc4`

# Ablation report: 20261001-213229-ablate-a8b26d

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.167, wins 210/360; by opponent: cpp_nicked_v92 -0.433, cpp_nicked_v75 -0.167, cpp_leviathan3 +0.567, v7-base-bot +0.467, nicked_v44 +0.533, nicked_lab +0.033

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| q_kb | -0.017 [-0.158, +0.108] | neutral | -0.450 | -0.161 [-0.333, +0.000] | neutral | -0.100 | -0.267 | -0.067 | -0.067 | -0.200 | -0.267 | -0.220 | +0.000 | 181/360 |
| qs_reach | -0.008 [-0.150, +0.125] | neutral | -0.517 | -0.178 [-0.356, -0.006] | essential | -0.133 | -0.200 | -0.033 | -0.133 | -0.233 | -0.333 | -0.250 | +0.021 | 178/360 |
| qs_dead | -0.008 [-0.150, +0.117] | neutral | -0.450 | -0.156 [-0.328, +0.000] | neutral | -0.100 | -0.300 | -0.067 | -0.067 | -0.133 | -0.267 | -0.212 | +0.000 | 182/360 |
| qs_full | -0.033 [-0.192, +0.133] | neutral | -0.533 | -0.200 [-0.378, -0.028] | essential | -0.267 | -0.100 | -0.033 | -0.200 | -0.267 | -0.333 | -0.273 | +0.000 | 174/360 |
| qs_full_nosplit | -0.067 [-0.225, +0.100] | neutral | -0.600 | -0.244 [-0.433, -0.061] | essential | -0.233 | -0.167 | -0.133 | -0.200 | -0.333 | -0.400 | -0.311 | -0.062 | 166/360 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.803 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.803^2 / (180 * K)): K=2: 0.117, K=3: 0.096, K=4: 0.083, K=6: 0.068, K=8: 0.059


---

## results/20261001-232813-ablate-9ec1d0/report.md

SHA-256: `d64d9a845a9a8c55dd9be1dd3440cc1160543a4c4bc257769e000c91989e6666`

# Ablation report: 20261001-232813-ablate-9ec1d0

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.161, wins 209/360; by opponent: cpp_nicked_v92 -0.467, cpp_nicked_v75 -0.067, cpp_leviathan3 +0.667, v7-base-bot +0.367, nicked_v44 +0.400, nicked_lab +0.067

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ms | +0.117 [+0.025, +0.217] | harmful (drop) | +0.217 | +0.150 [+0.050, +0.261] | harmful (drop) | +0.300 | +0.100 | +0.100 | -0.133 | +0.300 | +0.233 | +0.129 | +0.208 | 236/360 |
| ms_qsafe | +0.125 [-0.025, +0.283] | neutral | -0.383 | -0.044 [-0.267, +0.167] | neutral | -0.233 | +0.000 | -0.167 | +0.033 | +0.133 | -0.033 | -0.136 | +0.208 | 201/360 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.837 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.837^2 / (180 * K)): K=2: 0.122, K=3: 0.100, K=4: 0.086, K=6: 0.071, K=8: 0.061


---

## results/20261002-003855-ablate-58e7c5/report.md

SHA-256: `770347313780e5d815e989d02c38439c430d7ac7b725c49343fb5ce4e23ec13f`

# Ablation report: 20261002-003855-ablate-58e7c5

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.150, wins 207/360; by opponent: cpp_nicked_v92 -0.433, cpp_nicked_v75 -0.167, cpp_leviathan3 +0.567, v7-base-bot +0.433, nicked_v44 +0.433, nicked_lab +0.067

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qx2 | -0.008 [-0.158, +0.150] | neutral | -0.617 | -0.211 [-0.394, -0.028] | essential | -0.333 | -0.167 | -0.100 | -0.133 | -0.300 | -0.233 | -0.318 | +0.083 | 169/360 |
| qx3 | +0.042 [-0.125, +0.200] | neutral | -0.700 | -0.206 [-0.417, +0.006] | neutral | -0.233 | -0.033 | -0.267 | -0.233 | -0.167 | -0.300 | -0.333 | +0.146 | 170/360 |
| qx2_nosplit | +0.000 [-0.150, +0.167] | neutral | -0.667 | -0.222 [-0.406, -0.022] | essential | -0.233 | -0.167 | -0.167 | -0.200 | -0.333 | -0.233 | -0.341 | +0.104 | 167/360 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.888 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.888^2 / (180 * K)): K=2: 0.130, K=3: 0.106, K=4: 0.092, K=6: 0.075, K=8: 0.065


---

## results/20261002-013638-ablate-03f6ea/report.md

SHA-256: `5d28655fed3bd53580525562f7d2108c19e10dae74cd6e024ad2a17eb6bbad1e`

# Ablation report: 20261002-013638-ablate-03f6ea

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 11 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.130, wins 447/792; by opponent: cpp_nicked_v92 -0.470, cpp_nicked_v75 -0.242, cpp_leviathan3 +0.553, v7-base-bot +0.500, nicked_v44 +0.485, nicked_lab -0.045

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ms | +0.061 [-0.017, +0.150] | neutral | +0.074 | +0.068 [+0.013, +0.124] | harmful (drop) | +0.000 | +0.152 | +0.152 | +0.015 | +0.000 | +0.091 | +0.121 | +0.015 | 474/792 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.854 over 264 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.854^2 / (264 * K)): K=2: 0.103, K=3: 0.084, K=4: 0.073, K=6: 0.059, K=8: 0.051


---

## results/20261002-091849-ablate-0b2d16/report.md

SHA-256: `c6e1840ba4e81422eb63f0e35712449afba3431b5004552a0906f6f3c75058e2`

# Ablation report: 20261002-091849-ablate-0b2d16

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.239, wins 223/360; by opponent: cpp_nicked_v92 -0.333, cpp_nicked_v75 -0.100, cpp_leviathan3 +0.533, v7-base-bot +0.500, nicked_v44 +0.567, nicked_lab +0.267

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qt | +0.008 [-0.092, +0.100] | neutral | -0.100 | -0.028 [-0.106, +0.050] | neutral | -0.033 | +0.100 | +0.000 | -0.033 | -0.100 | -0.100 | -0.053 | +0.042 | 218/360 |
| ql | +0.042 [-0.025, +0.108] | neutral | -0.033 | +0.017 [-0.044, +0.078] | neutral | +0.067 | -0.067 | -0.133 | +0.067 | +0.033 | +0.133 | +0.008 | +0.042 | 226/360 |
| ql_qt | +0.083 [-0.025, +0.183] | neutral | -0.083 | +0.028 [-0.050, +0.117] | neutral | -0.067 | +0.200 | +0.067 | +0.033 | +0.033 | -0.100 | +0.015 | +0.062 | 228/360 |
| ql_qt_r2 | +0.025 [-0.083, +0.133] | neutral | -0.150 | -0.033 [-0.128, +0.056] | neutral | -0.167 | -0.100 | +0.100 | +0.000 | +0.167 | -0.200 | -0.061 | +0.042 | 217/360 |
| ql_qt_m1 | -0.017 [-0.100, +0.083] | neutral | -0.283 | -0.106 [-0.217, +0.006] | neutral | -0.167 | +0.000 | -0.033 | -0.267 | -0.033 | -0.133 | -0.144 | +0.000 | 204/360 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.767 over 180 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.767^2 / (180 * K)): K=2: 0.112, K=3: 0.092, K=4: 0.079, K=6: 0.065, K=8: 0.056


---

## results/20261002-104933-ablate-4d1d01/report.md

SHA-256: `a5552f1f2f65f9d0fe04ca061258c34ab4fdf1cf59b60a7872d50462c48a0cdd`

# Ablation report: 20261002-104933-ablate-4d1d01

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 11 official + 11 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.242, wins 492/792; by opponent: cpp_nicked_v92 -0.424, cpp_nicked_v75 +0.000, cpp_leviathan3 +0.636, v7-base-bot +0.530, nicked_v44 +0.530, nicked_lab +0.182

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ql_qt | +0.039 [-0.072, +0.144] | neutral | -0.042 | -0.005 [-0.076, +0.063] | neutral | +0.106 | +0.030 | -0.030 | -0.015 | -0.091 | -0.030 | +0.000 | -0.010 | 490/792 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.765 over 264 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.765^2 / (264 * K)): K=2: 0.092, K=3: 0.075, K=4: 0.065, K=6: 0.053, K=8: 0.046


---

## results/20261002-122654-ablate-9e01f6/report.md

SHA-256: `5a5465e022f99913834b73c69db0dc0375bdb31ae06d37d40a35fb6820631cb9`

# Ablation report: 20261002-122654-ablate-9e01f6

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.276, wins 268/420; by opponent: cpp_nicked_v92 -0.167, cpp_nicked_v75 -0.033, cpp_leviathan3 +0.733, v7-base-bot +0.600, nicked_v44 +0.567, nicked_lab +0.233, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qs250 | +0.000 [-0.021, +0.021] | neutral | +0.000 | +0.000 [-0.014, +0.014] | neutral | -0.067 | +0.000 | +0.033 | +0.000 | +0.033 | +0.000 | +0.000 | +0.000 | +0.000 | 268/420 |
| qs350 | +0.000 [+0.000, +0.000] | neutral | +0.000 | +0.000 [+0.000, +0.000] | neutral | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | 268/420 |
| qfeed | +0.043 [-0.043, +0.136] | neutral | -0.071 | +0.005 [-0.062, +0.071] | neutral | -0.267 | +0.133 | +0.100 | +0.000 | +0.100 | +0.067 | -0.100 | +0.019 | -0.036 | 269/420 |
| qs350feed | +0.050 [-0.043, +0.143] | neutral | -0.071 | +0.010 [-0.057, +0.081] | neutral | -0.267 | +0.133 | +0.133 | +0.000 | +0.100 | +0.067 | -0.100 | +0.026 | -0.036 | 270/420 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.884 over 210 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.884^2 / (210 * K)): K=2: 0.120, K=3: 0.098, K=4: 0.085, K=6: 0.069, K=8: 0.060


---

## results/20261002-133325-ablate-192622/report.md

SHA-256: `f0eac0820ee892fb5211025a36a62509d024311bbd6b33a22986f8867dc80857`

# Ablation report: 20261002-133325-ablate-192622

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.210, wins 254/420; by opponent: cpp_nicked_v92 -0.433, cpp_nicked_v75 -0.067, cpp_leviathan3 +0.667, v7-base-bot +0.433, nicked_v44 +0.667, nicked_lab +0.200, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| flight | -0.029 [-0.071, +0.007] | neutral | +0.014 | -0.014 [-0.048, +0.014] | neutral | +0.000 | -0.033 | +0.033 | +0.000 | -0.100 | -0.067 | +0.067 | -0.019 | +0.000 | 251/420 |
| qfood3 | -0.021 [-0.136, +0.079] | neutral | -0.071 | -0.038 [-0.133, +0.067] | neutral | -0.033 | -0.067 | -0.100 | +0.033 | +0.033 | -0.133 | +0.000 | -0.052 | +0.000 | 246/420 |
| qkeep6 | -0.043 [-0.150, +0.057] | neutral | -0.314 | -0.133 [-0.233, -0.038] | essential | -0.133 | -0.167 | -0.067 | -0.200 | -0.133 | -0.200 | -0.033 | -0.195 | +0.036 | 226/420 |
| qfood3_keep6 | -0.036 [-0.157, +0.079] | neutral | -0.200 | -0.090 [-0.205, +0.019] | neutral | -0.033 | -0.100 | -0.033 | -0.167 | +0.033 | -0.267 | -0.067 | -0.130 | +0.018 | 235/420 |
| all3 | -0.029 [-0.143, +0.100] | neutral | -0.286 | -0.114 [-0.224, -0.010] | essential | +0.000 | -0.133 | -0.167 | -0.067 | -0.067 | -0.233 | -0.133 | -0.175 | +0.054 | 230/420 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.816 over 210 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.816^2 / (210 * K)): K=2: 0.110, K=3: 0.090, K=4: 0.078, K=6: 0.064, K=8: 0.055


---

## results/20261002-145854-ablate-0e3685/report.md

SHA-256: `8e243f7b9a26a5e188167a2f4ac01f0b301df7f3891b687e612c0d36a72dac7c`

# Ablation report: 20261002-145854-ablate-0e3685

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.248, wins 262/420; by opponent: cpp_nicked_v92 -0.500, cpp_nicked_v75 +0.167, cpp_leviathan3 +0.767, v7-base-bot +0.567, nicked_v44 +0.600, nicked_lab +0.133, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hunt | +0.021 [-0.114, +0.157] | neutral | +0.000 | +0.014 [-0.090, +0.105] | neutral | +0.233 | -0.200 | -0.033 | -0.067 | -0.067 | +0.067 | +0.167 | -0.006 | +0.071 | 265/420 |
| hunt_strong | +0.043 [-0.029, +0.121] | neutral | -0.100 | -0.005 [-0.071, +0.062] | neutral | +0.267 | -0.133 | -0.033 | +0.000 | -0.067 | -0.067 | +0.000 | -0.032 | +0.071 | 261/420 |
| hunt_nopull | -0.021 [-0.064, +0.014] | neutral | +0.014 | -0.010 [-0.048, +0.024] | neutral | -0.033 | -0.100 | +0.067 | +0.067 | -0.033 | +0.000 | -0.033 | -0.013 | +0.000 | 260/420 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.828 over 210 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.828^2 / (210 * K)): K=2: 0.112, K=3: 0.091, K=4: 0.079, K=6: 0.065, K=8: 0.056


---

## results/20261002-163932-ablate-df1077/report.md

SHA-256: `ea919117df91b419dd8a72c97af789f6ab9adbde76fdb15649ff7b1626778bc3`

# Ablation report: 20261002-163932-ablate-df1077

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 11 official + 11 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.219, wins 563/924; by opponent: cpp_nicked_v92 -0.455, cpp_nicked_v75 -0.015, cpp_leviathan3 +0.773, v7-base-bot +0.500, nicked_v44 +0.591, nicked_lab +0.136, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hunt | -0.036 [-0.112, +0.038] | neutral | -0.022 | -0.028 [-0.081, +0.024] | neutral | +0.061 | -0.030 | -0.076 | -0.076 | +0.000 | -0.076 | +0.000 | -0.039 | -0.017 | 549/924 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.819 over 308 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.819^2 / (308 * K)): K=2: 0.091, K=3: 0.075, K=4: 0.065, K=6: 0.053, K=8: 0.046


---

## results/20261002-180409-ablate-3db476/report.md

SHA-256: `3bf7a322bdf1535f01bd1095ea12767abe9f5c48d1dc912a33bd15a2f4b81975`

# Ablation report: 20261002-180409-ablate-3db476

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 11 official + 11 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.212, wins 560/924; by opponent: cpp_nicked_v92 -0.303, cpp_nicked_v75 +0.015, cpp_leviathan3 +0.636, v7-base-bot +0.576, nicked_v44 +0.470, nicked_lab +0.091, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| travel | +0.000 [-0.071, +0.071] | neutral | -0.012 | -0.006 [-0.056, +0.043] | neutral | -0.030 | -0.076 | +0.061 | +0.015 | +0.030 | -0.076 | +0.030 | -0.048 | +0.035 | 557/924 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.837 over 308 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.837^2 / (308 * K)): K=2: 0.094, K=3: 0.076, K=4: 0.066, K=6: 0.054, K=8: 0.047


---

## results/20261002-192514-ablate-52aecd/report.md

SHA-256: `9c2fab8a7d5c4d6196978de331a73de8bc650c47b8ec4e5551acca3b7c7ef3b3`

# Ablation report: 20261002-192514-ablate-52aecd

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 11 official + 11 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.219, wins 563/924; by opponent: cpp_nicked_v92 -0.136, cpp_nicked_v75 -0.030, cpp_leviathan3 +0.591, v7-base-bot +0.485, nicked_v44 +0.545, nicked_lab +0.076, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| travel_w | -0.052 [-0.138, +0.024] | neutral | +0.000 | -0.024 [-0.074, +0.022] | neutral | -0.182 | -0.091 | +0.061 | +0.000 | +0.030 | +0.045 | -0.030 | -0.043 | -0.004 | 552/924 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.880 over 308 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.880^2 / (308 * K)): K=2: 0.098, K=3: 0.080, K=4: 0.070, K=6: 0.057, K=8: 0.049


---

## results/20261002-200810-ablate-394220/report.md

SHA-256: `0f2808b745be261c069a933313d7c0fccfad637a5a3cf86e0c014b7480965c6f`

# Ablation report: 20261002-200810-ablate-394220

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.219, wins 256/420; by opponent: cpp_nicked_v92 -0.467, cpp_nicked_v75 +0.067, cpp_leviathan3 +0.533, v7-base-bot +0.500, nicked_v44 +0.700, nicked_lab +0.200, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| d4 | -0.036 [-0.143, +0.064] | neutral | +0.000 | -0.024 [-0.090, +0.043] | neutral | +0.133 | -0.067 | -0.067 | +0.033 | -0.133 | -0.033 | -0.033 | -0.026 | -0.018 | 251/420 |
| d5 | -0.036 [-0.100, +0.021] | neutral | -0.029 | -0.033 [-0.090, +0.029] | neutral | +0.133 | -0.200 | +0.067 | -0.033 | -0.100 | +0.033 | -0.133 | -0.045 | +0.000 | 249/420 |
| keep300 | -0.014 [-0.036, +0.000] | neutral | +0.043 | +0.005 [-0.019, +0.033] | neutral | +0.000 | -0.067 | +0.067 | +0.033 | +0.000 | +0.000 | +0.000 | +0.006 | +0.000 | 257/420 |
| keep300x1 | -0.014 [-0.093, +0.057] | neutral | +0.029 | +0.000 [-0.067, +0.062] | neutral | +0.100 | +0.000 | +0.100 | -0.067 | +0.067 | -0.067 | -0.133 | -0.013 | +0.036 | 256/420 |
| d4_keep300 | -0.043 [-0.143, +0.057] | neutral | +0.043 | -0.014 [-0.090, +0.062] | neutral | +0.100 | -0.033 | -0.067 | +0.100 | -0.100 | -0.033 | -0.067 | -0.013 | -0.018 | 253/420 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.884 over 210 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.884^2 / (210 * K)): K=2: 0.120, K=3: 0.098, K=4: 0.085, K=6: 0.069, K=8: 0.060


---

## results/20261002-221412-ablate-3a1e25/report.md

SHA-256: `65cbb83fb7a76f53800590d11d0fce6d9158a5db47b818e86d8edbadf770de9f`

# Ablation report: 20261002-221412-ablate-3a1e25

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 11 official + 4 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.229, wins 258/420; by opponent: cpp_nicked_v92 -0.167, cpp_nicked_v75 -0.233, cpp_leviathan3 +0.533, v7-base-bot +0.667, nicked_v44 +0.633, nicked_lab +0.167, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| safe3 | +0.014 [-0.029, +0.050] | neutral | -0.071 | -0.014 [-0.052, +0.024] | neutral | -0.033 | -0.067 | -0.067 | -0.067 | +0.033 | +0.000 | +0.100 | -0.019 | +0.000 | 255/420 |
| safe6 | +0.014 [-0.036, +0.064] | neutral | -0.086 | -0.019 [-0.062, +0.019] | neutral | -0.033 | -0.067 | -0.100 | -0.067 | +0.033 | +0.033 | +0.067 | -0.026 | +0.000 | 254/420 |
| safe3_g2 | +0.021 [-0.114, +0.157] | neutral | -0.086 | -0.014 [-0.114, +0.086] | neutral | -0.167 | +0.267 | +0.167 | -0.233 | +0.000 | -0.100 | -0.033 | +0.006 | -0.071 | 255/420 |
| safe3_d4 | +0.114 [+0.014, +0.221] | harmful (drop) | -0.014 | +0.071 [-0.005, +0.157] | neutral | -0.100 | +0.100 | +0.267 | -0.133 | +0.067 | +0.067 | +0.233 | +0.091 | +0.018 | 273/420 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.851 over 210 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.851^2 / (210 * K)): K=2: 0.115, K=3: 0.094, K=4: 0.081, K=6: 0.066, K=8: 0.058


---

## results/20261002-234510-ablate-a5b1f7/report.md

SHA-256: `43b24fe7c1d883ba771da00650b1b305707e86478156a2cd86231c8a7d8e5916`

# Ablation report: 20261002-234510-ablate-a5b1f7

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 11 official + 11 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.238, wins 572/924; by opponent: cpp_nicked_v92 -0.197, cpp_nicked_v75 -0.091, cpp_leviathan3 +0.727, v7-base-bot +0.591, nicked_v44 +0.439, nicked_lab +0.197, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| kx1 | +0.033 [-0.029, +0.100] | neutral | -0.062 | -0.018 [-0.066, +0.027] | neutral | +0.121 | -0.076 | -0.030 | -0.091 | +0.045 | -0.030 | -0.068 | -0.017 | -0.019 | 563/924 |
| kx1_g2 | -0.014 [-0.081, +0.062] | neutral | -0.093 | -0.057 [-0.110, -0.005] | essential | +0.015 | -0.030 | -0.136 | -0.091 | +0.015 | -0.136 | -0.038 | -0.056 | -0.058 | 545/924 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.800 over 308 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.800^2 / (308 * K)): K=2: 0.089, K=3: 0.073, K=4: 0.063, K=6: 0.052, K=8: 0.045


---

## results/20261003-114945-ablate-1bdd7a/report.md

SHA-256: `1e7d5eb2de1613ebb06d1c813bd0ce7dcc9e8cce91ee44b8c5a003409cd84e40`

# Ablation report: 20261003-114945-ablate-1bdd7a

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab; 17 official + 0 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.186, wins 242/408; by opponent: cpp_nicked_v92 -0.294, cpp_nicked_v75 -0.294, cpp_leviathan3 +0.588, v7-base-bot +0.529, nicked_v44 +0.500, nicked_lab +0.088

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| nobookmap | -0.217 [-0.450, -0.033] | essential | +0.000 | -0.064 [-0.176, +0.039] | neutral | -0.029 | -0.088 | +0.029 | -0.059 | -0.059 | -0.176 | -0.064 | - | 229/408 |
| nobooks | -0.400 [-0.667, -0.167] | essential | -0.014 | -0.127 [-0.275, +0.005] | neutral | -0.206 | -0.029 | +0.029 | -0.118 | -0.088 | -0.353 | -0.127 | - | 216/408 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.804 over 204 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.804^2 / (204 * K)): K=2: 0.110, K=3: 0.090, K=4: 0.078, K=6: 0.064, K=8: 0.055


---

## results/20261003-115128-ablate-71a0f6/report.md

SHA-256: `6971e7f895449c6075f84e14ebae11446eb3bb63f800893b27c4225e2e5a0eea`

# Ablation report: 20261003-115128-ablate-71a0f6

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 17 official + 0 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.147, wins 273/476; by opponent: cpp_nicked_v92 -0.588, cpp_nicked_v75 -0.235, cpp_leviathan3 +0.676, v7-base-bot +0.559, nicked_v44 +0.471, nicked_lab +0.147, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t2 | -0.014 [-0.100, +0.071] | neutral | +0.113 | +0.076 [-0.008, +0.160] | neutral | +0.324 | +0.000 | +0.235 | -0.147 | +0.029 | -0.382 | +0.471 | +0.076 | - | 291/476 |
| t2_d4 | +0.071 [+0.000, +0.157] | neutral | +0.030 | +0.042 [-0.042, +0.130] | neutral | +0.206 | +0.088 | +0.088 | +0.059 | -0.059 | -0.206 | +0.118 | +0.042 | - | 283/476 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.739 over 238 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.739^2 / (238 * K)): K=2: 0.094, K=3: 0.077, K=4: 0.066, K=6: 0.054, K=8: 0.047


---

## results/20261003-115234-ablate-b8901c/report.md

SHA-256: `2eaaca660688aca7907c1e8a98f847da5113da50734e8b266c5340e74def18a3`

# Ablation report: 20261003-115234-ablate-b8901c

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, v11q; 17 official + 0 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.071, wins 255/476; by opponent: cpp_nicked_v92 -0.529, cpp_nicked_v75 -0.294, cpp_leviathan3 +0.529, v7-base-bot +0.441, nicked_v44 +0.412, nicked_lab -0.059, v11q +0.000

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| y150 | +0.000 [+0.000, +0.000] | neutral | +0.018 | +0.013 [+0.000, +0.029] | neutral | +0.000 | +0.000 | +0.000 | +0.000 | +0.029 | +0.029 | +0.029 | +0.013 | - | 258/476 |
| y300 | +0.000 [+0.000, +0.000] | neutral | +0.018 | +0.013 [+0.000, +0.029] | neutral | +0.000 | +0.000 | +0.000 | +0.000 | +0.029 | +0.029 | +0.029 | +0.013 | - | 258/476 |
| y150_t2 | +0.100 [-0.029, +0.257] | neutral | +0.137 | +0.126 [+0.025, +0.218] | harmful (drop) | +0.265 | +0.206 | +0.088 | +0.147 | -0.029 | +0.176 | +0.029 | +0.126 | - | 285/476 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.815 over 238 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.815^2 / (238 * K)): K=2: 0.104, K=3: 0.085, K=4: 0.073, K=6: 0.060, K=8: 0.052


---

## results/20261003-125123-ablate-6a262e/report.md

SHA-256: `f7460a0b5513983e6326f7a3b2700c5b543ebd0cd4d0b840b18a521ac99b3cd6`

# Ablation report: 20261003-125123-ablate-6a262e

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy; 17 official + 0 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin -0.063, wins 222/476; by opponent: cpp_nicked_v92 -0.412, cpp_nicked_v75 -0.324, nicked_lab -0.029, opp-careful-queen +0.000, opp-raider -0.206, opp-growth-queen +0.353, opp-economy +0.176

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ref100 | +0.014 [-0.093, +0.164] | neutral | +0.054 | +0.042 [-0.074, +0.162] | neutral | +0.059 | +0.176 | +0.235 | +0.029 | +0.000 | -0.147 | -0.059 | +0.042 | - | 233/476 |
| ref250 | +0.086 [-0.007, +0.193] | neutral | +0.024 | +0.042 [-0.067, +0.155] | neutral | +0.118 | +0.029 | +0.088 | -0.088 | +0.176 | -0.029 | +0.000 | +0.042 | - | 233/476 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.830 over 238 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.830^2 / (238 * K)): K=2: 0.105, K=3: 0.086, K=4: 0.075, K=6: 0.061, K=8: 0.053


---

## results/20261003-134712-ablate-e3fcd5/report.md

SHA-256: `64a6d4d4efa3a862b2aa69390f00d289b1bf0e1abdcf233365b8b0da360caec4`

# Ablation report: 20261003-134712-ablate-e3fcd5

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy; 17 official + 0 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.050, wins 534/1020; by opponent: cpp_nicked_v92 -0.667, cpp_nicked_v75 -0.314, cpp_leviathan3 +0.569, v7-base-bot +0.588, nicked_v44 +0.392, nicked_lab -0.157, opp-careful-queen +0.000, opp-raider -0.098, opp-growth-queen +0.137, opp-economy +0.049

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t2 | -0.003 [-0.067, +0.070] | neutral | +0.100 | +0.070 [-0.003, +0.141] | neutral | +0.294 | +0.039 | +0.098 | -0.176 | +0.020 | +0.118 | +0.157 | -0.078 | -0.059 | +0.284 | +0.070 | - | 571/1020 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.831 over 340 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.831^2 / (340 * K)): K=2: 0.088, K=3: 0.072, K=4: 0.062, K=6: 0.051, K=8: 0.044


---

## results/20261003-171036-ablate-775827/report.md

SHA-256: `8d903f46adac724aa33c8c908abaea9248ba1a1b647901af3e58c20916fa2d60`

# Ablation report: 20261003-171036-ablate-775827

4 seeds, opponents v11q; 17 official + 0 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.103, wins 75/136; by opponent: v11q +0.103

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.945 over 34 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.945^2 / (34 * K)): K=2: 0.317, K=3: 0.259, K=4: 0.225, K=6: 0.183, K=8: 0.159


---

## results/20261003-171037-ablate-052b88/report.md

SHA-256: `d92b359a3cd5e29ba8c4a4d8c421ba7b96c62a3725832f9c7edfc2350515064d`

# Ablation report: 20261003-171037-ablate-052b88

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy; 17 official + 0 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.053, wins 358/680; by opponent: cpp_nicked_v92 -0.500, cpp_nicked_v75 -0.118, cpp_leviathan3 +0.559, v7-base-bot +0.559, nicked_v44 +0.324, nicked_lab -0.147, opp-careful-queen -0.029, opp-raider -0.088, opp-growth-queen +0.029, opp-economy -0.059

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ref100 | +0.040 [+0.010, +0.070] | harmful (drop) | +0.125 | +0.100 [+0.029, +0.176] | harmful (drop) | +0.235 | -0.059 | +0.000 | +0.088 | +0.059 | +0.147 | +0.000 | -0.029 | +0.324 | +0.235 | +0.100 | - | 392/680 |
| ref250 | +0.050 [-0.050, +0.140] | neutral | +0.092 | +0.079 [+0.003, +0.156] | harmful (drop) | +0.265 | -0.088 | +0.088 | +0.088 | -0.029 | -0.029 | +0.088 | +0.059 | +0.059 | +0.294 | +0.079 | - | 385/680 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.840 over 340 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.840^2 / (340 * K)): K=2: 0.089, K=3: 0.073, K=4: 0.063, K=6: 0.052, K=8: 0.045


---

## results/20261003-183034-ablate-3ac260/report.md

SHA-256: `b89639111f28f718a42f248b8e86dada21672c9215eddc8f3f31d969059b061f`

# Ablation report: 20261003-183034-ablate-3ac260

3 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy, v11q; 17 official + 0 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.119, wins 627/1122; by opponent: cpp_nicked_v92 -0.373, cpp_nicked_v75 -0.275, cpp_leviathan3 +0.667, v7-base-bot +0.608, nicked_v44 +0.373, nicked_lab -0.078, opp-careful-queen +0.078, opp-raider -0.196, opp-growth-queen +0.137, opp-economy +0.284, v11q +0.078

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | vs v11q | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ref100 | +0.024 [-0.067, +0.145] | neutral | +0.027 | +0.026 [-0.045, +0.097] | neutral | +0.020 | +0.020 | +0.078 | +0.000 | +0.000 | -0.020 | -0.069 | +0.196 | +0.020 | +0.108 | -0.069 | +0.026 | - | 641/1122 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.795 over 374 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.795^2 / (374 * K)): K=2: 0.081, K=3: 0.066, K=4: 0.057, K=6: 0.047, K=8: 0.040


---

## results/20261003-183036-ablate-5c644b/report.md

SHA-256: `bee3693e4bc5a5bf067064c7adf4c2531ec4f0ff8084948773bdf26bfcfc78e9`

# Ablation report: 20261003-183036-ablate-5c644b

4 seeds, opponents v11t; 17 official + 0 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin -0.015, wins 67/136; by opponent: v11t -0.015

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs v11t | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.945 over 34 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.945^2 / (34 * K)): K=2: 0.317, K=3: 0.259, K=4: 0.225, K=6: 0.183, K=8: 0.159


---

## results/20261003-192712-ablate-d2ca26/report.md

SHA-256: `a881af317684d5c40593907bc373711fc232454e744efc967d52bac172d8b0c7`

# Ablation report: 20261003-192712-ablate-d2ca26

2 seeds, opponents cpp_nicked_v92, cpp_nicked_v75, cpp_leviathan3, v7-base-bot, nicked_v44, nicked_lab, opp-careful-queen, opp-raider, opp-growth-queen, opp-economy; 17 official + 0 extra maps, both sides. Objective: wins. Delta = variant score minus base score on the same (opponent, map, seed, side); positive means removing the group helped. 95% CI resamples (map, seed) blocks.

base: mean margin +0.182, wins 402/680; by opponent: cpp_nicked_v92 -0.382, cpp_nicked_v75 -0.294, cpp_leviathan3 +0.794, v7-base-bot +0.500, nicked_v44 +0.588, nicked_lab +0.147, opp-careful-queen +0.206, opp-raider -0.059, opp-growth-queen +0.265, opp-economy +0.059

| variant | current pool delta [95% CI] | pool verdict | other maps | delta all 15 [95% CI] | verdict | vs cpp_nicked_v92 | vs cpp_nicked_v75 | vs cpp_leviathan3 | vs v7-base-bot | vs nicked_v44 | vs nicked_lab | vs opp-careful-queen | vs opp-raider | vs opp-growth-queen | vs opp-economy | official | extra | wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sx2 | -0.040 [-0.130, +0.020] | neutral | -0.087 | -0.074 [-0.153, -0.009] | essential | -0.088 | -0.059 | -0.088 | -0.118 | -0.059 | -0.088 | -0.147 | -0.059 | -0.088 | +0.059 | -0.074 | - | 377/680 |
| sx3 | -0.090 [-0.180, -0.010] | essential | -0.046 | -0.059 [-0.144, +0.009] | neutral | +0.000 | +0.029 | -0.059 | -0.088 | -0.059 | -0.235 | -0.206 | -0.029 | -0.118 | +0.176 | -0.059 | - | 382/680 |

Noise: seed-to-seed SD of base's margin within a (opponent, map, side) cell 0.854 over 340 cells. Expected paired CI half-width with K seeds, 1.96 * sqrt(2 * 0.854^2 / (340 * K)): K=2: 0.091, K=3: 0.074, K=4: 0.064, K=6: 0.052, K=8: 0.045


---

## results/QUEEN_AWARE_PANEL.md

SHA-256: `9c62cb63ef4f47100be1606e490827d1bc4ddd77830a7bcbaa067c4e0272517e`

# Queen-aware opponent panel (3 Oct)

Specialists built from our own controller (one shared lineage, not independent
strategies), to stop local tests underpricing queen survival:

- opp-careful-queen: v11q behaviour (light queen + 3-step escape search), small careful queen.
- opp-raider: v11q + CPP_QUEEN_HUNT (bonus 600, pull 400): workers chase and trade into enemy queens.
- opp-growth-queen: v11q + queen food x3 + keep length 6: big queen.
- opp-economy: v11ms (multistep, no queen protection): strong economy, careless queen.

Report results against this family separately from the old nicked-family panel.

