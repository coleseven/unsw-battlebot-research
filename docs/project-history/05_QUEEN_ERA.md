# 5. Queen era: v11ms, v11q and v11t

[Project history](../../PROJECT_HISTORY.md) · [Previous](04_LEARNING_RESEARCH_RESET.md) · [Next: evidence and gaps](06_EVIDENCE_AND_GAPS.md)

All results below are historical through commit `69095e5`, 3 October 21:30 EDT. The main chronological source is the preserved [feature experiment log](snapshot-2026-10-03/FEATURE_EXPERIMENT.md); plans and generated reports are in the [run register](RUN_REGISTER.md). A table's game count is **per variant**, unless explicitly stated otherwise. Wins are counts, not the generated signed-score metric.

## Q0: update the laboratory

The isolated unswbc 1.2.3 runtime verified six engine-rule tests, introduced queen diagnostics and switched new plans to actual recorded outcomes. v10o was legal under that runtime, with sandbox peak about 8.0M; the log records upload around **00:48 UTC October 2**.

The basic worker policy still split at four, leaving most dragons with one free step. The challenge was to preserve that productive economy while making original queens survive and using extra movement when it genuinely helped.

## Q1–Q3: protect/grow everything was expensive; selective free movement worked

| Stage | Conditions and variants | Outcome |
|---|---|---|
| Q1 baseline | 15 maps, six opponents, both sides, two seeds; 360 games | Base **200 wins**, queen alive at round limit **10**, enemy 43; median queen death around rounds 84–87 |
| Q1 queen mode | Queen protected, queen-only feeding, king beacon disabled | `q_on` **148** wins/28 surviving queens; no-split 147/31; later variant 158/33. Large win loss despite more surviving queens |
| Q2 movement | Use extra free steps for a visible pearl | Implemented and legal; initially noted to trigger rarely with split-at-four |
| Q3 larger split thresholds | Base 216/360; queen+multistep, thresholds seven/eleven and combinations | q_ms 175; q_ms_s7 100; q_ms_s11 83; q_s7 86; ms_s7 126. Larger workers lost heavily |
| Q1b safety/beacon | Base 210/360 | Keep beacon 181; reach 178; dead-end 182; full 174; full/no-split 166. None solved the tradeoff |
| Q1c wider threat reach | Base 207/360, queen alive 9 | Margin+2:169/32; +3:170/32; +2/no-split 167/33. Survival improved, wins fell |
| Q3b multistep alone | Base 209/360 | **236 wins**, strong-opponent subset 95 versus 76; with full queen safety 201 |
| Q3c confirmation | 15 ranked + seven reconstructed Sprint maps, six opponents, three seeds; 792 games | **474 versus 447 wins**; known maps 335 versus 308, Sprint 139 versus 139; signed outcome delta +0.068 [+0.013, +0.124] |

This produced **v11ms**, hash `d8a1433a6097d63c`, v10o plus pearl-directed multistep. Direct 120-game checks gave **62 wins versus v10o**. The full queen-safety combination scored **48/120 against v11ms**, despite 17 surviving queens versus 12.

The opponent panel was largely inherited from old scoring. Its bots frequently lost their queens, making longest-dragon play unusually important. That limited the panel's relevance, but did not license ignoring losses against it. The next successful queen change needed to improve survival without sacrificing most of the worker game.

Diagnostics reinforced a model problem: in one 12-game queen-safety sample, seven queen deaths were enemy head-ons at lengths 12–20, while four queens boxed themselves in early. Once a queen had zero available moves, larger scoring penalties could not create an exit.

## Q4: light queen plus short escape tactics

The new light mode prevented a queen from feeding itself to a worker and added nearby-worker avoidance. The first tactical search looked three steps ahead, simulated the queen's body and considered multi-step threat reach and friendly heads. It retained the incumbent move unless another line survived longer.

| Q4 screen variant | Wins /360 | Surviving queens |
|---|---:|---:|
| Base v11ms behavior | 223 | 13 |
| Tactics only | 218 | 19 |
| Light only | 226 | 22 |
| **Light + tactics** | **228** | **37** |
| Light + tactics + radius 2 worker guard | 217 | 51 |
| Light + tactics + extra threat margin | 204 | 14 |

The broader guard preserved more queens but hurt strong-opponent wins. Overestimating threat reach could make nearly every candidate appear doomed.

Confirmation on **792 games** gave light+tactics **490 wins versus 492**, with **79 surviving queens versus 24**. Known-map wins tied 353–353; Sprint 137 versus 139. The broad panel was neutral, but direct tests were favorable: **80/120 against v10o**, **73/120 against v11ms**, with 20 surviving queens in each candidate matchup versus two and one for the controls.

This became **v11q**, hash `1c547e93cdff8382`, sandbox peak about 8.0M. The correct historical claim is “survival and direct-matchup improvement with neutral old-policy panel,” not a large universal pooled-win improvement.

## Q5–Q11: growth, hunting, travel and stronger safety did not replace v11q

| Stage | Main test and counts | Decision |
|---|---|---|
| Q5 selective growth/feeding | Seven opponents including v11q; base 268/420. Split cutoffs 250/350 no effect; queen-feed 269; cutoff+feed 270, but v92 wins 17 versus 25 | Mixed; not adopted |
| Q6 flight and food | Base 254/420. Flight 251; food×3 246 | No gain |
| Q6 keep queen length 6 | keep 6 226, food+keep 235, all 230; queen survival 27/26/27 versus 56 | Rejected; surviving queens could be longer but survival fell sharply |
| Q7 assassination screen | Base 262/420, enemy queen alive 40. Hunt 265/alive 25; stronger hunt 261/27; no-pull 260/31 | Mechanism moved, weak initial gain; confirm |
| Q7 confirmation | 924 games, seven opponents, three seeds, 22 maps: hunt 549 versus 563; enemy queens 65 versus 72 | Did not replicate; not adopted |
| Q8 extra travel toward hubs | 924 games: 557 versus 560; our queens 75 versus 94 | No gain; queen travel harmful in this sample |
| Q8b workers-only travel | 924 games: 552 versus 563; v92 wins 45 versus 57; queens 101 versus 102 | Rejected; retain pearl-only multistep |
| Q9 depth and keep-away | Base 256/420, queens 50. Depth 4 251/57; depth 5 249/44; keep 300 257/55; keep 300+margin 1 256/63; depth 4+keep 253/57 | Survival leads only, no convincing win improvement |
| Q10 room safety | Base 258/420, queens 55. Safety×3 255/56; ×6 254/56; ×3+guard 2 255/69 | Safety multipliers ineffective; guard combination advanced for confirmation |
| Q11 confirmation | Base 572/924, queens 94. Keep-away 563/104; keep-away+guard 2 545/107 | Rejected: more surviving queens, fewer wins |

These trials reject the listed implementations and settings. They do not prove queen hunting, growth or cooperation can never help. In particular, increasing a generic guard radius is not the same intervention as reserving a queen's specific required exit.

## Recorded live performance and changing loss anatomy

The log records v11q uploaded around **21:04 UTC October 2**. Its first 20 games yielded **12 wins**, with our queen alive in seven versus v10o's two in the earlier 50-game cohort. Different opponents and sample windows prevent reading that as a controlled +31-point survival treatment effect.

Later snapshots were mixed. One report described 82 games and 34 wins, with 22 outcomes determined by unequal queen survival. At about 00:00 UTC October 3 the team was **rank 108/973, rating 1529**, with rank 100 at 1560. This was a point-in-time gap, not an achieved rank 100.

A later reported 162-game cohort split losses into **16 elimination, 33 longest, eight queen length and 31 queen survival**, making unequal survival its largest deficit. Its stated battle/game count combination needs audit because the record also describes typical five-game ranked battles. Do not silently use it to derive a number of independent battles.

Top-ladder sampling under the new rules examined 185 games: approximate deciding-condition shares were 31% elimination, 31% longest with both queens dead, 23% queen survival and 15% unequal living queen length. Surviving queens had median length 3. These descriptive profiles argued against assuming large queens were necessary, while not establishing an optimal target size.

## Current engine/maps: C1

The October 3 review found that current official **1.2.9** maps differed from the older local/reconstructed set. The project installed an isolated runtime, reran six rules tests, copied all 22 official maps into `maps/v129`, and stored hashes/spawner counts in a manifest. Among 16 maps seen in recent ranked replays, edges matched; some initial dragons were side-swapped. Current rotation was **17 maps**: the previous ten plus seven Sprint maps.

C1 used those 17 maps, six opponents, two seeds, both sides: **408 games per variant**.

- v11q baseline: **242 wins**, 84 surviving queens versus 51 opponent queens.
- Map completion disabled: **229 wins**.
- All books disabled: **216 wins**.

Books remained useful under the refreshed setup. Elimination decided 96 games, of which ours won 40. Loss concentrations included Trophy 14, PD 11, Stripes 9, Devil 7 and weakhold 6. This already supported investigating the worker economy alongside queens.

## C2/C3/C5: corrected queen search becomes v11t

The new search corrected several representations: food retains the tail, threats follow traversable paths, uncertain exits are distinguished from known continuations, line counts are tracked, and the action validated by search is the final emitted movement. These were substantive model changes, not another broad safety-weight sweep.

| Stage | Panel | Base | Corrected-search candidate | Interpretation |
|---|---|---|---|---|
| C2 | Seven opponents, 17 maps, two seeds; 476 games |273 wins, 101 queens |**291 wins, 158 queens**; depth 4 version 283/152 | Positive screen; v92 25 versus 14, v11q 50 versus 34; lab regression 26 versus 39 |
| C3 worker yield | Same size panel, fresh seeds; 476 games |255 wins, 91 queens |Yield alone 258/91 at both strengths; yield+corrected search **285/175** | Yield alone not adopted; combination supplies supporting evidence, but is not a pure search-only replication |
| C5 confirmation | Ten opponents including four queen-aware specialists, 17 maps, three seeds; 1,020 games |534 wins, 207 queens |**571 wins, 346 queens** | Third positive result with different conditions; reported signed outcome delta +0.070 [−0.003, +0.141] |

C5's interval includes zero. The historical adoption relied on the sequence of results, mechanism corrections, improved queen survival and subsequent direct evidence—not on claiming that this individual interval established a strict-positive effect.

The queen-aware panel consisted of careful, raider, growth and economy specialists derived largely from our own v11q/v11ms lineage. It improved behavioral coverage but did not constitute four independent externally developed families. The [panel description](snapshot-2026-10-03/results/QUEEN_AWARE_PANEL.md) records the construction.

**v11t**, hash `668938a734ff8da6`, was frozen as v11q plus corrected search. On 136 fresh direct games across 17 maps and four seeds it won **75/136**, with **48 surviving queens versus 26**. Stripes 0/8 and Tower Defense 1/8 remained weak; weakhold 8/8 was strong. The sandbox peak was **8.4M points**. It was recommended for upload; this archive has no independent confirmation of that upload.

## C4/C6/C7: refuge looked promising, then failed confirmation

Temporary refuge pulled a crowded light queen toward more open cells. Its trigger considered nearby heads and available exits.

| Stage | Results | Decision |
|---|---|---|
| C4, old search |476 games;  base 222/82 queens; refuge 100 **233/95**, refuge 250 **233/105** | Test on the new search before adoption |
| C6, on v11t |680 games;  base 358/218 queens; refuge 100 **392/243**, refuge 250 **385/256**. Signed delta for 100 +0.100 [+0.029, +0.176] | Freeze experimental **v11u**, then confirm |
| Direct v11u versus v11t |**67/136 wins**, queens 54 versus 56 | No head-to-head superiority |
| C7 confirmation |1,122 games;  base 627/406 queens; refuge 100 **641/395**; delta +0.026 [−0.045, +0.097] | Initial gain did not establish a robust replacement; refuge not adopted |

The confirmation point estimate was still positive. “Failed confirmation” therefore means uncertainty and direct evidence did not support promotion, not that the point estimate reversed below zero. v11u remained a preserved experimental snapshot.

## Queen death audit and C8: association did not identify the remedy

The 674 C5 games in which v11t's queen died were replayed; all reproduced their winners. Causes were **358 wall/kelp,213 enemy head-on,50 friendly head-on,43 friendly body,10 enemy body**. Death length was two in 332 cases and three in 314.

Among 358 wall deaths,355 had no free ordinary move under the diagnostic's model. **241** came within two rounds of a queen split, although that window contained only 1.9% of queen turns. Approximately 107 followed an already-doomed fallback split; about 131 followed ordinary length-four splits with just one or two exits. The hypothesis was that splitting consumed the queen's turn and bypassed useful escape search.

C8 tested requiring at least two or three free open exits before light-queen splitting:

| Variant | Wins /680 | Surviving queens |
|---|---:|---:|
| v11t-equivalent base |402 |240 |
| Require two exits |377 |211 |
| Require three exits |382 |193 |

Both were rejected. The latest log interprets shrinking to length two as protective. The conservative historical conclusion is that **these minimum-exit restrictions reduced wins and survival**. It does not prove all post-split deaths were unavoidable, that no individual split contributed to death, or that earlier corridor-entry decisions were correct. A branch comparison at the actual decision would be needed for those causal claims.

## The separate 95-game live replay review

The earlier same-day [live review](snapshot-2026-10-03/LIVE_GAME_REVIEW_2026-10-03.md) froze **19 completed ranked battles / 95 games**, battle timestamps 12:12–18:19 UTC on October 3. Pending battle 981941 was excluded. All replay winners matched public metadata. The profile then showed **rank 121, rating 1531**. The experiment log associated the live bot with v11q, but public `botVersion` was null; the upload hash was not independently verifiable.

| Deciding condition | Wins | Losses |
|---|---:|---:|
| Elimination |6 |18 |
| Longest/total after equal queen lengths |31 |22 |
| Only one queen survives at round limit |6 |10 |
| Both queens survive at unequal lengths |1 |1 |
| Total |**44** |**51** |

Our queen survived 14/95, theirs 23/95. Our 81 queen deaths were 39 walls, 32 enemy head-ons, five friendly head-ons, four friendly body collisions and one self-collision. Detailed queen-state reconstruction covered the **first 55 games**, not all 95; all 21 wall deaths in that detailed subset lacked an unoccupied immediate exit on the fatal turn.

Concrete cases retained for Claude:

- **Maze 981445 and 980023:** same queen corridor path and round 13 death at (12,16), length 3; a prior split at round 11. The relevant question is earlier entry/split choice, not a new penalty after every exit is blocked.
- **Portals 975841**, plus 972500/971790: repeated terminal cell (16,7); weakhold 976811 and 981443 repeated a similar three-walls-plus-neck configuration at (13,0).
- **Devil 973653 and Portals 973652:** friendly workers killed the queen later in the same round after her move. A local yield rule must check whether the worker had an alternative; failing that, earlier traffic decisions matter.
- **Portals 975268:** after consecutive food collections retained body length, a portal exit led into the queen's own tail. This is a precise transition-model case.
- **Elimination economics:** Devil 981442 had population 4 versus 23 at round 100; Stripes 979005 3 versus 13; Trophy 975842 6 versus 29; Trauma 975267 5 versus 34. Other Stripes losses first led and then collapsed, separating failure to establish an economy from failure to sustain it.
- **Schooltime positive control:** six wins in six games, every queen ending at length 3. Five matched enemy queen length and won through secondary scoring.

This cohort's largest deficit was elimination, unlike the earlier queen-survival-heavy cohort. They may overlap and have different schedules; neither invalidates the other, and pooling them without deduplication would be wrong. Nor can this live cohort evaluate v11t, whose recommendation occurred later.

## Position at the cutoff

v11t remains the recommended candidate; refuge and minimum-exit split restrictions remain off. The frozen parameter snapshot confirms light queen, initial tactics, corrected tactics, pearl multistep, king beacon, big feeding, map completion and age 30 hub sharing active; R4, R5, queen hunt, extra hub travel, worker-yield and refuge additions inactive.

The next historical entry should record actual v11t deployment and a correctly versioned live cohort if available. The current evidence supports investigating both confinement/traffic and worker economy, while retaining the failed experiments as constraints on proposed fixes.
