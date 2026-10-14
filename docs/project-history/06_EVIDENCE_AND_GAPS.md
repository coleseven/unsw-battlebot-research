# 6. Infrastructure, evidence corrections and archival continuation

[Project history](../../PROJECT_HISTORY.md) · [Previous](05_QUEEN_ERA.md)

## What “everything” means in this edition

The archive captures all 49 root Markdown documents present at collection, selected report metadata from the results tree, experiment JSON configurations, the official-map manifest and frozen v11t parameters. The run register lists 314 top-level result directories, including 186 dated runs. The tuning register contains **12 actual run directories**, including incomplete starts; pointer files are not counted as runs. Git history contains 151 reachable commits through `69095e5`.

The narrative manually synthesizes the main experiment logs, research writeups, selected saved comparisons and the most recent source/reporting logic. **Archival inclusion is not an independent audit of every run.** Source reports are preserved in full where selected, including their own detailed subvariants and audit counts. The appendix and register prevent small or unsuccessful runs from disappearing merely because the narrative groups a family of experiments into one table.

No global total of “games played” or “CPU hours spent” is asserted. Summing all report denominators would double-count controls, resumes, repeated deterministic conditions, replay audits and overlapping live cohorts. It would also mix invalid and valid suites. Training evaluations are not necessarily one game each.

## Infrastructure actually built

| Capability | Concrete work and purpose | Evidence boundary |
|---|---|---|
| Frozen evaluation | Self-contained candidate/opponent copies, source hashes including dependencies, plans, side pairing, error separation, map coverage | Git commit alone does not identify dirty experiment inputs |
| Shared framework sync | Edit shared framework and synchronize live bundles; frozen versions excluded | Prevents a baseline silently changing with a candidate |
| Replay decoding/reconstruction | Decode server/local replays, reconstruct the acting dragon's observations and histories, verify chosen actions | Action reproduction verifies implementation fidelity, not counterfactual superiority |
| Dataset V2 | Complete action/sonar sequences, legal observation fields, provenance, cache invalidation, battle-grouped splits, streaming | Specification/tooling exists; full conversion of every replay is not asserted |
| Population/movement experiment runners | Fixed designs, selection gates, validation, procedural maps, replay audits and budget probes | Early engine randomness limits independence |
| Mixed-language opponents | Framework adapter detection, subprocess bot handling, prebuild and runtime fixes | Third-party snapshots stay local and pinned; no claim that all share our in-process ABI |
| CPU verification | Actual judge sandbox, per-turn maxima/percentiles, history-restoring probes, intentional-feeding classification | Sampled passes are not worst-case proofs |
| Judge-calibrated Python clock | Reproduce limited search effort in local Python tests | Corrected a major local/judge mismatch; not a native simulator rewrite |
| C++ code generation/parity | Parameters, learned weights and books generated; action and live-game equivalence | Parity tested specific builds and observations |
| In-process C++ | Independent handles, compiler/flag matching, cached DLL/shared-library builds | Speeds bot execution while still using the official game engine |
| CMA-ES | Parameter/group spaces, booleans, adaptive backend, evaluated means, warm starts, fresh seeds and paired map sampling | Training F is not held-out strength |
| Feature ablation | Group toggles, paired comparisons, map/opponent breakdowns, fresh-seed confirmation | Additive feature reports retained old removal-oriented verdict wording |
| Resource guards | Bounded process recycling, RSS/available-RAM checks, one heavy-job lock, worker caps and build locks | Historical crashes and partial runs must not become wins/draws |
| Map tooling | Semantic signatures, official/ladder suites, perturbations, hidden-spawn segregation, spawn reconstruction, 1.2.9 manifest | Original maps, inferred maps and actual current official maps are distinct datasets |
| Queen diagnostics | Original queen mapping, outcome classification, death causes, exact-case replay inspection | Elimination must be classified before round-limit queen comparisons |
| R5 teaching/export | Reply hooks, identity fixtures, 64-feature traces, forced continuations, residual fitting and C++ inference checks | Learner failed game screening; branch-state/RNG teacher was not completed |

Implementation files remain under `bcsim/`, `framework/`, `cppbot/`, `cppbot_inproc/`, `experiments/` and `tests/`. This documentation turn did not modify them or rerun their test suites.

## Corrections that must travel with the results

| Issue | Affected evidence | Correct historical treatment |
|---|---|---|
| Explicit open edges changed map signatures | First population run, screen/validation overlap | Use corrected map-audit; 96 games excluded by identity, originals preserved |
| Stale final lengths / incomplete hashing / game errors | Initial arena setup | Prefer repaired evaluations; original smoke reports retain their historical status |
| Deterministic repeats labeled as new seeds | Old-engine experiments, especially v4/v5/v7 | Different seed numbers need not be independent games;  bot RNG and board RNG differed |
| Navigation off-window index | Superseded preflight snapshot | No strength games on that invalid candidate; corrected run is separate |
| ctmes compile-cache race | First mixed v4 grower attempt | Excluded partial run; reran in a new frozen directory |
| Unused nicked cutoff constant | v4 phase experiment rationale |300-cutoff was not an imitation of the live opponent function |
| Host wall time overstated Python search | Early v6 comparisons | Use judge-calibrated fair-search/floor-fix release evidence |
| Feeding counted as invalid/no action | Some old sandbox output | Deliberate empty turns are strategic feeding; preserve historical classifier context |
| Engine1.1.0 changed pearl RNG | Tuned v7 recommendation | Multi-seed recheck reversed preference to untuned v7-base |
| Compiler tie behavior | In-process C++ development | Match toolchain/flags; parity belongs to the tested path |
| Recompile storm / memory instability | September28 operational failures | Keep partial artifacts distinct; use guarded runs and source/build signatures |
| Missing hidden spawners | Initial Sprint baseline, grouped ablation, portions of R5 source/test data | Retract unseen-map conclusions; ranked-map R5 rejection still stands |
| Waiting resume deleted running replays | Early queen-era ablation | Lock moved before cleanup; log records affected run redone |
| Old objective / old opponents after rule reset | Queen-era selection | New actual-outcome metric and queen-aware panel; old scoring cannot settle promotion |
| Approximate/outdated maps | Q-series versus C-series | Keep 1.2.3/reconstructed results separate from 1.2.9 current-map validation |
| Queen ID assumed from side | Side-swapped replay analysis | Derive original queen/team mapping from replay initial state |
| Overlapping live cohorts | Repeated ladder reviews | Deduplicate by game ID before combining; no simple sum of win rates |
| Post-split death association treated as cause | Queen-death diagnosis and C8 | Failed split restrictions reject that intervention, not every possible earlier action |

## Newly identified reporting defect: the C-series “current pool” column

This was found while preparing this history, through source inspection at the recorded cutoff. `bcsim/ablate.py` builds its pool set directly from `official_suite.CURRENT_POOL` and tests each game's map key for exact membership. The newer 1.2.9 files use lowercase stems and two renamed files, while the old tuple mixes uppercase stems and older names.

For C5's saved plan, the exact intersection is only:

`trophy`, `queen_of_spades`, `default`, `schooltime`, `weakhold`.

Thus the generated **“current pool” result is a five-map subset**, while 12 genuinely current maps are assigned to “other maps.” For example, the C5 report shows current-pool delta −0.003 and overall +0.070, despite every one of its 17 maps belonging to the intended current rotation. This is not evidence that the candidate only helped an obsolete regression pool.

The overall 17-map comparison and its win totals use the full result set and are not selected by this faulty membership condition. The report's literal header **“all 15”** is also stale, and “harmful(drop)”/“essential” are inherited from feature-removal reports even when the variant adds a feature. For the C-series narrative, use the **plan's map list, full-suite counts, named variant and actual delta sign**. Do not read those labels literally.

No experiment code was changed in this documentation task. A future reporting-only repair should canonicalize map identity, derive labels from the frozen plan, and regenerate reports from existing result rows; it need not replay matches merely to fix grouping. Preserve the originals so the correction remains auditable.

Sources: [C5 plan](snapshot-2026-10-03/results/20261003-134712-ablate-e3fcd5/plan.json), [C5 report](snapshot-2026-10-03/results/20261003-134712-ablate-e3fcd5/report.md), `bcsim/ablate.py` report function and `bcsim/official_suite.py` at commit `69095e5`.

## Numbers and uncertainty: conventions for continuing this writeup

- **Win count:** actual wins. W–D–L means wins, draws, losses, in that order. A score includes half draws only where explicitly described.
- **Signed outcome metric:** later `objective="wins"` uses win=+1, draw=0, loss=−1. A delta of +0.070 is not +7 percentage points of win probability. Draw changes also prevent inferring the exact metric solely from win counts.
- **Aligned metric:** the older composite result/longest/trajectory measure. Its numerical deltas cannot be compared directly to percentage-point win gains or later signed outcome deltas.
- **Matched panel comparison:** candidate and control each face the same contextual matchups. “571 versus 534” is not the head-to-head score between them.
- **Head-to-head:** explicitly named direct candidate-versus-control games, such as v11t 75/136 versus v11q.
- **Selection versus confirmation:** the winner of a screen is selected partly for favorable noise; preserve the separate untouched confirmation result and its losses.
- **Neutral versus rejected:** neutral means evidence was insufficient or mixed under the gate. Rejected means that tested configuration was not retained; it need not prove every parameterization harmful.
- **Measured mechanism versus causal explanation:** seeing more food, fewer deaths, more surviving queens or a later death is informative, but the tested game objective decides strength. Replay correlation alone does not identify which alternate action would have won.
- **Intervals:** retained as originally computed, with their clustering unit where documented. This edition does not re-estimate all intervals or claim simultaneous coverage after many experiments.
- **Dates:** use original UTC timestamps for website cohorts and explicit offsets for Git. Cloud author dates and local committer dates can disagree; topological history is preserved.

## What was proposed but has no completed successful run here

The archival distinction matters because plans often contain detailed implementation instructions:

- Full recurrent multi-agent reinforcement learning, centralized critic training and a self-play league.
- A complete independent-state/RNG branching teacher for repeated continuations from one decision.
- A successful nonlinear replacement for the deployed v3 linear ranker.
- A full belief-state/POMCP planner or a general learned strategic controller.
- Scheduled, lineage-aware delivery optimizing what the scoring dragon can actually collect.
- A universally beneficial cooperative traffic/reservation system.
- A separate GTX 980-machine research deployment.
- A demonstrated sustained top 100 finish.

Some underlying plumbing, smaller probes or related heuristics exist. None should be promoted in this history to a completed successful system without a concrete run and outcome.

## Remaining archival work, in priority order

1. **Reconcile result rows, not just reports.** For each dated run, count unique completed job keys, identify errors/resumes, distinguish control replay reuse, and classify completed/partial/invalid. The current register deliberately says whether metadata exists rather than certifying completion from a filename.
2. **Repair and document C-series map grouping.** The source-level mismatch is established above; regenerate the derived reports with canonical identities and compare full totals unchanged. Keep this separate from strategy changes.
3. **Establish upload boundaries.** Match local hashes, packaged ZIPs, submission IDs and website/upload records. v11q deployment is recorded; v11t is only a recommendation at this cutoff. Public redacted versions cannot fill the gap by assumption.
4. **Resolve counts in older live summaries.** The log's 14-battle/82-game and 30-battle/162-game descriptions do not trivially match five-game battles. Investigate series sizes, cohort filters or prose errors rather than changing numbers silently. Also reconcile Sprint “1–6” with the mentioned draw.
5. **Close unlogged tuning/feature outcomes.** Several directories contain partial starts or short optimizer campaigns. Their plans and available reports are preserved; do not assign promotion or failure solely because later work moved on.
6. **Audit teacher integrity before reuse.** Explain M2b's three errors/two reproduction failures, tag foodless-map source games, and preserve exact model/feature hashes and train/dev/test source-game membership.
7. **Reconcile source and release provenance.** The early bulk commit includes several days of work. Recover dates from frozen run plans and, if needed, original chat/session records; Git alone cannot identify every intermediate author/action. ZIP hashes are recorded, but not every ZIP was re-extracted and behaviorally verified this turn.
8. **Add an append-only experiment ledger for future work.** Give each experiment a stable ID, hypothesis, exact base, variant settings, runtime/map/opponent hashes, seeds, metrics, screen/confirmation role, result and final disposition. Link diagnostics separately from strength trials.

These items do not require repeating all historical matches. Much of the next archival pass can be read-only reconstruction from saved JSONL, plans and replay manifests. Expensive reproduction should target actual discrepancies.

## Archive organization and verification scope

`snapshot-2026-10-03/` retains selected source files under their original relative paths. `EVIDENCE_MANIFEST.json` records each copied file's SHA-256 and byte size; files were copied individually, so this is not an atomic snapshot of an actively changing workspace. The Git cutoff anchors tracked source, while copied uncommitted documents have their own hashes.

Report discovery skipped frozen bot source trees, map copies inside runs, opponent copies, replay directories, engine packages and build caches. It descended a bounded number of metadata levels. `RUN_REGISTER.md` is therefore an index of discovered artifacts, not a promise that no deeper report exists. Original raw data remains under the ignored `results/`, `data/`, `replays/` and `sparring/` trees.

`ORIGINAL_RUN_REPORTS.md` preserves historical text, including stale relative links and reporting labels. The readable chapters provide corrected context and links to selected captured sources. Do not execute command snippets in those preserved reports as current instructions without checking the current engine, maps and authorization.

The production code, active experiment logs, existing queue and upload packages were left unchanged by this history work. The newly authored chapters and metadata archive are the deliverable.
