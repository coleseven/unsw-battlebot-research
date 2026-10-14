# Overnight review and revised route to top 100

Prepared 30 September 2026, approximately 08:35 EDT / 12:35 UTC. Repository inspected at `9870b6a`. This is a follow-up to [TOP_100_RESEARCH.md](<C:/Users/Sea7/Desktop/unsw battlebot/TOP_100_RESEARCH.md>), using the completed overnight run and the experiment currently executing. No bot code, tuning configuration, or running process was changed for this review.

## What I would do next

**Let the current comparison finish. Do not launch another broad overnight CMA run yet.** The project is now testing the right small defects, but the first completed result suggests these fixes alone will not close the ladder gap. The next substantial improvement should come from better king/feeder coordination and clearer experiments that isolate opening, endgame, and map-robustness failures.

The immediate sequence I recommend:

1. Finish the current six-way comparison and retain its separate controls.
2. Evaluate the promising tune checkpoints against the baseline on **matched original and perturbed maps**, because the current comparison omits the latter.
3. Treat the hub-spacing fix as a small, uncertain competitive change, not the main breakthrough.
4. Make the next structural experiment **fresh, identity-bound king announcements and verified food recipients**. Follow with reachable drop placement and collection priority.
5. Replace another large parameter sweep with **phase-specific interventions, an incumbent checkpoint, and selective extra evaluation of promising candidates**.
6. Keep the spare machine on refreshed evaluator data and small-model experiments. The overnight run does not supply new evidence that a full reinforcement-learning rewrite is the fastest route to top 100.

## 1. What happened overnight

The v12 tune at [results/20260929-201541-tune-6e4812](<C:/Users/Sea7/Desktop/unsw battlebot/results/20260929-201541-tune-6e4812/plan.json>) completed all **12 generations**, with **12 sampled candidates plus the distribution mean per generation**: **156 evaluations and 15,600 games**. Logged game-running durations sum to about **10.6 hours**; total elapsed time also includes setup and scoring.

It started from v10h, with 17 tunable dimensions, one engine seed per generation, five opponents, and one original-or-perturbed map chosen from each current-pool family. Four of those five opponents belong to the nicked family. Its objective was mean aligned score plus 0.25 times the worst map's score.

| Generation | Distribution-mean objective F | Wins / 100 | Mean aligned score before worst-map penalty |
|---:|---:|---:|---:|
| 0: baseline parameters | −0.0627 | 55 | +0.0449 |
| 1 | +0.0863 | 63 | +0.1694 |
| 2 | −0.0120 | 55 | +0.0633 |
| 3 | −0.1062 | 53 | −0.0117 |
| 4 | −0.0459 | 56 | +0.0521 |
| 5 | +0.0802 | 61 | +0.1389 |
| 6 | −0.2165 | 50 | −0.0354 |
| 7 | −0.1543 | 53 | +0.0178 |
| 8 | −0.1656 | 46 | −0.0636 |
| 9 | −0.1858 | 51 | +0.0032 |
| 10 | −0.2713 | 44 | −0.1174 |
| 11 | −0.2798 | 47 | −0.0898 |

Source: [evaluations.jsonl](<C:/Users/Sea7/Desktop/unsw battlebot/results/20260929-201541-tune-6e4812/evaluations.jsonl>) and [run.log](<C:/Users/Sea7/Desktop/unsw battlebot/results/20260929-201541-tune-6e4812/run.log>). These are training-condition measurements, not held-out results.

**The late deterioration is a warning, not proof that the final bot is worse.** Seeds and selected map variants changed between generations. There was no frozen baseline re-evaluated on each generation's conditions. Consequently, a harder generation and a worse policy cannot be separated from this curve alone. Removing the worst-map penalty would not make the observed deterioration disappear: the unpenalized score also fell, but it has the same confounding.

The export is explicitly labeled **“last distribution mean”** in [final-073704.json](<C:/Users/Sea7/Desktop/unsw battlebot/results/20260929-201541-tune-6e4812/final-073704.json>). The tuner selects that by construction; “recommended” does not mean “beats the baseline on confirmation data.” See [selection logic](<C:/Users/Sea7/Desktop/unsw battlebot/bcsim/tune.py:431>).

### What the final candidate changed

| Parameter/behavior | v10h control | Generation 5 mean | Final evaluated mean |
|---|---:|---:|---:|
| Food weight multiplier | 1.00 | 1.90 | 2.90 |
| v3 learned-score multiplier | 1.00 | 1.37 | 1.64 |
| Attack/trade multiplier | 1.00 | 2.00 | 2.19 |
| Feeding attraction multiplier | 1.00 | 1.47 | 2.08 |
| Population cap | 56 | 55 | 52 |
| Population floor | 24 | 23 | 21 |
| Small-map split cutoff | 450 | 407 | 384 |
| Large-map split cutoff | 321 | 363 | 330 |
| King announcement round, before large-map shift | 300 | 298 | 250 |
| Minimum king-announcement length | 8 | 10 | 11 |
| Big-feed round, before shift | 430 | 416 | 400 |
| Large-map feeding shift | 40 | 38 | 46 |

These changes are strongly coupled. The final candidate is not just “better food weights”: it changes population rebuilding, king eligibility, and the timing of conversion simultaneously. Raising the minimum beacon length can reduce access to a recipient even while the beacon round moves earlier. On large maps, effective big feeding starts at round **354** in the final candidate, versus **390** in the control, because the shift is subtracted.

I checked that the current ablation's `v12tune` and `v12gen5` parameter overrides match their actual saved checkpoint headers. I found no mismatch in those exported values.

## 2. What is running now

The active process is `bcsim.ablate results/20260930-073741-ablate-f5f4ba --run --workers 12`, with its worker processes present. It is a **validation/ablation job, not another CMA generation**. Its [plan](<C:/Users/Sea7/Desktop/unsw battlebot/results/20260930-073741-ablate-f5f4ba/plan.json>) contains:

| Variant | Purpose | Status at the detailed snapshot |
|---|---|---|
| `base` | v10i, intended to retain v10h behavior with new switches off | Complete: 540 games |
| `hubsep` | Enable corrected wrapped-distance spacing between learned hubs | Complete: 540 games |
| `v3portal` | Replace portal actions' local v3 score with the mean of ordinary actions | In progress; final inspected progress line 384/540 |
| `both` | Both defect treatments | Pending |
| `v12tune` | Final evaluated overnight mean | Pending |
| `v12gen5` | Generation-5 mean | Pending |

The planned total is **3240 games**: six variants, six opponents, 15 layouts, both sides, three fresh seeds (`191001–191003`). It runs variants sequentially. Counts will advance after this timestamp; incomplete variants have no final result here. The inspected completed base and hub runs had no recorded game errors.

This is a sensible response to the previous report: the two defects are now implemented behind independent switches, and tune candidates are being tested on the same conditions. Do not duplicate those implementation experiments or infer portal performance from whichever games happened to finish first.

### The completed hub fix is small and mixed

| Scope | Control wins | Hub-spacing wins | Difference |
|---|---:|---:|---:|
| Current ten-map pool | 235/360 | 238/360 | **+3 wins; +0.83 percentage points** |
| All 15 maps | 339/540 | 342/540 | +3 wins |

On the current pool, paired aligned-score change is **+0.0115**. My fixed-map paired-seed bootstrap gives approximate 95% intervals of **−0.83 to +2.78 percentage points for wins**, and **−0.0095 to +0.0336 for aligned score**. These describe the fixed opponent/map sample, with only three seed blocks per map; they are not broad generalization guarantees.

| Affected map | Control wins / 36 | Hub-spacing wins / 36 |
|---|---:|---:|
| Autarky | 32 | 30 |
| Prisoners Dilemma | 13 | 12 |
| Slithery Fight | 18 | 19 |
| Portals | 18 | 23 |

The other current-pool maps had identical results. Across the pool there were 29 changed win/loss outcomes, netting three extra wins: this is not an entirely inactive change. It redistributes behavior, with Portals helping and Autarky hurting in this sample. It produced **no net additional wins against nicked v92** in the current pool.

**Interpretation:** the geometric correction is valid, but its competitive gain is not established. Do not immediately gate it by map name because of this small table; that would fit the test set. Measure the actual number and usefulness of distinct selected patches, then confirm on fresh seeds if the combined variant looks promising.

Sources: [base margins](<C:/Users/Sea7/Desktop/unsw battlebot/results/20260930-073741-ablate-f5f4ba/runs/base/margins.json>), [hub margins](<C:/Users/Sea7/Desktop/unsw battlebot/results/20260930-073741-ablate-f5f4ba/runs/hubsep/margins.json>).

### The portal test answers a narrower question than “are portals fixed?”

The new [portal treatment](<C:/Users/Sea7/Desktop/unsw battlebot/cppbot/v6_brain.hpp:476>) gives a portal action the average v3 score of available ordinary moves, or zero when none exist. This avoids using the adjacent neighborhood as if it were the remote destination and retains a comparable score scale when ordinary alternatives exist.

It **does not estimate the destination's value**. A loss would reject this neutral replacement, not prove that the old portal features were semantically correct. A win would support removing the misleading local comparison, not establish that destination-aware planning is solved. The next version, if warranted, should represent remembered landing information and uncertainty explicitly, with its own calibration.

## 3. The ladder has not shown a breakthrough overnight

The refreshed public snapshot was **rank 163, Elo 1613**; rank 100 was **1699**, an **86-point gap**. The earlier report recorded rank 149 at 1624. That is an 11-Elo decline and a changing rank distribution, not evidence that the unsubmitted overnight candidate caused anything. The last version you explicitly confirmed uploaded was v10; this review does not assume that changed. [Team 777](https://game.battlecode.au/teams/590), [leaderboard](https://game.battlecode.au/leaderboard?search=777), [top-100 cutoff](https://game.battlecode.au/leaderboard?page=10)

I inspected **16 new ranked battles / 80 games**, selected from the first three battle-list pages after the previous cohort cutoff. They run from **02:20 to 12:13 UTC on 30 September** and total **37 wins, 43 losses (46.25%)**. This is the inspected cohort, not a claim that every overnight game was captured or that its upload version is known.

| Map | New wins / games |
|---|---:|
| Default | 2/8 |
| Portals | 2/7 |
| Trophy | 3/9 |
| Trauma | 3/9 |
| Schooltime | 3/8 |
| Slithery Fight | 3/6 |
| Devil | 6/11 |
| Prisoners Dilemma | 5/9 |
| Autarky | 6/8 |
| Queen Of Spades | 4/5 |

The same ten map names appeared. Samples are too small to make fine rankings, but the earlier weaknesses have not disappeared. This morning's review used public game metadata for these 80 outcomes, not a new full replay-mechanics audit.

The local control also shows why aggregate wins can mislead. Its current-pool results were **55/60 against v7-base**, **50/60 against leviathan3**, but **21/60 against nicked v92**, **30/60 against v75**, **36/60 against nicked_lab**, and **43/60 against v44**. A candidate can improve an already easy matchup and look better overall while leaving the difficult strategic gap intact. Opponent families should be reported separately; the six builds are not six independent families.

## 4. The most important evaluation gap

**The overnight tune trained on original and perturbed layouts, but the current ablation tests the 15 original layouts only.** That makes the current run useful, but insufficient to judge robustness or fully explain the tune's behavior.

For the final mean, its evaluated original-map slots averaged about **+0.150 aligned score**, while its perturbed-map slots averaged **−0.330**. Those slots contain different map families, so this is not a controlled estimate of a perturbation effect. It is a strong reason to perform the missing matched comparison. At generation 5, the corresponding slot averages were about +0.120 and +0.151.

### A targeted recovery test

After the current run, compare **v10h-equivalent control, generation 5, and final mean** on:

- All 15 original layouts, both sides.
- The ten existing perturbed layouts, also both sides.
- The same opponents and engine seeds for every candidate.
- A later confirmation set with newly generated perturbations, rather than repeatedly selecting against `_p1`.

One bounded starting design is 25 layouts × 2 sides × 2 seeds × 4 selected opponent builds = **400 games per bot, 1200 games for three bots**. Choose diverse opponent behavior and retain a strong nicked representative. This is a diagnostic budget, not a claim that two seeds establish small effects. The original 15 retain full-suite coverage; extra layouts measure robustness separately.

Also reproduce the final generation's exact sampled map/seed conditions with the frozen baseline. That directly answers whether its low score arose primarily from hard conditions or policy drift. If doing this as a small diagnostic, do not present it as a substitute for the full suite.

Report original-pool and perturbed-pool deltas separately. Until live map distributions are better understood, show sensitivity to several mixture weights rather than declaring a 50/50 synthetic mix to be the ladder. The perturbation generator changes rates at existing spawners; it does not cover arbitrary moved spawns or topology changes. [Perturbation implementation](<C:/Users/Sea7/Desktop/unsw battlebot/bcsim/perturb_maps.py:56>)

## 5. Better methodologies for the next iteration

### A. Keep an incumbent and distinguish training from promotion

Maintain a frozen **incumbent** that changes only after paired confirmation. Save promising mean checkpoints, but call them candidates. The final generation should not automatically replace a better confirmed policy.

During future tuning, evaluate the incumbent on each generation's shared conditions. This adds approximately one candidate's evaluation cost: with 12 samples and a mean, about **7.7% more games**. It makes progress interpretable as a paired delta. Subtracting the same baseline from every candidate does **not** change their ranking within a generation; this is a monitoring and selection improvement, not a magical cure for CMA sampling noise.

Use a fixed development panel for checkpoint comparisons and a separate untouched confirmation panel. Do not repeatedly pick winners from the final test set. Keep generation 1 as an archived candidate; its high raw F alone is not a reason to add another exhaustive test before seeing the existing comparisons.

### B. Spend more games on the decisions that remain uncertain

The overnight run spent the same 100 games on every sample, including weak samples. A future experimental scheduler can screen broadly, then allocate fresh paired blocks to surviving candidates.

A conservative example: screen candidates on all 15 layouts, both sides, one seed and a small opponent panel; add seeds and families to the better candidates; run final confirmation only on the few finalists. Use fewer games, not artificially short matches, as the reduced budget. Truncating at round 200 would systematically undervalue feeding strategies that win at round 500.

This borrows the resource-allocation idea of successive halving and Hyperband. Their theory and reported savings do not transfer automatically to correlated game outcomes; predeclare stages, preserve map coverage, and keep a fresh confirmation set. [Jamieson & Talwalkar, 2016](https://proceedings.mlr.press/v51/jamieson16.html), [Li et al., Hyperband, 2018](https://www.jmlr.org/papers/v18/16-558.html)

### C. Tune fewer coupled mechanisms, with bounded excursions

After confirming a structural change, tune its own small parameter group: for example recipient eligibility, drop distance, and collection commitment. Keep unrelated attack, portal, and opening weights fixed initially.

For weight tuning, compare normalized contributions and action changes, not just raw coefficient growth. Multiplying every term in an additive action score by the same positive constant leaves its argmax unchanged. The current group tuning does not multiply every term uniformly, but its simultaneous increases can still obscure which relative preference changed.

Use modest local bounds around the incumbent as the next baseline optimizer experiment. Do not automatically reuse covariance learned under the previous opponent/objective distribution after changing the strategy. Compare a fresh local search with a warm covariance only if that choice matters empirically. CMA remains useful; the goal is to make each run answer a smaller question.

### D. Separate opening and endgame interventions

Use two classes of policy experiment:

**Opening-only changes:** modify target allocation, map confidence, or early portal exploration for the first 100–150 rounds, then revert to the incumbent. Record useful-region access, environmental food intake, population, and full-game wins. Trophy/Trauma are the diagnostic priorities, while all maps remain in evaluation.

**Endgame-only changes:** keep the incumbent's behavior identical until a chosen round, then enable a coordination or tactical change. With fixed seeds and opponents, the shared prefix gives a much cleaner comparison of conversion from the same starting economy. This can be done by replaying the common prefix; it does not require inventing a simulator snapshot API. Verify prefix identity before claiming the intervention is isolated.

Apply this to late king protection rather than reviving universal early protection. The existing failed length-4 protection experiment changed the economy before it had developed. A narrowly gated late-game intervention asks a different question.

### E. Make each feature prove it affects the intended decisions

Before another overnight campaign, collect a small diagnostic set with decision-level measurements:

| Feature | Mechanism metric | Failure that would change the next step |
|---|---|---|
| Hub separation | Distinct productive patches selected, actual route choices | Geometrically separate hubs lead to the same region or have no useful resources |
| Portal treatment | Portal-entry decisions changed, landing outcomes, information age | Neutral scoring just adds a blanket portal bias |
| King protocol | Correct recipient ID, source age, time chasing invalid positions | Relays keep a dead or moved target fresh |
| Feeding | Food delivered to intended surviving lineage, stolen/uncollected food | More sacrifices do not yield more winning length |
| Tactical search | Saved valuable length and successful cheap trades | More survival sacrifices too much collection or slows the judge |

Do not confuse this with optimizing the proxy instead of wins. Mechanism metrics explain why a feature worked or failed and prevent repeated blind retuning.

## 6. Strategic changes with the best remaining rationale

### First: make king identity and freshness reliable

The two newly added switches do not change the existing king protocol. Its relay timestamp still tracks reception rather than the original announcement, and beacon feeding can still associate a nearby friendly head with a king without matching identity. Those remain concrete reasons to mistrust the information used by expensive sacrifices. See [current king-message logic](<C:/Users/Sea7/Desktop/unsw battlebot/cppbot/v6_brain.hpp:803>) and the detailed source analysis in the earlier report.

The next candidate should preserve original announcement age across relays, carry a recipient ID, use deterministic election ties, and invalidate locally contradicted locations. Test king death, movement, stale relay loops, and emergency-split succession. It should change the correctness of target selection before tuning how strongly feeders are pulled toward that target.

This recommendation does not assert that these failures occur in most live games. Public sonar payloads are redacted in the inspected replay format, so local diagnostics are needed to measure their incidence.

### Second: optimize collection, not the number of sacrifices

Replace “a large teammate is nearby” with “this recipient can collect useful food before the deadline.” The drop decision should consider the feeder's actual corpse cells, traversable routes, recipient facing, nearby competition, and remaining rounds. Give the recipient a bounded collection commitment so it does not continue ordinary foraging past the offered food.

A rough design principle is to compare expected useful pearls delivered with the feeder's alternative contribution and the risk to the recipient. A length-L death creates at most `ceil(L/2)` corpse pearls; it does not donate L length. The value of those pearls is especially high when they change the final longest survivor, and low when they are stranded or taken by another small worker. [Official death rules](https://game.battlecode.au/docs/death)

A useful follow-up is **local recipients by reachable region**. On a large or portal-divided map, forcing every feeder toward one globally announced king may waste the remaining game. Compare choosing a verified local recipient against a distant larger king using estimated delivery time. Consolidate regions only when travel can pay off. This is a new hypothesis, not a measured improvement, and should follow protocol correctness rather than be bundled with it.

Food accounting must follow split lineage. A newborn can inherit almost all of a trapped king's length; counting only the final dragon ID's direct meals falsely makes successful transfers disappear. Likewise, raw pearl counts include recycled corpses. The earlier 155-game audit found 22 losses with more final total length than the opponent: the objective is converting that available strength, not increasing a misleading intake statistic.

### Third: selective late-game tactics

After a verified king exists, use accurate short lookahead for threats and emergency splits. Model facing, current body, consumed food, turn order, and short sprint costs. Spend this compute on valuable or decisive situations first.

The old beam remains disabled and contains the previously identified tail-rule/food-state limitations. Increasing its depth is not an appropriate next test. Preserve the swarm's productive risk-taking outside the valuable-dragon cases and verify both judge cost and full-game wins.

### Fourth: improve opening decisions with better evidence

The v10g map-book change remains the best replicated existing structural gain: the earlier two runs improved current-pool wins from 398/720 to 463/720. Preserve it as a reference rather than letting it disappear into a bundle of uncertain changes.

For the remaining weak openings, inspect whether founders reach productive regions and whether multiple dragons choose redundant routes. Test target-local crowd estimates and stable route allocation only when those diagnostics support them. The already tested global hub-gradient change did not establish a reliable gain; changing its coefficient again is lower priority than diagnosing where the route or resource belief is wrong.

## 7. How to interpret the current run when it finishes

| Result | Recommended response |
|---|---|
| Final mean clearly wins on originals | Run the missing matched perturbation check before promotion; do not infer robustness from the original-map gain |
| Generation 5 wins; final mean loses | Preserve generation 5, confirm it, and add incumbent/checkpoint selection before another tune |
| Neither tune candidate wins | Keep the control; concentrate on protocol and collection changes instead of another unrestricted sweep |
| Portal treatment wins; hub fix is inconclusive | Confirm portal alone; compare the combination without assuming the hub correction adds competitive strength |
| Hub or portal fixes lose | Separate semantic correctness from this particular policy treatment; inspect decision changes, then redesign or defer |
| Combination wins but individual changes do not | Treat interaction as a new finding and confirm the exact combination on fresh conditions |
| Gains come primarily from leviathan3/v7-base | Inspect stronger-family results and refresh the opponent mix before calling it progress toward top 100 |

A useful promotion gate is a positive, practically meaningful paired **win-score** gain on fresh current-pool conditions, reasonable original/perturbed robustness, no material opponent-family regression, and passing judge stress checks. A wide interval means “not established yet,” not “no effect.” The previous report's scholarly sources on uncertainty, opponent mixtures, and learned evaluators still apply; this morning's evidence mainly strengthens the case for better experiment design.

## 8. A bounded next work package

1. **Finish the existing 3240-game job.** Do not stack another heavy process beside its 12 workers.
2. **Write a decision table for the six candidates**, using current pool, guard maps, opponent family, actual wins, and paired uncertainty. Archive all results, including failures.
3. **Run the missing robustness comparison** for only the finalists/control, including a matched diagnostic of the final generation's conditions.
4. **Implement and test king identity/freshness as its own feature**, followed by recipient validation. These are proposals for later implementation; no code was changed here.
5. **Run endgame-only collection experiments** and a separate opening diagnosis. Combine only independently promising changes, then test the combination again.
6. **Use the spare GTX 980 machine for audited data and a refreshed compact ranker.** Keep current public replay missingness explicit. Do not divert the main evaluation machine into an unbounded RL project before the incremental experiments answer their questions.

The working target is a confirmed improvement over the v10h/v10g controls against the difficult current-pool matchups. That provides a credible bridge from approximately 1613 toward the current 1699 top-100 boundary; it does not imply a guaranteed Elo gain or timetable.

## Evidence notes

- Source state: commits `9e3ee3e` (two defect switches) and `9870b6a` (overnight result/current ablation), plus the exact run files linked above.
- Hub intervals: 10,000 bootstrap resamples, random seed 300926; maps held fixed, paired seed blocks resampled within each map, both sides/all six opponents retained together. With three seeds and related opponents, these intervals should not be treated as broad certainty.
- The active run was inspected through process commands, completion files, and its log. It was neither paused nor modified. The portal count is a timestamped progress observation, not a final score.
- New ranked battle IDs inspected: 704602, 703291, 699155, 694793, 693312, 691364, 688253, 682728, 677766, 672304, 670821, 667140, 665127, 662067, 657368, 652647. Each contains five games. This cohort's upload version was not independently identifiable from public metadata.
- No new matches or training were launched. All numerical local conclusions were calculated from existing completed output; proposed methods and strategic gains remain untested.
