# Claude task: make evaluation results trustworthy

Own `bcsim/arena.py`, `bcsim/match.py`, `bcsim/paths.py`, and `bcsim/sync.py`.
Put your tests in `tests/test_arena.py` and `tests/test_sync.py`.

1. Exclude frozen `versions/` from synchronization. Ensure freezing captures all
   dependencies needed to reproduce the bot, including feature code when used.
2. Exclude errored games from scores and confidence intervals; report error counts
   separately. Distinguish win rate from match score (wins plus half of draws).
3. Estimate uncertainty using paired opponent/map/seed blocks, preserving side
   pairing. Document what the interval estimates and how small samples behave.
4. Record hashes of the actual bot files used for each run, including shared
   dependencies; a Git commit alone is insufficient for dirty working trees.
5. Fix final longest-dragon statistics. They currently use lengths observed before
   a dragon's last action, so final growth/sprinting/splitting can make them stale.
   Prefer the engine/replay's final result and test a last-turn change in length.
6. Validate with focused tests and a small real-engine smoke run. Do not run a
   full tournament or submit a bot for this task.

Astra owns `framework/features.py`, `bcsim/dataset.py`, `bcsim/dataset_v2.py`,
`tests/test_dataset.py`, and `DATASET_V2.md`. Avoid these and the root README while
the work is concurrent. The new dataset is in `data/dataset_v2/`; preserve existing
downloads and `data/dataset/`. No changes to the playing strategy are part of
either infrastructure task. Report your changes and validation when complete.
