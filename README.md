# UNSW Battlecode — team 777

Competition: https://game.battlecode.au (21 Sep – 17 Oct 2026). Rules: https://game.battlecode.au/docs

## Best tested local candidate

`versions/v7` (hash `b033b4202f624d25`, upload package `battlebot-v7.zip`) is
the C++ port of v6.1 with CMA-ES-tuned weights (tune `20260926-001535-tune-79f3f9`,
gen 7 c05: N_SEARCH 357, DEPTH_MAX 12, all section-5 switches off). Over all 11
maps and both sides it scored 14/22 vs nicked v44, 20/22 vs ctmes, 15/22 vs v6
and 12/22 vs the untuned C++ bot (untuned: 9, 21, 16 of 22). Judge sandbox CPU
max 7.0M of 100M. See [V7_EXPERIMENT.md](V7_EXPERIMENT.md), section "Tuned release".

Previous: `versions/v6` (hash `4959b003957277f5`, upload package `battlebot-v6.zip`) is
the search-core bot: per-dragon map memory, one bounded search score per move
with an even per-move CPU budget, founder/long-dragon kings and late feeding.
Under the judge-calibrated local clock (`BCSIM_DETERMINISTIC_V6=1`) it scored,
over all 11 maps and both sides: 21/22 against live v4, v3 and ctmes, 16/22
against the previous v6 and nicked v34, and 8/22 against nicked v44. The
22-game judge CPU suite passed (max 81.9M of 100M points). The live ladder bot
is v4 (submission 5204) until v6 is uploaded. See
[V6_EXPERIMENT.md](V6_EXPERIMENT.md) for the full log, and
[TOP_TEAMS_SCOUTING.md](TOP_TEAMS_SCOUTING.md) and
[COMPETITOR_RESEARCH.md](COMPETITOR_RESEARCH.md) for the research behind it.

`cppbot/` is a 1:1 C++ port of the v6 core (V7): it plays v6 move-for-move but
uses about 7M of the judge's 100M CPU points per turn instead of ~80M, leaving
the budget free for a deeper search. Its data headers are generated from the
Python single source with `python -m bcsim.gen_cpp`, and `python -m
bcsim.parity` proves the two implementations pick identical actions. See
[V7_CPP_PORT_PLAN.md](V7_CPP_PORT_PLAN.md) and
[V7_EXPERIMENT.md](V7_EXPERIMENT.md).

## Layout

| path | what |
|---|---|
| `mybot/` | **our bot** — edit `brain.py`. Submit with `unswbc submit mybot` |
| `framework/` | shared source: `bc.py` (parser + `Brain` base), `tactics.py`, `features.py`. Edit here, then `python -m bcsim.sync` copies it into every bot |
| `opponents/` | sparring bots: `wanderer`, `greedy`, `hunter`, `splitter`, `turtle`, plus the official helper-based `starter` |
| `versions/` | frozen snapshots of mybot (`v1`, `v2`, …) to test new versions against |
| `maps/` | bundled maps; `maps/server/` = extra maps harvested from ranked games |
| `bcsim/` | tooling (below) |
| `data/` | scraped replays, `index.jsonl`, new `dataset_v2/` shards; legacy `dataset/` retained (git-ignored) |
| `results/` | arena outputs (git-ignored) |

## Writing a bot

A bot is `class Brain(bc.Brain)` with `turn(self, obs) -> "MOVE N" | "MOVE NNE" | "SPLIT 3"`.
One instance per dragon; keep all state on `self` (dragons share no memory on the judge).
`obs` is a `bc.Obs`: 7×7 window, cells `k = row*7 + col`, head at `bc.CENTER`;
`obs.occ[k]`, `obs.pearl[k]`, `obs.pearl_in[k]`, `obs.edge(k, d)`, `obs.passable(k, d)`, `obs.bfs()`.
Extra output lines (SONAR, INDICATOR, LOG, DOT) go in `self.extra`.

## Testing (all 11 official maps)

```
python -m bcsim.full_change_test --prepare --candidate mybot --vs versions/v3 opponents/splitter
python -m bcsim.full_change_test results/<printed-run-directory> --screen
python -m bcsim.arena eval mybot --maps all --vs v3,splitter --seeds 1
python -m bcsim.arena tournament mybot v2 v1 splitter     # round robin + Elo table
python -m bcsim.arena freeze                              # snapshot mybot -> versions/vN
```

Every bot-change comparison, even one targeting a single map, must include
both sides of Default Small, Trophy, Queen Of Spades, Default, Devil,
stronghold, Trauma, Schooltime, Big Empty, Arena, and Colosseum. The frozen
`full_change_test` runner enforces this, saves replays, and uses eight workers
by default on this host (the measured memory-safe full-suite setting), with guarded
workers by default (bounded RSS and available-RAM checks). Small diagnostic
screens are useful for debugging but cannot establish an improvement. Repeated
bot RNG seeds do not independently reseed the map engine for deterministic
bots; use distinct maps and opponents instead of counting duplicate replays.

Framework bots run in-process. Other bots
(C++, the helper-based starter) run one process per dragon, like `unswbc run`: faithful but slow.
Losing games' replays are saved under `results/…/replays/` — open them in VS Code.

In-process runs don't measure the judge's CPU budget (100M points/turn). Check with:
`unswbc run maps/default.map mybot opponents/splitter --sandbox`

## Data

```
python -m bcsim.scrape --pages 200 --min-elo 1650 --max-battles 600   # public ranked games (incremental)
python -m bcsim.dataset --limit 5 --workers 2                         # small V2 conversion check
python -m bcsim.dataset --workers 2                                  # replays -> data/dataset_v2/*.npz
python -m bcsim.dataset --partition data/dataset_v2/battles-v1.json   # freeze battle-grouped train/validation/test sets
python -m bcsim.reconstruct                                          # self-test: rebuilt turns == real turns
```

Downloaded ranked replays (`replays/`, .zip bundles or .replay files) have a
compact report tool; start any match analysis here instead of reading replays:

```
python -m bcsim.analyze                         # all of replays/: per-game table, us-vs-them aggregate, flags
python -m bcsim.analyze replays/mygames --maps  # one folder, plus a per-map breakdown
python -m bcsim.analyze --game M120441          # one game: timeline, deaths by cause, split sizes, CPU
python -m bcsim.analyze --json games.json       # all per-game stats as JSON
```

Our side is auto-detected (the site only records our submission name and CPU);
otherwise games are compared winner vs loser. Results are cached by content hash.

`bcsim.replay` decodes any .replay (local or server). `bcsim.reconstruct` rebuilds each
dragon's exact round block from a replay (verified identical on ~39k turns), and
`framework/features.py` encodes it. See [DATASET_V2.md](DATASET_V2.md) for the new
lossless sprint labels, exact auxiliary observation fields, versioned caches,
grouped partitions, and `iter_batches()` training examples. The full corpus is
tens of millions of turns: stream selected columns and sample deliberately.
`load_all()` is restricted to small fixed-column samples. Existing V1 shards are
preserved but must be rebuilt from raw replays to recover full sprint paths.
