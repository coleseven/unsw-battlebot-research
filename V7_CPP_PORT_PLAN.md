# V7: port the v6 search core to C++ (cloud session plan)

Written 2026-09-26 for a cloud Claude Code session with no prior context.
Read `CLAUDE.md`, `README.md` and `V6_EXPERIMENT.md` first. **Never run
`unswbc submit`**; the user uploads bots.

## Why

The judge charges CPU in points: 100M per dragon-turn, and a turn over budget
kills the dragon. The official docs give a 32x32 flood fill as about 19M points
in Python and 0.3M in C++. The Python v6 search is budget-bound: in the judge
sandbox on Big Empty its soft cutoff fired on 87% of moving turns, with a median
of 77 search expansions. 8 of the current top-10 ladder teams use C++.

## Principle: port first, match exactly, then spend the speed

1. **Port the Python v6 core 1:1** into a C++ bot, `cppbot/`.
2. **Prove it matches exactly:** feed identical observation sequences to the
   Python and C++ bots and require the same action on every turn (section 3).
3. **Only then** raise the search budget, depth and lookahead (section 5), and
   evaluate every change with the full suite rules in `CLAUDE.md`.

## 1. What to port (source of truth: this branch's `framework/` and `experiments/v6/`)

The bot is assembled by `bcsim/v6_initial.py:variant()`: frozen `versions/v3`
plus the files in its `MODULES` list. Port these, keeping function boundaries
so each part can be tested on its own:

| Python | Role | Port notes |
|---|---|---|
| `experiments/v6/brain.py` | Turn order: memory, goal, sonar, feed, split, hard fallback, search, emergency split, beacon | Keep the exact order. `""` (no action) means intentional feeding |
| `framework/core_memory.py` | Per-dragon memory: navigation, spawns, pearls, occupancy, trail, portal book, hub-book map identification, learned hubs, sectors and exploration goal | `update()` must run exactly once per turn |
| `framework/navigation.py` (`Memory`) | Edge memory and `destination()` through portals | Edge keys: north edge of cell = `y*w+x`, west edge = `w*h+y*w+x` |
| `framework/core_search.py` | `legal_moves` (including attacks), `head_threats`, `food_value`, `search_one` (bounded weighted BFS), `score_moves` | The core; see the matching rules in section 3 |
| `framework/core_split.py`, `framework/core_king.py` | Split schedule, protection, feeding | Small |
| `framework/core_params.py` | Every tunable number | Generate `params.hpp` from it with a script, so Python stays the single source |
| `framework/v6_portal_book.py`, `framework/v6_hub_book.py` | Official-map books | Generate `.hpp` from `bcsim/portal_book.py` and `bcsim/hub_book.py` output; the hub layout bitsets can be `std::bitset` or byte arrays |
| `versions/v3/action_value.py` + `action_model.py` | The 24 v3 features and the linear model (the `W_V3` term and the hard fallback) | Feature extraction calls `obs.bfs()` and `tactics`; port those exactly |
| `versions/v3/tactics.py` | `danger_cells`, `safe_moves`, `room`, `pearl_targets` | Used by features and the split guard |
| `versions/v3/bc.py` | Observation parsing, `Obs.step/edge/passable/bfs`, `Brain.fallback` | Prefer the official C++ helper (`helper.hpp` from the unswbc templates) for I/O, and port the `Obs` geometry helpers on top of it |
| `framework/v4_sonar.py` | Sonar beacon and decode | Must emit identical packets |

Use the official C++ helper (`unswbc init` or the template under the unswbc
package) for the protocol. Output: one write per turn (each write costs 2.5M
points plus 4,000 per byte); no logging in release builds.

## 2. Build and run

- Local C++ builds need a compiler (`g++` or `clang++`). The judge compiles
  with clang to wasm32-wasi, `-O2 -msimd128`, against libc and libc++ only.
  Vendor any library as source.
- `unswbc run MAP BOT_A BOT_B` builds folder bots. Check whether the installed
  toolkit's `--sandbox` supports C++; `bcsim/clangtool` in unswbc 0.3.10 ships
  the judge clang, but the docs said C/C++ could not yet be sandboxed locally.
  If it doesn't, try a newer `unswbc` in a separate venv (PyPI has up to 1.1.0;
  no changelog). Record which version was used for every CPU claim.
- The local harness (`bcsim.match`) runs non-framework bots as one OS process
  per dragon (slower than the in-process Python bots). That is fine for
  matching and for full-suite games; see `bcsim.full_change_test` and
  `bcsim.official_suite.DEFAULT_WORKERS`.
- `data/`, `results/`, `replays/` and `sparring/` are git-ignored and **not in
  the repo**. Regenerate whatever you need: games with
  `python -m bcsim.full_change_test`, or downloaded ladder replays with
  `python -m bcsim.scrape`. Do not add third-party bots to git (no licenses).

## 3. Matching harness (`bcsim/parity.py`, write this first)

Goal: identical actions from Python v6 and C++ v7 for the same observation
sequence of one dragon.

- **Inputs:** replays, from local full-suite runs or `bcsim.scrape`, covering
  all 11 official maps (`bcsim.official_suite.official_maps()`).
  `bcsim.reconstruct.turns(replay)` yields each dragon's exact round block, in
  order, with its id and team; it matches real engine blocks on ~39k turns.
- **Per dragon:** create a fresh Python brain
  (`bcsim.match.InProcessBot(bot).new_brain(init_text, seed)`) and a fresh C++
  process. `init_text` is `ID {id}\nTEAM {team}\nMAP {w} {h}\nUNIT_LIMIT 64\n`.
  Feed each block in order and compare the action line of every reply. Stop
  following a dragon at its first mismatch (their memories diverge) and report
  it with the block, the map and both actions.
- **Matching mode:** the Python v6 budget uses `time.perf_counter()`
  (`SOFT_S`, `HARD_S`). In matching mode, both implementations must use a
  fixed expansion budget and no time cutoff. For example, a `PARITY = True`
  parameter turns `SOFT_S`/`HARD_S` off and gives each move exactly
  `N_SEARCH // len(moves)` expansions. Add the same switch to the Python core
  first, and check that Python-with-switch equals Python-without-switch
  wherever the cutoff did not fire.
- **Determinism rules the C++ port must follow:**
  - **Move order:** iterate moves in `NESW` order everywhere. Python `max()`
    keeps the *first* maximum, so C++ must use strict `>` in the same order.
    `max(scores, key=lambda d: (scores[d], d == facing))` breaks ties by facing.
  - **Priority queue:** Python `heapq` orders tuples `(cost, arrival, cell)`
    lexicographically; reproduce exactly (a min-heap on the same triple).
  - **Floating point:** use `double` and the same operation order as Python
    (for example, `sum()` adds left to right). `obs.length / 4` is true
    division.
  - **Integers:** Python ints are unbounded. The goal noise
    `((did * 2654435761 + idx * 40503) >> 7) % 1000` must use 64-bit unsigned
    or signed arithmetic that gives the same result for ids up to a few
    thousand; test it.
  - **Dict iteration order:** Python dicts keep insertion order. Where the
    Python iterates a dict (for example `mem.occupied.items()`,
    `hub_area`, the learned-hub `local` dict with its sort), the C++ must
    reproduce the same order or prove the order cannot change the result. The
    learned-hub sort is by value, then by insertion order for ties.
- **Pass mark:** 100% identical actions on at least 20,000 dragon-turns
  spread over all 11 maps and both sides, with no crash and no invalid output.
  Any mismatch is a bug in one side; fix it or document it before moving on.

## 4. Judge CPU check for the port (matching settings)

Before any strength test: full sandbox games on every official map and both
sides (Python equivalent: `bcsim.v6_cpu_suite`). Pass: zero over-budget
turns, zero invalid-action deaths, and first turn well under budget (imports
and static data are charged to turn 1). With matching settings the C++ should
use a small fraction of what Python does; record max and p99 per map.

## 5. Spending the speed (only after sections 3 and 4 pass)

Each is a separate change, judged by the full suite (`CLAUDE.md`: all 11 maps,
both sides, the previous version plus distinct opponents, including nicked v34,
nicked v44, v3, ctmes and the live Python bot):

1. Raise `N_SEARCH` and `DEPTH_MAX` (for example 10x) and set the CPU guard from
   the sandbox, not wall time.
2. Path-based distances to every hub and exploration goal: a full-map BFS per
   turn is affordable in C++ and replaces the straight-line fallbacks.
3. Lookahead: a short beam over our own moves with predicted enemy-head reach
   (Leviathan-style width 24, depth 14 is known to fit in C++).
4. The CMA-ES tuner from `V6_CORE_PLAN.md` section 4.4, now affordable in the
   cloud: tune `params.hpp` against nicked v34 and live v6.x on the full suite.

## 6. Deliverables and gates

| Gate | Pass |
|---|---|
| G1 matching | 100% identical actions on at least 20k dragon-turns, all 11 maps |
| G2 CPU (matching settings) | Sandbox suite: zero over-budget turns on all maps and sides |
| G3 strength (matching settings) | Full suite against Python v6.x is about even (the same bot) |
| G4 speed-up | Each section 5 change beats the previous C++ version and live Python v6.x on the full suite, with G2 re-passed |
| G5 release | User decision; the user uploads |

Write a `V7_EXPERIMENT.md` log in the same style as `V6_EXPERIMENT.md`
(frozen hashes, result directories, per-map tables), and commit work on a
branch.
