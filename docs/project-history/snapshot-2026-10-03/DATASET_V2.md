# Dataset V2

The new builder preserves complete movement actions and local observation details.
`python -m bcsim.dataset` now writes **data/dataset_v2/**. Existing **data/dataset/**
shards and raw replays are retained. V1 sprint summaries cannot recover missing
directions; rebuild V2 from the raw replays, not from V1 arrays.

## Build and freeze partitions

Use the project's Python environment:

```powershell
.\.venv\Scripts\python.exe -m bcsim.dataset --limit 5 --workers 2
.\.venv\Scripts\python.exe -m bcsim.dataset --workers 2
.\.venv\Scripts\python.exe -m bcsim.dataset --partition data/dataset_v2/battles-v1.json --group-by battle --seed 0
```

The first command is a small smoke run. The second converts all available replays;
it can take substantial time and disk space. Two workers are the default to avoid
monopolizing the machine during other work. `--games 38924,38925` selects exact games.

Every shard records its schema, feature version, pipeline source fingerprint,
replay checksum, filter settings, game/battle/submission IDs, map checksum, and row
count. Compatible caches are reused. Stale caches fail explicitly. Use `--rebuild`
to atomically replace selected outputs, or `--output data/dataset_v2_experiment`
for another configuration. Rebuilding never deletes the corpus first. Empty
filtered games are cached as zero-row shards. Legacy/unversioned files and mixed
pipeline/filter datasets are rejected by V2 readers.

Partitioning defaults to an 80/10/10 hash assignment of complete **battles**, not
individual turns or games within a battle. Ratios are approximate because group
sizes vary. The manifest records exactly which shards are included and their
metadata fingerprints. Later downloads do not silently enter that frozen split;
changed shards are rejected. Manifest files cannot be overwritten in place.

Additional experiments can use `--group-by map` or `--group-by submission`.
Submission grouping builds connected components: if A plays B and B plays C,
all those games remain together. It fails if a requested partition is empty.
A tightly connected league may not permit a useful submission split; do not
randomly split its turns to work around this. Collect independent cohorts or
construct an explicit held-out-opponent experiment instead. Battle grouping
does **not** claim to hold out maps, teams, or submissions.

## Streaming training inputs

```python
from bcsim.dataset import iter_batches

for batch in iter_batches(
    batch_size=512,
    partition_manifest="data/dataset_v2/battles-v1.json",
    split="train",
    columns=("grid", "scalar", "turn_order", "portal_ids", "kind", "steps",
             "split", "action_tokens", "policy_eligible", "won"),
    where=lambda z: z["policy_eligible"],
    category_keep={"step": 0.05, "sprint": 1.0, "split": 1.0, "other": 0.0},
    seed=0,
):
    # Feed chosen observation fields to the model. kind/split/action_tokens
    # are targets; won is a team outcome target, never an inference input.
    # Use action_tokens_mask to exclude padding from the sequence loss.
    pass
```

Memory scales with one game's selected arrays plus one batch, not the full
corpus. Compressed NPZ requires decompressing each selected array for the current
game; this is **not** row-level memory mapping or a strict fixed-byte RAM cap.
The last batch of each game can be smaller. Shards and rows are shuffled with a
reproducible seed. Change the seed for a new epoch. `shuffle=False` retains
within-game chronological order. Recurrent training should group by
`(game, dragon)` and reset memory at a dragon's birth; randomly shuffled rows
are not observation sequences.

`category_keep` thins categories without replacement. Unspecified categories
have probability 1; `fraction` multiplies all retention probabilities. The example
keeps all split/sprint samples but only 5% of ordinary steps. This is an
experimental sampling policy, not an established optimal balance. Evaluate on
an unthinned held-out distribution and report each action class separately.

`where` sees only the requested fixed fields. Include the fields it needs in
`columns`. The default returns every fixed field and both sequence fields.
`load_all` remains available for small fixed-column samples, with a default
512 MiB array-output allowance including concatenation. It deliberately rejects
ragged fields; use `iter_batches` for complete action and sonar sequences.

## Stored observation fields

All input fields come from the acting dragon's own observation or initial setup.
No full-map occupancy, hidden enemy lengths, or another dragon's memory is added.

| Field | Per-turn shape / encoding |
| --- | --- |
| `grid` | uint8 `[17,7,7]`, original compact channels; compatible with `features.encode` |
| `scalar` | float32 `[5]`: length, team population, round, facing, sonar count |
| `dragon_ids` | int32 `[7,7]`, -1 empty; visible segment ownership retained |
| `turn_order` | uint8 `[7,7]`: 0 empty, 1 lower ID, 2 self, 3 higher ID |
| `portal_ids` | int32 `[4,7,7]`, NESW; -1 no portal, otherwise actual pair identity |
| `coordinates` | int32 `[2,7,7]`, exact absolute x/y of each visible tile |
| `pearl_countdown` | int32 `[7,7]`, exact timer; -1 never spawns |
| `map_size` | int32 `[2]`, width/height |
| `unit_limit` | int32, currently the engine default 64 |
| `sonar_values`, `sonar_offsets` | ordered uint32 messages, ragged storage |

IDs and directions are categorical. Scale continuous inputs appropriately;
do not treat portal ID 100 as geometrically farther than portal ID 2. Preserve
the -1/255 sentinel meanings when normalizing countdowns. Portal geometry outside
the window remains unknown. The feature encoder preserves information, but does
not supply persistent memory or interpret an opponent's private sonar protocol.

## Targets and provenance

`kind`: 0 MOVE, 1 SPLIT, 2 suicide, 3 absent action.
`dir`, `steps`, and `split` remain convenient summaries. **dir + steps is not a
complete move label.**

`action_values` contains every step (N/E/S/W = 0/1/2/3); `action_offsets` has
N+1 entries. `NNE`, `NEN`, and `NNN` remain distinct, with no fixed sprint cap.
The batch loader emits `action_tokens` padded with -1 and `action_tokens_mask`.
Sonar is padded with zero plus `sonar_mask`; zero is also a valid real message,
so the mask is authoritative. Empty sequences have width zero when every row in
the batch is empty. No NumPy object arrays/pickle are used.

`game`, `battle`, `submission`, `round`, `dragon`, and `team` identify trajectories.
`won` is 1/0.5/0 for the eventual team result; winning does not mean every action
was good. `elo` is source metadata and is not guaranteed to be a historical
pre-game rating. `points=-1` means unavailable, not zero cost. `budget_exceeded`
and `timed_out` preserve replay failure flags. `policy_eligible` excludes absent,
empty-move, suicide, and recorded timeout/budget-failure actions. It is **not a
proof of action legality, survival, or quality**; lethal head trades may be useful.

Outcome and provenance columns are training labels/metadata, not deployable model
inputs. A submitted dragon does know its own ID/team/round, but does not receive
the opponent's submission ID, its future game result, or its team's Elo.

## Checks and limits

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p test_dataset.py -v
```

Tests cover complete sprint reconstruction, exact feature fields, zero/max uint32
sonar, cache invalidation, empty filtered games, variable sequence masks,
deterministic thinning, memory guarding, legacy/mixed-cache rejection, incomplete
outcomes, and grouped/frozen partitions. The builder uses the existing replay
reconstructor; improving its portal/split/sonar edge-case coverage remains useful.

This change prepares reliable inputs and labels. It does not train a network,
change the playing bot, or establish a competitive-strength improvement.
