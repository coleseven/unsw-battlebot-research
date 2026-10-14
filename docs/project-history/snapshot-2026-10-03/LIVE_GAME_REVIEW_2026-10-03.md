# Live-game review for Claude — 3 October

## Cohort and conclusion

Downloaded and decoded **95 distinct completed ranked games from 19 battles**, covering battle timestamps **3 October 12:12–18:19 UTC**. These were the completed battles on the first two public listing pages when collection started. The pending battle 981941 was excluded. This is a fixed recent sample, not all games played today and not a randomized comparison.

All 95 replay winners matched the website's game metadata. Team membership and queen ID were derived from each replay, including side-swapped starting configurations: **team B does not always mean queen ID 1**. The experiment log says v11q is live; public `botVersion` was null, so this report cannot independently verify the uploaded hash or exclude an unrecorded switch.

At collection start the [team profile](https://game.battlecode.au/teams/590) showed rank 121, rating 1531. These are transient figures, not a performance estimate.

**Main recommendation: finish C2 confirmation, add the repeatable dead-end cases below as diagnostics, and investigate worker food access/population collapse alongside queen survival.** The newest cohort changes the relative priority: elimination is its largest net deficit. Do not turn every loss into a queen-only problem.

## Outcomes

| Deciding condition | Wins | Losses | Net |
|---|---:|---:|---:|
| Team elimination | 6 | 18 | −12 |
| Longest/total after equal queen lengths | 31 | 22 | +9 |
| Only one queen survives at the round limit | 6 | 10 | −4 |
| Both queens survive with unequal lengths | 1 | 1 | 0 |
| **All games** | **44** | **51** | **−7** |

Elimination takes precedence in this classification. Equal living queens are classified under longest/total, not queen length. There were no draws. We won 20/40 games as team A and 24/55 as team B; opponent and map differences prevent interpreting that as a causal side effect.

Our queen survived to game end in **14/95**, theirs in **23/95**. Our 81 queen deaths comprised **39 wall/kelp, 32 enemy head-ons, five friendly head-ons, four friendly-body collisions and one self-collision**. Median death round was **140**, median length **3**. Death round uses the replay's zero-based round number.

These observations complement, rather than invalidate, the earlier 162-game cohort where unequal queen survival was the largest deficit. The samples may overlap, face different opponents and mix different map frequencies; do not pool them as independent evidence or infer a policy regression from the change in proportions.

## Map priorities

| Map | Wins/games | Interpretation for the next investigation |
|---|---:|---|
| Schooltime | 6/6 | Preserve this behavior; every queen finished at length 3 |
| Slithery Fight | 5/7 | Useful positive control for small-queen survival |
| Trauma | 4/6 | Mixed: good overall, but one severe economy collapse |
| Maze | 3/5 | Positive results conceal a repeated early queen trap |
| Portals | 4/9 | Both terrain traps and teammate/own-body collisions |
| Trophy | 2/7 | Four elimination losses; opening economy is urgent |
| Stripes | 2/7 | All five losses were eliminations |
| Devil | 1/5 | Weak economy and an early friendly queen kill |
| Prisoners Dilemma | 1/5 | Mixed elimination, queen survival and narrow conversion losses |
| Tower Defense | 1/4 | Severe population deficit in a representative loss |
| weakhold | 1/4 | Repeated terminal corridor trap |

Small map samples are diagnostic leads, not stable map win-rate estimates. Full results for all 17 observed maps are in the saved summary.

## Case 1: Maze food corridor — intervene before round 9

**Games 981445 and 980023**, against different opponents, reproduce the same queen route and death at **round 13, cell (12,16), length 3**. A third game, 979008, reaches the same terminal cell and dies at round 16, despite the team eventually winning.

- Round 8: queen at (10,14), moves east.
- Round 9: at (11,14), length 2, moves south; north and east are also unoccupied immediate alternatives.
- Round 10: at (11,15), length 3, continues south; side edges are walls.
- Round 11: at (11,16), length 4, **splits 2**.
- Round 12: parent queen, now length 2, moves east.
- Round 13: at (12,16), length 3, north/east/south are walls and west contains its own neck. It attempts east and dies.

The fatal move is already forced in the one-step movement action space. The actionable decision is the corridor entry and its interaction with food and splitting, not a larger penalty at round 13. The existence of an immediately legal alternative at round 9 does not prove that alternative wins or remains safe; test it.

**Claude task:** reproduce this route using the current map and locally captured observations; compare baseline and C2 decisions around rounds 8–12. Include split transitions in the diagnostic. The current decision pipeline can return a split before invoking movement tactics, so a corrected move search alone does not establish that the intervening split is safe. Reject entering an unrecoverable food-lined terminal branch earlier; do not hardcode only this coordinate.

Evidence: [battle 981442](https://game.battlecode.au/visualiser?match=981442), game 981445; [battle 980020](https://game.battlecode.au/visualiser?match=980020), game 980023. Exact short histories: [981445](results/live-review-20261003/981445-queen-opening.json), [980023](results/live-review-20261003/980023-queen-opening.json).

## Case 2: the same trap family appears elsewhere

In the detailed **55-game subset**, 21 queen wall deaths were examined at their final own turn. **All 21 had zero unoccupied immediate movement destinations.** This establishes immediate boxing-in, not whether the trap was static, avoidable, or dynamically created several turns earlier.

- **Portals 975841:** length-3 queen enters (16,7), dies round 50; three walls and its neck block all exits. Games **972500** and **971790** die at the same cell at rounds 68 and 70. Those two teams still win, so match wins alone conceal the defect. [Battle 975838](https://game.battlecode.au/visualiser?match=975838)
- **weakhold 976811:** at (12,0), length 4, queen splits at round 54; moves east at 55 and dies length 3 at (13,0) at 56. Game **981443** dies at the same terminal cell at round 92. [Battle 976807](https://game.battlecode.au/visualiser?match=976807)

These justify a small regression suite of **terrain + body + food + split** sequences. Use the last open junction as the intervention point. A branch with one entrance and no room to turn deserves explicit analysis before the queen commits. Do not classify all 39 wall deaths as this exact mechanism without inspecting them.

## Case 3: workers kill queens after the queen has moved

**Devil 973653:** our queen travels north through a narrow corridor. At rounds 25–27 its only unoccupied move is north. At round 27 it enters (11,0), grows to length 3, and **our dragon 2 kills it by head-on collision later that round**. [Battle 973650](https://game.battlecode.au/visualiser?match=973650)

**Portals 973652:** queen moves from (17,0) to its only unoccupied destination, (16,0), at round 222. **Our dragon 127 then kills it**. The queen had choices earlier: at round 221, north and west were both immediately open.

**Claude task:** capture the offending worker's own observation/action as well as the queen's history. Check whether it knowingly enters the visible queen head, is itself trapped, or follows another overriding policy. First test a narrow worker veto for a visible friendly queen head when a safe alternative exists. When no worker alternative exists, diagnose the earlier approach conflict. Broad guard-radius penalties already failed; these cases motivate specific yielding and corridor scheduling instead.

These are directly attributed friendly head-ons, not inferred from nearby bodies. They do not establish that the worker had a safe alternative on the fatal turn.

## Case 4: portal tail occupancy

**Portals 975268**, round 293: queen length 12 at (4,14). West/north are walls, east is its neck, and the south portal leads to **(28,1), occupied by its own tail**. It moves south and self-collides. The previous two moves collected food, growing length 10→11→12. [Battle 975266](https://game.battlecode.au/visualiser?match=975266)

**Claude task:** include this as a C2 body/growth/portal test. The current tail blocks before movement. A model based only on contiguous local head history cannot assume the tail has vacated, especially after portal movement and growth. Saving it may require an earlier route or a legal split; neither is demonstrated by this replay alone.

## Case 5: worker economies collapse before endgame conversion matters

Representative elimination losses show large population gaps early:

| Game | Map | Round-100 population, us/them | Game ends after rounds | Pearls eaten, us/them |
|---|---|---:|---:|---:|
| 981442 | Devil | 4 / 23 | 119 | 18 / 181 |
| 979005 | Stripes | 3 / 13 | 140 | 3 / 80 |
| 975839 | Tower Defense | 3 / 26 | 461 | 37 / 699 |
| 975842 | Trophy | 6 / 29 | 148 | 21 / 190 |
| 975267 | Trauma | 5 / 34 | 454 | 54 / 1213 |

Pearl counts include corpse collection, so these totals do **not** by themselves prove which side controls natural spawners. They establish a resource-acquisition and population disparity requiring earlier diagnosis.

Not every elimination follows the same pattern: **Stripes 972503** had us ahead in population 13/9 at round 100 and 12/5 at 150, then lost by elimination after 354 rounds. **Stripes 962400** also started ahead before collapsing. Separate failure to establish an economy from failure to sustain an established advantage.

**Claude task:** prioritize Trophy and Stripes opening/territory audits in parallel with C2 confirmation. Track natural versus corpse pearls, first useful food access, newborn survival and productive-region coverage. For the reversal cases, inspect the period between the population peak and collapse. Do not respond with a global split delay—the earlier tests rejected that change decisively.

## Case 6: keep conversion as a secondary project

With queens dead/equal, some losses still have abundant total mass:

- **Autarky 981446:** longest 19 vs 25, total 118 vs 60.
- **Around UNSW 973654:** longest 40 vs 42, total 360 vs 207.
- **PD 966059:** longest 26 vs 27, total 57 vs 40.

These are candidates for late collection/retention studies, not evidence to sacrifice queen safety globally. Conversely, Schooltime won all six sampled games with a surviving length-3 queen; in five of them the enemy queen also finished at 3 and our secondary score won. Preserve the worker economy and conversion behavior behind these successes.

## Immediate handoff

1. **Finish the already-running/queued C2 confirmation.** The latest log records its promising screen; this public sample does not validate that unuploaded candidate. Report lab-family regressions and queen-aware results separately.
2. **Test the listed corridor sequences against C2.** Include split decisions and the final emitted action, not only the candidate move score. Use fresh local games for causal comparison; public observations omit private memory and may redact sonar/spawn timers.
3. **Investigate worker yielding using 973653 and 973652.** Record the killer's alternatives before proposing an override.
4. **Add Trophy/Stripes economy diagnostics.** Elimination is the largest deficit in this current cohort, and queen survival alone cannot address all of it.
5. **Retain wins as the promotion criterion.** More queen survival or a fixed replay is a mechanism check, not sufficient release evidence.

No bot code, training job or submission was changed by this review. No message was sent to another task; this document is the handoff.

## Evidence bundle

All files are under `results/live-review-20261003/`:

- [summary.json](results/live-review-20261003/summary.json): 95-game totals and all map results.
- [details.json](results/live-review-20261003/details.json): per-game outcome classes, queen deaths, final sizes and timelines.
- [games.json](results/live-review-20261003/games.json): full analysis plus metadata and replay SHA-256 hashes.
- [battles.json](results/live-review-20261003/battles.json): frozen public cohort selection.
- [queen-cases.json](results/live-review-20261003/queen-cases.json): detailed queen histories for the first 55 games analyzed, explicitly a subset.
- `<game ID>.replay`: all 95 raw replays, with small analysis scripts retained for reproducibility.

The report contains observations and testable hypotheses. It does not claim a counterfactual win, knowledge of an opponent's source code, or an exact reconstruction of private bot state.
