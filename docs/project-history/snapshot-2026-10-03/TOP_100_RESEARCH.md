# Getting team 777 into the top 100

Research snapshot: 29 September 2026 EDT / 30 September 2026 UTC. Website refreshed around 02:01 UTC. Repository baseline inspected: `a1f8943`. You confirmed **v10 is uploaded; v10h is being tuned**. This report contains analysis and proposed experiments; no bot implementation, tuning configuration, or submission was changed.

## The recommendation

**Keep the C++ bot and its swarm economy. Improve the information it acts on, opening resource access, and the conversion of many small dragons into a winning survivor.** The evidence does not justify discarding the current strategy yet. It does justify moving beyond another broad parameter search over essentially the same decisions.

The most useful next steps, in order:

1. **Treat v10g's map-book addition as the strongest existing improvement.** Preserve v10g as a control when evaluating v10h and the current retune. Earlier feeding is much less convincingly established on the current ranked maps.
2. **Correct and isolate three concrete decision defects:** learned-hub spacing, portal inputs to the learned action scorer, and king messages that can remain stale or identify the wrong nearby teammate. Their presence is confirmed in source; their win-rate effects have not been measured.
3. **Run two strategic tracks:** opening access and population growth on Trophy/Trauma/Default; reliable food concentration and selective king protection on Schooltime/Slithery. A single global “be safer” or “grow kings earlier” setting is contradicted by the experiments already completed.
4. **Use spare C++ compute for accurate short tactical decisions**, particularly king escape, emergency splitting, and cheap attacks against enemy kings. Increasing the existing flood search is not equivalent to planning these actions.
5. **Put the spare GTX 980 machine on a small learned-evaluator project first.** Refresh the demonstrator data, teach difficult decisions with stronger offline search, and retain the C++ runtime. A full recurrent reinforcement-learning bot is a possible second project, with explicit throughput and validation gates.

The top-100 gap is meaningful but not enormous: roughly **70–80 Elo at this snapshot**. There are credible improvements to test without betting the project on a complete rewrite. None of the untested ideas below is a promised rating gain.

## 1. What the website actually shows

### Position and sample

The correct identity is **team name 777, team ID 590**. Team ID 777 belongs to a different team.

| Item | Observation |
|---|---:|
| Team 777 rank | 149 |
| Current Elo | 1624 |
| Recorded peak Elo | 1644 |
| Lifetime record | 810 wins, 711 losses, 0 draws |
| Rank-100 threshold, initial inspection | 1700 |
| Rank-100 threshold, refresh around 02:01 UTC | 1695 |
| Leaderboard entries at refresh | 928 |
| Recent ranked sample analyzed | 31 battles, 155 games |
| Recent result | 79 wins, 76 losses: 51.0% |

Sources: [team profile](https://game.battlecode.au/teams/590), [leaderboard search](https://game.battlecode.au/leaderboard?search=777), [ranks 91–100](https://game.battlecode.au/leaderboard?page=10), [team battles](https://game.battlecode.au/battles?teams=590). These are moving pages, so the timestamp matters.

I fetched the first four battle-list pages, filtered the actual `ranked` field, obtained the five games for each ranked battle, and decoded all 155 public replays. The cohort runs from **29 September 03:19:21 UTC through 30 September 01:37:35 UTC**. It contains the current ten map names, consistent with the project's existing current-pool definition.

**This is a recent team cohort, not a controlled v10 trial.** Public battle data did not expose the uploaded bot version, and I do not have the exact upload boundary. Your confirmation establishes what is live now; the lifetime record and potentially some earlier games in this cohort span other versions. Opponents and maps also vary. A battle-cluster bootstrap gives an approximate 95% interval of **43.2–59.4%** for this cohort's win rate; it is descriptive, not a stable estimate against all future opponents.

### Where the losses are

| Map | Wins / games | Win rate | Losses by elimination | Main diagnostic priority |
|---|---:|---:|---:|---|
| Trophy | 4 / 17 | 23.5% | 10 of 13 losses | Opening access, expansion, map knowledge |
| Default | 5 / 15 | 33.3% | 1 of 10 | Midgame economy and concentration |
| Trauma | 6 / 18 | 33.3% | 0 of 12 | Resource access and routing |
| Schooltime | 6 / 16 | 37.5% | 0 of 10 | Concentration and valuable-dragon losses |
| Prisoners Dilemma | 6 / 14 | 42.9% | 6 of 8 | Access, portal decisions, contested survival |
| Portals | 6 / 11 | 54.5% | 0 of 5 | Portal valuation and transfer routes |
| Slithery Fight | 8 / 14 | 57.1% | 0 of 6 | Convert a large economy into one long survivor |
| Devil | 11 / 16 | 68.8% | 3 of 5 | Preserve the effective swarm behavior |
| Queen Of Spades | 11 / 15 | 73.3% | 1 of 4 | Preserve corridor-specific behavior |
| Autarky | 16 / 19 | 84.2% | 1 of 3 | Regression guard for new changes |

These are small, opponent-dependent samples. The map ordering should determine which replays and mechanisms to inspect, not become a permanent hard-coded policy on its own.

Across all 76 losses, **22 finished with more total surviving length than the opponent**. Conversely, 22 of the 79 wins had less total surviving length. This directly reinforces the mismatch between a large swarm and the game's final objective. There were 22 elimination losses and 54 round-limit losses. Only 16 losses had more total pearl-consumption events than the opponent, so “our economy is always better; only feeding is wrong” would also be false.

Specific evidence:

- **Trophy:** median round-100 population was 11 versus 28, and total length 29 versus 69. This is already an opening deficit. Fixing a round-400 feeding rule cannot rescue games that lose their economy much earlier.
- **Trauma:** median total pearl-consumption events were 55 versus 344. At round 300, median total length was 30 versus 53.5. Access to useful areas deserves priority over king micro here.
- **Default:** median total length was approximately tied at round 100, then 48 versus 71 at round 300. The problem is not uniformly the initial split.
- **Schooltime:** 7 of its 10 losses contained at least one non-no-action death of a length-10-or-greater dragon after round 400. This warrants tactical inspection, but those dragons were not necessarily the elected king.

| Inspectable game | Result and why it matters |
|---|---|
| [563874, Slithery vs CookAgent](https://game.battlecode.au/visualiser?match=563873) | Lost with **266 vs 161 total length**, but **21 vs 51 longest**. Pearl-consumption events: 3764 vs 1078. |
| [557811, Slithery vs CookAgent](https://game.battlecode.au/visualiser?match=557809) | Lost with **262 vs 207 total**, **20 vs 40 longest**. The concentration problem repeats. |
| [643235, Schooltime vs Hydra](https://game.battlecode.au/visualiser?match=643234) | Lost with **388 vs 220 total**, **47 vs 56 longest**. Two large no-action deaths also occurred late; whether their food reached the right recipient needs attribution. |
| [572261, Schooltime vs codih](https://game.battlecode.au/visualiser?match=572261) | Lost **22 vs 23 longest**, despite **273 vs 150 total**. Small conversion improvements can decide games. |
| [647761, Default vs Oxbridge Rejects](https://game.battlecode.au/visualiser?match=647761) | Won **40 vs 31 longest**. Our eventual king directly ate 34 pearls from friendly no-action corpses after round 400. The current feeding mechanism can work. |

The links open the battle containing each game; select the stated game/map. Direct replay data is available at `/api/matches/<game ID>/replay`.

**Measurement caution:** pearl consumption counts recycled corpses as well as environmental spawns. A split/death/recollection loop can inflate this count without creating an equally valuable surviving force. Also, tracking only the final king's ID misses growth inherited through a split. In several inspected losses the final longest dragon was born late. Food attribution must follow lineage and length transfers before concluding that its low direct consumption means no feeding occurred.

### What top 100 requires

The site updates Elo from the fraction of the five games won in a ranked battle, with draws worth half. It does not reward winning a game by an enormous length margin. [Official Elo rules](https://game.battlecode.au/docs/elo)

A 71-point rating difference corresponds to about a **60:40 expected score** between two stationary players under the Elo formula. This gives the scale of the task; it is not a conversion formula from a local benchmark improvement to ladder Elo. The cutoff itself moved during this review. Aim for durable strength around and above the current 1700 boundary, rather than one favorable rating spike.

## 2. What the completed work already establishes

The project has progressed far beyond the earlier basic Python planner. I reviewed the architecture, frozen versions, C++ port and in-process runner evidence, CMA spaces and run records, feature experiments, replay/dataset pipeline, and competitor research. The most relevant history is in [FEATURE_EXPERIMENT.md](<C:/Users/Sea7/Desktop/unsw battlebot/FEATURE_EXPERIMENT.md>), [V7_EXPERIMENT.md](<C:/Users/Sea7/Desktop/unsw battlebot/V7_EXPERIMENT.md>), and [V7_CPP_PORT_PLAN.md](<C:/Users/Sea7/Desktop/unsw battlebot/V7_CPP_PORT_PLAN.md>).

| Development | Evidence | Consequence for the next stage |
|---|---|---|
| C++ port | Recorded parity over 481,092 dragon-turns; in-process/process parity on 198 configurations | Keep this infrastructure. It makes experiments affordable, though unexercised branches can still contain mismatches. |
| First CMA run | A promising single-seed v7 result became 29/66 versus the untuned baseline's 32/66 against nicked v44 on the newer engine | More generations on a narrow sample are not reliable progress. |
| Learned v3 action ranker | Removing it cost 0.355 aligned-score units on the current pool in the major ablation | This is a valuable component and a natural target for better data/features. |
| Food, spawn anticipation, hubs | All had strong negative removal effects on the current pool | Preserve resource-oriented behavior while improving its inputs. |
| Removing trap/defend terms | Training gain replicated, but held-out pool delta was only +0.032 with CI spanning zero; Queen Of Spades suffered | Safety depends on geometry and role. A global removal was not established as a general improvement. |
| v9 | Held-out 153 versus 124 wins out of 270 against the comparison baseline | CMA has already delivered useful gains when the design and evaluation support it. |
| v10 king beacon / big feeding | Held-out 207 versus 198 wins out of 270 against v9 | Coordination helps, but the measured gain is modest and does not establish that the protocol is correct. |
| v11 retune | Held-out 205 versus v10's 207; opponent-specific gains and regressions | The later plateau is real enough to justify structural experiments. |
| Early protection at length 4 | Current-pool aligned delta −0.185; adding protection-floor/rescue adjustments worsened it | Do not revive “grow a king immediately” as an unqualified recommendation. |
| Dead-end and split-safety variants | Fewer deaths did not reliably produce more wins | Small-dragon deaths can be productive; evaluate role and downstream outcome. |

The source tree is not interchangeable with the live bot:

| Bot | Content hash | Interpretation |
|---|---|---|
| `versions/v9` | `7bad14b4e4fd110b` | Previous frozen baseline |
| `versions/v10` | `c1fbdb633f1627e3` | User-confirmed live version |
| `results/v10g-bot` | `d9266f47a6194429` | v10 plus `CPP_BOOK_MAP=1` |
| `results/v10h-bot` | `f9d00cd150ff2c53` | v10g plus `CPP_FEED_SHIFT_LARGE=40` |

`cppbot` is the development template; its default parameters are not the tuned live v10 settings. Future experiments need a frozen baseline hash, not just “current C++.”

### The strongest improvement is already in the local results

I recomputed the **actual win counts on the current ten maps**, separately from the reports' aligned-score objective:

| Change | First experiment, baseline → variant | Confirmation, baseline → variant | Combined current-pool gain |
|---|---:|---:|---:|
| Map-book open-edge fill, v10 → v10g | 214 → 249 / 360 | 184 → 214 / 360 | **398 → 463 / 720; +9.03 percentage points** |
| Earlier large-map feeding, v10g → v10h | 215 → 225 / 360 | 215 → 217 / 360 | **430 → 442 / 720; +1.67 percentage points** |

A fresh analysis holding the ten maps and six opponent builds fixed, and resampling paired seed blocks within each map, gives approximate 95% win-difference intervals of **+6.1 to +11.8 points for the book**, and **−0.4 to +3.8 points for the feeding shift**. These intervals describe these local samples; they do not cover uncertainty about different opponent families or hidden server maps.

Book gains were concentrated where the live cohort is weak: Trauma **25→49/72**, Schooltime **35→50/72**, Trophy **31→41/72**, Default **40→49/72**, Queen Of Spades **41→48/72**. The four ladder-only maps had identical outcomes because this book addition does not supply their missing layouts. This is a much stronger rationale than simply hoping another global weight vector fixes those maps.

Sources: [book screen](<C:/Users/Sea7/Desktop/unsw battlebot/results/20260929-134853-ablate-5617dc/report.md>), [book confirmation](<C:/Users/Sea7/Desktop/unsw battlebot/results/20260929-152611-ablate-5cb6f9/report.md>), [shift screen](<C:/Users/Sea7/Desktop/unsw battlebot/results/20260929-163912-ablate-263928/report.md>), [shift confirmation](<C:/Users/Sea7/Desktop/unsw battlebot/results/20260929-182640-ablate-e2493c/report.md>). Counts come from each run's `runs/base/margins.json` and variant counterpart. The generic “harmful (drop)” label in the ablation report assumes feature removal; here the variant **adds** a feature, so use the positive delta and wins, not that label.

**Recommendation:** after the current tuning run, compare its candidate against v10h, v10g, and live v10 on the same fresh games. Do not allow the uncertain feeding shift to disappear into a bundled comparison. The book improvement is the leading near-term promotion candidate, subject to the normal final checks and your upload decision.

## 3. Specific defects and the experiments they suggest

The distinction throughout this section is important: **a source defect can be certain while its rating cost remains unknown**. No code change or counterfactual game was run during this review.

### A. Learned hubs do not enforce the intended separation

In [v10 `learn_hubs`](<C:/Users/Sea7/Desktop/unsw battlebot/versions/v10/v6.hpp:398>), wrapped coordinate differences use the **maximum** of the direct and wrapped distances. The [Python original](<C:/Users/Sea7/Desktop/unsw battlebot/framework/core_memory.py:134>) uses the minimum, then combines the axes with a maximum for Chebyshev distance. The same mismatch remains in the inspected v10h/development path.

On a 32×16 board, horizontally adjacent cells have true wrapped Chebyshev distance 1; the C++ expression can report 31. On the inspected map sizes, its “within five cells” exclusion cannot perform its intended job. Up to four chosen hubs can therefore be adjacent representatives of the same rich patch.

**Experiment H1:** change only this distance calculation. Measure distinct selected patches, early teammate concentration, coverage, and wins. The most relevant maps are those that fall through to learned hubs, including the ladder-only layouts. Do not bundle a new exploration policy with the correction. Earlier port parity does not establish coverage of this learned-only branch.

### B. The strongest learned feature evaluates portal moves at the wrong location

[v10 `v3_scores`](<C:/Users/Sea7/Desktop/unsw battlebot/versions/v10/v6_brain.hpp:60>) starts its local BFS from the adjacent cell in the 7×7 observation. For a portal action, the actual destination is the portal's remote endpoint. The overall movement scorer accepts portal directions and adds this learned score with `W_V3=24.705`.

Thus a portal move can receive food, room, crowding, and continuation features describing a neighborhood it will not enter. This is an input-semantic problem, not evidence that the learned ranker should be removed. Its training also focused on ordinary movement rather than a complete portal action model.

**Experiment P1:** gate the v3 contribution only for portal actions, keeping the rest of portal navigation intact. Then compare a second variant using destination-aware remembered features with explicit unknown-information flags. The first is a cheap diagnostic; the second needs retraining or calibration because missing remote vision is not equivalent to an empty destination.

**Success evidence:** fewer feature/action mismatches, better portal-entry outcomes, and replicated wins on Prisoners Dilemma/Portals/Trauma without losing useful ordinary-move ranking.

### C. King messages can keep obsolete information alive

[v10 `receive_king` and `king_lines`](<C:/Users/Sea7/Desktop/unsw battlebot/versions/v10/v6_brain.hpp:768>) transmit location and quantized length, but no king identity or origin timestamp. A qualifying relay resets `king_round` to the receiver's current round. Receivers then rebroadcast their stored message.

The TTL therefore measures **time since the last relay**, not time since a real king reported its position. Relays can sustain an obsolete location or dead king's claim. Length is quantized in groups of four, and equal-strength messages overwrite each other without a stable identity tie-breaker.

**Experiment K1:** introduce an identity-bearing announcement with origin freshness, deterministic election ties, bounded forwarding, and invalidation when locally contradicted. A relay must preserve the age of the original information. A smaller new king must eventually replace a dead larger one. Test split succession as well as movement and death.

Protocol 3 offers 64-bit sonar values and additional echo fields, making a richer message practical. Upgrading requires the whole input/output parser contract, including `ECHOES`, to be handled correctly; it is not just changing the integer type. Directed sonar itself is not exclusive to protocol 3. [Protocol upgrade specification](https://game.battlecode.au/docs/protocol-upgrade)

**Measure before judging:** stale-target travel, announced king actually alive, target identity changes, duplicate-relay traffic, food delivered, and match outcome. Public replay sonar payloads were redacted in the sample, so I cannot estimate the live incidence of this failure from those replays.

### D. A nearby teammate can be mistaken for the king

[v10 `beacon_target`](<C:/Users/Sea7/Desktop/unsw battlebot/versions/v10/v6_brain.hpp:801>) searches visible friendly heads near the beacon cell and uses the nearest one. It does not match an announced ID or verify that the selected visible teammate has the announced length. The source accepts a head within four toroidal Manhattan steps of the beacon location.

A small teammate near an old king position can therefore become the apparent recipient. Separately, `visible_target` estimates length by counting visible segments; for a long dragon this is only a lower bound.

**Experiment K2:** bind feeding eligibility to an identified, recently confirmed recipient. Separate the identity of the recipient from a rough attraction point. Preserve a fallback for a visibly suitable king when communication is missing. This is particularly important for large feeders: misdirecting a length-20 dragon costs more than misdirecting a length-2 worker.

Do not “fix” the issue by assuming every visible head's full length is known. It is not available from a partially visible body. [Vision specification](https://game.battlecode.au/docs/vision)

### E. Feeding currently checks proximity, not whether the recipient can collect

[v10 `should_feed`](<C:/Users/Sea7/Desktop/unsw battlebot/versions/v10/v6_brain.hpp:644>) allows a drop at geometric distance 2–4, avoids the king's immediate front cell, and checks enemy heads within a small radius of the king. It does not evaluate the actual corpse-pearl cells, walls/portals between them and the recipient, collection time, or competing collectors.

This motivates a **rendezvous and collection policy**, not just an earlier timer:

1. Elect a recipient and pick a reachable meeting area with turning room.
2. Route feeders toward useful drop positions; avoid clogging the king's next moves.
3. Evaluate the cells that the feeder's actual body will turn into pearls, and whether the recipient can reach them before opponents or the deadline.
4. Make the recipient actively prioritize that nearby food for a bounded period.
5. Retain an exit if the recipient dies, changes identity through a split, or the meeting area becomes contested.

A corpse supplies pearls on alternating body cells; its entire length does not transfer one-for-one. Arrival order, the recipient's facing, and remaining rounds matter. [Death rules](https://game.battlecode.au/docs/death), [execution order](https://game.battlecode.au/docs/execution-order)

**Experiment F1:** first add only identity/reachability checks and collection priority. **F2:** then compare a small rendezvous policy with the current chasing policy. **F3:** only after that, tune when to start. Keep map-area timing as a baseline; route time and available recipients are more informative hypotheses than area alone.

Use the existing [food-provenance tracer](<C:/Users/Sea7/Desktop/unsw battlebot/bcsim/feed_trace.py>) as a starting point, but extend the analysis conceptually to split lineage. Report friendly corpse pearls created, collected by the intended recipient/continuation, stolen, left at the deadline, and length spent delivering them. The existing `fed_deaths` proximity proxy does not establish a successful transfer.

### F. Valuable-dragon tactics need a better transition model

[v10 `search_one`](<C:/Users/Sea7/Desktop/unsw battlebot/versions/v10/v6_brain.hpp:263>) is a useful weighted spatial search. It is not a game-tree search that maintains facing, body shape, consumed food, and opponents' scheduled actions on every branch. A best value per cell merges states that can have very different future survival. Food valuation largely rewards the best reachable item rather than a realizable sequence of collections.

The inactive [beam search](<C:/Users/Sea7/Desktop/unsw battlebot/versions/v10/v6_brain.hpp:340>) is also not ready to become the solution simply by increasing its width. It permits entering the current tail when not growing, whereas the game's collision check occurs before the tail advances. Its food query is not a per-branch consumed-food state. `CPP_BEAM=0` in both v10 and v10h, so these are **dormant-model defects, not explanations of current live actions**.

**Experiment T1:** accurate, bounded 2–4-round tactical evaluation only when a valuable dragon faces a threat, a split is being considered, or a small dragon can trade with an enemy king. Include ordinary moves, a small set of legal short sprints, and relevant split choices. Model ascending IDs and newborn actions. Use several plausible opponent responses under fog, not an oracle or the union of every possible attack as an absolute prohibition.

The fallback [emergency split](<C:/Users/Sea7/Desktop/unsw battlebot/versions/v10/v6_brain.hpp:934>) can transfer almost all length into a newborn child. This may save a trapped king, but changes identity and resets the child's memory. Test a short post-birth feeding lockout and king succession together with actual escape success; do not prohibit emergency splits universally.

Historical sandbox measurements around 7–8 million points leave room beneath the 100-million-point per-turn limit. Those are measurements of earlier tested configurations, not proof that a new search is cheap. Keep the project's conservative 60-million maximum target, count parsing/output overhead, and measure difficult states, cold starts, and large maps. The judge also limits each dragon to 48 MB and one thread. [Official runtime limits](https://game.battlecode.au/docs/timeouts)

### G. Map knowledge should carry confidence

The strong book result supports using known topology. However, the map book should distinguish **observed edges** from **inferred edges**. In the inspected development path, open edges filled after a unique identification are not comprehensively rolled back if later observations invalidate that map hypothesis. Local observations correct their own cells, but unvisited inferred cells can remain stale.

Existing project analysis found a server Default variant with 66 differing edges and hidden spawn parameters. The present perturbation generator changes rates at existing spawners; it does not test moved spawner support or changed walls.

**Experiment M1:** retain the book benefit while adding inference provenance and invalidation. **M2:** test learned resource patches against the book only when observations consistently contradict the expected productive regions. A familiar wall layout does not prove the current resource distribution matches the book.

For Trophy and Trauma, instrument the first 100–150 rounds: time to first productive patch, blocked or avoided portal attempts, useful territory reached, population, and environmental food intake. Then test route allocation by stable per-dragon identity and target-local crowding. Do not repeat the old geometric Voronoi or blanket split-safety experiments under a new name; the new hypothesis is whether actual reachable resources are being accessed and divided efficiently.

## 4. Make the experiments answer the ladder question

### What to change about the next tuning cycle

The inspected [v12 plan](<C:/Users/Sea7/Desktop/unsw battlebot/results/20260929-201541-tune-6e4812/plan.json>) starts from v10h, tunes 17 dimensions, uses population 12, one engine seed per generation, current maps paired with fixed perturbed copies, and an aligned objective with `worst_weight=0.25`. Four of five training opponents are nicked-family versions; the fifth is v7-base. The run was still early when inspected, so this is a critique of its experimental scope, not a verdict on its result.

Keep the run intact. When it finishes:

- Evaluate the distribution mean and a small predeclared candidate set against frozen v10h **and v10g**. A single best sampled candidate often benefits from selection noise.
- Use fresh matched seeds. Generation-to-generation absolute scores are confounded when the seed and sampled map variant change; a frozen baseline evaluated on the same generation conditions gives a much clearer progress signal.
- Preserve the useful common-random-number pairing within each generation. Add resampling for close finalists rather than multiplying every candidate's budget indiscriminately.
- Compare plain mean versus the worst-map penalty as an explicit objective experiment. A minimum over noisy one-seed map scores can move because of sampling noise, and is not the site's expected-win objective.
- Increase opponent-family diversity. Four versions of a strong family are useful pressure, but they are not four independent strategic tests. Include different swarm, growing-king, portal, and aggressive policies; keep some families outside selection.
- Reduce the next CMA space to the few knobs of a feature that has first shown a reproducible benefit. Changing coefficients cannot supply missing identity, correct a portal destination, or create a meaningful tactical state.

The existing aligned score is `0.5 × outcome + 0.25 × final longest share + 0.25 × average total-length share`. It is a reasonable training surrogate, but averaging it can rank candidates differently from expected wins. **Promote on actual game score first; use length, economy, and aligned score to explain the result.** [Scoring implementation](<C:/Users/Sea7/Desktop/unsw battlebot/bcsim/margin.py:23>)

### A practical experiment ladder

The budgets below are proposed starting budgets, not statistical power guarantees. All bot-change comparisons cover all 15 ranked layouts and both sides, with the current ten maps primary and the other five a regression guard.

| Stage | Design | Decisions |
|---|---|---|
| Mechanism check | Small diagnostic states/replays; no claim of win-rate improvement | Does the feature fix its intended failure? |
| Screen | 15 maps × 2 sides × 2 seeds × 4 opponent families = **240 games per bot** | Drop clear regressions; retain at most one or two candidates |
| Confirmation | Fresh 3–6 seeds, all 15 maps, both sides, 4–6 families = **360–1080 games per bot** | Require a useful paired win gain with uncertainty; inspect map/family regressions |
| Final test | Previously untouched seeds and at least one genuinely unused strategic family; sandbox stress cases | Decide whether to recommend upload |
| Ladder observation after user upload | Record exact upload version/time, then accumulate new ranked battles | Check transport to the live distribution; do not infer a gain from one 5–0 battle |

Cache identical baseline games by full bot/map/engine/configuration hash. Keep both sides paired within seed blocks; bootstrap at the game-condition block, not at the individual dragon-turn. Hold map weights fixed to the target pool when estimating that pool's expected win change, and separately report sensitivity to opponent-family weighting. The intervals recomputed in section 2 follow this distinction.

Repeatedly consulting a “held-out” set turns it into development data. Reserve a new final test ledger. Different seeds on the same fixed perturbed map are not a substitute for testing fresh perturbation families. Hidden server exports with zeroed spawn information must not be run as if they were faithful reproductions of the live resource process.

Concrete decision rules:

- A source correction is kept as a correctness improvement only after checking that the corrected behavior is intended; its competitive effect still needs measurement.
- A strategic feature advances when it improves wins on fresh confirmation data, with an interval and a plausible mechanism. For a tiny gain, extend confirmation or defer it rather than calling noise a breakthrough.
- Stop a branch after two adequately scoped failures unless a specific diagnosed defect changes the hypothesis. “Try a bigger number” is not a new mechanism.
- Test combined winners again. The book, routing, feeding, and new learned scorer can interact; their individual deltas cannot be added into a predicted Elo increase.

The evaluation principles are consistent with Agarwal et al.'s treatment of uncertainty in small-run learning experiments; the specific map/opponent blocking here is tailored to this repository. [Agarwal et al., 2021](https://arxiv.org/abs/2108.13264)

## 5. The learning opportunity is more concrete than “try neural networks”

### Existing assets and the gap

At inspection, the repository had **4238 raw replay files, about 1.69 GB**, **861 legacy dataset shards**, and only **two V2 dataset shards**. The V2 pipeline exists; the large corpus has not yet become a complete current training dataset.

The deployed v3 model is a small linear action ranker with 24 features and a bias, trained from 12 battles / 60 games, with roughly 68,100 training examples. Its 8/2/2 battle split separated battles, not entire opponent families or maps. A previously tried tiny MLP improved imitation accuracy slightly but won fewer games in the original screening comparison: 63/88 versus the linear model's 67/88. Later direct linear-versus-neural transfer games actually favored the neural model, but with a wide interval. The history establishes that action-label accuracy alone is insufficient; it does not establish that linear models are universally better or that learned evaluation has reached its ceiling.

Sources: [HYBRID_EXPERIMENT.md](<C:/Users/Sea7/Desktop/unsw battlebot/HYBRID_EXPERIMENT.md>), [DATASET_V2.md](<C:/Users/Sea7/Desktop/unsw battlebot/DATASET_V2.md>), [V2 eligibility logic](<C:/Users/Sea7/Desktop/unsw battlebot/bcsim/dataset_v2.py:181>).

### A new data limitation must be handled first

The current public replay sample exposes board events and actions, but the inspected payloads omit private information needed to reproduce the bot's full observation. For example, game 643238 had visible movement, splits, deaths, and pearl changes, **no pearl-countdown events**, zeroed spawn parameters in its map, and redacted sonar values. CPU data and bot names were also absent from these public payloads.

That does **not** invalidate the outcome and body-event analysis above. It does invalidate treating every reconstructed timer of −1 as “this tile never spawns,” or treating a zero sonar payload as the actual message the bot saw.

Before expanding training:

1. Classify replay schemas and information availability. Separate complete local/older data from redacted public cohorts.
2. Add missingness indicators or omit unavailable features consistently. Do not fabricate timer or communication labels.
3. Collect exact local observations from current controlled matches for timer-, memory-, and communication-dependent learning.
4. Audit action classes. V2's default `policy_eligible` condition excludes suicide/absent actions. It cannot teach intentional feeding if used blindly. Equally, an absent action must not automatically be labeled a successful sacrifice; it can represent a failure.
5. Balance sampling by game, map, phase, and tactical event. Tens of thousands of routine turns from a long Slithery game must not drown out the opening decisions that lose Trophy.

### Recommended second-machine project: a stronger small evaluator

**First milestone:** refresh the linear ranker on audited data, with the old feature set as a reproducible baseline. Then add portal-aware features, relative action order, role, target freshness, reachable collection value, and short-search outcomes one group at a time.

**Second milestone:** compare a small nonlinear ranker, perhaps a 64–128-unit MLP or a compact local-grid encoder. A proposed ceiling around 100,000 parameters is ample for an initial experiment and is not a requirement to reach. The output should score a bounded candidate set. Preserve hard protocol legality and the existing strategy outside the learned decision boundary.

**Third milestone:** create stronger labels on states the new policy actually visits. Use a slower, accurate local teacher to compare candidate actions with matched rollout randomness and several plausible hidden states. Emphasize portal entry, recipient/drop selection, king escape, and opening choices. Distill those preferences into the small deployed scorer.

This is an adaptation of **Expert Iteration**: expensive planning supplies useful targets for a cheap policy. The original work studied Hex; it does not prove that the same recipe solves this partially observable multi-dragon game. Our proposed advantage is concentrating expensive analysis on a small set of costly decisions. [Anthony, Tian & Barber, 2017](https://arxiv.org/abs/1705.08439)

Collecting states visited by the student and asking a teacher to label them follows the motivation of **DAgger**, addressing the mismatch between demonstration states and states induced by the learner's own mistakes. Merely downloading more fixed replays is not DAgger: it requires a teacher that can answer on newly encountered states. [Ross, Gordon & Bagnell, 2011](https://proceedings.mlr.press/v15/ross11a.html)

Report held-out game wins, per-action-class performance, decision changes, and CPU cost. A higher top-1 imitation score is only a diagnostic. Teacher labels themselves need checks: a planner with the wrong tail rule will efficiently teach the wrong game.

## 6. What a more ambitious rebuild would look like

If the small evaluator project works and the spare machine can generate enough valid experience, the next experiment should learn a **strategic controller over the existing movement system**: harvest, relocate, rendezvous, feed, preserve, and attack. This narrows credit assignment and action space before asking a network to rediscover movement and team coordination together.

A fuller bot could later use a shared recurrent actor for all dragons, a centralized training critic, an opponent league, and the C++ observation/memory/runtime shell. Actor inference must use only the dragon's legal observation and its own state. Privileged board state belongs in training diagnostics or the critic, not in deployed features, action masks, or hidden-state lookups.

### Research that changes the design

| Scholarly source | What it supports | Application here and limitation |
|---|---|---|
| [Yu et al., *The Surprising Effectiveness of PPO in Cooperative, Multi-Agent Games*, NeurIPS 2022](https://arxiv.org/html/2103.01955v4) | Shared-policy PPO and centralized value estimation can be strong cooperative baselines; implementation choices matter | Start a learned team controller with shared parameters and a training-only critic. Its experiments do not establish success in this game's adversarial, partially observed, changing-population setting. |
| [Lanctot et al., *A Unified Game-Theoretic Approach to Multiagent Reinforcement Learning*, NeurIPS 2017](https://arxiv.org/abs/1711.00832) | Training against mixtures of policies addresses opponent-specific overfitting | Maintain diverse frozen policies and an empirical matchup matrix. A simple balanced league is the first step; a full PSRO solver is not necessary initially. |
| [Silver & Veness, *Monte-Carlo Planning in Large POMDPs*, NeurIPS 2010](https://dspace.mit.edu/entities/publication/5210cdcc-e73d-46f1-be33-d7887e6978f4) | Sampled hidden-state hypotheses can support planning under partial observability | Use a small set of plausible enemy continuations/unknown occupancy states in tactical teaching. Full online POMCP over the entire game is likely too expensive and needs a reliable generative model. |
| [Terry et al., *PettingZoo: Gym for Multi-Agent Reinforcement Learning*, 2021](https://arxiv.org/abs/2009.14471) | The Agent Environment Cycle model makes sequential multi-agent interactions explicit | Preserve dragon-by-dragon live observations. Batch inference across independent games, not by freezing all dragons' observations once per round. |
| [Huang & Ontañón, *A Closer Look at Invalid Action Masking in Policy Gradient Algorithms*, 2022](https://arxiv.org/abs/2006.14171) | Correct state-dependent masking can improve policy-gradient learning | Mask genuinely illegal commands using available information. Do not erase useful sacrifices or intentional head trades by equating “dies” with “invalid.” Never use unseen occupancy to give the actor an oracle mask. |
| [Ng, Harada & Russell, *Policy Invariance Under Reward Transformations*, ICML 1999](https://ai.stanford.edu/~ang/papers/shaping-icml99.pdf) | Potential-based shaping can preserve an MDP's optimal policies under its assumptions | Consider shaping of the form γΦ(next) − Φ(now), with correct terminal handling. Raw pearl bonuses can reward recycling. The theorem is not a blanket guarantee for changing opponents and independently terminated dragons. |
| [Petrenko et al., *Sample Factory*, ICML 2020](https://proceedings.mlr.press/v119/petrenko20a.html) | Efficient experience generation, batching, and process organization can dominate practical RL throughput | Profile engine, observation construction, and inference separately before changing algorithms. The paper's reported throughput is not a forecast for this older i5 or this simulator. |
| [Nomura et al., *CMA-ES with Learning Rate Adaptation*, 2023](https://arxiv.org/abs/2304.03473) | Adaptive CMA learning rates address difficult/noisy optimization regimes | The repository already uses this family of improvement. More optimizer sophistication cannot compensate for a misaligned evaluation population or a missing action/state representation. |

### Requirements before full reinforcement learning is worth running

**Environment fidelity.** Reuse the official engine wherever feasible. If a faster native environment becomes necessary, compare state transitions and observations against it on wraps, portals, pre-tail collision, sprint costs, spawn reset/occupancy, split bodies, same-round newborn actions, sonar delivery order, and terminal scoring. Existing in-process bot parity is valuable but does not certify a newly written engine.

**Birth, death, and credit.** Reset recurrent state at birth. A new child's memory is not inherited merely because the training framework makes that convenient. Preserve the team-level episode after an individual dragon dies, and make the credit convention explicit; otherwise a feeding action can lose all access to the later reward it enabled. Absolute dragon IDs should not be treated as stable agent slots across an episode with thousands of births.

**Reward.** Start with the actual team game outcome. Add only carefully audited auxiliary signals. Penalizing every death teaches the opposite of useful feeding and attacks; rewarding every eaten pearl can teach wasteful loops. A king-length potential needs terminal handling and a clear team-time definition. Do not normalize rewards in a way that rewards producing more decision-making dragons by itself.

**League.** Train against a mixture of frozen historical bots, structurally different sparring policies, and selected recent learners. Keep old opponents after beating them so the learner cannot forget a strategy. Track the matchup matrix; a policy that beats the immediately preceding checkpoint can still be broadly weaker.

**Deployment.** Export small fixed weights into the C++ runtime, verify identical features and actions on a frozen observation corpus, then run judge-sandbox checks. The GTX is for training; the submitted bot does not receive a GPU or PyTorch runtime.

**Go/no-go gate.** Before committing to a long run, demonstrate a reproducible improvement on one bounded task, such as recipient/drop selection or king escape, across at least three training seeds and held-out opponents. Then broaden. An end-to-end learner that cannot outperform the current heuristic on the simpler controlled task does not yet justify an overnight full-game training campaign.

## 7. Using the GTX 980 / older i5 / approximately 16 GB machine

Assuming “980” means a **GeForce GTX 980**, this is a useful auxiliary research machine. The exact CPU, GPU variant/VRAM, and OS remain unconfirmed. I would not buy new hardware to start this plan.

| Workload | Suitability | Starting approach |
|---|---|---|
| Replay audits and dataset conversion | Good | One or two workers, streamed shards, monitor peak RAM |
| Linear ranker / small MLP | Good | CPU baseline first; GPU only if compatible and measurably faster |
| Compact imitation/search-distillation model | Good candidate | Small batches, cached features, bounded teacher jobs |
| Independent confirmation games | Useful if engine throughput is acceptable | Benchmark 1, 2, then 4 workers; do not copy the main machine's worker count |
| Small strategic-controller PPO | Conditional | Only after environment and throughput gates pass |
| Large end-to-end self-play system | Poor first use | Likely limited by simulation, experimentation budget, and engineering complexity |

The GTX 980 is a Maxwell device with compute capability **5.2**. A current default CUDA installation is not automatically compatible. NVIDIA's CUDA 13 release notes remove offline compilation/library support for Maxwell, and PyTorch's September 2026 notice identifies 2.14 as its last release with published CUDA 12.x wheels covering these older architectures. Choose a tested CUDA 12.6-compatible build for the actual OS/Python combination, verify an actual GPU tensor operation, and pin the working environment. CPU training is a reasonable fallback for these small models; spending days on a source build would be a poor first experiment. [NVIDIA GPU table](https://developer.nvidia.com/cuda/gpus/legacy), [CUDA 13 release notes](https://docs.nvidia.com/cuda/archive/13.0.2/cuda-toolkit-release-notes/index.html), [PyTorch support notice](https://dev-discuss.pytorch.org/t/notice-cuda-12-6-wheels-will-no-longer-be-published-from-pytorch-2-15-drops-maxwell-pascal-volta/3432)

Use float32 initially. Do not assume modern mixed-precision recipes improve this GPU. Keep a bounded data-loader queue and stream selected columns rather than expanding the entire replay corpus into memory. The existing compressed NPZ loader decompresses selected arrays for a game; it is not a fixed-memory row store. Measure actual peak RAM on the largest games.

Benchmark **dragon decisions per second**, complete games per second, peak memory, and learner utilization. A fast neural forward pass does not mean the simulator can supply samples quickly enough.

For scale only, 100 million decisions take approximately:

| Measured sustained throughput | Sampling time alone |
|---:|---:|
| 100 decisions/second | 11.6 days |
| 1,000 decisions/second | 27.8 hours |
| 10,000 decisions/second | 2.8 hours |

These are arithmetic examples, **not hardware estimates or claims that 100 million decisions are necessary or sufficient**. Training, evaluation, and failed experiments add time. Start with an audited dataset and a small evaluator because it produces a useful artifact without depending on enormous simulation throughput.

## 8. Ordered work plan

| Priority | Experiment | Why now | Continue only if |
|---|---|---|---|
| 1 | Fresh v10 / v10g / v10h / retune comparison | Distinguishes the proven book gain from an uncertain timer shift | Actual current-pool wins support the chosen candidate |
| 2 | H1: learned-hub distance correction | Small, confirmed port mismatch | Selection geometry is corrected and competitive effects are acceptable |
| 3 | P1: portal-only learned-score correction | Strong feature currently describes the wrong landing neighborhood | Portal outcomes and paired wins improve |
| 4 | K1/K2: identity and freshness | Direct prerequisite for reliable feeding | Target correctness improves without communication/routing regression |
| 5a | F1/F2: reachable drops and recipient collection | Addresses observed total-length-to-longest losses | More delivered value reaches the intended surviving lineage and wins rise |
| 5b | Trophy/Trauma opening access | Addresses early losses feeding cannot repair | Round-100 access/economy improves and full-game wins follow |
| 6 | T1: selective accurate tactical search | Uses C++ headroom where a decision is valuable | Valuable-dragon survival/trades improve within sandbox limits |
| 7 | Refreshed learned evaluator on spare machine | The existing tiny ranker is already useful | Held-out gameplay improves, not merely imitation accuracy |
| 8 | Learned macro controller, then possible recurrent full policy | Higher ceiling with substantially higher uncertainty | Fidelity, throughput, and controlled learning gates pass |

Suggested allocation of development effort: roughly **60% on the first six incremental experiments, 30% on data and the small evaluator, 10% on feasibility work for the larger learner**. These are priorities, not a requirement to run jobs concurrently. Respect the repository's one-heavy-job-at-a-time discipline and the active tune.

Things I would deliberately defer: another large unrestricted CMA sweep; globally prohibiting small-dragon deaths; immediately protecting all length-4 dragons; increasing the old beam without fixing its model; a giant neural policy; and assuming all public replays contain exact private observations. Each has either contrary local evidence or a prerequisite that is currently missing.

## Appendix: evidence and reproducibility

**Scope.** This review used repository documents, frozen/development source, existing result JSON, public website data and replays, official game documentation, and primary research papers. It did not run new bot matches, start training, modify bot code, stop the active tune, or upload a submission. Runtime/parity figures are reported from existing project records, not newly reproduced benchmarks.

**Recent replay analysis.** Team identity came from the website and was joined to A/B sides through battle metadata. All 155 replays in the stated cohort were decoded using the existing `bcsim.replay` / `bcsim.analyze` logic. Eight illustrative replays were also inspected with `bcsim.feed_trace`: 563874, 557811, 643237, 643235, 647761, 572261, 567662, 577159. Those eight were selected for diagnosis, not randomly sampled; their transfer statistics must not be generalized as a league-wide rate.

**Intervals.** Recent win-rate uncertainty used 10,000 resamples of the 31 whole five-game battles. The book/shift comparisons used 10,000 resamples of paired `(run, seed)` blocks independently within each of the ten fixed maps, keeping both sides and all six opponents together within a block; point estimates average maps equally. Random seed: 20260930. These differ deliberately from the stored reports' aligned-score intervals, which resample `(map, seed)` blocks. Neither estimates the uncertainty of transporting results to novel opponent families.

**Important limits.** The live cohort has no verified version boundary. Public timer/sonar redaction prevents exact private-observation replay. Corpse provenance is observational and does not prove intent. Final-ID food counts omit split ancestry. Sparse per-map results do not prove causation. Source findings establish mechanisms, not their frequency or Elo cost. The GPU recommendation assumes the card is a GTX 980; actual hardware and software compatibility still require inspection.

**Local reading trail.** In addition to the linked sources: `README.md`, `CLAUDE.md`, `V6_CORE_PLAN.md`, `COMPETITOR_RESEARCH.md`, `TOP_TEAMS_SCOUTING.md`, `CORPUS_STRATEGY_AUDIT.md`, the older strategy/hybrid experiment notes, current tuning and perturbation code, `bcsim/official_suite.py`, `bcsim/reconstruct.py`, and the existing nicked v92 source copy. Competitor code informed hypotheses about identity, relay control, and recipient safety; those mechanisms still require experiments in our substantially different swarm policy.

### Recent cohort index

Each listed battle contained five games with consecutive IDs beginning at the battle ID: for example, battle 563873 contains games 563873–563877. Results are from team 777's perspective. This index makes the 155-game cohort recoverable without depending on temporary analysis files or a changing first page of results.

| Battle ID | Opponent | Wins–losses |
|---|---|---:|
| 647761 | Oxbridge Rejects | 5–0 |
| 643234 | Hydra | 2–3 |
| 642787 | Wapowpow | 3–2 |
| 638831 | PoGang | 1–4 |
| 634336 | Wapowpow | 2–3 |
| 630049 | Oswald | 4–1 |
| 626193 | Quantify | 3–2 |
| 624671 | Silly Stamies | 3–2 |
| 622658 | Just Reboot Normalize | 3–2 |
| 618800 | TYSHBK | 2–3 |
| 614579 | 11 | 2–3 |
| 610252 | All Roads Lead to Makuhari | 1–4 |
| 605576 | AllYouNeedIsKill | 3–2 |
| 600943 | An IQ too high? | 4–1 |
| 602708 | Quantify | 3–2 |
| 596188 | PoGang | 2–3 |
| 598686 | Quantify | 2–3 |
| 591396 | Hydra | 2–3 |
| 586806 | Oxbridge Rejects | 5–0 |
| 581660 | UNSW Sigmas | 1–4 |
| 577155 | !ghaplebaaz | 2–3 |
| 572261 | codih | 1–4 |
| 574924 | Silly Stamies | 3–2 |
| 567658 | 360 no scope | 3–2 |
| 569533 | Silly Stamies | 2–3 |
| 562716 | bongcloud | 3–2 |
| 563873 | CookAgent | 1–4 |
| 558310 | Ravenus | 4–1 |
| 557809 | CookAgent | 2–3 |
| 552926 | fandagong | 1–4 |
| 548054 | Candiru | 4–1 |

The next milestone should be a **small, auditable set of changes that beats frozen v10g on fresh current-pool games**, while the spare machine produces a better learned evaluator. That is a concrete route toward top 100 and a useful foundation even if a larger learning project later becomes worthwhile.
