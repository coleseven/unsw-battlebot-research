# Strategic reset: build for the game that exists now

Research and instructions only. Reviewed 1 October 2026, approximately 22:46 UTC. No bot implementation, package upgrade, training run, submission or activation was performed.

## The most important finding

**There is a much larger opportunity than tuning the existing mover: the rules changed today, while our local engine and strategy still target the previous game.**

The official **Slay Queen update** introduces queen scoring and length-dependent free movement, resets ratings, and marks existing submissions idle. The announcement also says map revisions will progressively place queens in safer starting locations. This explains why the public profile now shows 777 with no active bot; it does not establish a problem with our files. [Official announcements](https://game.battlecode.au/updates)

The scoring queen is the original dragon with ID 0 or 1, depending on team. After elimination checks, its surviving length is the first tiebreak; a dead queen scores zero. Longest surviving dragon and total length are secondary. **A large child does not inherit queen status.** [Current scoring](https://game.battlecode.au/docs/structure)

A dragon gets `ceil(start-of-move length / 4)` free steps. Length 5 gives two, 9 gives three, 13 gives four. Growth during an action does not raise that action's allowance. Paths can turn and collect pearls at each step. [Current movement rules](https://game.battlecode.au/docs/movement)

Our installed `.venv/Lib/site-packages/unswbc/__init__.py` says **1.1.0**. `cppbot/v6_brain.hpp::decide` normally returns a single direction. `bcsim/margin.py` still rewards longest-dragon share and total mass. The existing bot therefore both leaves movement capacity unused and optimizes resources around an outdated primary objective.

**My strongest recommendation: implement a queen-specific controller and a correct multi-step action planner before doing any more broad CMA-ES or R5 training.** This is an evidence-backed capability gap, not yet a measured win improvement. The opportunity is large enough to justify a structural change.

## What the recent work actually establishes

| Finding | What survives this review |
|---|---|
| R5 residual: 184 wins versus 270 baseline at tau 0.5, 528-game mixed screen | Strong negative result for that intervention. The spawnerless Sprint portion is invalid as a generalization test; ranked-map regressions still reject the candidate. |
| R5 source teacher forced one move, then resumed the incumbent | Offline branch selection did not predict repeated deployment. The student changed about a third of eligible decisions, producing trajectories absent from its isolated-intervention labels. |
| R5 was implemented as a linear residual using two ReLU units | We did not test the full nonlinear proposal successfully. More importantly, increasing network capacity does not repair the label/deployment mismatch. |
| Sonar adoption age 30: 563 versus 542 confirmation wins | A useful old-rules candidate, v10o. It is not a validated new-rules release. |
| Corrected Sprint reconstruction: v10h 82/168, v10o 83/168 | Retracts the dramatic earlier 35% generalization-collapse story. Reconstructed spawn timers remain estimates, not the server's exact maps. |
| Top-team replay examples showed substantial corpse-to-king conversion | Evidence that resource concentration can work under the previous rules. Arbitrary king selection and late transfer to a child must not be copied into queen scoring. |

Sources: [mover results](NEW_MOVER_RESULTS.md), [experiment log](FEATURE_EXPERIMENT.md), [previous replay analysis](TOP_5_STRATEGIC_ANALYSIS_2026-09-30.md).

I would retract my earlier decision to put the generic contextual ranker ahead of structural action planning. Its experiment usefully exposed a failed approach; it did not show that ordinary movement is solved. It excluded attacks and could not change feeding or splitting, which return before move scoring. It also never explored multi-step paths.

The public [777 profile](https://game.battlecode.au/teams/590) reported rank null, rating 1500 and `hasBot=false` during this review. [Rank 100](https://game.battlecode.au/leaderboard?page=10) was 1410 in the direct public data snapshot. **Do not compare that to our old 1671 or claim we already meet top 100.** The rating regime and active population changed. A fresh evaluated submission and subsequent results are needed.

## Priority 0: make the laboratory measure the current game

Claude should do this before implementing the experiments below. Preserve the old engine environment and all old results; create a separately identified current-rules environment when implementation is authorized. The announcement lists 1.2.3, but verify actual engine behavior rather than treating a package version as proof of parity.

Required small fixtures:

1. A short living queen beats a dead enemy queen despite an enormous enemy child; equal queen lengths fall through to the secondary tiebreaks.
2. Splitting preserves the parent's ID and creates a non-queen child. A rear-child escape does not transfer the primary score.
3. Lengths 4/5, 8/9 and 12/13 have the expected free-step boundaries; crossing a boundary by eating changes the next turn's allowance only.
4. Verify paid-step cost, food consumption, current-tail collision, portal facing and child same-round execution against the official engine.
5. Verify ID order and replay winner extraction, including queen death without immediate team elimination.

Replace the tuning target with actual game result as primary. Record queen alive/length and queen-death round explicitly; retain longest/total as diagnostics and true secondary tiebreaks. A convenient scalar shaped reward must not promote losses with larger non-queen bodies. Audit `match.py`, `margin.py`, `tune.py`, `mover_teacher.py`, replay summaries and in-process/native parity.

Refresh current ranked map contents, spawn positions and hashes. Keep historical 15-map coverage as a regression report, but do not call its September pool current. Map identity must include meaningful geometry and spawn changes; a familiar name or partial topology match is insufficient for a book lookup. Separate actual maps, reconstructed Sprint maps, and perturbed diagnostic maps in every result.

Keep the existing single-job guard and 12-worker cap. Do not interrupt another experiment to install dependencies underneath it. Do not activate or submit without the user's authorization.

## Priority 1: turn movement into a short exact path decision

**New action space: safe paths of varying lengths, not four direction scores.** Preserve the existing one-step action as a candidate, but allow it to lose to a better complete path.

For the initial prototype, enumerate all useful paths through two or three free steps, then introduce a bounded beam for longer allowances. Maintain simulated own-body order, consumed pearls, facing and actual portal destinations for every node. Score complete prefixes as well as maximum-length paths. Spending every free step is optional; stopping early can leave a safer position or avoid blocking food production.

Within one dragon's action the other dragons do not interleave moves. That makes the immediate path much more tractable than a general multi-agent rollout. The difficult part is the endpoint: units with later IDs can act before our next turn. Track their possible attacks using their new movement capacity, not the old adjacent-head danger map. Their visible body count is only a lower bound on length; use uncertainty rather than treating it as their exact speed. [Engine ordering](https://game.battlecode.au/docs/execution-order)

Do not reuse the dormant beam without fixing body/food semantics. Do not merge search nodes solely by head cell: two paths reaching that cell can leave different bodies and legal next moves. Clip paths at unknown geometry or treat remote remembered occupancy as uncertain. A longer free path is not permission to drive blindly beyond the observed area.

Start with three comparisons: incumbent one-step policy, multi-step collection for workers only, and multi-step collection including the queen. Measure pearls per dragon-turn, unused safe movement, queen deaths, self-collisions and actual wins. A faster worker that steals the queen's food is not necessarily progress.

**Potential scale:** a length-17 dragon can make five free steps instead of our usual one. This is five times the movement allowance, not a promise of five times the food or win rate. Geometry, body occupancy and observation range constrain the benefit.

## Priority 2: a queen economy with speed thresholds

Replace the interchangeable late king with a fixed strategic recipient. The queen must be recognized by exact ID, including when it is short. Length-based recipient selection can otherwise feed a large worker while starving the scoring unit.

The creative opportunity is that **queen growth now buys both score and future movement capacity**. The pearl taking a queen from 4 to 5 or 8 to 9 has a different immediate strategic value from an ordinary pearl. Likewise, a split from length 9 to 7 loses a movement tier as well as two scoring segments. Express that explicitly in decisions instead of hoping a weight search discovers it indirectly.

Test these policies independently:

- **Threshold bootstrap:** prioritize a safe route to the queen's next speed boundary. Compare with ordinary greedy growth and with unchanged opening reproduction. Do not starve the initial worker economy merely to protect every queen segment.
- **Queen-specific split budget:** price the child by expected future queen delivery, access gained and elimination insurance. Keep the queen's own escape quality in the calculation. A split that saves its life at length 2 can be better than death, but preserving a large child alone is no longer a queen rescue.
- **Reserve food corridors:** nearby workers yield a narrow route and selected pearls to the queen instead of maximizing their individual food scores. Start locally with visible queen position and a short expiry; do not require global shared memory.
- **Adaptive delivery:** donate when the queen can collect safely and the delivery is more valuable than continued harvesting. Test earlier deliveries around speed thresholds instead of only moving the late feeding cutoff.

Measure queen length at rounds 50/100/200/400/500, time at each free-move tier, queen food by source, and the worker economy sacrificed to achieve it. Include both sides: queen 0 and queen 1 have different action order.

## Priority 3: schedule collection instead of chasing a moving head

The existing beacon says roughly where a king was. A fast queen can make that target stale quickly. Increasing attraction to stale coordinates is not coordination.

Try a **short queen collection route with announced drop locations**. The queen commits to a small safe route segment; workers choose reachable drop cells beside that route. Start with one visible donor and one queen, then extend to relayed intent if that mechanism wins.

Important timing: queens act before their own workers. A worker dropping food later in round r normally supplies the queen in round r+1 or later, not retroactively this round. Plan the exposed interval and enemy interception. The queen must move each turn, so a protected loop or circuit is more useful than an instruction to remain stationary. Corpses place pearls on alternating body segments; do not count a donor's entire length as delivered food. [Execution and death sequence](https://game.battlecode.au/docs/execution-order)

A more radical experiment is a **depot economy**: workers collect in surrounding patches while the queen repeatedly traverses a protected collection circuit. This can reduce rendezvous uncertainty and exploit multi-move harvesting. It can also fail through congestion, predictable attacks, food stolen by workers or blocked spawns. Test a local version before building an elaborate protocol.

Record delivered pearls actually eaten by the queen, enemy interception, leftover pearls, queen detours, and worker harvesting forgone. Compare against equally sized donor populations under the existing chase policy. More suicides or more corpse pearls alone is not success.

## Priority 4: queen assassination and defense

Under the new primary objective, cheap workers can threaten a disproportionately valuable target. A head collision kills both participants. This suggests a tactical specialist that searches complete paths to the enemy queen's currently visible head, including paid steps when worthwhile. This is an original proposed controller, not a claim about any competitor's implementation.

Separate cases:

| State | Proposed strategic response |
|---|---|
| Our queen alive, enemy queen visibly attackable | Sacrificing a worker can be very valuable; still preserve a surviving team and account for retaliation. |
| Our queen alive and credible lead | Favor queen escape routes and screened endpoints over unnecessary worker harvesting nearby. |
| Our queen dead, enemy queen alive | Shift workers toward finding and attacking the enemy queen; growing an arbitrary king cannot overcome a living enemy queen at the deadline. Elimination remains another winning route. |
| Both queens confirmed dead | Restore longest-dragon consolidation as the appropriate fallback objective. |

A missing queen is not a confirmed dead queen. Maintain explicit observed/unknown/dead states. Do not use omniscient replay information in live policy. Queen sightings need IDs and timestamps; do not infer identity from size.

Defense must evaluate endpoints after the whole move. Workers acting later in the round may reach a queen that looks locally safe now. Defensive escorts should block plausible attack paths without blocking the queen's escape or consuming its reserved food. First test exact visible threats; broad worst-case danger everywhere may immobilize the queen.

## What the NN should become

Keep R5 stopped. The useful new learning problem is **ranking short plans or choosing roles**, after a correct action generator exists.

First generate candidate plans with known immediate legality and outcomes. A small network can estimate endpoint danger, near-term queen gain, or whether to harvest, deliver, escort or raid. Inputs should include queen identity/status, movement tier, ordered path/body summaries, role, reachable food, enemy action-order risk and information freshness. Do not use the old 64-feature vector unchanged: it cannot represent a multi-step path or the new objective adequately.

Use exact immediate labels for collision and food consequences. For delayed value, compare options sustained over a short horizon, with the same information and matched source state; use several future continuations when feasible. Explicitly distinguish oracle labels using hidden state from features available to the bot. A teacher with privileged knowledge is only useful if its advantage is learnable from those features.

Evaluate students by deploying them over complete games, then collect their own visited states. R5's one-change offline evaluation did not cover the cumulative effect of many changes. Never relax an online failure because held-out row accuracy improved.

The GTX 980/i5/16 GB machine can be a separate small-model training and data-analysis worker, subject to an actual software compatibility check. It is not necessary for the first breakthroughs: action planning and queen policy can be tested without GPU training. Keep large end-to-end self-play off the critical path until a small learning loop improves current-rules games.

## Search for different strategies, not endless variants of one strategy

CMA-ES over existing additive weights cannot invent an absent action or a controller that is bypassed by an earlier return. After the first capabilities work, compare a small portfolio of genuinely different policies: mobile harvesting queen, depot queen, aggressive queen-raiding workers, and mixed economy.

Keep several distinct contenders instead of discarding every strategy with a slightly lower mean in an early noisy screen. A small quality-diversity archive could track queen survival, queen growth rate and attack pressure, retaining useful specialists. Do not reward novelty at promotion time: final selection is by fresh games against a diverse opponent panel.

The six-opponent panel contains several nicked versions from one family. Those remain useful controls but are not six independent strategic styles, and their frozen old-rules behavior can become an easy benchmark. Add current-rules opponents and controlled specialists before claiming ladder strength. Report family-balanced results as well as individual matchups.

## Concrete work order for Claude

| Stage | Deliverable | Gate before continuing |
|---|---|---|
| Q0 | Separate current-rules environment; scoring/movement fixtures; refreshed map manifest | Correct engine behavior, replay scoring and native/in-process parity |
| Q1 | Minimal queen identity, recipient and split-safety adaptation | No queen donation or false child succession; full-suite baseline recorded |
| Q2 | Exact short multi-step planner; workers and queen tested separately | Legal paths, correct body/food updates, sandbox budget, fresh-game improvement |
| Q3 | Threshold bootstrap and local queen food reservation | Queen mobility/growth gain survives worker-economy costs |
| Q4 | Visible queen attacks and endpoint defense | Better wins and survival against multi-step attackers, not only old bots |
| Q5 | Scheduled delivery/depot pilot | Actual queen collection and win gain beat the chase control |
| Q6 | Small learned plan evaluator or role selector; strategic portfolio | Correct labels, whole-game evaluation, new-state collection, independent confirmation |

For Q1–Q5, use matched seeds and both sides across the refreshed ranked pool, retain the historical suite separately, and reserve fresh confirmation seeds. Diagnose with targeted states, but never promote on targeted probes alone. Count wins/draws correctly and show uncertainty grouped by games/map/opponent, not millions of correlated decisions. Keep labels, engine hashes and map hashes with every run.

If Q2 does not improve play, separate planner bugs from strategy failure: verify safe movement utilization and food gain first; then inspect endpoint deaths and queen food theft. If Q3 grows queens but loses, investigate queen survival and depleted worker control. These are distinct failure modes requiring distinct fixes.

The first release candidate should be the smallest combination of validated changes. Recheck the live rules and maps immediately before its evaluation and submission decision. No automatic upload is authorized by this document.

## Scholarly grounding and limits

- **Sutton, Precup and Singh (1999), options:** temporally extended actions provide a framework for choosing sustained behaviors. Relevant to harvest/deliver/escort/raid options; not proof that a particular role policy wins here. [Paper](https://people.eecs.berkeley.edu/~russell/classes/cs294/f05/papers/sutton%2Bal-1999.pdf)
- **Phillips and Likhachev (2011), SIPP:** reasons about safe times in dynamic environments. Useful inspiration for endpoint occupancy and scheduled queen routes. Its standard guarantees do not directly apply to partially observed adversarial dragons and a moving self-body. [Paper](https://www.cs.cmu.edu/~maxim/files/sipp_icra11.pdf)
- **Mouret and Clune (2015), MAP-Elites:** retains high-performing solutions across behavior descriptors. Relevant to searching multiple strategic families rather than one CMA basin; the choice of descriptors and noisy game evaluation still need care. [Paper](https://arxiv.org/abs/1504.04909)

The decisive evidence in this review is the current rulebook and the inspected decision pipeline. The proposed queen economy, depot system and tactical specialization are testable hypotheses. None has been implemented or shown to reach top 100 yet.
