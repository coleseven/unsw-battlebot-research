# 1. Foundations and v1â€“v3: September 22â€“24

[Project history](../../PROJECT_HISTORY.md) Â· [Next: v4â€“v6](02_V4_V6.md)

## Starting point and first measurements

The earliest retained commit is `f876927`, September 22 at 14:47 EDT: starter Python bot and maps from unswbc 0.3.10. The inspected bot used local BFS to food, static flood-fill space estimates and a neighboring enemy-head penalty. It saw a 7Ã—7 window, did not deliberately route through portals, and lacked the later persistent world model and strategic coordination.

The first saved arena report, `20260922-150650-mybot`, recorded a score of **81/180** against greedy, hunter, splitter, turtle and wanderer. Against splitter it scored **4/36**. The six-bot 540-game tournament ranked splitter above the other scripts. These initial reports predate evaluation fixes and should be read as early diagnostic output, not a robust Elo estimate. The tournament's local Elo is not website Elo.

After evaluation repairs, the 15:55 smoke test recorded **2â€“16 against splitter** and **9â€“9 against frozen v1**. The 16:07 integration check recorded 0â€“8 against splitter, 8â€“0 against the official starter, and 4â€“4 against v1 on its small map subset. The consistent useful finding was that reproduction was missing from the original baseline.

Sources: [initial evaluation](snapshot-2026-10-03/results/20260922-150650-mybot/summary.md), [tournament](snapshot-2026-10-03/results/20260922-153401-tournament/summary.md), [evaluation task](snapshot-2026-10-03/CLAUDE_EVALUATION_TASK.md), [initial research plan](snapshot-2026-10-03/RESEARCH_EXPERIMENT_PLAN.md).

## Building a laboratory before changing strategy

The setup added an arena, frozen bot snapshots, scripted opponents, replay decoding, observation reconstruction, map identity, source hashing and result summaries. The evaluation repair task required frozen versions to stay outside synchronization, errors to be reported rather than counted as draws, side-paired uncertainty estimates, dependency-complete hashes, and final lengths measured after the last action.

The original research plan proposed classical planning, persistent memory, population experiments, tactical search, evolutionary tuning, a narrow neural evaluator and a conditional reinforcement-learning branch. Those were research directions, not already implemented features. The first controlled gameplay work deliberately tested population before spending resources on a network.

Dataset V2 separately repaired training provenance. It preserved full variable-length MOVE sequences instead of reducing a sprint to its first direction and length; exact IDs, portal identities, turn order, coordinates, countdowns and sonar sequences; source/replay fingerprints; and frozen battle-grouped partitions. It supplied streaming batches rather than requiring the full corpus in RAM. Outcome labels and submission metadata were explicitly excluded from legal inference inputs. This was enabling work, not evidence of a stronger playing policy.

Source: [Dataset V2](snapshot-2026-10-03/DATASET_V2.md). The current archive preserves its specification; it does not assert that the entire available corpus was converted.

## Population and endgame: the first successful changes

| Experiment | Design and result | Decision |
|---|---|---|
| Population cap, September 22 | No splitting versus live caps 2/4/8/64, split at length eight. Corrected screen: 240 games. Selected cap 64; reserved-map comparison: **78.3% versus 34.2%**, 120 games per policy; paired gain **44.2 percentage points**, map-cluster interval +35.0 to +52.5. | Reproduction established as valuable. Cap 64 reproduced the existing splitter; it did not beat that same behavior in a mirror or prove an optimal cap. |
| Late split cutoff | Perpetual splitting versus cutoffs 200/300/400/450. Stop450 selected at 87.5% screen score. Validation: **90.0% versus 79.2%**, gain **10.83 points** [+4.17,+16.67]; **33â€“7 versus splitter**. | Passed both predeclared local gates. Frozen round-450 experimental baseline became the next control. |
| Split size/threshold | Screen: threshold four **28â€“8**, six 26â€“10, ten 11â€“25, twelve 8â€“28; length-eight/child-two 21â€“15 against baseline. | Threshold four advanced unchanged. |
| Fission confirmation | Candidate **386â€“46** across pool versus baseline **317â€“115**; direct baseline **117â€“27**. Paired gain **15.97 points** [+6.71,+24.54]. | Frozen as **v2**, hash `9f29ab4138b51d26`. |
| Fission transfer | Eight new connected symmetric layouts, no portals; **124â€“4** against the old round-450 baseline. | Passed the declared procedural-family transfer gate; not proof against ladder teams. |

The population experiment initially ran 576 scheduled games. A map-signature defect treated explicit open edges as identity-bearing miscellaneous fields, duplicating maps across stages. The corrected report excluded **96** games on map identity alone, leaving 240 screen and 240 validation games;  the selected policy stayed the same. Original artifacts were retained. Use the run's **map-audit** result, not the original summary.

The endgame change reduced round-limit losses from 19 to six while elimination losses stayed six. Fission confirmation reduced elimination losses from 43 to zero, but its 46 remaining losses were round-limit length losses. Queen of Spades regressed despite the large aggregate improvement.

Fission verification reproduced **4, 150, 627 candidate actions** in official validation and **722, 699** on new maps. The full-game judge check peaked at **31.25M CPU points**, with about 20.56 MiB memory; 75 regression tests passed at that stage. These counts establish execution fidelity on those observations, not millions of independent strength samples.

Sources: [population](snapshot-2026-10-03/POPULATION_EXPERIMENT.md), [endgame](snapshot-2026-10-03/ENDGAME_EXPERIMENT.md), [fission](snapshot-2026-10-03/FISSION_EXPERIMENT.md).

## Movement safety: plausible gains that did not generalize

The first loss audit found 297 own-turn deaths in 12 baseline losses. Every dying position had no admissible ordinary move under the conservative helper, which excluded portals. That suggested anticipating confinement, but did not prove every position lacked a legal escape.

| Trial | Measured outcome | Disposition |
|---|---|---|
| Three-step trap avoidance | Validation 79.2% versus 74.2%; gain +5.00 points, adjusted 97.5% interval **âˆ’2.50 to +15.83**; direct 23â€“17. | Failed gate. All six net extra wins came from Arena. |
| Emergency two-step sprint | Validation 73.3% versus 74.2%; âˆ’0.83 points [âˆ’2.50, 0.00]; direct 21â€“19. | Failed gate. It emitted 1, 885 sprints; none died during execution, so legal execution was not sufficient for strategic value. |
| Unchanged trap on related layouts | Arena 19â€“5; Schooltime 17â€“7; baffles 16â€“8; **pockets 6â€“18**; slow food 12â€“12. | Original Arena signal repeated, but severe pocket failure ruled out global promotion. |
| Guarded trap variants | Screen selected moving-tail guard at 24â€“12; head/food guards each 47.2%. Confirmation **75â€“69** direct; pooled +0.69 points [âˆ’3.01,+4.40]. | Not promoted. Pocket stress improved to 8â€“8, but broad benefit remained unproven. |

The guarded model checked collision before tail release and retained the tail when food caused growth. It fell back to static occupancy for incomplete bodies. This early work already recognized a transition issue that returned in the queen-era search review.

Movement validation audited 360 replays; guarded validation/stress audited 912 and reproduced 2, 318, 083 candidate actions. Guarded movement's full Arena sandbox game peaked at 48.71M points. No successful promotion followed from these runtime passes.

Sources: [movement experiments](snapshot-2026-10-03/MOVEMENT_EXPERIMENTS.md), [trap follow-up](snapshot-2026-10-03/TRAP_FOLLOWUP.md), [guarded movement](snapshot-2026-10-03/GUARDED_MOVEMENT.md).

## Growers and birth survival

On v2, fixed earlier cutoffs and hashed quarter-population grower roles were tested. `quarter350` won the screen **21â€“15**, but confirmation was **74â€“70 versus v2**, with a 40.97â€“60.42% map-cluster interval. Across the pool it won **347/432 versus 343/432**, only +0.93 points [âˆ’2.78,+4.17]. It was rejected. A full judge game and millions of replayed actions verified the implementation; they did not rescue the failed strength gate.

A descriptive newborn audit examined 144 frozen-v2 mirror games: **28, 044 births**, 159 deaths before the child's first turn, and 1, 243 deaths during the first turn among 27, 885 children that received one (**4.46%**). Later-age counts were censored by match end. The audit explicitly did not infer that suppressing those births would win games. Some children could trade, collect or reproduce before dying.

Sources: [grower experiment](snapshot-2026-10-03/GROWER_EXPERIMENT.md), [split survival](snapshot-2026-10-03/SPLIT_SURVIVAL.md).

## Portals and persistent navigation

| Trial | Measured outcome | Interpretation |
|---|---|---|
| Last-resort portal wrapper over v2 | **131â€“109**, 54.58%; five-map interval 49.58â€“59.58%. 1, 222 fallback redirects, 889 survived their immediate turn; chosen exits were unseen. | Encouraging but failed promotion gate. |
| Unchanged portal replication | 1, 728 official-pool games plus 256 procedural games. Official portal direct score **53.13%**, interval 46.88â€“59.38%; pooled gain +0.87 points [âˆ’0.35,+2.37]. | Official criteria failed. |
| Portal procedural transfer | **172W/1D/83L**, 67.38%; family interval 63.48â€“70.70%. All 384 paired non-portal control games identical. | Genuine transfer result on that synthetic family, insufficient to override the official failures. |
| Persistent terrain memory | Screen **39W/1D/32L**. | Lost selection narrowly to portal-enabled memory; not independently confirmed. |
| Persistent terrain plus known portal routing | Screen **40â€“32**. Confirmation **70W/2D/72L versus v2**; pooled score gain exactly zero. | Failed; conditional new-layout batch not run. |

Portal fallback activated about **13 times more often** on generated layouts than official maps. That difference helps explain why a synthetic success could be irrelevant to the main distribution, without proving geometry alone caused the performance gap.

The navigation wrapper used per-dragon static terrain memory, eight-round food expiry and a bounded 96-node search; newborns inherited no memory. It usually overrode exploration rather than an existing local food route. In confirmation, Default improved from 36â€“12 to 48â€“0 across the pool, but Queen of Spades regressed from 33â€“15 to 18W/1D/29L. Elimination losses rose from eight to 17. The new ability existed, but was not a robust replacement.

A preflight-only navigation snapshot contained an off-window index bug and was superseded before strength games. The corrected build passed full games and history-restoring probes, with a peak of 85.00M points. Across screen/validation, 1, 080 replays and 5, 185, 642 candidate decisions were audited.

Sources: [portal initial](snapshot-2026-10-03/PORTAL_EXPERIMENT.md), [portal replication](snapshot-2026-10-03/PORTAL_FOLLOWUP.md), [navigation](snapshot-2026-10-03/NAVIGATION_EXPERIMENT.md).

## Learning experiment: the successful v3 linear ranker

The hybrid study separated reproduction roles from move evaluation. The movement candidates shared the same conservative visible-empty ordinary-move set and the same 24 features. It compared a fixed heuristic, a learned linear scorer and a 16-hidden-unit tanh MLP. It did not learn portals, multi-step movement, split policy or sonar.

Training used 60 archived high-rated games from 12 battles, split **8/2/2 whole battles** into train/dev/test. The extraction inspected 1, 209, 469 turns, sampled one eighth and filtered to teacher single-step decisions with at least two available candidate moves. Final counts were **68, 099 train, 19, 311 dev, 16, 591 test**. Battle separation did not make opponents or map families unseen.

| Model | Test accuracy | Test cross-entropy | Parameters/status |
|---|---:|---:|---|
| Linear | 58.09% | 0.8310 | 25 parameters; ultimately selected in games |
| MLP seed 0 | 59.37% | 0.8140 | Diagnostic test result; not the dev-selected seed |
| MLP seed 1 | 59.27% | 0.8187 | Dev-selected model; 417 parameters |
| MLP seed 2 | 59.17% | 0.8171 | Not selected |

Portable inference agreed with PyTorch to below 0.0000013 absolute score error on probes. A separate 26-game top-team diagnostic gave 65.53% linear and 65.87% selected-MLP agreement; it was not used to refit or reselect the model.

The 88-game-per-policy screen versus v2 produced **63â€“25 heuristic**, **67â€“21 linear**, and **63â€“25 MLP**. Linear advanced under the declared rule; its four-win lead was not proof of general superiority to the neural model. The matched heuristic's success also meant the screen could not attribute every gain specifically to learning.

Linear confirmation was **126â€“50 versus v2**, score 71.59% [57.39, 83.52]. Across three opponents it won **445/528 versus 393/528** for control: +9.85 points [+4.36,+14.20]. It improved both elimination and length-loss counts, though Default regressed and Trauma remained weak.

Generated-layout transfer used 16 layouts from four families. Linear versus v2 was **210W/32D/14L**, score 88.28%; the gate passed. The MLP scored 206W/32D/18L. Their small direct diagnostic favored the MLP, 18â€“10 with four draws, but its family interval did not establish superiority; the chosen release was not changed after seeing it.

The mature-role branch still failed strict-positive confirmation: 400/528 versus 393/528 pooled wins, with the lower confidence bound at zero, and gains concentrated on Big Empty. Thus v3 adopted the **linear mover**, not the grower policy.

The combined confirmation audit covered 1, 584 games and 10, 383, 046 exact actions. Transfer audited another 544 games and 6, 985, 884 learned-bot actions. Sampled/full-game sandbox checks passed; the MLP was also executable within budget. **v3** was frozen at hash `69382825b699723d`; its release package was prepared, with upload left to the user.

Source: [complete hybrid experiment](snapshot-2026-10-03/HYBRID_EXPERIMENT.md).

## What this era established

The strong local baseline came from three distinct advances: a reproductive economy, a growth phase, and better action evaluation. More memory, a neural network, safer-looking trajectories and portal support were each implemented or explored, but none automatically earned deployment. This era's negative results are specific to its baseline, candidate sets, maps, opponents and old engine; they are not permanent bans on those ideas.
