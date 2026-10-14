# New mover / R5: staged implementation instructions for Claude

> **1 October status:** R5 failed its online screen and is stopped; see [NEW_MOVER_RESULTS.md](NEW_MOVER_RESULTS.md). New queen scoring and length-dependent free movement change the action representation and labels. [STRATEGIC_RESET_2026-10-01.md](STRATEGIC_RESET_2026-10-01.md) supersedes this plan's implementation priority. The following is a historical experiment contract; do not restart it automatically.

**Status: instructions only. No implementation or training was performed to create this plan.**

Read [CLAUDE.md](CLAUDE.md), [WORK_QUEUE.md](WORK_QUEUE.md), and the latest entries of [FEATURE_EXPERIMENT.md](FEATURE_EXPERIMENT.md) before starting. This document specifies the mover work in queue priority 3. It does not replace the queue's other experiments or authorize submission.

## 1. Decision: what to build

Build an **action-conditioned residual move scorer**, trained on the consequences of alternative moves taken by our own bot. Its first neural version is a shared **64 → 24 → 1 MLP**, with ReLU hidden activation and a bounded scalar output: **1,585 trainable parameters**. Evaluate it once per eligible direction, at most four times per decision.

The NN learns a correction to the incumbent's complete movement score. It does not initially replace the rules, choose a king, decide to sacrifice, select split sizes, issue sonar, or run search during a live turn. The simulator does expensive teaching offline; deployed inference is small C++ matrix/vector arithmetic.

Why this design:

- v3 is valuable; removing or weakening it hurt substantially.
- R4 predicted nicked v92's moves better but played worse. Labels must assess consequences under our own continuation policy.
- The current mover combines food, space, danger, hub, goal and king attraction with W_V3 times the old ranker. A replacement trained in isolation can be overwhelmed by, or double-count, those other terms.
- A bounded correction to the actual combined score preserves a strong fallback and makes the first experiment attributable.
- Context allows the same local geometry to mean different things for a newborn, worker, feeder or protected collector.

The NN output is a **ranking correction, not a calibrated win probability or confidence estimate**. No CNN, recurrent network, transformer, PPO loop or full multi-agent RL system in this first implementation.

## 2. When to do it

At the last inspected experiment-log entry, sonar adoption ages 30/60 had mild initial gains and were entering fresh-seed confirmation with perturbed layouts, seeds 341001–341003. Re-read the log: this is a historical checkpoint, not a statement that the job is still running.

1. Let any active guarded game job finish; inspect its result.
2. Freeze the latest actually validated incumbent, its artifact hash, parameters, engine version and opponent versions. If the sonar variants fail confirmation, retain v10h; do not assume an experimental variant is the new base.
3. Start the mover's contract and rollout pilot in the next available heavy-job slot. Resource/endgame research need not be “solved” first, but do not silently change those policies while labeling or validating R5.
4. If another structural change is promoted during this work, finish the current comparison against its frozen base. Then explicitly rebase and revalidate; old continuation labels are not automatically current.
5. Implement each stage below only after its predecessor's gate. A failed gate means investigate or stop that branch, not automatically enlarge the network.

Maintain a short stage checklist and results in **NEW_MOVER_RESULTS.md** when implementation begins. Record the current stage, frozen hashes, completed gate, next action and exact run directory after every batch. This is the handoff location for a later Claude session.

## 3. Scope and integration contract

### First eligible decisions

R5 is active only after the incumbent has chosen to enter ordinary movement, when at least two ordinary candidate moves remain. Preserve the incumbent's candidate legality/feasibility filters and deterministic tie-breaking.

For the initial experiment, defer the entire decision to the incumbent if its attack-specific candidate branch is present. This avoids comparing learned scores to a differently scaled attack score. Also preserve feeding, ordinary splitting, emergency split fallback, and all existing action-priority rules. Record the fraction of turns and failure cases this eligibility rule excludes.

All “off,” zero-strength, invalid-input, numerical-failure and unsupported-context paths return the exact incumbent decision. A hard CPU-budget fallback also uses the incumbent; never leave an empty action accidentally. Preserve deterministic operation in the reference backend.

### Where Claude should inspect

| Existing component | Intended use |
|---|---|
| cppbot/v6_brain.hpp: score_moves and Brain decision order | Find the full ordinary-move score and insert a separately switchable correction after the existing score adjustments |
| cppbot/model.hpp | Existing generated v3/R4 parameters; preserve them and avoid hand-editing generated weights |
| framework/action_value.py and C++ v3 feature implementation | Existing 24 features and their Python/C++ consistency |
| bcsim/ranker_v4.py | Reuse useful corpus/export conventions; do not reuse opponent-action labels as the R5 objective |
| bcsim/match.py, replay.py, reconstruct.py | Deterministic game reconstruction and reference event comparison |
| bcsim/guard.py, bounded.py, official_suite.py | Resource lock, worker cap and evaluation coverage |

Reinspect current implementations; line numbers and available helpers can change. Some needed components—especially the forced-action intervention and memory-aware feature logging—are **new work**, not presumed capabilities of these modules. Keep shared Python source in framework and synchronize through the established workflow; keep C++ changes in canonical source, not frozen versions or generated bot copies.

### Exact score interface

Let S0(a) be the **complete incumbent score** for ordinary move a. Define q0(a) = [S0(a) − mean of S0 over eligible moves] / s, where s is one positive score scale frozen from the training set. Start with the median nonzero per-decision score range, with a documented numerical floor.

The network emits f(a); use residual r(a) = 2 × tanh(f(a)). Rank by:

**q(a) = q0(a) + lambda × r(a).**

Training initially uses lambda = 1. Deployment includes lambda = 0 as the identity control and a small development-only choice among 0.25, 0.5 and 1. Do not simultaneously retune W_V3 or the rest of S0.

Let a0 be the incumbent choice and a* the highest q. Override only when q(a*) − q(a0) exceeds a fixed margin tau; otherwise use a0. Initially tau = 0 with incumbent tie preference. At most test one additional predeclared development-set margin. This is a conservatism gate, not probabilistic confidence.

Freeze normalization, s, lambda, tau, feature schema and model weights in one versioned artifact. Do not subtract v3 and add it a second time: the residual modifies the full S0 once.

## 4. Feature schema: 64 floats per candidate action

Use a shared scorer so directions are compared through the same function. Do not provide map name, team name, opponent identity, absolute dragon ID or absolute coordinates as shortcuts. Candidate-relative distances/progress and available topology are preferable.

Each feature must have a written definition, source, range, missing-value behavior and C++/training implementation. Normalize using training data only; keep binary flags binary, clip continuous features to documented ranges, and never let unknown equal known-zero without a validity flag.

| Slots | Count | Inputs |
|---|---:|---|
| 1–24 | 24 | Existing v3 candidate features in their existing order, preserved for the first comparison |
| 25–36 | 12 | Decision context, specified below |
| 37–64 | 28 | Candidate-specific context, specified below |

**Decision context, 12:** normalized round; normalized remaining rounds; log-scaled own length; team unit count / unit limit; clipped own age; founder flag; incumbent protected flag; active cash-target flag; known-hub flag; fraction of static map information currently known; local spawn-rate estimate; validity of that rate estimate.

Round and remaining rounds are redundant but explicit in version 1; removing redundancy is a later ablation, not a reason to drift the schema mid-run. “Founder” means born at the start, not “king.” The protected/cash flags expose existing policy intent without inventing a new controller.

**Candidate context, 28, in this order:**

1. Four baseline signals: centered/scaled S0, its weighted v3 contribution, the remaining non-v3 contribution, and whether the move continues the current facing.
2. Six topology signals: portal-crossing flag; landing-location-known flag; landing information age; capped estimated reachable room divided by own length; normalized known exits; landing surroundings sufficiently known flag. Unknown landing information uses masked values. The room estimate is the incumbent's estimate, not ground-truth guaranteed space.
3. Six resource signals: landing pearl-status-known flag; pearl-present flag; valid route distance to selected hub; change in that distance; target spawn-rate-known flag; estimated target spawn rate.
4. Six collection signals: valid route distance to cash target; change in that distance; target information age; validity of that age; blocking-the-known-recipient-front flag; recipient currently visible flag.
5. Six interaction signals: nearby friendly-head count; nearby enemy-head count; destination threatened by a visible lower-ID enemy; threatened by a visible higher-ID enemy; visible fraction of own body; largest nearby enemy visible-length lower bound relative to own length.

Use true walking distance only when available under the same live memory. Do not label a geometric approximation as exact; encode invalid/unknown and keep the fallback definition consistent. Threat features are conservative estimates from live information, not exact future enemy actions. Enemy visible-body counts are lower bounds, not full lengths.

Features may require additional bookkeeping. Log actual per-dragon live memory while generating local data; an observation block alone cannot reproduce historical hubs/goals or remembered portal exits. Sonar payloads redacted from public replays cannot be recovered by setting them to zero. Public games are for diagnosis, not the primary supervised feature corpus.

If a feature is unavailable, document and reserve its slot with validity false; do not fill it from privileged simulator state. If important omissions make the 64-input contract unsuitable, revise and hash the schema before collecting the main corpus.

## 5. Teacher: counterfactual moves under our own policy

### Deterministic intervention first

For a chosen local decision, identify game hash, map/layout, seed, side, dragon ID and round. Replay the original game from the beginning, maintaining every bot's private state and RNG. Override exactly that one eligible move after the bot's normal decision/state updates; retain its other output under a documented convention. Then let the original frozen policies continue.

“No override” and “force the original chosen move” must each reproduce the reference game, including subsequent behavior. Exclude volatile timing/log fields from event equality, but not actions, tile changes, deaths, splits or outcomes. If the adapter changes memory or RNG on no-op intervention, fix it before collecting labels.

A proposed override is the initial action actually implemented by the future mover, not a transcript of the original future. Recompute subsequent decisions from their changed observations. Do not replay a canned future action sequence.

Full replay from the beginning is the default. Do not promise snapshot speedups unless engine and bot-private-state snapshots have been verified.

### Which decisions to sample

Pilot: 200–500 decisions from multiple complete games, all 15 maps and both sides represented in the source corpus. Include early food access, target-versus-local-food conflicts, crowding, portals, late collection and valuable-dragon danger. Include a random background sample so the dataset is not only failures.

Cap examples per game and nearby turn sequence; keep sample weights or strata. Track excluded split/sacrifice/attack decisions. The mover cannot solve a failure caused entirely by one of those excluded actions.

Start with at most four ordinary directions per decision. Evaluate all candidates from the same prefix. Changing the initial game seed changes the state and is not another rollout of the same decision. Broaden evidence with independently seeded source games. Only branch future randomness from an identical state if a validated continuation-state/RNG interface later makes that possible.

### Outcome targets and ambiguity

The primary label is the terminal team result: win 1, draw 0.5, loss 0. Do not use total length or individual survival as the primary teacher objective.

Run the 200-decision throughput pilot to terminal when feasible. A short continuation of approximately 30 rounds can screen immediate consequences, but nonterminal decisions remain unlabelled for game-result preference. Extend them rather than silently treating short-term growth as a win.

Store terminal result, both teams' longest and total lengths, elimination time, valuable-dragon survival and lineage-aware length expenditure separately. For candidates with the same terminal result, terminal aligned margin may supply a **secondary, lower-weight** preference, flagged as such. Set its loss weight initially to 0.1 relative to a terminal-result preference. Exclude tiny or unstable secondary differences. Confirm improvements on wins; more decisive wins are not automatically more wins.

Repeated execution of an identical deterministic branch is a correctness check, not extra evidence. Paired outcomes from one hidden state are noisy estimates of what a partially informed policy should do in similar states. Do not expose that hidden state to the student.

**Pilot gate:** report runtime per prefix/branch, label distribution, proportion of decisions with useful preferences, and representative reversals. The best terminal branch at each sampled state is an oracle upper bound, not an unbiased teacher win estimate. Fit a provisional simple residual on one part of the pilot and evaluate its choices on decisions from reserved source games: choose without revealing their branch outcomes, then compare the already recorded outcomes with the incumbent's. This small pilot checks that the labels contain learnable signal under live-visible features; it is not a full-game promotion test. A separately validated continuation-resampling interface can later support an independent rollout-teacher check, but is not assumed here.

If almost all alternatives tie, increase useful state diversity or extend the horizon. If labels are unstable or the teacher does not improve held-out decisions, stop scaling. More NN parameters cannot repair an uninformative or biased teacher.

## 6. Models, loss and training

Train the following on identical grouped data partitions:

| Model | Purpose |
|---|---|
| Frozen incumbent | Real performance baseline |
| 24-feature linear residual | Isolate benefit of outcome labels without new context |
| 64-feature linear residual | Isolate context from network capacity |
| 64 → 24 → 1 NN residual | Test nonlinear interactions between context and action features |

The shared one-hidden-layer NN has 64×24 + 24 + 24×1 + 1 = **1,585 parameters**. At four candidates it uses about 6,240 dense multiply-accumulates, excluding feature extraction and activations. That arithmetic count is not a judge CPU benchmark. Use float32 during training; export enough precision and validate the chosen C++ arithmetic.

Use a weighted pairwise logistic ranking loss on q(a) − q(b) for teacher-preferred alternatives. Keep all comparisons from one decision in the same batch/group. Cap total weight per decision so a four-action state does not dominate a two-action state. Add modest L2 regularization and a small residual-size penalty to favor the incumbent where labels are weak. Include all legal candidates at inference, not only candidates appearing in retained training pairs.

Suggested initial training defaults, to be measured rather than treated as tuned facts: Adam, learning rate 0.001, batch about 256 decision groups, at most 50 epochs, early stopping after five validation epochs without improvement, and three fixed training seeds. Use stable randomness and save all seeds. Select regularization and checkpoints using development data only; no large hyperparameter sweep.

Start with a zero output layer so the initial residual is zero. Verify that hidden weights begin receiving gradients after the output layer updates. No dropout or batch normalization in version 1; keep deployment simple and deterministic.

Split by **whole source-game groups**, with side-swapped matches, counterfactual siblings and related seed/layout cases kept together. Reserve fresh seeds and at least one opponent-family/perturbed-layout challenge for final game evaluation. Store explicit manifests; do not depend on Python's process-randomized hash or ad hoc filename splitting.

Offline metrics: pairwise preference accuracy, terminal-result regret relative to evaluated alternatives, secondary-margin regret separately, override frequency, outcome by role/phase/map family, and calibration of the override margin as a decision rule. NN softmax scores are not proof of confidence.

Proceed to NN even if the linear residual underfits, provided the teacher gate passed. If the linear model is equally good in actual games, keep the simpler model.

## 7. Stage schedule and required deliverables

| Stage | Work | Required output | Advance only when |
|---|---|---|---|
| M0 — freeze | Inspect current runs, freeze base/opponents and write experiment contract | NEW_MOVER_RESULTS.md + immutable run manifest | No overlapping heavy job; incumbent and evaluation conditions are explicit |
| M1 — identity/parity | Implement disabled/zero residual, feature logging, no-op intervention, Python/C++ feature comparison | Reference fixtures and parity report | Off and zero-strength preserve incumbent actions; intervention preserves future events |
| M2 — teacher pilot | Label 200–500 decisions and measure cost/information | Pilot dataset, oracle upper bound, provisional-student held-out check | Useful, learnable preferences under visible features; affordable throughput |
| M3 — data and linear control | Expand initially to about 2,000 well-spread decisions; train both linear controls | Dataset manifest, models and grouped validation | Labels/features sound; choose bounded candidate configurations |
| M4 — NN | Train the 1,585-parameter model on the same data | Three-seed fit report, frozen normalization and model artifact | Held-out ranking/regret justifies a candidate; do not require imitation accuracy |
| M5 — C++ integration | Export generated parameters and run runtime/parity checks | Export manifest, feature/output fixtures, judge-budget report | Finite outputs, matching selected actions except documented numerical ties, safe runtime |
| M6 — game comparison | Compare incumbent, best linear and NN candidates | Full-suite paired report with mechanism diagnostics | A candidate improves actual wins with acceptable map/family behavior |
| M7 — confirmation | Fresh seeds and original/perturbed layouts, locked model/settings | Confirmation report and rollback artifact | Strong-panel win gain survives confirmation without material hidden regression |
| M8 — iteration or handoff | Collect states visited by the winner, or record why it failed | Next-stage decision and candidate artifact | No automatic upload; keep/revert based on results |

M1 fixtures should cover portals, stale/unknown targets, occupied tails, newborns and king contexts. They verify a new interface, not just mirror implementation. Do not build a new simulator for M1; use the existing engine as the reference.

For normalized model outputs, start parity tolerance at 1e-5 × max(1, absolute reference output), and require matching decisions whenever score separation exceeds the combined numerical tolerance. Test exact tie handling explicitly. If tolerances must change, document the numerical reason; do not relax them to conceal an extraction or export mismatch.

Set a time/branch budget before M2. If it cannot fit the measured budget, reduce the pilot size or reuse validated prefixes—not validation coverage. Expand toward 10k decisions only after M6/M7 provide reason to spend more compute. Measure throughput instead of promising a fixed training duration.

## 8. Game evaluation and promotion

For each bot-change evaluation, use all **15 ranked maps, both sides**, distinct engine seeds and the repository's coverage checks. A starting comparison with six opponents and three seeds is **540 games per candidate** on the 15 base layouts. Diagnostic probes do not replace it.

Judge the currently sampled 10-map ladder pool first; report the other five separately. Include strong accessible opponents but identify shared families: several nicked versions are one family. Add an available genuinely different family when possible, without inventing access to a top team's private bot.

Lock candidate selection before fresh confirmation. Use the originals plus relevant perturbed layouts; if 25 layouts, six opponents, both sides and three seeds are used, that is **900 games per candidate**. Allocate enough samples to the observed uncertainty instead of declaring a tiny positive delta significant.

Use paired game-win difference as the promotion metric, with ties scored consistently. Report confidence intervals over matched conditions, opponent-family and map breakdowns, current-pool versus guard results, and the strong panel separately. For final promotion, seek a positive lower confidence bound on the primary current-pool comparison and no meaningful guard/family regression. An unresolved interval means “not established,” not a successful NN.

Mechanism diagnostics: fast-spawn food access, population before contact, king-lineage retained length, valuable deaths, and override effect by role. They explain wins; they cannot substitute for wins.

Do not multiply test data into training after every failed candidate and still call it held out. Retire consumed confirmation sets explicitly and obtain fresh conditions for the next iteration.

## 9. Deployment and compute constraints

Run labeling, corpus generation and validation through the existing guard/bounded infrastructure: one heavy job, at most 12 workers, respecting actual RAM headroom. Model fitting is small enough to start on CPU on the current PC. GPU support is optional; do not make the GTX 980 machine or a CUDA installation a prerequisite.

Inference uses exported arrays, normalization constants and ordinary C++ arithmetic. No training framework is required in the submitted bot. Do not assume tiny matrix multiplication guarantees low CPU: features and path queries can dominate. Reuse existing per-turn computations and profile the complete decision.

Use representative largest-map, late-population, portal and long-king cases in the judge sandbox. Initial engineering budget: target under 5M additional points per eligible turn and keep tested total turns under 80M of the 100M limit, with the incumbent fallback retained. These are proposed headroom gates, not measured guarantees.

The serialized model must include schema/version, base-policy hash, feature definitions, normalization, training/validation manifests, architecture, weights, score scale and integration settings. Keep generated C++ output reproducible from that artifact and preserve v3 and the rollback bot.

## 10. After the first mover passes—or fails

**If it passes:** collect some decisions from the updated mover's own trajectories and mix them with older coverage. Relabel under the explicitly chosen continuation policy. Confirm the next iteration as a new candidate. This addresses policy-induced state-distribution shift.

**If the teacher is useful but the NN fails:** inspect feature visibility, context aliasing, label noise, score-scale mismatch and residual bounds before adding layers. A missing target/role cannot be repaired just by model size.

**If the mover hardly reaches the relevant failures:** publish eligibility/exclusion counts. Split/sacrifice/attack mistakes require a later action-policy experiment; do not quietly expand R5's action space midway.

**Only after a successful baseline mover:** consider a separate controller choosing harvest, rendezvous, collect and preserve roles. Then consider exact short tactical search for valuable dragons. Each is a separately versioned intervention with new labels and full-suite checks.

**If wins do not replicate:** retain the incumbent and summarize what was learned. Do not promote on lower training loss or a pleasing replay.

The empirical direction is consistent with [rollout-based policy classification](https://users.cs.duke.edu/~parr/icml03.pdf), [adaptive rollout allocation](https://arxiv.org/abs/0805.2027), and [training on the learner's induced state distribution](https://proceedings.mlr.press/v15/ross11a.html). Those papers motivate the method; their guarantees do not directly transfer to this partially observed multi-agent game.
