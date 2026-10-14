# Top-five strategic analysis and implications for top 100

Prepared 30 September 2026, late evening EDT. **Current-leaderboard snapshot: 1 October, approximately 02:29 UTC / 30 September 22:29 EDT.** The leaderboard changed during the broader review, so this report distinguishes the current five from an earlier morning sample. No bot code, submission or game-running experiment was changed.

The implementation order is in [WORK_QUEUE.md](WORK_QUEUE.md), updated against the latest results in [FEATURE_EXPERIMENT.md](FEATURE_EXPERIMENT.md).

## Main finding

**The strongest transferable idea is control of where length goes, throughout the game:** first into useful workers, then into a defensible scoring dragon. Raw population, collected pearls, low death counts and a large search budget are each incomplete objectives.

There are several successful implementations of that idea. Cutlery concentrates aggressively; forgot to mention combines large amounts of worker turnover with strong late conversion; 3.14159265 can retain a larger supporting population while feeding a king; SSS supplies clear examples of both king growth and elimination pressure. cheji bt is particularly instructive because its public behavior changed across the day: an undated aggregate would hide that change.

The present gap is materially smaller than the gap to these leaders. At approximately 02:39 UTC, [777](https://game.battlecode.au/teams/590) was **rank 133, rating 1671**, while [rank 100](https://game.battlecode.au/leaderboard?page=10) was **1723**. That is a moving 52-point target, not evidence that we need to rebuild the entire bot to reach it.

## 1. Which teams, and what evidence?

### Current five

| Rank | Team | Rating | Fresh sample | Median opponent rating |
|---:|---|---:|---:|---:|
| 1 | [Cutlery](https://game.battlecode.au/teams/306) | 2137 | 17 wins / 25 | 1984 |
| 2 | [forgot to mention](https://game.battlecode.au/teams/264) | 2119 | 22 / 25 | 1942 |
| 3 | [3.14159265](https://game.battlecode.au/teams/314) | 2115 | 20 / 25 | 1917 |
| 4 | [SSS](https://game.battlecode.au/teams/91) | 2102 | 19 / 25 | 1917 |
| 5 | [cheji bt](https://game.battlecode.au/teams/70) | 2092 | 15 / 25 | 2060 |

All five were listed as C++. Ratings come from the live [leaderboard](https://game.battlecode.au/leaderboard), not a cached search result.

The fresh sample is five completed ranked battles per team, five games per battle. Battle timestamps span **01:59–02:23 UTC on 1 October**, mostly the same autoscrim batch. This is a recent behavioral sample, not a statistically independent ranking experiment. cheji bt faced a noticeably stronger schedule; its lower sample win rate does not rank its underlying ability below the other four.

The earlier snapshot, **30 September 13:32 UTC**, had cheji bt, forgot to mention, Stockfish, Cache me outside and SSS in that order. I analyzed ten ranked battles / 50 games per team there: **250 team-game observations across 215 distinct games**. Those opponents were generally stronger than the fresh cohort: median ratings were 2039, 2056, 2046.5, 2059.5 and 2040.5 respectively. The earlier cohort is used for additional mechanisms and temporal comparisons, with its date kept explicit.

No attributable public source repository was verified for these teams. **Their exact search, learning, messaging and parameter-tuning algorithms are unknown.** A name such as Stockfish is not evidence of chess-style search. Sonar payloads and CPU information are redacted in the public replays; ping counts do not reveal message contents.

### Fresh map results

Entries are wins / games, not estimated long-run win probabilities. A dash means no sampled game.

| Map | Cutlery | forgot to mention | 3.14159265 | SSS | cheji bt |
|---|---:|---:|---:|---:|---:|
| Autarky | 3/4 | 3/3 | 3/3 | 2/2 | 2/3 |
| Default | 0/1 | 1/1 | 3/4 | 2/4 | 1/2 |
| Devil | 2/2 | 0/1 | 2/2 | 2/2 | 1/2 |
| Portals | 4/5 | 3/3 | 1/2 | 1/2 | 3/5 |
| Prisoners Dilemma | 2/4 | 3/4 | 1/1 | 1/1 | 1/1 |
| Queen Of Spades | 1/2 | 2/2 | 2/2 | 1/2 | 2/2 |
| Schooltime | 2/3 | 3/3 | 2/4 | 2/2 | 1/2 |
| Slithery Fight | 2/2 | 2/3 | 1/1 | 2/2 | — |
| Trauma | — | 2/2 | 1/2 | 2/3 | 2/4 |
| Trophy | 1/2 | 3/3 | 4/4 | 4/5 | 2/4 |

Use these cells to choose cases to inspect. A 0/1 is not an established weakness, and a 4/4 is not proof of a solved map.

### How the current five finish games

The final-state medians below use **round-limit games only**. Elimination wins do not get treated as if their surviving dragons played on to round 500. Different maps/opponents still confound direct team-to-team comparisons.

| Team | Elimination W–L | Round-limit W–L | Median final dragons | Median final longest | Median final total |
|---|---:|---:|---:|---:|---:|
| Cutlery | 8–3 | 9–5 | 2 | 45.5 | 61 |
| forgot to mention | 10–2 | 12–1 | 10 | 48 | 118 |
| 3.14159265 | 10–1 | 10–4 | 15 | 37.5 | 106 |
| SSS | 13–3 | 6–3 | 7 | 42 | 74 |
| cheji bt | 9–6 | 6–4 | 2.5 | 44 | 59 |

These profiles suggest different amounts of support retained around a collector. They do not establish optimal population targets.

| Team | Splits performed at length 4 | Multi-step moves / move actions | Mean sonar pings / game | Games with a late large rear-child transfer |
|---|---:|---:|---:|---:|
| Cutlery | 60.9% | 0.61% | 18,125 | 10/25 |
| forgot to mention | 72.3% | 0.35% | 19,005 | 11/25 |
| 3.14159265 | 61.5% | 0.12% | 41,743 | 12/25 |
| SSS | 71.6% | 0.69% | 24,811 | 6/25 |
| cheji bt | 79.2% | 0.86% | 19,833 | 11/25 |

“Late large rear-child transfer” means round ≥400, child length ≥8, and parent left at length 2. The threshold is an analysis definition, not an inferred bot parameter. All five sent sonar in every fresh sampled game. Extra movement was rare, but rarity does not imply that a well-timed escape is unimportant.

Across the **60 fresh round-limit games, 32 final longest dragons were born at or after round 400**. This is why tracing the eventual king's ID alone badly understates earlier investment in many games.

## 2. Cutlery: concentrated scoring power, with little spare population

**Observed plan:** build an economy, recycle workers, and finish with a small set of scoring dragons. In its 14 fresh round-limit games, median population fell from **21 at round 100 to 14 at round 300 and two at the finish**. Median longest length rose from **10 at round 300 to 32 at round 400 and 45.5 at the finish**. These are separate medians, not one synthetic game's trajectory.

Its fresh sample produced eight elimination wins and three elimination losses. Thus this is not simply a passive one-king bot: it can also overwhelm an opponent before the deadline.

**A useful success:** in Schooltime game **797338**, the eventual winner grew from **15 at round 400 to 43 at the finish**. Its 28 late pearls comprised **17 from its own corpses, seven natural spawns and four enemy-corpse pearls**. That exact 28-length increase is a clean conversion example. See [battle 797334](https://game.battlecode.au/visualiser?match=797334).

Cutlery won four of five fresh Portals games, finishing those wins with longest lengths **58, 68, 56 and 55**. The fifth finished **37 versus 41**. This makes it a useful example for collection and preservation on constrained terrain; it does not identify its hidden portal planner.

**Failure mode:** a small surviving population can have no way to replenish a king. In the fresh Queen Of Spades loss, game **797390**, Cutlery ended with one length-5 dragon against an opponent's longest 29 and total 105. In Schooltime **797425**, it ended with one length-13 dragon against 36. These are cases to inspect for earlier resource loss and excessive reduction of support, not proof that all its sacrifices were mistakes. See [battle 797389](https://game.battlecode.au/visualiser?match=797389) and [battle 797424](https://game.battlecode.au/visualiser?match=797424).

**What to borrow:** judge the late policy by retained scoring length and safe completion, with a deliberately chosen reserve. Study how useful workers become donors without turning every remaining dragon into a donor.

**What not to copy blindly:** a target of two survivors. It is an observed outcome under particular opponents and maps, not a universally optimal population setting.

**Counter-hypothesis to test:** pressure the collection area while cheap attackers remain, or force a king to spend length escaping. The high concentration suggests this vulnerability, but the replays do not establish a winning counter-policy.

## 3. forgot to mention: heavy worker turnover and strong conversion, with context-dependent holes

The fresh 22/25 record is strong, but its schedule was easier than the earlier 27/50 cohort. Do not interpret the difference as measured improvement from a new upload.

**Observed plan:** rapid expansion and repeated empty-turn/default-suicide deaths, followed by much greater concentration. In the fresh 13 round-limit games, median final longest length was **48**, with **10 dragons and total length 118**. The earlier 24 round-limit games had medians **37.5**, **8.5 dragons**, and **72 total**. Opponent and map mix differ.

The earlier Slithery sample is particularly informative: **five wins in six games**, with median final longest length **70**. Workers turned over in large numbers, yet the policy repeatedly produced large scoring dragons. Empty-turn death counts alone cannot prove intent—default suicide also occurs after missing output—but repeated corpse collection supports a recycling interpretation.

**A valuable preservation sequence:** in Slithery game **707324**, a length-71 dragon split at round 489 into a **length-2 parent and length-69 child**. The parent died the next round; the child finished at 70 and won against a longest 60. Reconstruction showed the original head had no immediately empty movement destination at the split. This is a concrete rescue, not ordinary population growth. See [battle 707323](https://game.battlecode.au/visualiser?match=707323).

**A distinct failure:** in Trauma **712379**, its final king was length 24 at round 400 and ate 11 own-corpse pearls afterward. Five length went into successful extra movement steps; three ordinary splits spent another six. It finished at 24 and lost to 40. The donor pipeline was functioning, but the king retained none of its net income. See [battle 712378](https://game.battlecode.au/visualiser?match=712378).

The earlier cohort also went **7/7 on Devil, 1/7 on Portals and 0/3 on Trophy**. In the fresh cohort, those records became **0/1, 3/3 and 3/3**. This is exactly why weak-map labels must stay attached to a date, version uncertainty and opponent sample.

**What to borrow:** separate reproduction, recycling, collecting and preserving. Track a king across child IDs. Account explicitly for reproduction and movement expenditure after committing to a scoring dragon.

**Counter-hypothesis:** interrupt the donor-to-collector path rather than merely killing random workers. Making a large collector split or sprint repeatedly can neutralize incoming food. That hypothesis needs paired tests against accessible proxy policies.

## 4. 3.14159265: substantial turnover without abandoning support

**Observed distinction:** it can generate a strong king while retaining a useful supporting population. Its current sample includes both elimination wins on compact maps and large late collectors. Trophy was **4/4**, but against this sample's opponents; it is a promising opening reference rather than proof of universal superiority.

In Slithery game **797661**, it won **71 versus 34 longest**, despite having **177 versus 296 total length** and **23 versus 54 surviving dragons**. Its final king already existed at round 400: **45 → 55 at round 450 → 71 at the finish**. All **26 late pearls** eaten by that king came from its own corpses. See [battle 797659](https://game.battlecode.au/visualiser?match=797659).

The same game recorded **826 wall deaths** on its side. That number is not a valid standalone navigation-quality metric. However, it would be equally wrong to call all 826 deliberate feeding: of the king's 26 late own-corpse pearls, **23 came from self-collision corpses, one from a wall-death corpse, and two from other-body collision corpses**. The replay proves food flow; it does not explain every death's intention.

**Limits:** it lost Portals **797435**, longest **47 versus 52**, and Trauma **796956**, **23 versus 61**. In Default **796954**, Cache me outside eliminated it while retaining 64 dragons. A good scoring mechanism does not remove opening and resource-control failure modes. See [battle 797434](https://game.battlecode.au/visualiser?match=797434) and [battle 796954](https://game.battlecode.au/visualiser?match=796954).

**What to borrow:** grade workers by productive service and resource transfer, and grade kings by preservation and scoring. A single survival penalty for every dragon can discourage the behavior that made this game successful.

**Counter-hypothesis:** exploit the period before a protected collector becomes dominant, or force the collector to abandon a productive area. The Default elimination is evidence that this route can exist, not a complete counter-strategy.

## 5. SSS: a strong example of changing from swarm pressure to concentrated growth

SSS's earlier and current samples both show that economy and endgame growth can coexist. Its current sample went **19/25**, including **4/5 on Trophy**; the earlier sample was **30/50** and only **1/5 on Trophy**. The old description of SSS as categorically weak on Trophy is too strong without fresh, version-matched evidence.

The fresh sample contains **13 elimination wins** and a median final longest of **42** in its nine round-limit games. In current Slithery game **797412**, it beat forgot to mention **80 versus 62 longest while both teams had total length 237**. It retained 39 dragons to the opponent's 30, so concentrating effectively does not require reducing every map to a tiny population. See [battle 797409](https://game.battlecode.au/visualiser?match=797409).

**A clear conversion example:** in Slithery **687878**, SSS and cheji bt were both near the population cap around round 200. By round 400, SSS's eventual king was already **54**, reaching **93** at the finish. It ate **39 late pearls: 35 from its own corpses and four natural spawns**. SSS won **93 versus 19 longest** while holding only **172 versus 343 total length**. See [battle 687878](https://game.battlecode.au/visualiser?match=687878).

**An elimination example:** in Schooltime **709263**, SSS was slightly behind Stockfish in population at round 100, **14 versus 16**. By round 200 it led **40 versus 22**, and it eliminated Stockfish at round 427. This is a midgame resource/population divergence, not simply an opening script or a late feeding win. See [battle 709262](https://game.battlecode.au/visualiser?match=709262).

**A preservation failure:** in the same battle's Trauma game **709266**, SSS lost a length-36 dragon to Stockfish's length-3 dragon in round 499. Its remaining longest was four. Stockfish's own king was already longer, so this trade did not necessarily change the winner; it demonstrates that even a sophisticated collector can be cheaply removed.

**What to borrow:** preserve expansion while the economy is useful, then build a strong collector without assuming founder identity equals king identity. Include the last few turns in tactical protection.

**Counter-hypothesis:** cheap attacks on exposed kings have a much larger payoff than symmetric worker attrition. Use turn order and feasible local attacks, not an indiscriminate aggression bonus.

## 6. cheji bt: the strongest warning against mixing behavioral versions

This team was first in the morning snapshot and fifth in the late snapshot. The morning 50-game record was 25/50; the fresh record is 15/25 against the strongest median opponent schedule among the current five.

A sharp **observed behavioral boundary** occurred in the earlier cohort:

| Battle period, UTC | Games | Sonar pings | Round-limit wins / games | Median final longest in round-limit games |
|---|---:|---:|---:|---:|
| 04:27–07:24, 30 September | 20 | 474,708 | 7/9 | 40 |
| 08:26–13:12, 30 September | 30 | 0 | 1/12 | 20.5 |
| Fresh 02:20–02:23, 1 October | 25 | 495,816 | 6/10 | 44 |

Every one of the six sampled battles in the 08:26–13:12 period was sonar-free, across multiple maps. **This strongly suggests a changed behavior/configuration, but public data does not identify the uploaded version or prove sonar removal caused the results.** Opponent and map mixes also changed. In particular, the three Schooltime wins from the earlier 50-game cohort belong to the 04:27–07:24 period.

**The current sample has sonar back in all 25 games and much stronger concentration than the sonar-free morning cohort:** median 2.5 survivors and longest 44 in its ten round-limit games. Therefore “cheji bt is a sonar-free swarm bot” would be an incorrect current description. On fresh Portals game **797557**, it won **51 versus 50 longest despite total 53 versus 64**—one retained length mattered more than the opponent's larger total. See [battle 797554](https://game.battlecode.au/visualiser?match=797554). Different schedules and missing submission IDs prevent attributing the improvement to a particular change.

In that later morning cohort, cheji bt was formidable at producing population on some maps. Trophy **709253** reached **46 dragons versus two at round 100** and eliminated calc at round 104. See [battle 709252](https://game.battlecode.au/visualiser?match=709252).

Its Slithery failure was almost the opposite. Across six earlier sampled Slithery games it won none, with final totals **325, 322, 403, 409, 343 and 389**, but longest lengths only **16, 22, 26, 22, 19 and 22**. The opponents' smaller economies repeatedly produced the longer scoring dragon. In game **709255**, cheji bt still had 61 dragons and total 325 at the finish, but lost 16 versus 36 longest.

It also made many large rear-child splits. More reversals therefore do not automatically mean better endgame play: preserving numerous medium dragons is different from producing one sufficiently long, safe king.

**What to borrow:** inspect its effective population expansion and route allocation on specific compact maps. Preserve version/cohort separation when measuring the result.

**What not to infer:** that sonar is unnecessary, that its Schooltime success describes the sonar-free period, or that the highest-rated team's latest observed policy is a complete template for us. The fresh 25-game sample contains **no Slithery Fight**, so it cannot establish whether that particular earlier failure has been fixed.

## 7. Two earlier leaders still provide valuable examples

### Stockfish: clean conversion on Portals

Stockfish is sixth in the late snapshot. Its earlier 50-game sample went **32/50**, including **7/7 on Portals**. The 25 round-limit games had median final longest **50**.

In Portals **708587**, its king grew **39 → 53 → 62** from round 400 through 450 to the finish. It ate exactly **23 own-corpse pearls**, with no late split expenditure or extra-step expenditure by that king. Of those pearls, 22 came from self-collision corpses and one from a wall-death corpse. It won against longest 54 despite having **67 versus 82 total length**. See [battle 708585](https://game.battlecode.au/visualiser?match=708585).

This is the most useful clean illustration of the retention objective. It does not reveal how the king chose its route or how teammates coordinated.

### Cache me outside: economy can beat a feeder before the endgame

Cache me outside is tenth in the late snapshot. Its earlier sample went **27/50**, with **5/5 Default and 5/5 Trauma**, but only **1/8 Autarky** and **2/6 Slithery**.

In Default **709213**, it led forgot to mention **23 versus eight dragons at round 100** and eliminated it at round 299, with 63 dragons remaining. In Trauma **712379**, it led **58 versus eight dragons at round 400**, winning longest **40 versus 24**. See [battle 709211](https://game.battlecode.au/visualiser?match=709211) and [battle 712378](https://game.battlecode.au/visualiser?match=712378).

These cases support two separate priorities for our bot: get a usable economy first; convert it efficiently when the game will reach the deadline. A universal “feed earlier” intervention cannot fix both.

## 8. What this changes in our development plan

**First, make existing information useful.** Our new PD diagnostics locate a concrete gap: fast-spawn food access, absent hub knowledge in some founders, and crowding/overriding elsewhere. Selective sharing and marginal patch value are better next hypotheses than another generic increase in attraction strength.

**Second, make cash-in a coherent role.** A collector should not simultaneously receive food, replenish the whole swarm and spend away its advantage. Measure net growth along its lineage and maintain a justified reserve. A role controller can separate harvest, expand, rendezvous, collect and preserve, with the move ranker operating inside that intent.

**Third, upgrade the evaluator through our own outcomes.** Opponent imitation already improved prediction accuracy while hurting wins. The larger research bet should be a small contextual model taught by counterfactual continuations of our own games, with a feasibility pilot and real-game promotion gate. The scholarly basis and implementation constraints are in priority 3 of [WORK_QUEUE.md](WORK_QUEUE.md).

**Fourth, search selectively for preservation and high-value trades.** The game permits a king to move its head to its old tail by creating a large rear child; that child acts in the same round and starts with fresh program state. A handoff can save a trapped king, but also spends two length on the remaining parent. Our bot already has an emergency split fallback. The experiment is earlier, exact evaluation plus role succession—not merely adding a split command. See the official [splitting rules](https://game.battlecode.au/docs/splitting).

**Finally, stop treating whole-team imitation or more CMA generations as the main route.** The data support targeted architecture and objective improvements. Our latest local results have already rejected broad retuning, a stronger feeding pull, and straightforward opponent-ranker imitation. Those failures belong in the work queue so we do not repeat them under new names.

## 9. Interpretation rules and measurement limits

The game ends on elimination or, after 500 rounds, compares **longest living dragon first, total length second**. This is why the mass-versus-longest examples are strategically meaningful. See [official scoring](https://game.battlecode.au/docs/structure).

- **Feeding:** direct corpse-origin tracing is stronger evidence than a nearby suicide count. It proves which food was eaten, not the donor's intention.
- **King identity:** a final king born in round 489 may inherit 69 length immediately. “Its length at round 400 was zero” does not mean king construction began at round 489. Direct final-ID food counts omit inherited history.
- **Deaths:** default suicide, collision and invalid-action deaths must not all be interpreted as crashes or as planned sacrifice. The engine defaults to suicide when no action is supplied; illegal splits and unaffordable extra moves can also kill. See [execution order](https://game.battlecode.au/docs/execution-order).
- **Sonar:** observed pings are real, but public zero-valued payloads are redacted. We cannot derive election, encryption, map-sharing or warning protocols from them.
- **Search:** public CPU fields do not establish search depth or cost. No claim here attributes neural learning, minimax or Monte Carlo search to a named team.
- **Samples:** battles share map and opponent conditions; players can upload between observations. Side balance is imperfect: in the fresh cohort Cutlery/forgot/SSS played A in 20/25 games, 3.14159265 in 15/25, and cheji in 25/25. Do not read pooled wins as a controlled league.
- **Offline learning:** full replay states may label outcomes, but hidden information unavailable during play must not become an input feature. Public sonar and spawn-timer omissions also prevent exact reconstruction of every private decision context.

The practical lesson is not to minimize every failure counter. It is to distinguish **unproductive travel, useful turnover, wasted sacrifice, poor concentration and loss of a valuable collector**, and run separate experiments against the failure that actually occurs.

## Appendix: reproducible battle selection

Each battle contains five games. The viewer links above identify the case; choose the named map/game within the battle. Raw public replay downloads use `https://game.battlecode.au/api/matches/GAME_ID/replay`.

Fresh cohort, cutoff approximately 02:29 UTC on 1 October:

| Team | Battle IDs |
|---|---|
| Cutlery | 797334, 797389, 797424, 797339, 797344 |
| forgot to mention | 797404, 797399, 797419, 797429, 797414 |
| 3.14159265 | 797659, 797434, 796954, 795279, 794069 |
| SSS | 797684, 797409, 797099, 795509, 793859 |
| cheji bt | 797554, 797379, 797469, 797324, 797294 |

Earlier cohort, cutoff approximately 13:32 UTC on 30 September:

| Team | Battle IDs |
|---|---|
| cheji bt | 709252, 704212, 698745, 692932, 687878, 682378, 677416, 671939, 666775, 661707 |
| forgot to mention | 712378, 709267, 709211, 708580, 707323, 704217, 706432, 706382, 706233, 704081 |
| Stockfish | 712383, 709262, 708585, 707612, 707328, 706442, 704222, 706253, 704172, 704056 |
| Cache me outside | 712378, 712383, 711128, 709272, 709211, 708580, 708585, 708212, 707921, 707617 |
| SSS | 709262, 704227, 698765, 692947, 687878, 682393, 677426, 671964, 666780, 661722 |

Analysis used the repository's replay decoder, event statistics, and corpse-provenance reconstruction, plus targeted split-lineage and length-expenditure checks. Ranked flags were filtered explicitly; unranked challenges were excluded. Timeline summaries use round-limit games unless a specific elimination example is identified.

The combined analysis contains **375 team-game observations across 340 unique games**: 215 earlier and 125 fresh. No identical file or selected-action/event fingerprints repeated across those 340 games. Every decoded winner agreed with the public metadata, and the separate corpse-tracing reconstruction agreed with the statistics routine on every team's final longest length. No unknown consumed-pearl origins or flagged provenance inconsistencies were recorded. These checks support the reported event measurements; they do not remove sampling bias or reveal hidden bot state.
