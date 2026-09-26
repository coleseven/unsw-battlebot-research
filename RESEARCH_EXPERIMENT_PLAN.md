# UNSW Battlecode: initial research and experiment plan

Prepared 22 September 2026. These are proposed experiments, not measured results. Numbers for search sizes, model sizes, and evaluation budgets are starting configurations to benchmark, not established optima.

## Recommendation

Start with a modular hybrid: explicit per-dragon memory, a small finite-state controller for strategic intent, candidate action generation, and a scored movement planner. Add offline parameter optimization early. Test tactical search and small neural evaluators as interchangeable improvements. Treat full reinforcement learning as a separate, gated experiment.

These techniques solve different problems: a state machine chooses intent, search chooses actions, a neural network can estimate their value, and an evolutionary optimizer can tune either the heuristics or a small policy. Choosing one does not preclude the others.

Use Python for the existing baseline, experiment runner, data analysis, and training. Prototype a C++ planner when profiling shows that search or feature extraction limits useful decisions. The judge budgets 100 million CPU points and 48 MB per dragon per turn; its published flood-fill example is much cheaper in C++. Actual measurements of our bot decide when to port. Local unsandboxed speed does not establish judge compatibility. [Runtime limits](https://game.battlecode.au/docs/timeouts)

## Existing starting point

At inspection, `mybot/brain.py` uses BFS pearl routing, a static flood fill, and a neighboring-enemy-head penalty. `framework/bc.py` provides independent Brain instances and local observations. The opponent directories include starter, wanderer, greedy, turtle, splitter, and hunter variants. This is a useful initial opponent suite, not evidence of competitive strength.

The inspected movement helpers avoid all portals, inspect only the current 7x7 window, and do not distinguish threats by dragon turn order or sprint reach. These are natural experimental boundaries. Claude's setup is ongoing; this report does not certify or modify that implementation.

## Rules that change the engineering priorities

- Moves resolve in dragon ID order. Search must represent that schedule, including newborn dragons acting later in the same round. The current tail remains occupied during a collision check. Multi-step moves change the body after every step. [Execution order](https://game.battlecode.au/docs/execution-order)
- Winning prioritizes elimination, then the longest survivor at round 500, then total surviving length. Maximizing pearl intake or total length alone is an imperfect objective. [Scoring](https://game.battlecode.au/docs/structure)
- Head collisions kill both dragons regardless of size. A tiny expendable dragon can threaten a large scoring dragon. That makes selective sacrifice a legitimate candidate action. [Movement](https://game.battlecode.au/docs/movement)
- A split child starts with fresh memory. A team cannot assume a shared map, shared role assignment, or inherited recurrent-network state. [Splitting](https://game.battlecode.au/docs/splitting)
- A local view includes pearl countdowns, but future resets and unseen occupancy are uncertain. Keep uncertainty explicit. [Vision](https://game.battlecode.au/docs/vision), [Pearls](https://game.battlecode.au/docs/pearls)

## E0: establish trustworthy comparisons

**Question:** Can we measure a change without accidentally rewarding simulator bugs or overfitting?

Freeze the current bot and its dependencies as a baseline. Freeze opponent versions too: changing a shared helper can otherwise silently change both competitor and benchmark. Record code hash, framework hash, map, seeds, side, engine/toolkit version, and configuration with every result.

Use the official engine as the reference. If building a faster in-process simulator, compare its transitions and observations against the reference for wraps, both portal directions, pearl timing, moving tails, sprint costs, head collisions, splits, birth order, and end-of-round elimination. Test process-memory isolation as well as board mechanics. Match random event streams where possible; otherwise use fixed-event fixtures to separate RNG differences from rule differences.

Initial comparison budget: 200-400 games across maps, opponents, seeds, and both sides. Confirm finalists with 1,000 or more held-out games if throughput permits. These counts are screens, not guaranteed statistical power. Repeated deterministic matches are not independent evidence.

Primary metric: average game score, win=1, draw=0.5, loss=0. Also report the opponent-by-map matrix, longest-survivor margin, elimination losses, death causes, and p50/p95/p99/max CPU points. Bootstrap paired map/seed/side blocks; do not pretend paired games or turns from one game are independent. Preserve test maps and seeds that neither tuning nor training sees. Replicate stochastic training with at least three seeds for promising finalists.

Promotion requires a useful held-out improvement with uncertainty reported, acceptable performance in weak matchups, and no observed timeout or invalid-action regression. Reusing validation results to choose hundreds of candidates requires a fresh final test. [Why interval estimates matter](https://arxiv.org/abs/2108.13264)

## E1: establish a strong classical planner

**Hypothesis:** Better geometry and escape planning buy more early strength than complex learning.

Build a utility-based controller with a few modes: explore, forage, escape, engage, preserve. Use commitment or hysteresis to avoid changing targets every turn. Modes adjust priorities; the movement evaluator remains shared.

Compare incrementally:

1. Current greedy baseline.
2. Weighted action scoring with safe space, exits, pearl travel time, spawn timing, uncertainty, and enemy threat features.
3. Short path search that simulates the evolving body, pearl growth, and sprint costs.
4. Chokepoint/articulation-point penalties and an estimate of whether space remains available as the tail advances.

Start beam-search experiments with widths 8/32 and horizons 4/8 own decisions, under the same CPU cap. Replan after each real observation. Paths through unseen terrain are conditional plans, never certified safe routes.

Use BFS for uniform one-step distances and Dijkstra for weighted danger/costs. Ordinary Manhattan distance is not an admissible A* heuristic when portals can create shortcuts. Use zero or a portal-aware lower bound if optimality matters.

Hard filtering should reject malformed or demonstrably useless fatal moves, while separating intentional enemy-head trades into their own candidates. A safety layer cannot promise survival against unknown terrain or future enemy actions. When no survivable action is known, maximize team outcome rather than silently choosing an arbitrary death.

**Success signal:** Fewer self-traps and higher held-out score, not merely longer survival against harmless bots. Keep static flood fill as a cheap feature; its reachable-area count is neither a proof of escape nor an accurate model of moving bodies.

## E2: memory and uncertainty

**Hypothesis:** Reusing observations matters more than searching deeper inside the latest window.

Compare current-window-only behavior against:

- Persistent static terrain and discovered portal pairs.
- Static memory plus time-stamped pearls/countdowns and dynamic sightings.
- Those memories plus cautious symmetry inference and enemy reach estimates.

Static edges remain known. Unseen enemies and pearls become uncertain with age. Maintain the set of compatible map symmetries rather than guessing one immediately. Treat inferred occupancy as a hypothesis. A new child must reconstruct what it can from its own view; a parent can track its own body more completely over time than a newborn can.

First learn useful memory without sonar. This isolates the value of mapping from the cost of communication. [Map symmetry and wrapping](https://game.battlecode.au/docs/map-info)

**Success signal:** Improvements on mazes/portal maps and less repetitive wandering, without increased deaths caused by stale beliefs.

## E3: discover the right population strategy

**Hypothesis:** Population policy has a larger effect than fine movement optimization.

Hold movement code fixed and compare these deliberately different strategies:

| Variant | Policy | What it tests |
| --- | --- | --- |
| Single grower | No voluntary splitting; retain emergency splits | Strength of concentrated length |
| Limited colony | Split toward caps 2, 4, or 8; stop reproducing later | Whether early coverage repays lost size |
| Aggressive swarm | High cap, earlier splits, attack opportunities | Elimination pressure versus scoring |
| Grower plus escorts | Locally designated growers preserve length; others forage or attack | Value of role differentiation |

Use a coarse screen, not a huge Cartesian grid: split thresholds such as 6/10/16, small-child versus balanced splits, and several reproduction cutoff rounds. Inspect congestion, pearl availability, and the child's likely exit before splitting. Constant thresholds are experimental controls, not the final policy.

Role assignment must be implementable with local information. Prototype locally inferred roles, deterministic conventions, and later sonar-assisted announcements. Do not assume every dragon can identify a global champion or reliably detect its death.

**Success signal:** Match score by opponent/map/phase, supported by the maximum-length distribution, extinction risk, and friendly collision rate. There is no documented merge action; stopping reproduction does not recombine a swarm's length.

## E4: tactical search and selective sacrifice

**Hypothesis:** Short accurate adversarial search beats broad heuristic danger avoidance near enemies.

Compare:

1. An ID-aware danger map, including plausible enemy sprints.
2. Beam search against a small mixture of opponent policies: greedy, evasive, aggressive, and direct sacrifice.
3. Local minimax/alpha-beta over the nearest threats, with friendly units simulated by their own policy and a bounded set of sprint/split actions.
4. If still needed, sampled rollouts/MCTS over plausible hidden states and opponent behaviors.

Retain exact sequential resolution inside a candidate sprint: the enemy does not interrupt it. Simulate intervening dragons between our decisions in a deeper search. A short bounded sprint set is an approximation; evaluate its blind spots with longer-sprint opponents and adversarial fixtures.

Include deliberate head trades only when team value warrants them. A small dragon killing a larger enemy may be excellent, but sacrificing the team's last dragon can throw away the game. Enemy total length is not necessarily observable, so use bounds or uncertainty.

Global minimax over every dragon is a poor initial allocation of compute. Search nearby tactical interactions first. Under fog, ordinary perfect-information search risks making plans that depend on information the real bot will never receive. ISMCTS is a relevant later framework, not a drop-in solution. [ISMCTS paper](https://pure.york.ac.uk/portal/en/publications/information-set-monte-carlo-tree-search/)

**Success signal:** Fewer tactical deaths and profitable trades under the same judge budget. Use exact terminal outcomes when known; use estimated team value for uncertain nonterminal states.

## E5: evolution and automatic tuning

**Hypothesis:** The hand-built controller already contains useful behavior, but its tradeoffs are badly calibrated.

Start with random search as the control. Compare CMA-ES for roughly 10-30 normalized continuous parameters: space and exit weights, danger aversion, exploration value, pearl timing, sprint cost, and phase-dependent priorities. Keep discrete population caps and role structures in an outer coarse search. A genetic algorithm is reasonable for categorical structures or discrete strategy combinations; evolving an entire program or large neural network is a much larger initial search space.

CMA-ES is specifically designed for continuous, nonlinear, non-convex optimization. Its superiority here must still be measured. Compare methods on equal match budgets, paired scenario batches, and several optimizer seeds. [Hansen's tutorial](https://arxiv.org/abs/1604.00772)

Optimize match score against a diverse frozen league, then validate against fresh opponents and conditions. Keep archived champions so improvement does not mean only beating the latest self-play opponent. Rotate training scenarios between optimizer generations while pairing candidates within a generation. Favor robust improvements over a single large average gain that hides a fatal matchup.

**Success signal:** Consistent held-out gains over both hand tuning and equal-budget random search. Optimization runs offline; the submitted bot only loads the selected parameters.

## E6: a small neural network with a narrow job

**Hypothesis:** A learned nonlinear action evaluator improves choices beyond a tuned weighted sum, or approximates expensive planning cheaply.

Start with candidate features and a tiny MLP: approximately 40 inputs, hidden layers 64 and 32, and one score per candidate. This is only about five thousand parameters. Features should include geometry, threats, pearl timing, uncertainty, length, remaining rounds, and the candidate's costs. All deployed inputs must be available to that dragon.

Compare three evaluators using identical candidates and the same safety checks: tuned linear score, tiny MLP, and existing search. Train the MLP first from stronger offline planner preferences. Generate labels from observation-constrained beliefs; an omniscient teacher can recommend choices that are unlearnable from the student's information.

Collect mistakes on states the student actually visits and relabel them with the teacher (DAgger-style dataset aggregation). Split data by complete game/map, not adjacent turns, to avoid leakage. Later compare learned rollout-value targets against imitation targets; low imitation loss alone is not playing strength. [DAgger](https://arxiv.org/abs/1011.0686), [policy distillation](https://arxiv.org/abs/1511.06295)

If engineered features plateau, compare a small CNN on the 7x7 observation plus scalar inputs and explicit memory features. Portals still require connectivity information beyond ordinary local convolutions.

Train with an offline ML framework; export simple weights and inference for the permitted runtime. Benchmark feature extraction, inference, parsing, and output together. Do not assume the judge includes PyTorch or ONNX Runtime. [Available libraries](https://game.battlecode.au/docs/libraries)

**Success signal:** Better held-out play at comparable cost, or similar strength with enough saved CPU for additional search. Ship neither a model nor extra complexity merely because its training curves look good.

## E7: conditional reinforcement-learning branch

Attempt after measuring simulator throughput and establishing E0-E4. First spend a bounded pilot budget to plot strength against elapsed training time. Continue only if an overnight-scale run is feasible on the available machine and learning curves justify further compute.

Candidate: parameter-shared PPO with a small recurrent actor. Compare explicit map memory first; add a 32/64-unit GRU only when its value can be isolated. An optional centralized critic may use full simulator state during training, while the deployed actor gets only its own legal observation, memory, and sonar. Reset recurrent state at every birth. This is inspired by centralized-training/decentralized-execution methods such as MAPPO; published cooperative-game results do not establish performance in this adversarial game. [MAPPO study](https://arxiv.org/abs/2103.01955)

Start with a finite action set: normal moves, selected short sprints, and a few legal split sizes. Measure the cost of this restriction. Use team win/draw/loss as the principal return; indiscriminate pearl, survival, or population bonuses can reward behavior that loses the actual game. Test shaping as an explicit ablation. Train against historical policies and scripted opponents, not just identical current copies.

**Success signal:** Multiple training seeds beat the best classical bot and retain broad matchup coverage after export into the real runtime. If not, retain useful datasets or an auxiliary value model and stop spending competition time on that branch.

## E8: optional communication and unusual tactics

Compare no sonar against messages for nearby danger, intended movement, or a high-value resource location. Measure useful delivery rate and actual match-score benefit before adding elaborate coordination. A sender tag or checksum is not authentication; messages can reach either team without sender identity. Reject stale or geometrically inconsistent information. [Sonar](https://game.battlecode.au/docs/sonar)

Try stable cycling in a protected region as an endgame survival policy, but do not assume an enemy-free Hamiltonian-cycle argument survives kelp, portals, growth, and hostile interference. Test controlled sacrifice to feed a protected grower only as a later economic experiment: it destroys roughly half the donor's length and offers pearls to enemies. These should earn their complexity through results.

## Evidence and limits of transfer

A published Battlesnake implementation reports an RBC competition win using depth-limited minimax with alpha-beta pruning and handcrafted heuristics. This is evidence that classical search is a credible starting point, not that its exact algorithm transfers. [Author's repository](https://github.com/calvinl4/battlesnake-winter-2022)

A Battlesnake MCTS/RL study improved its learned policies over iterations, but its third iteration won only 6.8% against three flood-fill opponents in its reported four-player evaluation. It demonstrates both learning progress and the danger of treating self-improvement as competitive strength. [Study, Table II](https://uvicai.ca/assets/images/MCTS-and-RL-for-a-Four-Player-Simultaneous-Move-Game.pdf)

Another Battlesnake study found benefits from adding human heuristics to RL. That supports testing hybrid methods, without proving RL is the best use of this competition's development time. [Battlesnake Challenge](https://arxiv.org/abs/2007.10504)

UNSW differs materially from the researched Battlesnake variants: sequential turns, local vision, splitting, costly sprints, portals, and mutually lethal head collisions. Borrow methods and experimental discipline; rebuild rule assumptions.

## Suggested first-week order

1. First 1-2 days: freeze baselines, validate the simulator, collect a matchup matrix and failure taxonomy, and measure actual judge cost. Begin E1.
2. Next 2 days: E2 and the coarse E3 population comparison. Establish which failures dominate before expanding the architecture.
3. Next 2 days: E4 tactical search and E5 parameter tuning using fixed experiment budgets.
4. Then: choose E6 if decision evaluation is limiting strength; choose a bounded E7 pilot only if simulation throughput supports it. Keep the best measured bot available throughout.

Initial allocation suggestion: 60% of development effort to rules, evaluation, movement, and memory; 25% to population/combat experiments and tuning; 15% to exploratory learning. Reallocate based on results, especially if simple bots already saturate the opponent suite.
