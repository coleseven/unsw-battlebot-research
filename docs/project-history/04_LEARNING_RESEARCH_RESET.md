# 4. Learning experiments, opponent research and the rules transition

[Project history](../../PROJECT_HISTORY.md) · [Previous](03_CPP_CMA_V7_V10H.md) · [Next: queen era](05_QUEEN_ERA.md)

## R4: better imitation, worse games

The original v3 linear model remained one of the strongest components in ablation. R4 asked whether refreshing that model using a stronger demonstrator would improve it.

The dataset came from **300 local games** of nicked v92 against five strong bots across 15 maps, two seeds and both sides. It retained single-step decisions with at least two candidate moves, sampled 25%, and used the same 24 features, yielding about **650,000 examples**. Partitions were grouped by map/seed. Linear softmax fitting used LBFGS with regularization selected by development negative log likelihood.

On held-out v92 actions, agreement improved from **57.9% to 60.7%**, and NLL from 0.835 to 0.820. The new model more strongly avoided friendly proximity and favored space for long dragons; its weight norm was 1.76 times the old model's.

The paired game test tried the raw new ranker, norm-adjusted weighting and a weaker ranker contribution:

| Variant | Wins versus common base's 347 | Current-pool aligned effect |
|---|---:|---:|
| R4, original W_V3 | 333 | −0.044 |
| R4, equalized norm | 326 | −0.053 |
| R4, low contribution | 291 | −0.175 |

All were rejected. More accurate imitation of v92 did not produce better decisions inside our own search, reproduction and feeding policy. This is evidence against these fitted replacements, not proof that imitation can never work: v3 itself was an imitation success.

Source: [feature log, R4 section](snapshot-2026-10-03/FEATURE_EXPERIMENT.md); model configuration and retained results are indexed in the archive.

## Hub sonar returns in a different context: v10o

PD diagnosis showed founders sometimes never observed a spawn countdown, leaving them without learned hubs. Sonar hub sharing, which hurt the earlier v7-era bot against v75, now improved PD probes against v92: **5/12 wins**, versus 0/42 in an earlier baseline diagnostic. The comparison was a lead, not a matched promotion result.

The full suite showed why unconditional sharing was not enough: **337 versus 343** wins, PD improving from 15 to 20/36 while Slithery fell 24→16 and Portals 21→17. Stronger hub pull worsened the aggregate to 293.

A richness threshold could not reliably separate PD from Slithery. The next hypothesis distinguished old hub-less founders from newborns that would soon discover food independently: adopt a received hub only after a minimum age without one.

| Minimum adoption age | Screen wins, base 333 | Confirmation wins, base 542/900 |
|---|---:|---:|
| 15 | 331 | Not advanced |
| 30 | 340 | **563** |
| 60 | 342 | 552 |

Confirmation included **15 original plus ten perturbed layouts**. Age30 had all-layout aligned +0.038 [+0.010,+0.065]; its current-pool interval still included zero. The effect replicated modestly overall and was retained as **v10o**, hash `7623b9aa5ef6172b`. It did not preserve the dramatic PD-specific gain. That distinction prevents retelling v10o as a solved PD opening.

## R5: a structured attempt to learn from our own counterfactuals

The [new mover plan](snapshot-2026-10-03/NEW_MOVER_PLAN.md) specified stages M0–M8, an incumbent-preserving integration boundary, teacher integrity tests, a 64-feature action representation, progressively stronger models and game-based promotion. It did not authorize treating a planned NN architecture as an implemented success.

The actual work is recorded in [NEW_MOVER_RESULTS](snapshot-2026-10-03/NEW_MOVER_RESULTS.md).

### M0/M1: preserve state and verify interventions

The teacher hooked replies **after** the bot computed them, preserving its private-state update, and rewrote only one MOVE line for a chosen dragon/round. Other lines, including sonar, were retained. Identity tests checked no hook, pass-through hook and forcing the chosen action.

- Three games were identical under no-op hooks.
- Forcing the incumbent action reproduced the event stream at **13 sampled decisions**.
- Forcing a different direction changed the game; some initial checks deliberately used a neck reversal, so this was an intervention check rather than legal-candidate validation.
- Sixteen games compared mover-off, zero-weight mover-on and feature logging: all matched v10h.
- Logged decisions had **64 features**, combining the 24 v3 features, candidate context and decision context.

Training consumed the C++-logged features directly, avoiding a separate Python feature implementation. The residual score was bounded and gated by an override margin, with non-finite output falling back to the incumbent. Initial eligibility excluded attack candidates and required at least two ordinary moves.

### M2: final-result labels were too noisy

The first pilot used **44 source games, 308 decisions and 808 forced continuations**. Forcing the original move reproduced its source result at all 308 decisions. Alternatives changed final result in **50/308** decisions; final longest margin varied in 204/308.

Final-result differences had little relation to the incumbent's score preference. Longest-margin labels had more coherent signal but mostly agreed with the existing policy. A provisional margin-trained student reduced held-out total from 497 to 455; result-trained score barely moved 56→57.5. The pilot gate was not convincingly passed.

### M2b: more decisions and shorter horizons

The expanded set used **88 source games**, 1,220 sampled decisions and **1,075 fully labeled decisions**, with +20/+40/+80-round team totals and lengths as additional targets. A file-handle leak stopped the first continuation run at 2,609 games;  worker recycling and resumption followed.

Integrity was imperfect: **three errors**, and forcing the chosen move reproduced **1,073/1,075** source outcomes. This is a limitation of the teacher record, not a completed zero-error parity certificate.

Short-horizon targets did not reliably improve the true objective. Result labels showed weak offline signal. Across four data splits at override threshold 0.5, real labels gained +11/+9/+16/+16 held-out decision wins; within-decision permuted labels also gained +0/+11.5/+5/+4. Thus some apparent value came merely from deviating, rather than from learning useful labels.

The deployed experiment trained a **linear residual**, represented as two ReLU units for export, rather than the full prospective nonlinear network. Its strongest weights often opposed incumbent preferences: fewer exits, less pearl attraction, more friendly proximity and less hub progress. That was a warning sign.

M5 inference checks matched **14,329/14,330** C++ choices to Python recomputation; the single discrepancy lay within roughly 1e−5 of the override boundary. At threshold 0.5 it changed about a third of eligible moves. This was near parity with a documented boundary discrepancy, not exact parity on every case.

### M6: game outcomes rejected the residual

| Override threshold | Wins /528 | Base wins /528 | Recorded current-pool aligned effect |
|---|---:|---:|---:|
| 0.5 | 184 | 270 | −0.352 |
| 1 | 234 | 270 | −0.163 |
| 2 | 263 | 270 | −0.014 |

More overriding produced worse play. The model remained off and the project stopped at M6. M7/M8 promotion was not reached. The infrastructure survived for possible future work, but the result did not justify scaling the same final-result teacher or training a larger NN.

A later correction invalidated the Sprint-map portion of these results, described below. The large negative result at low thresholds still held on the valid 15 ranked maps. Because some teacher source games also used those bad Sprint extracts, that issue is relevant to any attempt to reuse the labels—not merely to reporting the test result.

The proposed prerequisites for a restart were lower-variance continuations, reliable state/RNG branching, or a narrower tactical teacher on high-value decisions. Those were **proposals**, not completed capabilities at the cutoff.

## Sprint maps: an apparent generalization crisis was partly a data error

The Sprint event brought seven new map names: Australia, Islands, Maze, Stripes, Tower Defense, Around UNSW and weakhold. The log records v10h entering as seed 131, receiving a bye, beating Split and Stack and losing to Citadel Insecurities. Its prose says “lost 1–6” but also mentions a drawn weakhold game; the precise series convention/outcome needs reconciliation before using it as a formal W/D/L statement.

Initial local tests appeared severe: **v10h 58/168**, v10o 52/168, including losses to older/easier bots. A grouped ablation of old weights and books was launched to explain the supposed collapse.

The diagnosis was subsequently retracted. All seven extracted maps had **zero pearl spawners**: the scraper's check accidentally matched `TILE_COUNT` instead of a real `TILE ` record. Tower Defense had 24/24 draws with zero pearls eaten. The experiment was testing foodless maps, not actual unseen-game generalization.

The extracts moved to a hidden-spawn directory and the matcher was fixed. A reconstruction tool inferred spawn cells from pearl appearances on phases without deaths, used take-to-respawn gaps for delay estimates, and pooled symmetry evidence. On known PD geometry it found 56 spawners with no false positives in that check, but recovered only eight of 12 every-round fast cells; slow delays remained approximate.

Using **57 real games per map**, it generated playable Sprint approximations. Corrected baseline results were **v10h 82/168**, **v10o 83/168**. Weakness was concentrated against strong opponents and on Tower Defense, weakhold and Islands; v10h beat v7-base 20/28 and leviathan3 26/28. The purported broad collapse versus weak bots disappeared.

These were still inferred maps. The later **official 1.2.9 files** superseded them for current validation; they did not retroactively make the earlier approximate tests exact.

## Opponent and live-game research

| Research artifact | Work actually done | What it contributed |
|---|---|---|
| Corpus strategy audit, September 22 | 12 archived high-rated battles, 60 games, nine submissions, seven teams | Length-four splits and two-length children common; multi-step moves rare. Descriptive support, not causal imitation evidence. |
| Competitor research / top-ten scouting, September 24 | Public-source reading and replay profiles | Memory, hubs, tactical trades, concentration and sonar became concrete hypotheses. Some intent/source claims were explicitly limited. |
| Top-100 review, September 29/30 | Decoded **155 games**, 79–76, from 31 recent ranked battles | Separated opening deficits from late conversion; identified source defects in hubs, portals and king information. |
| Overnight review, September 30 | **80 new game outcomes**, 37–43; inspected optimizer state and results | No claimed live breakthrough from an unuploaded retune; highlighted missing perturbed-map validation and easy-opponent gains. These 80 outcomes were not a fresh full replay-mechanics audit. |
| Top-five analysis, September 30/October 1 UTC | Fresh 25 games per top team; earlier 250 team-game observations over 215 distinct games | Multiple ways to concentrate length; lineage matters; behavior changes within a day; source algorithms unknown. |
| Strategic reset, October 1 | Read new official rules and checked local setup | Reprioritized queens, free movement, faithful current-engine tests and queen-aware opponents. |
| Next steps and live review, October 3 | Source/model review; current map mismatch; then 95 decoded recent games | Corrected queen search and worker-economy diagnostics; later C-series work tested parts of the advice. |

The September 30 fresh top five were **Cutlery, forgot to mention, 3.14159265, SSS and cheji bt**. All were listed as C++, but no attributable source repository was verified for them. Their search, learning and sonar algorithms were not known. The sample showed varied final supporting populations and **32 of 60** final longest dragons born at or after round 400. A late child can inherit a large body; following only its food consumption understates earlier investment.

The earlier top-five cohort additionally included Stockfish and Cache me outside. These were dated observations, not permanent membership or an inference of algorithms from team names.

Sources: [corpus audit](snapshot-2026-10-03/CORPUS_STRATEGY_AUDIT.md), [top-ten scouting](snapshot-2026-10-03/TOP_TEAMS_SCOUTING.md), [top-100 research](snapshot-2026-10-03/TOP_100_RESEARCH.md), [overnight review](snapshot-2026-10-03/OVERNIGHT_REVIEW_2026-09-30.md), [top-five analysis](snapshot-2026-10-03/TOP_5_STRATEGIC_ANALYSIS_2026-09-30.md).

## Scholarly work considered, and implementation status

The archived research documents contain the original paper links and caveats. This history records their role in the project; it does not represent a fresh literature review or claim that an algorithm was implemented merely because a paper was cited.

| Research direction | Intended application here | Status by cutoff |
|---|---|---|
| CMA-ES learning-rate adaptation, Nomura et al. | More stable noisy parameter search | Implemented through cmaes-lra and used in v9/later campaigns |
| Expert Iteration, Anthony et al.; DAgger, Ross et al. | Teach small evaluators using stronger decisions on relevant states | Inspired teacher/student proposals; R5 built a limited counterfactual pipeline, not a complete successful Expert Iteration/DAgger system |
| Cooperative multi-agent PPO, Yu et al. | Shared strategic controller, centralized training critic | Proposed; no successful PPO training run documented |
| PSRO/opponent mixtures, Lanctot et al. | Avoid fitting one opponent lineage | Frozen panels and specialists exist; no full PSRO solver documented |
| POMCP, Silver and Veness | Planning with plausible hidden states | Proposed for tactical teaching; no general belief-state planner documented |
| PettingZoo/AEC, Terry et al. | Preserve sequential agent observation/action semantics | Design guidance; not proof of a complete RL environment integration |
| Invalid action masking, Huang and Ontañón | Exclude truly illegal actions without removing useful sacrifices | Research/design guidance; no trained masked policy-gradient agent documented |
| Potential-based shaping, Ng et al. | Avoid pearl/death reward pathologies | Proposed; no validated shaped-RL result documented |
| Sample Factory, Petrenko et al. | Efficient experience generation | Throughput guidance; the concrete speed work here was in-process C++ and guarded local evaluation |

The spare machine was described by the user as a 980 GPU, older i5 and approximately 16 GB RAM. The research proposed replay work, small evaluators and bounded teacher jobs before full end-to-end RL. **There is no retained evidence of that machine being provisioned or a separate-machine training campaign completing.** Historical compatibility advice in those documents should be rechecked before installation, rather than copied as current setup instructions.

## October 1: a new game objective

The strategic reset recorded queen-first scoring, `ceil(starting length / 4)` free movement, reset ratings and idled submissions. Original queen identity had to come from the initial dragons/team mapping, not a casual assumption that team B always corresponded to ID1 in side-swapped replays.

The local default was still on the older runtime when the review began. Q0 introduced an isolated 1.2.3 runtime, explicit rules tests, queen diagnostics and actual outcome-based evaluation. That boundary ends this chapter: old king-feeding results remained useful historical mechanisms, but their old objective could no longer settle queen-era decisions.

Source: [strategic reset](snapshot-2026-10-03/STRATEGIC_RESET_2026-10-01.md).
