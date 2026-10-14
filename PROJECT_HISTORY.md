# Team 777: development and experimental history

> **Publication extension, 14 October 2026:** the original archive below retains its 3 October cutoff and hashes. Read [chapter 7](docs/project-history/07_V12_AND_CLOSEOUT.md) for C9–D22, v12s/v12x/v12z, corrected diagnostics and the October 12 close-out. [PROJECT_WRITEUP.md](PROJECT_WRITEUP.md) supplies the completed narrative; [PUBLICATION.md](PUBLICATION.md) explains the source and data archive. Statements such as “latest candidate” below describe the original snapshot.

**First archival edition — 3 October 2026.** This writeup reconstructs the project from its earliest retained setup on **22 September** through **C8 on 3 October, 21:30 EDT**. The repository cutoff is `69095e569c8717f2eeeb99863f10fd19d56075ab`. It covers what was built, what was proposed, what was tested, what happened, and where the interpretation subsequently changed.

This is a history of the available evidence, not a claim that every conversation or abandoned local command has survived. No new strength tests, training, uploads, or strategy changes were performed to produce it. Results are attributed to their original conditions; selected gaps in the written logs were filled from saved run artifacts. Website figures are **historical snapshots**, not a fresh leaderboard check.

## Reading order

| Part | Contents |
|---|---|
| [1. Foundations and v1–v3](docs/project-history/01_FOUNDATIONS_V1_V3.md) | Initial bot; reliable evaluation and datasets; reproduction; endgame; movement, portal and memory failures; first linear and neural rankers |
| [2. v4–v6: coordination and the search core](docs/project-history/02_V4_V6.md) | Teammate safety; growers; feeding and sonar; hotspot experiments; unified search; the judge-clock correction; floor fix and v6.1 |
| [3. C++ and CMA-ES, v7–v10h](docs/project-history/03_CPP_CMA_V7_V10H.md) | Port parity; runtime; deeper-search tests; seed correction; feature ablation; optimizer changes; v9/v10; map books; unsuccessful retuning and feeding changes |
| [4. Learning, scouting and the rules transition](docs/project-history/04_LEARNING_RESEARCH_RESET.md) | R4 imitation; sonar age; R5 teacher and residual model; Sprint map retraction; top-team research; scholarly proposals; transition to queen scoring |
| [5. Queen era: v11ms, v11q and v11t](docs/project-history/05_QUEEN_ERA.md) | Q0–Q11, current engine/maps, C1–C8, live replay findings and the latest accepted/rejected candidates |
| [6. Infrastructure, evidence corrections and remaining archival work](docs/project-history/06_EVIDENCE_AND_GAPS.md) | Tooling built; validity failures and repairs; evidence conventions; archival coverage; unresolved discrepancies and continuation checklist |

The narrative is accompanied by an evidence archive:

- [Run register](docs/project-history/RUN_REGISTER.md): **314** top-level result directories, including **186 dated runs**, with links to retained report metadata. Support snapshots and diagnostics are identified separately from dated experiments.
- [Original run reports](docs/project-history/ORIGINAL_RUN_REPORTS.md): preserved report text, including negative and superseded results. Its generated labels are historical, not editorially corrected.
- [Source-document index](docs/project-history/SOURCE_INDEX.md): every captured root writeup, plan and handoff.
- [CMA-ES register](docs/project-history/TUNING_REGISTER.md): training-run plans and logged evaluations, including incomplete starts.
- [Commit history](docs/project-history/COMMIT_HISTORY.tsv): **151** reachable commits, with both author and committer dates.
- [Evidence manifest](docs/project-history/EVIDENCE_MANIFEST.json): SHA-256 hashes for **757** preserved files, including **49 root Markdown documents**, selected result metadata, experiment configurations, the current-map manifest and frozen v11t parameters.
- [Release ZIP hashes](docs/project-history/RELEASE_PACKAGE_HASHES.json): identities of the **14** release/experimental packages present at capture.

The archive deliberately does not duplicate the large raw replay corpus, compiled caches, engine packages, or third-party bot sources. Those remain in the workspace. File preservation is broader than manual verification: the writeup does **not** claim that all archived rows or replays were independently re-audited in this session.

## What the project has accomplished

The starting bot used local BFS food collection, simple space and enemy-head checks, and no useful reproduction policy of its own. The first major gain came from **reproduction**, followed by a **late split cutoff**, then **splitting at length four**. The first successful learned component was a **small linear action ranker**, not a large neural network.

The next phase explored coordination and strategic roles. Many plausible additions failed: arbitrary growers, broad safety filters, emergency portals, remembered-food routing, early kings, and simple hub pulls. A unified movement search eventually made a stronger base, but its apparent performance initially depended on a misleading local wall clock. Dividing the actual work budget fairly across moves and fixing a split-floor rule produced the defensible Python v6 release.

The C++ port established action parity on hundreds of thousands of turns and cut measured judge cost from roughly 80 million points to roughly 7 million. That was a major engineering success. It did **not** make every larger search stronger. Early tuned-v7 gains disappeared after the engine gained meaningful per-game randomness. Later CMA-ES work, with a better objective, broader maps, adaptive learning rates and distribution-mean evaluation, produced the validated v9 improvement.

The v10 family added successful pieces incrementally: king beacons with larger feeders, known-map geometry, an earlier large-map feeding schedule, and eventually age-gated hub communication. Numerous follow-up tuning and feeding experiments did not confirm. Better imitation of a stronger opponent also failed to improve the playing bot. The R5 counterfactual learner passed important plumbing checks but **lost games** and was stopped.

The October rules change created a new problem: the original queen mattered before ordinary longest-dragon scoring, and length granted additional free movement. The team first preserved its successful worker economy, then added selective pearl collection with free steps, light queen behavior and tactical escape search. The most recent useful change was **correcting the queen search model**, rather than increasing a generic safety weight.

At the cutoff, **v11t is the latest frozen recommended candidate**. The archive does not establish that it was uploaded. v11u exists as a refuge candidate but failed confirmation; C8's minimum-exit split restriction also lost. A version directory is not proof of promotion or deployment.

## Release and strategy lineage

These rows describe accepted or notable artifacts. They are not a single comparable ranking of all versions.

| Artifact | Main change | Evidence/status at the time |
|---|---|---|
| v1 | Greedy local movement baseline | Initial comparator; weak against splitter |
| Round-450 experimental baseline | Split at eight, stop at 450 | Passed the early local endgame gates |
| v2 | Split at four, retain round-450 growth phase | Strong confirmation against the early scripted pool and procedural transfer |
| v3 | Learned 24-feature linear move ranker | Passed official-map and generated-layout gates; selected over the tested MLP |
| Additive v4 ZIP | v3 plus local feeding and sonar routing | Practical trial over live v2; **not** established superior to v3 |
| v5 experiments | Scouts, hotspots, kings and strategic wrappers | No generally validated v5 release in the retained record |
| v6 | Fair-budget unified search plus corrected split floor | Full-suite strength evidence and 22-game judge CPU suite |
| v6.1 working base | Portal/hub books, aggression and exploration | Improved some local matchups; basis of the C++ port |
| Tuned v7 | First CMA candidate | Frozen initially; preferred status reversed by the multi-seed recheck |
| v7-base | Untuned C++ v6.1 | Recommended after the engine/seed correction |
| v8 working family | Portal-age, topology and targeting experiments | Intermediate feature/tuning family, not a frozen release directory |
| v9 | Selected CMA distribution mean plus retained v8 behavior | 153 versus 124 wins in the held-out paired comparison |
| v10 | King beacon plus larger-dragon feeding | Positive screen and held-out comparison |
| v10g | Known-map open-edge completion | Strong replicated map-book improvement; intermediate candidate |
| v10h | v10g plus large-map feeding shift | Frozen and later recorded uploaded; broad retunes failed to replace it |
| v10o | Adopt shared hubs only after 30 hub-less rounds alive | Confirmation improvement across original and perturbed layouts |
| R4/R5 | Alternative learned move scores | Both rejected in games; preserved for research |
| v11ms | Use additional free steps to collect a visible pearl | Confirmed under queen-era rules |
| v11q | Light queen plus initial queen tactics | Neutral broad old-policy panel, much better queen survival and direct matchups; recorded uploaded |
| v11t | Corrected queen transition and threat search | Repeated positive local results, 75/136 direct versus v11q; latest recommendation |
| v11u | Temporary refuge on v11t | Promising screen; confirmation inconclusive and direct matchup 67/136; not promoted |

The names `v11` and `v12` in September tuning logs designate optimizer campaigns. They should not be confused with the October queen-era release names. Similarly, lettered `results/v11*-bot` directories are often experiment bases with unchanged playing behavior plus inactive switches.

## The boundaries between evidence eras

| Era | What changed | Consequence for interpretation |
|---|---|---|
| unswbc 0.3.10, September 22–26 | Early engine and local bot RNG seeds | Repeating a seed number did not necessarily vary the board or deterministic opponents. Large action counts are verification, not independent strength samples. |
| Python v6 clock correction, September 25 | Judge-calibrated work accounting replaced misleading host-time comparisons | Early v6 strength screens overstated executable judge behavior. Use the fair-search/floor-fix evidence for the release claim. |
| unswbc 1.1.0, September 26 onward | Per-match seed drives pearl spawns | Tuned-v7's single-layout advantage failed replication. Old-engine win rates are not interchangeable with new ones. |
| Hidden-spawn Sprint extracts, October 1 | Replay maps had no spawn definitions | Initial unseen-map and R5 Sprint conclusions were invalid; later reconstructed maps supplied a provisional replacement. |
| Queen rules / 1.2.3, October 1–2 | Original queens score first; extra free moves depend on starting length | Old longest-dragon objectives and opponent behavior became incomplete guides. Ratings reset. |
| 1.2.9 and official current maps, October 3 | Actual current map files replaced stale/reconstructed validation inputs | C-series results use the newer laboratory; Q-series results remain historical evidence. |

No cumulative win rate is calculated across these eras. It would mix different games, map distributions, opponents, selected candidates, repeated controls and overlapping live cohorts.

## What the accumulated experiments support

1. **Preserve the small-dragon economy unless a replacement wins.** Early reproduction gains were large. Later broad split brakes, premature king growth and larger-worker schedules repeatedly hurt. This does not prove every dragon should always split; it defines the burden of proof for exceptions.
2. **Correct inputs and transitions before tuning their weights.** Map identity, missing spawners, host/judge clocks, food-dependent tail occupancy and threat timing all materially affected what was being measured or chosen.
3. **A lower death count is not automatically better play.** Sacrifices, trades and newborn turnover can fund growth or territory. Queen deaths are particularly costly under the new rules, but policies that preserve queens at the expense of the entire worker economy also failed.
4. **Learning helped once and failed in later forms.** v3's linear ranker is a genuine successful learned component. The small MLP was feasible but not selected. R4's better imitation and R5's offline label gains did not translate to better games.
5. **Local improvements can be opponent-specific.** Several retunes mainly exploited already-easy opponents. Multiple nicked versions are useful tests but not independent strategic families; the queen-aware specialists also share our own lineage.
6. **A mechanism diagnosis is a hypothesis generator.** The association between queen splits and imminent wall deaths was striking. C8 nevertheless showed that the tested split restrictions made both wins and queen survival worse. Correlation located a difficult decision; it did not establish the correct intervention.
7. **Top 100 remains an objective, not an achieved milestone in this archive.** The retained snapshots got as close as rank 108, but neither that point nor a local candidate gain proves sustained top-100 strength.

## Status at this edition's cutoff

The most recent completed sequence is C5 confirmation and v11t freeze, followed by C6/C7 refuge testing and C8 split-exit testing. The latest 95-game live review belongs to an **earlier same-day cohort**, associated with recorded v11q deployment; it is not a v11t post-upload evaluation.

This archival review also identified a reporting defect: the C-series **“current pool” column includes only five of the intended 17 maps**, owing to case-sensitive/renamed map identifiers. The separate overall 17-map totals remain available. [Part 6](docs/project-history/06_EVIDENCE_AND_GAPS.md) records the evidence and the reporting correction needed; no experiment code was changed.

Two continuing strategic problems have evidence: queen confinement/traffic and worker-economy collapse. Their relative importance varies by cohort and map. The history supports targeted, current-engine experiments on both; it does not support another undifferentiated global safety change or an automatic restart of R5.

This edition provides the full chronological backbone and a source-preserving register. Remaining archival work is explicitly listed in [Part 6](docs/project-history/06_EVIDENCE_AND_GAPS.md): resolve unlogged runs, reconcile original game counts, verify deployment boundaries, and audit the few remaining reporting ambiguities. Existing logs and bot files have been left intact.
