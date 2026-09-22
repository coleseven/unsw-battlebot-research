# UNSW Battlecode — team 777

Competition: https://game.battlecode.au (21 Sep – 17 Oct 2026). Rules: https://game.battlecode.au/docs

Run everything with the project venv (it has the toolkit, numpy and CUDA PyTorch):

```
.venv\Scripts\python -m bcsim.<tool> ...
```

## Layout

| path | what |
|---|---|
| `mybot/` | **our bot** — edit `brain.py`. Submit with `unswbc submit mybot` |
| `framework/` | shared source: `bc.py` (parser + `Brain` base), `tactics.py`, `features.py`. Edit here, then `python -m bcsim.sync` copies it into every bot |
| `opponents/` | sparring bots: `wanderer`, `greedy`, `hunter`, `splitter`, `turtle`, plus the official helper-based `starter` |
| `versions/` | frozen snapshots of mybot (`v1`, `v2`, …) to test new versions against |
| `maps/` | bundled maps; `maps/server/` = extra maps harvested from ranked games |
| `bcsim/` | tooling (below) |
| `data/` | scraped replays, `index.jsonl`, `dataset/` shards (git-ignored) |
| `results/` | arena outputs (git-ignored) |

## Writing a bot

A bot is `class Brain(bc.Brain)` with `turn(self, obs) -> "MOVE N" | "MOVE NNE" | "SPLIT 3"`.
One instance per dragon; keep all state on `self` (dragons share no memory on the judge).
`obs` is a `bc.Obs`: 7×7 window, cells `k = row*7 + col`, head at `bc.CENTER`;
`obs.occ[k]`, `obs.pearl[k]`, `obs.pearl_in[k]`, `obs.edge(k, d)`, `obs.passable(k, d)`, `obs.bfs()`.
Extra output lines (SONAR, INDICATOR, LOG, DOT) go in `self.extra`.

## Testing (all CPU cores)

```
python -m bcsim.arena eval mybot                          # vs all sparring bots, every map, both sides
python -m bcsim.arena eval mybot --vs v3 --seeds 8        # new version vs old
python -m bcsim.arena tournament mybot v2 v1 splitter     # round robin + Elo table
python -m bcsim.arena freeze                              # snapshot mybot -> versions/vN
```

Framework bots run in-process (~12 full games/s on 15 workers). Other bots
(C++, the helper-based starter) run one process per dragon, like `unswbc run`: faithful but slow.
Losing games' replays are saved under `results/…/replays/` — open them in VS Code.

In-process runs don't measure the judge's CPU budget (100M points/turn). Check with:
`unswbc run maps/default.map mybot opponents/splitter --sandbox`

## Data

```
python -m bcsim.scrape --pages 200 --min-elo 1650 --max-battles 600   # public ranked games (incremental)
python -m bcsim.dataset                                              # replays -> data/dataset/*.npz
python -m bcsim.reconstruct                                          # self-test: rebuilt turns == real turns
```

`bcsim.replay` decodes any .replay (local or server). `bcsim.reconstruct` rebuilds each
dragon's exact round block from a replay (verified identical on ~39k turns), and
`framework/features.py` encodes it; see `bcsim/dataset.py` for the shard format and
`load_all(fraction=…, where=…)` for loading a subset. The full corpus is tens of millions
of turns — sample it.
