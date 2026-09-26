# V7 C++ port experiment log

Plan: [V7_CPP_PORT_PLAN.md](V7_CPP_PORT_PLAN.md). Goal: port the Python v6
search core 1:1 to C++, prove it matches exactly (G1), pass the judge CPU
budget (G2), then spend the speed (section 5 of the plan). **Never run
`unswbc submit`; the user uploads bots.**

Toolkit here: `unswbc` 0.3.10, Python 3.11 locally (the v6 decision path is
pure Python and version-independent, so parity is checked on 3.11). Local C++
builds use `g++`/`clang++`; the judge build and the CPU sandbox use the
toolkit's own clang -> wasm32-wasi.

## Groundwork (2026-09-26)

### PARITY matching mode in the Python core

`framework/core_params.py` gains `PARITY` (default `False`). With `PARITY =
True`, `core_search.score_moves` drops the `SOFT_S`/`HARD_S` wall-clock budget
(each move still expands up to `N_SEARCH`), and `experiments/v6/brain.py` never
takes the `HARD_S` v3 fallback. This removes host-timing nondeterminism so the
C++ port has a fixed reference to match. Release play keeps `PARITY = False`
and the time budget unchanged.

Validated (default_small, schooltime, Trauma; ~17k dragon-turns): PARITY is
deterministic across repeated runs and identical to normal v6 wherever the
wall-clock cutoff did not fire (all turns, on this host). Note the plan's
example divided `N_SEARCH` across moves; keeping the full per-move cap and only
removing the time check makes PARITY exactly equal to normal v6 whenever the
cutoff never fires, which is the property the port needs.

### Code generation from the single source

`bcsim/gen_cpp.py` mirrors the Python single source into `cppbot/*.hpp`:

- `params.hpp` from `framework/core_params.py` (one `constexpr` per tunable),
- `model.hpp` from `versions/v3/action_model.py` (the frozen v3 linear model),
- `portal_book.hpp` from `v6_portal_book.BOOK`,
- `hub_book.hpp` from `v6_hub_book.BOOK` (layout bitsets kept as hex strings,
  indexed bit-by-bit at run time; no bignum).

Re-run `python -m bcsim.gen_cpp` after touching any of those sources.

### The C++ port (`cppbot/`)

A 1:1 port of the assembled v6 bot (`bcsim/v6_initial.py`: frozen `versions/v3`
plus the framework v6 modules):

- `v6.hpp` — `Obs` parsing, `navigation.Memory`, `core_memory.WorldMemory`
  (portal book, hub book + map identification, learned hubs, exploration goal,
  sectors). `occupied` is an insertion-ordered map so it keeps Python dict
  order.
- `v6_brain.hpp` — `tactics` (danger/room), the 24 v3 features + linear score,
  `core_search` (`legal_moves` incl. attacks, `head_threats`, `food_value`,
  `search_one`, `score_moves`), `core_king` (protect/feed), `core_split`, and
  the `brain.turn` order.
- `main.cpp` — the `bc.run` stdin framing; one action line + `ENDTURN` a turn.
- `bot.toml` — `language = "c++"`.

Determinism choices that make the C++ match Python exactly: NESW iteration
everywhere; ties keep the first maximum (strict `>` in NESW order, like
Python's `max`); the search heap orders `(cost, arrival, cell)`
lexicographically; doubles in Python's operation order; the goal-noise hash in
64-bit. **Sonar is omitted**: v6 discards decoded sonar and only emits beacons
as extra lines, so it never changes the action line.

## G1 — matching (PASS)

`bcsim/parity.py` feeds each dragon's reconstructed round blocks
(`bcsim.reconstruct.turns`) to the Python v6 PARITY bot and to a fresh C++
process, comparing the action line of every reply and dropping a dragon at its
first mismatch.

Full official suite, v6 on both sides vs `opponents/splitter`, seed 1
(`python -m bcsim.parity --opponents opponents/splitter`):

| map size | maps | dragon-turns | mismatched dragons |
|---|---|---|---|
| 11x11 | arena | 3,491 | 0 |
| 16x16 | default_small, Colosseum | 15,751 | 0 |
| 25x25 | trophy | 23,878 | 0 |
| 25x35 | queen_of_spades | 18,746 | 0 |
| 32x16 | Devil | 18,215 | 0 |
| 32x32 | default | 32,524 | 0 |
| 48x24 | stronghold, Trauma | 44,830 | 0 |
| 60x40 | schooltime | 48,049 | 0 |
| 64x64 | big_empty | 90,513 | 0 |
| **total** | **all 11** | **295,997** | **0** |

**G1 PASS**: 100% identical actions on 295,997 dragon-turns over all 11 maps
and both sides (the plan asks for >= 20,000). Every subsystem is exercised:
portals (trophy, queen, default's 12 pairs, stronghold, Trauma, schooltime,
Colosseum), hub books and map identification, exploration goals, feeding and
splitting.

A second distinct opponent, `opponents/hunter` (which drives v6 through combat
and feeding states splitter does not), was run over the same suite as a check:
**185,095 dragon-turns, 0 mismatches**, all 11 maps and both sides. Combined
with the splitter run that is **481,092 dragon-turns across two distinct
opponents, both sides, every official map, with zero mismatches.**

### Live cross-check (not just recorded blocks)

The harness above replays blocks from games Python v6 already played. To rule
out a divergence that only appears in states not in those replays, the same
matchup was played twice with the same seed: `cppbot` vs splitter and the
Python v6 PARITY snapshot vs splitter, then the v6 side's moves compared.

| map | rounds | team-A turns | move diffs |
|---|---|---|---|
| default_small | 156 | 1,200 | 0 |
| Trauma | 500 | 5,115 | 0 |
| queen_of_spades | 281 | 2,943 | 0 |
| Colosseum | 64 | 1,013 | 0 |

Identical games (same rounds and same death breakdown), move-for-move. The
occasional wall-death ("A:W") appears identically in both, so it is v6's
last-resort fallback in a trapped position, not a port bug.

## G2 — judge CPU in matching settings (PASS)

`unswbc` 0.3.10 does support the C++ sandbox here (the plan was unsure). The
port compiles under the judge clang -> wasm and plays legal games.

Full-suite CPU sweep, `--sandbox`, cppbot on each side vs splitter, max points
per turn (limit 100M; Python v6 peaks around 80M on the same suite):

| map | cppbot as A (max) | cppbot as B (max) |
|---|---|---|
| default_small | 6.5M | 6.4M |
| trophy | 6.6M | 6.9M |
| queen_of_spades | 6.6M | 6.4M |
| default | 6.8M | 6.9M |
| Devil | 6.4M | 6.4M |
| stronghold | 6.8M | 6.9M |
| Trauma | 6.7M | 6.7M |
| schooltime | 6.7M | 6.5M |
| big_empty | 7.1M | 7.1M |
| arena | 5.3M | 5.2M |
| Colosseum | 6.3M | 6.6M |

**G2 PASS (matching settings)**: every side of every official map stays under
7.1M of 100M points per turn, no over-budget turns, no CPU-error deaths. This
is the ~12x speed-up over Python v6 the plan predicted, with the whole budget
still to spend on section 5. (The "hit a wall" deaths in sandbox games are
v6's last-resort fallback and are identical to Python v6 — see the live
cross-check — not port or CPU faults.)

## Status and next steps

- G1 matching: **PASS** (481,092 turns over two opponents, 0 mismatches, all 11
  maps + a move-for-move live cross-check).
- G2 CPU (matching settings): **PASS** (all 11 maps, both sides, max 7.1M of
  100M, no over-budget turns).
- G3 strength (matching settings): the port equals Python v6 by construction
  (identical actions), so a full-suite strength run should be about even; not
  yet run.
- Section 5 (spend the speed: raise `N_SEARCH`/`DEPTH_MAX`, full-map BFS
  distances, lookahead beam, CMA-ES tuning) is future work, each judged by the
  full-suite rules in `CLAUDE.md`.

Do not upload; the user uploads bots.
