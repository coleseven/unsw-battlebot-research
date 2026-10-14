# Next steps for Claude — 4 October 2026

> **Subsequent update, 5 October:** the user confirms v12x uploaded **2026-10-05 10:04:34** (timezone unspecified). v12x supersedes the live-version uncertainty in this dated review. Later experiments in FEATURE_EXPERIMENT.md supersede completed or rejected recommendations here; v11t remains the historical control for the analysis below. Normalize server timestamps and verify submission identity before attributing games around the upload cutoff.

## Decision

**Keep v11t as the local control. Diagnose worker food production first, then test a short harvesting-and-return planner. Investigate late collection separately. Do not spend the next cycle widening queen danger masks or retuning the same safety parameters.**

This is a research handoff, not a claim that the proposed changes work. The goal remains top 100; local win rates cannot establish that rank. This review inspected the completed C9–C11 work through commit `61990c9`, the current C++ decision code, saved game outcomes, and current official documentation. No bot code, matches, training, or submissions were changed. The live upload is not verified here: v11q is the latest recorded live version, while v11t is the recommended local candidate. Record the actual submission identity before attributing new website games to either.

Read this before the older queue. The 3 October runtime/map refresh and corrected queen search have already happened. Do not restart them. [PROJECT_HISTORY.md](PROJECT_HISTORY.md) preserves the earlier history through C8; this handoff covers later evidence without changing that historical cutoff.

## 1. What the overnight results actually establish

| Experiment | Baseline wins | Candidate wins | Decision |
|---|---:|---:|---|
| C9 paid-sprint threat expansion, 680 games each | 394 | 370 / 373 | Reject both masks |
| C10 trapped worker avoids killing queen, 1,122 each | 647 | 645 | Keep off; queen survival is not the objective |
| C11 nearby worker bodyguard, 680 each | 385 | 381 / 379 | Reject these implementations |

Earlier C7 also failed to confirm refuge, and C8 rejected the tested split-exit restrictions. Do not automatically bundle C10 because it sounds logically safe: it gained 15 queen-survival outcomes but did not gain wins. If a later candidate creates a specific interaction, evaluate that interaction explicitly.

Two conclusions in the overnight narrative need narrowing:

1. Losing with wider hard danger masks does not prove queen improvement is exhausted. Those masks collapse plausible and merely possible threats into the same forbidden cells. They test a particular decision representation, not all threat reasoning.
2. Both-queens-dead play is not the weakest outcome class by win rate or net losses. Elimination is substantially worse. Classes describe the endpoint and can change under a candidate; they are not causal labels.

### Recount of the saved C10 baseline

The recount gives elimination precedence, then separates queen states. It does not pool different experiment panels.

| Terminal class | Wins | Losses | Net wins |
|---|---:|---:|---:|
| Elimination | 71 | 135 | −64 |
| Both queens dead | 294 | 254 | +40 |
| Only our queen alive | 244 | 0 | +244 |
| Only opposing queen alive | 0 | 46 | −46 |
| Both queens alive, equal queen length | 19 | 19 | 0 |
| Both queens alive, unequal queen length | 19 | 21 | −2 |
| **All games** | **647** | **475** | **+172** |

Of the 254 losses with both queens dead, **57 finish with more total length** and **64 lose longest length by 1–5**. These groups may overlap. The remaining 197 have no total-length advantage. Thus there is a real conversion opportunity, but a blanket “feed more” response cannot explain the majority of these losses. Total length at the end also does not reveal whether earlier food acquisition or later deaths caused the deficit.

Each map below has 66 games in this panel. These are descriptive priorities, not stable estimates of ladder performance:

| Map | Overall W/L | Main loss concentration |
|---|---:|---|
| Stripes | 19/47 | 45 elimination losses |
| Trophy | 34/32 | 26 elimination losses |
| Dilemma | 25/41 | 26 elimination losses |
| Tower Defense | 26/40 | 12 elimination, 24 both-dead losses |
| weakhold | 24/42 | 30 both-dead, 6 elimination losses |
| Portals | 36/30 | All 30 losses both queens dead |
| Islands | 37/29 | All 29 losses both queens dead |
| Schooltime | 49/17 | All 17 losses both queens alive at equal queen length |

The earlier C5 and C7 baselines also have large elimination deficits (61/123 and 73/156 respectively). That recurrence makes early survival/economy worth investigating before another universal late-game policy. It does not prove an economy fix will work.

Evidence: [outcome audit](results/next-steps-20261004/outcome-audit.json), [loss case index](results/next-steps-20261004/diagnostic-case-index.json), [experiment log](FEATURE_EXPERIMENT.md). The index includes map, opponent, seed, side, ending length, and replay location for targeted review.

## 2. First task: make comparisons trustworthy

**Reporting repair, not a new game batch.** `bcsim/ablate.py` still partitions maps through exact membership in the old `CURRENT_POOL`. Only five names in the 17-map C-series suite match: trophy, queen_of_spades, default, schooltime, weakhold. The other twelve are classified elsewhere. Overall totals remain usable; the purported current-pool subtotal is not the current 17-map suite. `results/queen_stats2.py` lowercases names but still misses the Dilemma/Prisoners Dilemma and UNSW/Around UNSW aliases.

Claude should:

1. Derive the suite from each saved run's frozen plan. Canonicalize aliases explicitly, preserve raw names, and assert every played map is assigned exactly once. Do not silently overwrite historical suite definitions.
2. Report all 17 current local layouts individually and their equally weighted aggregate. Replace stale “15 maps” headers. Label an online pool only if actually sampled or documented; the local suite alone does not prove online selection frequencies.
3. Make direction unambiguous: adding a candidate feature versus removing an incumbent feature. “Harmful (drop)” labels are misleading for feature-addition runs.
4. Regenerate C5–C11 summaries from saved records and compare totals with this audit. No rerun is needed for reporting errors.
5. Freeze `versions/v11t`, its parameter file, source/build hashes, engine and map hashes, opponent hashes, seeds, and flags. The shared `cppbot/params.hpp` template has different defaults from the frozen tuned v11t parameters. Do not accidentally replace the control's parameters while introducing a switch.
6. Check that all new switches off reproduce the control's actions on saved states before spending on games. Run meaningful transition fixtures for new mechanics, rather than testing that constants equal themselves.

The current official Elo description uses submission ratings with map offsets and aggregates team rating across current maps. It also accounts for first-move advantage. This strengthens the case for per-map, both-side evaluation; it does not give a conversion from a local percentage gain to rating points. See [official rating documentation](https://game.battlecode.au/docs/elo). The latest listed rules/maps release inspected was 1.2.9; preserve the already updated local setup and record future changes rather than mixing versions. See [updates](https://game.battlecode.au/updates).

## 3. Bounded replay diagnosis before implementation

Create `results/next-steps-20261004/DIAGNOSTIC_FINDINGS.md`. Start with **24 cases**, selected deterministically before viewing:

- Twelve elimination losses: four each from Stripes, Trophy, and Dilemma; spread across opponent families and sides, use the case index, and avoid choosing only dramatic examples.
- Six both-dead losses: three with a total-length advantage and three without, across Portals, Islands, weakhold, and Tower Defense where available.
- Six nearby controls: baseline wins on the same map and opponent where available, otherwise the same map and opponent family. These are descriptive controls, not matched causal experiments. Include Schooltime equal-queen losses in a second small pass if collection is pursued.

For elimination, reconstruct the first 120 rounds and the interval leading to the collapse. Record natural pearls collected separately from recycled/death pearls; worker count and living worker-turns; productive spawn occupancy; ready pearls passed over; travel without collection; blocked exits; split timing; and the first persistent length/population deficit. Use legal replay observations to reconstruct what each dragon could have known. An analyst may inspect hidden state for diagnosis, but candidate decisions and teacher features must not receive it.

For late losses, record when the collection target becomes known, food dropped, food actually collected by the intended recipient, competing pickups, recipient death, missed turns due to congestion, and longest-length margin through time. Distinguish “could not produce”, “could not deliver”, and “delivered then died”. Do not infer the cause from the final scoreboard alone.

**Decision gate:** proceed with harvesting if repeated missed collection/return opportunities precede collapse in at least two target maps and appear less in controls. If deaths precede the food deficit, investigate the concrete collision/territory failure instead. The threshold is a practical diagnostic rule, not a significance test. Stop at 24 cases unless a specific ambiguity needs more; do not build an endless replay-analysis project.

## 4. First behavior experiment: worker harvesting and return cycles

### Why this differs from failed food-weight changes

In [cppbot/v6_brain.hpp](cppbot/v6_brain.hpp), `search_one` carries `tm.food = max(tm.food, food_value(...))`. Its food search term rewards the best encountered food value rather than cumulative harvest along a route. The cell-keyed search also compresses arrivals that can have different headings, body geometry, and return prospects. Other features do reflect local food, so this is not a claim that the entire policy ignores multiple pearls.

The hypothesis is narrower: **a worker sometimes needs to choose a short sequence that collects twice or returns to a replenishing patch, even when its first step has a lower individual food score.** More hub pull, more travel, and universal camping have already been tried. Do not reproduce them with a new name.

### Minimal candidate

Add an optional worker-only local macro evaluator, initially restricted to productive patches and the early economy window. Include the incumbent action as an explicit candidate and retain it on ties or uncertain simulation. Enumerate a small set of legal collect-and-return routes over roughly 2–4 future turns; benchmark a fixed node cap. Replan every turn, execute only the first action, and never commit blindly to the entire route.

State must distinguish heading, occupied trail, growth, consumed pearls, and elapsed turns. Count each existing pearl once. Use observed spawn countdowns only according to verified engine semantics; represent uncertain future spawn value conservatively. Do not count a pearl every time the route revisits its tile. Respect turn-start free movement, paid movement cost, portal transitions, and action ordering. Use known terrain memory where legal; an offline map identity must not reveal unseen enemy occupancy or future random outcomes. The official [vision specification](https://game.battlecode.au/docs/vision) describes the limited wrapped view; portal travel does not grant remote vision.

Score **collectible cumulative food minus travel expenditure and trapping risk**, with a terminal continuation value from the existing evaluator. Initially preserve the incumbent split decision: test whether worker movement improves before opening a second axis of split policy. Log when the ordinary split early return prevents the planner from running. If that dominates missed opportunities, make “harvest one turn versus split now” a separate subsequent experiment, with an explicit population cost.

A short repeated route is allowed only when it predicts another collection and remains escapable. There should be no unconditional claim on a patch, permanent camper role, new beacon protocol, or map-specific opening script in the first candidate. Existing occupancy and reservations can discount teammate competition; do not solve multi-agent scheduling at the same time.

### Instrumentation and gates

Log activation frequency, candidate/incumbent predicted food, realized food over the next few turns, route abort reason, worker survival, paid segments, and CPU points. Compare natural food yield per living worker-turn alongside total yield and worker population: either ratio alone can look good while the team gets worse.

First require legal transitions and actual realizable food predictions on saved examples. Then screen one setting, not a weight grid. Continue only if the expected mechanism moves in the right direction and all-map wins are promising without a new elimination deficit. If yield improves but wins fall, inspect population and access competition before tuning weights. If activations are too rare or predictions are systematically wrong, stop and record why.

## 5. Second experiment: convert available length into a surviving collector

Pursue this only after the late-loss diagnostic establishes the bottleneck. The 57 both-dead losses with more total length are a tractable starting set, not proof that all 57 are recoverable. Schooltime's equal-queen outcomes are another useful target because secondary scoring matters while both original queens remain alive.

The existing `visible_target`/`should_feed` logic relies on local target information and geometry. Seeing body segments does not reveal full dragon length. Prior broader feeding and reach proposals failed. The new question is **whether a specific donation can be picked up by the intended recipient at the right time**, not whether to increase the amount donated.

For a first candidate, require a fresh identifiable recipient, a short legal pickup sequence, and a drop tile the recipient can reach under actual turn order. Account for donor action timing, other workers, growth occupying the exit, and recipient continuation after pickup. Preserve uncertainty when the visible body is incomplete. Do not drop food because a stale beacon says a king exists. Do not starve the expansion front to raise a collector that promptly dies.

Choose exactly one intervention based on evidence:

- Food never reaches the collector: pickup-aware drop placement/timing, keeping the baseline donation volume.
- Food arrives but the collector dies: short collector escape validation around growth, keeping the baseline feeding rule.
- Collection begins too late despite persistent surplus: test a modest activation trigger based on observed surplus and time remaining; do not start with a broad age sweep.

Measure pickup completion, wasted donation, surviving longest length, lost worker production, and wins. End-state longest length alone is not a promotion metric. Do not combine this with harvesting until each is evaluated separately.

## 6. Third experiment: prevent entering a proven queen trap

This is lower priority than worker economy, but not abandoned. The death audit found 355 of 358 wall deaths had no legal move at the final decision. That directs attention to earlier entry/growth decisions. It does not establish that splits are harmless: C8 only rejects its particular exit-count rule.

Build a small regression corpus from the recorded Maze corridor, Portals tail, and friendly obstruction cases in [LIVE_GAME_REVIEW_2026-10-03.md](LIVE_GAME_REVIEW_2026-10-03.md). Validate exact trail/portal and growth transitions first. Current corrected queen search uses a local static representation in places; portal-connected trails and future growth deserve specific examples, not another global horizon increase.

Try an event-triggered viability check **before entering a narrow known corridor or taking growth that closes an exit**. On those rare states, compare the incumbent with available alternatives over a bounded 6–8-turn deterministic own-body rollout. Unknown terrain is uncertainty, not a promised escape. A local proof is conditional on modeled occupancy; moving opponents cannot be assumed static or cooperative. An override requires a demonstrable incumbent trap and a legal better continuation. Otherwise preserve the incumbent.

Do not mark every enemy's maximum paid reach forbidden. If opponent response reasoning is later needed, evaluate a few distinct responses with separate scores rather than one union mask that erases all distinctions. This is a new representation experiment only after transition correctness and the corridor mechanism pass. Do not simultaneously revive refuge, deeper generic Q9 search, and split restrictions.

## 7. Where a neural network belongs

**Not on the critical path yet.** R4 improved imitation without improving games; R5's residual approach failed. A larger model or the old GTX 980 does not fix a poor target or simulator mismatch.

If the harvesting or trap teacher is useful but expensive, collect its state/action comparisons at actual activation points. Train a simple linear ranking baseline first; only then test a small MLP on the same legal features. Suitable targets are short-horizon realized harvest, conditional trap outcomes, and preference between two candidate routes. Keep food and survival targets separate so a single scalar does not hide the tradeoff. Avoid attributing a full-game win to every local action.

Split data by complete games, seeds and maps; never randomly split adjacent states from the same game across train/test. Include incumbent-selected and alternate actions, uncertain labels, and failed candidate routes. Report calibration and ranking error, then frozen full-game tests. Deploy only as a gated evaluator with the incumbent fallback. A small CPU model is sufficient to begin; no separate-machine setup or fresh self-play system is justified before a useful teacher exists.

## 8. Evaluation sequence and promotion rules

1. **Freeze control and hypotheses.** Keep tuned v11t parameters. Record the primary win-score metric, mechanism metrics, stop conditions, and candidate settings before games.
2. **Transition checks and replay probes.** Verify the new mechanics and disabled equivalence. Small map probes are diagnostics, never a promotion claim.
3. **One bounded screen per hypothesis.** Suggested panel: 17 maps × 2 sides × 2 fresh seeds × 6 opponents = **408 games per variant**. Select opponent families before seeing results; include current queen-capable controls and distinct external behavior where available. Budget and guard the batch.
4. **Confirm only a selected finalist.** 17 × 2 × 3 new seeds × 10 opponents = **1,020 per variant**, or 1,122 with 11 opponents. Do not reuse screening seeds as independent confirmation. Include direct v11t comparison. Keep opponent identities and family weights fixed.
5. **Report paired deltas and uncertainty.** Win=1, draw=0.5, loss=0; distinguish percentage-point win-score changes from signed-outcome deltas. Pair baseline/candidate by map, opponent, seed, and side. Bootstrap blocks preserving both sides and opponent results for a map/seed; show per-map and per-family results too. Small seed counts and related opponents limit confidence regardless of the interval.
6. **Require practical benefit.** Aim for at least roughly +2 percentage points on confirmation as a working hurdle, not a magic statistical boundary. A smaller gain needs stronger repeatability and low implementation cost. A noisy gain with a plausible mechanism remains unconfirmed. Do not keep testing until an interval becomes positive.
7. **Check opponent concentration.** Several nicked versions are one related family, not independent strategic diversity. Show equal-family sensitivity alongside the frozen panel aggregate. The test panel cannot establish performance against unavailable top teams.
8. **Check cost and packaging.** Sandbox worst-case activated states with comfortable headroom under the 100M limit, verify the final built artifact and flags, and preserve a rollback. One heavy job at a time, guarded, at most 12 workers. Existing v11t's recorded 8.4M maximum is not a bound for new code.
9. **Combine only proven components.** If A and B pass independently, compare base/A/B/A+B on fresh seeds. C10 stays off unless its additional contribution is explicitly tested. No simultaneous CMA-ES sweep while behavior is being evaluated.
10. **Online validation follows authorized upload.** Record submission/hash/time, map, opponent, side, and game outcome. Separate versions and rules epochs. Compare map-stratified performance over a meaningful sample; avoid reading a short rating streak as proof. No automatic submission.

## 9. Claude's next work session

Do these in order, leaving a short result at each gate:

1. Repair report coverage and regenerate saved C-series summaries. Deliver exact baseline manifest and a statement of which online version is known versus unknown.
2. Complete the 24-case diagnostic and classify whether economy loss starts with missed harvesting, combat/access loss, or split/congestion. Name the first irreversible-looking divergence, not just the final death.
3. If the harvesting gate passes, implement one bounded worker route evaluator behind an off-by-default switch. Keep queen, feeding, splitting, beacon protocol, and tuned parameters fixed for this first comparison.
4. Verify legal rollout, disabled equivalence, and sandbox cost; run the 408-game screen. Record losses and mechanism results, including failures.
5. Confirm a promising candidate on untouched seeds. If rejected, move to the diagnosed collector bottleneck; do not immediately turn the failed idea into a large tuning sweep.

Suggested deliverables: `DIAGNOSTIC_FINDINGS.md`, a frozen experiment manifest, one feature flag, a full outcome/coverage report, and an explicit **adopt / reject / unconfirmed** conclusion in [FEATURE_EXPERIMENT.md](FEATURE_EXPERIMENT.md). Update this queue only after those results exist.

The strongest opportunity supported by this review is better use of worker turns to produce and retain food, followed by more reliable conversion of existing surplus. That is a testable direction toward top 100, not a guarantee. Keep the current queen improvement while investigating the earlier decisions that determine how much useful material the team has left.
