# UNSW Battlecode — team 777

Development and research archive of a solo UNSW Battlecode 2026 bot: Python heuristics, a learned linear movement ranker, a C++ port, CMA-ES tuning, queen tactics, and the experiments that succeeded or failed.

**Publication edition: 14 October 2026.** Development snapshot: `a979c15` (12 October). Latest adopted local bot: **v12z**, hash `5a2c6685c062fff3`. Live snapshots stop on October 12; they are not a current leaderboard check. Top 100 was the objective, not a verified final achievement.

## Start here

- [Project writeup](PROJECT_WRITEUP.md): the complete narrative, versions, experiments, outcomes, and suggested replay/video sequence.
- [Audited history](PROJECT_HISTORY.md): detailed chapters, original reports, run registers, and provenance. The original October 3 snapshot is preserved and extended by a later chapter.
- [Experiment log](FEATURE_EXPERIMENT.md): results through D22 and the October 12 head-to-head check.
- [Research continuation](NEXT_STEPS_2026-10-14.md): completion of the interrupted review, reconciled with work that subsequently landed.
- [Publication contents and restoration](PUBLICATION.md): Git contents, release data, checksums, and exclusions.

## Final local result

v12z retains v12x's exploration and small-map opening changes, adding sprint queen attacks, paid queen escape, and the trapped-worker queen-sparing rule. D22: **741/1,224 wins versus 671/1,224** for v12x, **+5.7 percentage points**, reported interval **[+2.4, +9.1]**. A separate October 12 direct comparison was **91/136 for v12z**, over 17 maps, both sides, and four fresh seeds. Recorded sandbox maximum: **12.4 million CPU points per dragon-turn**, against a 100-million limit. These are local results, not estimated ladder gains.

The October 12 live snapshot was rank **153 of 1,001**, rating **1604**, with rank 100 at **1813**. The inferred v12z-era five-game-battle cohort won **948/1,995** against opponents averaging **1632**. Deployment was inferred from timing and behavior, not verified against a server hash. New maps and different opponents limit local/live comparisons. See the writeup for cohort caveats.

## Layout

| Path | Contents |
|---|---|
| `versions/` | Frozen bots, parameters, models and version notes |
| `cppbot/`, `cppbot_inproc/` | C++ working core and evaluation bridge |
| `framework/`, `mybot/`, `opponents/` | Python framework and project-created opponents |
| `bcsim/` | Replay reconstruction, datasets, evaluation, optimization and guarded runners |
| `experiments/`, `maps/` | Feature/tuning configurations and historical evaluation maps |
| `results/` | Plans, reports, outcome rows, diagnostics and experiment snapshots |
| `data/`, `replays/` | Corpus metadata; bulky data restored from release assets |
| `showcase/` | Illustration scripts/tables and separately archived replays |
| `docs/project-history/` | Audited history and preserved evidence |
| `battlebot-*.zip` | Original retained submission packages |

## Reproduction boundaries

The project spans incompatible rules/runtime versions. Keep old longest-dragon tests, seeded 1.1.0 tests, and queen-era 1.2.9 tests separate. Map lists called “current” in code refer to the sampled October 3 rotation; more maps appeared later.

Use each run's frozen plan and parameters. Do not replace tuned frozen parameters with working-template defaults. Reports and outcome files can be inspected without new matches. A fresh machine needs Python, the relevant `unswbc` dependencies, and a C++ compiler. Some scripts retain original machine paths. In-process evaluation does not measure judge CPU cost.

The queen launcher expects `unswbc==1.2.9` under `results/queen-runtime-packages/1.2.9/`. After configuring Python and dependencies:

```text
python -m pip install --no-deps --target results/queen-runtime-packages/1.2.9 unswbc==1.2.9
```

This installs only the isolated package, not its dependencies or compiler. See [official CLI documentation](https://game.battlecode.au/docs/cli) and the historical setup notes. External opponent sources without redistribution permission are referenced, not included.

Use guarded runners and one heavy job at a time. The original machine used at most 12 workers after memory failures; other machines need their own safe limit. The 132 single-seed showcase games illustrate mechanisms and are not strength evidence.

## Rights

Public availability does not assign one license to every component. See [third-party notices](THIRD_PARTY_NOTICES.md). No new project-wide license is asserted. Original third-party notices and redistribution restrictions are retained.
