# 7. From v11t to v12z: access, exploration and queen sprint rams

**Completed 14 October 2026. Evidence cutoff: the saved 12 October records.** This
chapter extends the original archive, whose chapters 1–6 stop at commit `69095e5` on
3 October. It does not change that snapshot or claim to record the competition's final
standings. Read [the narrative](../../PROJECT_WRITEUP.md) for the whole story and
[the experiment log](../../FEATURE_EXPERIMENT.md) for the original running notes.

The last frozen release is **v12z**, bot hash `5a2c6685c062fff3`. The last
**user-confirmed upload** is **v12x**, reported as 5 October at **10:04:34**, timezone
unspecified. A later live cohort beginning around 7 October 23:10 UTC behaves like
v12z; that is an attribution from replay signatures, not a verified server hash.

## What changed after the original cutoff

Three changes survived the late experiments:

1. **v12s: let the queen establish the opening economy on a tiny map.** For the first
   40 rounds on maps with at most 300 cells, the queen uses the worker mover. In the
   tested 17-map pool, this affected only Stripes. It restored access to a productive
   portal pocket that v11t's safety search kept rejecting.
2. **v12x: make exploration strong enough to act when no productive target is found.**
   Walking-distance goal progress, multiplied by 30 only when a candidate search finds
   neither food nor a hub, let workers leave foodless starting zones. The successful
   bundle also included v12s.
3. **v12z: trade workers for enemy queens using sprint movement.** A worker may spend
   at most one paid step to hit a visible enemy queen this turn. The release also
   includes paid queen flight and a trapped-worker fallback that avoids our queen.

None was a wholesale replacement of the learned v3 ranker. Two broad efforts to reduce
its weight and many attempts to add generic caution failed. The important progression
was from identifying a wrong decision, to a narrow change, to held-out game evidence.

The outcome still falls short of the original top-100 aim. The saved 12 October
standings show **rank 153 of 1,001, rating 1604**. The closest recorded rank is **108**
on 3 October. These are snapshots; neither proves the best rank reached between checks
nor the final competition result.

## The laboratory was repaired before the next strategy change

The 4 October work completed two requirements from
[the previous handoff](../../NEXT_STEPS_2026-10-04.md): report repair and a frozen
control manifest. The older report compared current lowercase map stems with a stale
map-name set; only five of the 17 current maps landed in the intended subtotal. The
overall totals were valid, but the subtotals and labels were misleading.

The repair derives coverage from each run's frozen plan and canonicalizes explicit
aliases, including `dilemma` / `prisoners_dilemma` and `unsw` / `around_unsw`. It also
reports equal-map and equal-family changes and makes the sign of an added feature's
effect explicit. Regenerated C1 and C4–C11 totals agreed with the saved audit. This was
a reporting correction, not new evidence from rerunning those games.

The [v11t manifest](../../results/next-steps-20261004/v11t_manifest.json) records the
frozen source, package, engine, maps, opponents and settings. New builds were checked
with feature switches disabled against the frozen control; the common equivalence
panel was 17 maps × 2 sides × 2 opponents = **68 games**. Such agreement is a regression
check on those fixtures, not a proof of equivalence on every possible observation.

Throughout the following tables, candidate and control **each** play the stated number
of matched fixtures. Counts are wins, not candidate-versus-control head-to-head scores.
The later `pp` metric is win score with half a draw; older signed-outcome deltas have
twice that numerical scale. Intervals below are retained from the existing analyses.
They have not been adjusted for selecting among many experiments.

## C9–C11: the overnight hypotheses did not improve v11t

| Experiment | Tested mechanism | Games per variant | Candidate wins versus control | Disposition |
|---|---|---:|---|---|
| C9 | Add one or two paid sprint steps to every enemy head's forbidden reach | 680 | 370 / 373 versus 394; queens alive 188 / 183 versus 231 | Rejected |
| C10 | A doomed worker rams an adjacent enemy or dies away from our queen | 1,122 | 645 versus 647; queens alive 371 versus 356 | Neutral overall; not adopted alone |
| C11 | Workers trade with nearby enemies as queen bodyguards, radius 2 or 3 | 680 | 381 / 379 versus 385 | Rejected |

The C10 baseline contains **71 elimination wins and 135 elimination losses**, while
both-queens-dead games are **294 wins and 254 losses**. That corrected an overnight
summary that called longest-dragon play the weakest class. Elimination was the larger
net deficit in this panel. Of the 254 both-dead losses, only 57 finished with more total
length than the opponent; a universal feeding fix was not justified.

The negative C9 result did not establish that enemy sprinting was irrelevant. It tested
a particular representation: take the union of possible enemy reaches and declare those
cells unsafe. Later live evidence and an explicit sprinter opponent separated a real
threat from a harmful way of responding to it.

Sources: [outcome audit](../../results/next-steps-20261004/outcome-audit.json),
[case index](../../results/next-steps-20261004/diagnostic-case-index.json), and
[experiment log](../../FEATURE_EXPERIMENT.md).

## D1–D9: reaching food mattered more than a better harvesting route

The [24-case diagnostic](../../results/next-steps-20261004/DIAGNOSTIC_FINDINGS.md)
selected 12 elimination losses, six both-dead losses and six comparison wins before
reconstructing the replays. All 24 reproduced their recorded winner. Reconstruction
provided an analyst's full board, which must not be confused with information available
to the bot during play.

The cases changed the proposed plan. Stripes and Portals had food-access failures from
the opening. Trophy was an early population race, with similar yield per worker-turn.
Dilemma and Islands did not support the same production diagnosis. The planned
cumulative-harvesting mover therefore did not pass its intended diagnostic gate: there
was little value in optimizing a sequence of food pickups for dragons that never
reached the food in the first place.

| ID | Hypothesis and settings | N | Wins: variant / control | Outcome |
|---|---|---:|---|---|
| D1 | Goal progress by walking distance (`gp`); hub area by walking distance (`hp3`) | 408 | 236 / 221; 220 / 221 | `gp` +3.7 pp, selected; hub path rejected |
| D2 | Reserved-seed goal-path confirmation | 1,122 | 659 / 652 | +0.6 pp [−2.8, +4.1]; not retained alone |
| D3 | Trust queen portal moves; combine trust with escape-line caps 2 or 1 | 408 | 207, 218, 219 / 212 | Stripes improves, losses elsewhere; none adopted |
| D4 | Start feed travel earlier by distance to the king, capped at 60 rounds | 408 | 217 / 205 | +2.9 pp [+0.5, +5.6]; selected |
| D5 | Lower escape-line cap only when no enemy head is visible | 408 | 199, 219 / 230 | −7.4 / −2.7 pp; rejected |
| D6 | Reserved-seed feed-travel confirmation | 1,122 | 631 / 627 | +0.4 pp [−1.2, +2.0]; not retained |
| D7 | Queen acts as a worker before round 40 or 80 | 408 | 230, 222 / 221 | Round-40 setting selected |
| D8 | Reserved-seed round-40 confirmation on all maps | 1,122 | 647 / 634 | +1.2 pp [−2.4, +4.9]; not retained globally |
| D9 | Restrict round-40 worker queen to maps ≤300 cells; test Stripes on six new seeds | 132 | 53 / 25 | Retained as v12s |

**The Stripes mechanism.** v11t's queen search preferred an extra escape line at an
early fork, and treated a portal move into the founding pocket as having zero survival
because its tactical simulation followed only open in-view edges. Trusting portals
alone did not restore the opening; weakening escape preference everywhere hurt other
maps. Acting as a worker during the small-map opening restored founding without changing
the other 16 tested maps. The v12s non-Stripes equivalence check was 64/64; its sampled
sandbox maximum was 8.2 million CPU points against the 100-million budget.

This is a narrow successful workaround, not a general fix for portal-aware tactical
planning. The area threshold was chosen with known-map evidence. Future small maps
could trigger it under different conditions, so non-Stripes equivalence does not imply
unseen-map safety.

**The transport mechanism.** Across the 548 both-dead C10 baseline games, the late-game
diagnostic reported similar donated-pearl pickup efficiency in wins and losses, about
38–39%. In a subset of 160 losses classified as delivery-limited, 44.5 of 66 worker
length remained more than 12 cells from the king at round 480. D4's targeted response
looked promising, but D6 did not confirm it. The transport observation survives; the
particular rule of leaving up to 60 rounds earlier did not establish a useful gain.

Frozen evidence: [v12s](../../versions/v12s/FROZEN.txt).

## D10–D11: v12x changes which objective wins a local disagreement

On weakhold, v11t workers spent **92% of rounds 30–199** in empty starting zones in the
diagnostic sample. Debug scores showed why: the learned ranker contributed 70–106
points, with roughly 15 points between candidate moves, while exploration contributed
less than one point and goal progress at most ten. Turning off traps or increasing an
unseen-cell bonus did not reliably lead into the central food.

The successful intervention was conditional. When a candidate's search found no food
or hub, its goal-progress contribution was multiplied; progress used walking distance
through remembered terrain, with unknown edges assumed open. The normal food-seeking
decision retained its tuned ranker. This is distinct from globally lowering `W_V3`.

| ID | Variant | N | Wins: variant / control | Evidence |
|---|---|---:|---|---|
| D10 | ×10 exploration plus goal path | 408 | 238 / 213 | +6.1 pp [−0.7, +13.0] |
| D10 | ×30 exploration plus goal path | 408 | 238 / 213 | +6.2 pp [−0.5, +13.1] |
| D11 | ×30 plus goal path, new seeds | 1,122 | 678 / 631 | +4.2 pp [−0.1, +8.6] |
| D11 | Same plus v12s small-map queen | 1,122 | 684 / 631 | **+4.7 pp [+0.6, +8.9]**, retained as v12x |

The bundled version won 60/102 directly against v11t within D11. Tower Defense improved
52 versus 28 and weakhold 45 versus 24; Australia, Autarky and Dilemma slipped. The
combination did not preserve v12s's entire isolated Stripes gain: it won 17 versus the
control's 20 there, whereas exploration without the small-map rule won 11.

The [paired outcome audit](../../results/strategy-review-20261006/completed-experiment-audit.json)
adds an important correction to a simple success story. v12x turned 233 baseline
non-wins into wins but lost 180 baseline wins, for the net +53. It saved the queen in
144 fixtures and lost a previously surviving queen in 168: **357 queens alive versus
381** overall. Its strength gain was not a queen-survival gain. Outcome classes are
also changed by the treatment, so comparing class-conditioned rates is descriptive,
not an independent causal decomposition.

[v12x](../../versions/v12x/FROZEN.txt) was frozen with hash `515739481d60c57f`, sampled
sandbox maximum 12.1 million points, and uploaded according to the user's timestamp.
The later live analysis labels a cohort around 14:20–14:24 UTC on 5 October. The
timezone of the user-supplied 10:04:34 was never specified; do not silently equate them.

## D12–D20: a real live weakness survives several failed defences

The first saved live review after the inferred v12x boundary counted **31/65 wins**,
with our queen dying to enemy head-ons 23 times, walls 14 times and our dragons 12
times. Later, in the larger attributed cohort of 532 games, the count was **288 wins,
244 losses**. Australia and Autarky frequently had ample worker material but lost our
queen while the opponent retained theirs. Dilemma instead showed early elimination and
failure to hold productive spawners.

The corrected [queen-ram audit](../../results/strategy-review-20261006/queen-ram-audit.json)
found **117 enemy rams in those 244 losses**. **75** executed paid steps. The rammer was
visible at the queen's last turn in **104**, and within two cells in **39**. The earlier
114-visible / 80-close figures mixed later enemy positions into the queen's decision
state and must not be reused. A ram occurred in 48% of these losses, but the audit does
not establish that 48% were winnable by a defensive change.

The queen-step diagnostic found 74 last moves outside all visible enemies' free reach
that were nevertheless hit by paid movement; 66 had a free-safe alternative. Only eight
cases moved avoidably into free reach, while 31 had no free-safe move. These categories
describe the tested reach model, not an oracle's proof that an alternative survives
future play.

| ID | Tested change | N | Wins: variant / control | Decision |
|---|---|---:|---|---|
| D12 | Doomed-worker avoidance (`dq`); radius-2 bodyguard | 476 | 260, 254 / 254 | +1.3 pp and neutral; neither adopted |
| D13 | Halve or quarter ranker weight everywhere | 476 | 259, 238 / 253 | +1.3 / −3.2 pp; retain original weight |
| D14 | `dq` on reserved seeds | 1,122 | 663 / 653 | +0.9 pp [−1.2, +3.0]; not adopted alone |
| D15 | Add one or two paid steps to enemy forbidden reach; sprinter in panel | 544 | 266, 263 / 273 | Rejected; queen survival falls |
| D16 | Apply sprint mask only to enemy lengths ≤3 | 544 | 258 / 294 | −6.6 pp [−11.6, −2.0]; rejected |
| D16 | Queen may spend a segment on a two-step escape | 544 | 303 / 294 | +1.7 pp [−0.9, +4.4]; candidate held |
| D17 | Keep a length≥8 founder unsplit before round 100 or 200 | 544 | 274 / 273, both settings identical | Mixed map effects; rejected |
| D18 | Paid flight plus `dq`, reserved seeds | 1,224 | 739 / 720 | +1.6 pp [−1.6, +4.7]; not promoted |
| D19 | Workers intercept small sprint threats within radius 3 or 4 of queen | 544 | 277, 266 / 277 | Neutral / −2.0 pp; rejected |
| D20 | Exempt queen from v12x exploration multiplier | 544 | 282 / 292 | −1.8 pp [−4.4, +0.7]; rejected |

D14's paired audit makes the meaning of “low-cost safety” precise: `dq` gained 83 wins
and lost 73, and saved 77 queens while losing 49. It was not behaviorally harmless
merely because its average effect was small. It later entered a successful bundle;
there is no justification for calling its standalone improvement proven.

The new `opp-hunter` and `opp-sprinter` were built from **our own v12x lineage**, not
independent opponents. The sprinter won 39/68 directly against v12x. Adding it corrected
a missing tactical style, but did not create a diverse external league. Crucially,
the sprint masks still failed against the expanded panel. “The old opponents did not
sprint” was therefore insufficient to explain their failure.

A separate [immediate-kill audit](../../results/strategy-review-20261006/immediate-queen-kill-audit.json)
looked at ten distinct-map replays and found seven adjacent legal enemy-queen kill
opportunities in 109,608 worker turns, three taken and four missed. None of the misses
occurred while our queen was alive. That bounded diagnostic did not support a sweeping
claim that simple adjacent captures were the largest missed opportunity; it excluded
portals and paid multi-step routes.

## D21–D22: the successful use of sprint reach was offensive

The same sprint mechanism that made a dangerous opponent became a candidate feature.
When a worker can reach a visible enemy queen **this turn**, the attack converts one
worker into the opponent's deciding piece. It does not ask all our dragons to avoid
every cell an enemy could ever reach.

| ID | Variant | N | Wins: variant / control | Win-score change |
|---|---|---:|---|---|
| D21 | Hunt with at most one paid step | 544 | 305 / 283 | +4.0 pp [+0.6, +7.4] |
| D21 | Hunt with at most two or three paid steps | 544 | 297 / 283, both | +2.6 pp |
| D22 | One paid hunt step, reserved seeds | 1,224 | 717 / 671 | **+3.8 pp [+1.6, +5.9]** |
| D22 | Hunt + paid queen flight + `dq` | 1,224 | 741 / 671 | **+5.7 pp [+2.4, +9.1]** |

The last row was frozen as [v12z](../../versions/v12z/FROZEN.txt). Its queen survived
445 games versus 363, and the opponent's 129 versus 211. Australia improved 53 versus
37 and Autarky 50 versus 35; Maze declined 45 versus 51 and Schooltime 42 versus 45.
The sampled sandbox maximum was 12.4 million CPU points.

Hunting alone has positive confirmation evidence. The additional 24 wins from the
bundle are an incremental comparison on the same fixtures, but the experiment did
not separately compare hunt + flight and hunt + `dq`, nor supply a new componentwise
interaction analysis. Retaining the successful bundle is supported; claiming each
defensive feature independently proven is not.

The [12 October head-to-head](../../showcase/games-h2h-v12z.json) supplied another
comparison on four seeds, 17 maps and both sides: **v12z 91 wins of 136 against v12x,
queens alive 65 versus 22**. Stripes and Trophy were weakest at 3/8 each. This is useful
direct evidence against its predecessor, not a replacement for external opponents or
a test of the later new maps.

## What the last live snapshot can and cannot establish

[The saved standings](../../results/final_leaderboard_team590.json) show rating 1604,
rank 153 and a cumulative wins field of 3,421. The log records 1,001 teams and rank 100
at 1813. This is the 12 October closeout snapshot, not a new website observation on
14 October.

The compact [battle export](../../results/final_ladder_battles.json) has 950 rows from
late September through 12 October. The original writeup's late cohorts were selected
by time and `games == 5`. The export lacks a ranked flag and draw count. Accordingly:

| Attributed version cohort | Recorded wins / games | Average recorded opponent rating | Interpretation |
|---|---:|---:|---|
| v10o | 171 / 345 | 1449 | Historical five-game cohort |
| v11q | 533 / 1,080 | 1521 | Historical five-game cohort |
| v12x | 472 / 895 | 1572 | Timestamp attribution around a confirmed upload |
| v12z | 948 / 1,995 | 1632 | Inferred post-7-October cohort |

These are not certified ranked-only results. They do not identify which bot hashes
played each game, and the opponent and map distributions differ. A simple Elo inverse
applied to each average opponent and win fraction would neither reconstruct the site's
changing rating method nor establish a causal v12z improvement.

The [100-game final replay sample](../../results/live-review-final/games.json) was
chosen from the start, middle and end of the post-cutoff period. It includes paid-step
requests by our team in 62 games, 120 such requests overall, 64 by the queen, and 43
enemy-queen rams by our workers versus 35 rams on ours. Twenty-five of our queen rams
were accompanied by a paid-step request. These signatures fit v12z and differ from
the earlier 150-game v12x sample, which had no such requests.

The [checker](../../results/final_v12z_check.py) compares **requested action length**
with the free budget. Unlike the corrected 117-case audit, it does not independently
count every executed step. Requests can terminate early. The final sample therefore
supports the deployment inference without proving 120 executed paid moves or a
specific server artifact. Its 63/100 wins also should not be substituted for the much
larger cohort's 47.5% win fraction.

Thirteen map names absent from the old books appear in that sample: Athena, Atlantis,
Caution, Detention, Ezam, Hive, Maelstrom, Metro, Ouroboros, Thermopylae, Trolley Problem,
Trolley Problem (Buffed), and Whale Song. They account for **25 of the 70 sampled games
dated 11–12 October**. Across the whole 100-game sample, wins were 12/25 on these names
and 51/75 on known maps. This is evidence that evaluation coverage became stale, not
proof that missing map books caused the entire performance gap.

## Showcase material and remaining uncertainty

The showcase contains **72 old-rules and 60 queen-rules games**, plus the separate
136-game v12z head-to-head. The single-seed showcase is designed for explanation. For
example, v12z loses 8 of its 12 illustrative games against v12x, despite winning the
larger direct comparison. The older showcase uses the 1.1.0 seeded engine; it does not
reproduce the exact pre-1.1.0 experimental conditions under which v1–v6 were first
selected. The frozen v6 and v7-base also differ in strategy features, so that matchup
is not the port's parity test.

Useful entry points are [the fixture script](../../showcase/make_showcase.py),
[old summaries](../../showcase/games-old.json),
[queen summaries](../../showcase/games-queen.json), and
[the narrative's selected replay moments](../../PROJECT_WRITEUP.md#23-showcase-reel).
Reproduction requires compatible engine, maps, frozen source and runner settings;
having the same seed alone is insufficient.

This completion closes the missing late experimental narrative, but does not invent
answers to the archive's unresolved questions:

- The Sprint 1 loss is logged as 1–6 while also mentioning a draw. The exact series
  score still requires bracket evidence; the qualitative loss is established.
- The v12x user timestamp lacks a timezone; v12z's server artifact is inferred.
- The compact late export discarded ranked/draw/submission fields. Raw event metadata
  would be required to certify a ranked-only cohort and exact W–D–L.
- Sampled CPU maxima do not prove a worst-case bound on every future map.
- The local panel contains related bots, and reserved seeds on the same layouts test
  seed generalization more strongly than style or new-map generalization.
- The first archive's run register indexes discovered metadata; it does not certify
  every historical partial run as complete. Those limits remain in
  [chapter 6](06_EVIDENCE_AND_GAPS.md).

## What this evidence leaves worth doing

These are proposals, not implemented or validated improvements:

1. **Restore evaluation coverage first.** Obtain the current official map/rule files
   and preserve ranked, draw and submission metadata. Keep the old 17-map panel as a
   regression set; it cannot remain the sole promotion target after new maps appear.
2. **Test specific enemy responses rather than a union of all threats.** The repeated
   failures of sprint masks motivate a small scenario-based queen controller. It must
   compare move and paid-flight choices under plausible individual replies, using only
   information actually visible at decision time. The corrected 104-visible cases are
   a diagnostic source, not a training/test split by themselves.
3. **Learn from the v12z bundle without blindly accumulating safety switches.** A
   factorial follow-up could separate hunt, flight and `dq` on fresh maps/opponents.
   Preserve the successful frozen control and report both new wins and lost wins.
4. **Address economic access and retention where it remains measured.** Dilemma's
   spawner-control failures, Stripes' opening dependence and unfamiliar maps are more
   specific targets than another global food or hub multiplier. Test food access,
   occupancy and births before committing to a learned harvesting system.
5. **Build any new learner around a validated decision problem.** The old v3 ranker
   remains useful; R4 imitation and R5 final-result corrections failed. A compact model
   estimating short tactical replies or scoring bounded candidate plans has a clearer
   target than a full rewrite, but must first beat an explicit non-neural baseline.

The demonstrated late gains came from better access to the economy and a precise
queen-kill action. Continued work should preserve those gains while testing the
unresolved threat model and the changed environment, rather than restart already
rejected sweeps from an earlier queue.
