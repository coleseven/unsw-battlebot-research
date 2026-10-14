# Work queue: highest expected value toward top 100 first

> **Current documentation, 14 October:** [NEXT_STEPS_2026-10-14.md](NEXT_STEPS_2026-10-14.md) reconciles the interrupted review with completed D15–D22 work. v12z is the latest adopted local control. Current-map transfer and full-action tactical comparison remain open; do not restart implemented sprint hunting or rejected broad masks/escort variants. The publication writeup and archive extend through the October 12 evidence snapshot; older queue entries below are historical.

> **Live version update, 5 October:** user-confirmed **v12x uploaded 2026-10-05 10:04:34**, timezone unspecified. This supersedes the upload uncertainty below. Check subsequent FEATURE_EXPERIMENT.md results before acting on the 4 October plan; its v11t baseline is historical. Match server time/submission identity before attributing cutoff-adjacent games.

> **Current handoff, 4 October:** [NEXT_STEPS_2026-10-04.md](NEXT_STEPS_2026-10-04.md) supersedes the priorities and running-status notes below. C9 sprint masks and C11 bodyguard failed; C10 is neutral and stays off. v11t is the local control; live upload identity is unverified. Next: repair stale map-report classification using saved results; diagnose early worker economy; test bounded cumulative harvesting/return routes; then targeted collector pickup and rare queen corridor-entry checks. The runtime/map refresh and corrected queen search are already complete. Read the diagnostic gates before implementation.

> **Fresh live evidence, 3 October:** [LIVE_GAME_REVIEW_2026-10-03.md](LIVE_GAME_REVIEW_2026-10-03.md) analyzes 95 completed games (44W/51L). Elimination is the largest net deficit in this cohort (6W/18L); keep Trophy/Stripes economy diagnostics alongside C2 queen-search confirmation. It supplies repeatable Maze/Portals/weakhold corridor traps, exact friendly queen-kill cases, and a portal-tail collision for Claude's regression suite. See the evidence bundle; do not treat the pending C2 candidate as the uploaded bot.

> **Current handoff, 3 October:** read [NEXT_STEPS_2026-10-03.md](NEXT_STEPS_2026-10-03.md) first. v11q is the incumbent; Q7–Q11 hunt/travel/safety follow-ups did not confirm. Next: (1) current toolkit and exact maps—1.2.9 differs from our tested maps; (2) correct queen escape/body/food/threat modeling and validate the final multi-step action; (3) cooperative worker yielding/reservations; (4) temporary queen refuge; (5) selective growth. Build a queen-aware opponent panel alongside these. The older priorities and running-status notes below are historical.

> **Superseded priority order, 1 October:** [STRATEGIC_RESET_2026-10-01.md](STRATEGIC_RESET_2026-10-01.md) is the current handoff. Today's queen scoring and length-dependent free movement invalidate the old objective and ranking-gap assumptions below. New order: Q0 current-engine/scoring/map parity; Q1 queen identity and policy; Q2 multi-step planner; Q3 queen speed-threshold economy; Q4 queen attack/defense; Q5 scheduled delivery; Q6 learned plan evaluation. R5 failed and stays stopped. v10o's sonar-age gain was confirmed under the old setup only. The remainder is historical context, not instructions to resume those runs.

Reordered 30 September 2026, late evening EDT. The ordering is a judgment about expected benefit, evidence, implementation cost and speed of validation—not a claim that these untested changes improve the bot.

Sources: [FEATURE_EXPERIMENT.md](FEATURE_EXPERIMENT.md), [TOP_5_STRATEGIC_ANALYSIS_2026-09-30.md](TOP_5_STRATEGIC_ANALYSIS_2026-09-30.md), [OVERNIGHT_REVIEW_2026-09-30.md](OVERNIGHT_REVIEW_2026-09-30.md), and [TOP_100_RESEARCH.md](TOP_100_RESEARCH.md). Later experiment results supersede earlier recommendations.

**Incumbent: v10h**, `results/v10h-bot`: v10 + CPP_BOOK_MAP + CPP_FEED_SHIFT_LARGE 40. The experiment log records v10h uploaded by 21:59 UTC on 30 September. Keep **v10g**, book map only, as a second control where timing matters; its book gain is established and the incremental feed-shift gain is much smaller.

**Live target check, approximately 22:39 EDT / 02:39 UTC:** [777](https://game.battlecode.au/teams/590) is rank **133**, rating **1671**; [rank 100](https://game.battlecode.au/leaderboard?page=10) is **1723**, a **52-point** gap at this snapshot. The threshold moves. This favors extracting a few robust improvements from the current system before putting a full rewrite on the critical path; it does not convert to a guaranteed number of local wins.

**One heavy game job at a time, guarded, at most 12 workers.** This document changes the plan only. No bot code, experiment or upload was changed.

## Finish the current experiment

The broad sonar-hub ablation has **finished**:

- Sonarhub: 337 wins versus 343 baseline; current-pool aligned delta −0.011. Prisoners Dilemma improved 15 → 20 wins out of 36, but Slithery Fight fell 24 → 16 and Portals 21 → 17.
- Sonarhub plus three times the hub weight: 293 wins, pool delta −0.193. Do not repeat a generic stronger-hub-pull sweep.
- The current follow-up is **sonar adoption age 15 / 30 / 60**, `results/v12-sonarage-dir.txt`, based on v10n with v10h behavior, seeds 331001–331003. At inspection its top-level files contained the plan and an empty run log; there was no completed comparison there. That alone does not establish process progress.

Read the result when complete. Advance an age gate only if it preserves PD's improvement without the Slithery/Portals regressions. Confirm any finalist on fresh seeds and matched original/perturbed layouts. If it fails, keep the diagnosis and move on; do not search ages indefinitely.

## Priority order

**Status update for the mover handoff:** FEATURE_EXPERIMENT.md now records the age comparison complete: age15 331 wins, age30 340, age60 342, baseline 333. Ages 30/60 are mildly positive, but the earlier PD advantage did not persist. Fresh-seed confirmation with ten perturbed layouts added is the next recorded run (seeds 341001–341003). Recheck its actual status before mover stage M0; the earlier running-status paragraph is historical.

| Priority | Work | Why here | First decision gate |
|---|---|---|---|
| 1 | Productive-area control and selective resource sharing | Directly measured food-access failure; a partial intervention moves it | More fast-spawn food and early survivors, then wins without crowding regressions |
| 2 | Endgame conversion with a persistent king role and a length budget | Many losses have sufficient total mass but an inferior longest dragon | More retained king length and replicated strong-panel wins |
| 3 | Our own contextual move ranker, taught by counterfactual outcomes | Main larger research investment; v3 is crucial and imitation failed | A small rollout teacher improves held-out decisions before scaling |
| 4 | Exact short tactics for valuable dragons | A single late error can destroy the whole investment | Fewer valuable deaths and useful rescues without excessive length spending |
| 5 | Opening allocation on the remaining elimination maps | Feeding cannot repair early Trophy/Default Small/Arena collapse | Better productive-cell access and population before contact |
| 6 | King protocol and collection-aware feeding as supporting components | Existing standalone fixes have not shown robust wins | Revisit when a new role/rendezvous policy demonstrably needs them |
| 7 | Destination-aware portals and limited retuning | Important representation; tested portal switch and broad CMA failed | Correct a measured decision failure, then replicate a win gain |
| 8 | A separate learning system from scratch | Potential upside, weakest evidence for a short route to top 100 | First make a small teacher/student improvement loop work |

The first two address different loss classes and should remain separate experiments. Priority 3 moves up from the old queue's final structural item; begin with a feasibility pilot, not a large training commitment.

## 1. Control productive areas, with selective information sharing

**Evidence:** PD was 0/42 against v92 in the earlier baseline panel, with 41 elimination losses. Its valuable food comes from two fast six-cell patches across the vertical wrap, not the slow central cells. Before round 150, v92 ate 94–116 pearls from the fast cells versus our 16–38. Some founders never saw a spawn timer and kept no hub. Sonar helped a small probe, but its full-suite regressions show that broad sharing is not a general solution.

**Structural hypothesis:** optimize the marginal food a dragon can actually collect. A rich destination becomes less useful when teammates already cover its access routes.

Start with selective adoption by a dragon that has persistently lacked a useful food target; the running age gate is a cheap approximation. If it fails, distinguish information missing, information received but overridden, and too many dragons choosing one patch before adjusting another weight.

Next candidates, tested separately:

- Score known spawn rate, route cost, freshness and observed competition. Unknown timers need an uncertainty flag, not a zero-productivity assumption.
- Allocate distinct reachable entry routes or temporary patch assignments, with reassignment when crowded or unproductive. Use local observations or communicated estimates, not inaccessible global teammate positions.
- Keep a mobile reserve instead of sending every recruit to one remembered hub. Measure whether occupancy blocks spawning or collection.
- Condition sharing on unmet need and expected gain. Absolute richness already failed to separate PD from Slithery; map identity alone is also an incomplete explanation.

**Measure:** time to first useful target, fast-cell pearls, empty travel turns, population at rounds 50/100/150, and teammates concentrated at each patch. A PD-only gain that loses more elsewhere fails the promotion gate.

Distinguish productive worker turnover from accidental losses. Top-team replays include large numbers of wall, self-collision and empty-turn deaths alongside successful corpse collection. Minimize wasted work and lost scoring potential, not every death indiscriminately; a generic survival reward can suppress a useful recycling policy.

## 2. Convert existing mass into retained king length

**Evidence:** late feeding volume was 3–10 times below v92's in the diagnostic sample. Wider donors (`sum12`) increased longest length versus v92 by about 2.5 in two runs, but the overall win gain did not replicate: +14 wins, then −1. Stronger king-gradient pull barely moved king length.

Top-team examples sharpen the objective. In game 712379, forgot to mention's king started round 400 at length 24, ate 11 corpse pearls, spent five length on extra movement and six on children, and finished at 24. In game 708587, Stockfish converted 23 own-corpse pearls into 23 retained length, from 39 to 62, and won. These illustrate mechanisms; they are not a controlled algorithm comparison.

Test an explicit cash-in role from an adequate economy:

- **Recipient:** choose a reachable, defensible dragon with growth potential. Preserve the role through a large rear-child split; a newborn ID may inherit almost all of an old king's length.
- **Donor:** compare continued harvesting against a reachable corpse drop before the deadline. Increasing FEED_MAXLEN alone does not solve this choice.
- **Collection:** use short rendezvous routes and bounded recipient collection priority. Attribute food to king lineage, other teammates, enemies, or uneaten remainder.
- **Spending:** charge reproduction and extra movement against expected final length. Population rescue needs an explicit reason and cost rather than repeated stripping of a protected king.

Two larger extensions deserve small, separate pilots after this mechanism works. First, switch between protecting a credible lead and taking risks to catch up, using only observed enemy lengths and uncertainty rather than the replay's omniscient maximum. Second, price the insurance value of a small backup population: one surviving short dragon can matter after a head-on king trade. Compare this with both unrestricted rescue splitting and sacrificing every spare; do not assume one reserve count fits every map.

Keep baseline behavior until the intervention round for a clean prefix comparison. Later states may diverge. Do not repeat early length-4 protection, which cost −0.185 pool aligned score.

**Measure:** lineage-aware length at intervention and finish; food delivered and retained; split/sprint expenditure; valuable-dragon survival; backup dragons; and strong-panel wins. Reject a larger king that dies more often.

## 3. Our own contextual move ranker (R5)

**Instructions for Claude:** [NEW_MOVER_PLAN.md](NEW_MOVER_PLAN.md) defines stages M0–M8, the 64-input / 1,585-parameter neural residual, rollout labels, integration boundaries and promotion gates. Follow it for this work and freeze the actual validated incumbent before collecting labels. Its detailed contract supersedes the preliminary outline below where more specific.

**Why move it up:** removing v3 cost about −0.36 aligned score, and lowering its weight to 9 cost −0.175 in the newer R4 test. It is a 24-feature linear model from the v3 era. Refitting to v92 improved imitation accuracy from 57.9% to 60.7% yet reduced wins. Better imitation is not the objective; a larger network alone is not an answer.

**Pilot:** roughly 200–500 consequential decisions from our own games, stratified by role, phase and map family. Replay the original seed to the decision, force one legal alternative, then let our unchanged policy continue. First verify that a no-op intervention reproduces the original event prefix and outcome, including bot memory, communication, engine version and RNG handling.

Use short rollouts to screen obvious navigation errors; extend ambiguous and king-critical choices toward the true game objective. A short survival target must not teach donors never to sacrifice. Compare actions on shared conditions and add samples to close decisions. Privileged simulator information may score offline outcomes; deployed features must remain available to the live bot.

**Features:** retain v3 inputs and add phase/role, target direction and walking distance, known spawn timing plus unknown flag, teammate congestion, remembered portal landing information plus uncertainty, and king-length expenditure. Test contextual features before increasing capacity.

If another global linear score keeps overriding strategic intent, test a small hierarchy: a controller selects harvest, expand, rendezvous, collect or preserve; the move ranker chooses a legal action within that role. This directly addresses conflicting movement incentives. It is a proposed architecture, not an inference that any named leader implements it.

**Model:** linear or a small residual over the incumbent first; then consider a tiny MLP, initially around 1–2k parameters. Preserve incumbent choices when learned preference is weak, and evaluate that fallback threshold. Check C++ numerical parity and judge CPU. The recorded v10h maximum of 7.9M points does not benchmark the new model.

**Learning loop:** split by whole games and held-out seeds/opponents/layout variants, not neighboring turns. After an improvement, collect states the updated policy visits. This uses the distribution-shift lesson of [Ross, Gordon and Bagnell (2011)](https://proceedings.mlr.press/v15/ross11a.html); our teacher is counterfactual simulation, not an accessible top-team bot. Rollout-derived classification follows [Lagoudakis and Parr (2003)](https://users.cs.duke.edu/~parr/icml03.pdf). Neither establishes that this bot will improve.

**Scale gate:** benchmark prefix replay and continuation cost, label stability, and teacher improvement before collecting 10k states. The old 1.5-second-rollout budget was an estimate; reconstructing long prefixes may dominate. Allocate samples to uncertain choices, as motivated by [Dimitrakakis and Lagoudakis (2008)](https://arxiv.org/abs/0805.2027). Labeling and confirmation games use the guarded heavy-job slot; model fitting is small.

Promote on paired full-suite wins and fresh-seed confirmation against the strong panel, not label accuracy.

## 4. Exact short tactics for kings and cheap attackers

Focus on a valuable king in danger, a useful rear-child reversal, a portal landing near enemies, or a cheap attacker with a credible king trade. Stockfish exchanged length 3 for SSS's length 36 in round 499 of game 709266. Stockfish was already ahead in longest length: this demonstrates vulnerability, not proof the trade flipped that result.

Our C++ bot already returns `SPLIT length-2` when movement scores are empty. New work means evaluating preservation before the last moment, transferring the king role, and avoiding unnecessary repeated two-length losses.

The forward model must correctly handle the occupied tail before movement, food removed within each branch, extra-step length costs, portal destination/facing, ID turn order and the newborn's same-round turn. Consider a few plausible enemy responses under partial observation. Start narrow; do not simply deepen the old beam.

## 5. Allocate the other weak openings

PD belongs in priority 1. On Trophy, Default Small, Arena and other early-elimination cases, diagnose productive-cell access, redundant founder routes, newborn escape, and population before contact. Separate Trauma's opening and endgame failures rather than assigning one treatment by map name.

Use successful public openings as hypotheses. Strong teams have pronounced map weaknesses. Do not imitate their routes without considering their split/communication policy, or blend all top-team moves into one teacher.

Require both sides and perturbed layouts. Keep map-book recognition and falsification safe so that a mistaken remembered edge cannot invalidate an otherwise good opening.

## 6. Protocol and reachability as dependencies

CPP_KB_V2 already supplies a compact identity token, origin age, relay expiry and visible contradiction checks. Its confirmation helped easy opponents but not the strong three. Feed-reach variants also failed to establish wins. They are no longer unimplemented first priorities.

When priorities 2 or 4 need a real handoff, test identity collisions, original timestamps, ties, death invalidation, fresh child state and explicit succession. Protocol 3's 64-bit payload is an option if the compact format is inadequate, with full parser/ECHOES support. Test the behavior the protocol enables.

Reachability remains incomplete without corpse geometry, recipient collection behavior, turn order and enemy access. Another radius-4 versus radius-6 sweep cannot answer those questions.

## 7. Integrate portals; tune demonstrated mechanisms only

The negative CPP_V3_PORTAL result does not prove destination information is useless. Suppressing a bad departure-side score differs from evaluating a landing state correctly. Revisit through R5 or a measured landing-error class, with uncertainty for unknown exits.

Tune a few knobs only after a mechanism passes confirmation. Evaluate the incumbent on every generation's shared conditions. Screen broadly, allocate extra seeds to survivors, and reserve untouched confirmation conditions. Do not restart the failed 17-dimensional overnight sweep or automatically reuse its covariance after a strategy change.

## 8. Separate-machine / from-scratch research

The GTX 980 / older i5 / roughly 16 GB machine is not assumed available. Its first useful independent assignment would be replay annotation, a small contextual evaluator, or the R5 pilot after environment verification. Simulation throughput and RAM safety matter more initially than network size.

Full multi-agent RL, a large network or a long self-play league remains a later research branch. Current evidence does not justify putting it on the critical path to top 100. No separate setup or process was started for this plan.

## Completed results: avoid circular work

| Tried | Disposition |
|---|---|
| Hub spacing alone | Small uncertain gain; available for combinations. On PD, spreading hubs can send dragons to slow cells. |
| v12 final and generation-5 tunes | Both worse in paired validation, particularly versus v92; incumbent retained. |
| KB2 alone | Initial gain concentrated in easy opponents; strong-panel confirmation failed. |
| Feed reach 4/6 and KB2 + reach4 | Within noise overall and slightly negative versus v92; not adopted. |
| Stronger king-gradient pull | Longest length barely moved; not adopted. |
| Wider donors, sum12/sum64 | sum12 moved king length; overall wins did not replicate. Redesign the mechanism. |
| R4 imitation of v92 | Better prediction accuracy, worse games; more imitation data alone is not the next step. |
| Broad sonar sharing | PD improved, Slithery/Portals regressed; age/need gating is the follow-up. |
| Early length-4 protection | Large measured regression; endgame protection must not indiscriminately suppress opening growth. |

## Promotion and top-100 tracking

Every bot-change evaluation retains **all 15 maps, both sides**. Judge the observed current 10-map pool first and report the other five as a guard; recheck the live pool when it changes. Use distinct seeds and opponent-family diversity: nicked v92/v75/v44/lab are one strategic family.

Require a held-out strong-panel win gain that survives fresh seeds and original/perturbed layouts. Report uncertainty over matched conditions and map/opponent breakdowns; do not promote on pooled aligned score, food, prediction accuracy or longest length alone. Diagnostic probes do not replace this gate.

Track uploaded hash/time, current rank/rating, contemporaneous rank-100 rating, and the subsequent ranked cohort. Separate pre/post-upload games and account for schedule and rating lag. No fixed local threshold or isolated five-game battle establishes sustainable top-100 performance. Keep a rollback artifact and obtain the user's go-ahead before submission.
