# Cloud task 3: run the C++ bot in-process for fast local simulation (2026-09-26)

For the cloud Claude Code session. Read `CLOUD_HANDOFF.md` and `V7_EXPERIMENT.md`
first. **Never run `unswbc submit`; do not merge into `master`.** Branch from
`v6-release-and-port-prep` (for example `claude/v7-inproc`).

## 1. Why

Local tuning (`bcsim/tune.py`) spends most of its time on process overhead,
not on bot thinking. Measured on the local Windows PC (unswbc 1.1.0, gen 0 of
`20260926-170140-tune-268a93`, 864 games):

- the C++ bot costs about 5M judge points per dragon-turn (a few ms of wasm,
  well under 1 ms native), yet a Big Empty game costs about 1.4 ms per
  dragon-turn;
- games against another process bot (nicked, C) average 38 s; games against
  the heavy Python v6.1 search, which runs **in-process**, average 26 s.

`bcsim.match.ProcessBot` starts one OS process per dragon (hundreds per game)
and does a pipe round trip every turn. On Windows that dominates. GPU/CUDA was
considered and rejected: the engine is the official wasm (a reimplementation
could drift from the judge), and the per-dragon search is branch-heavy.

## 2. The task

Give `bcsim` an in-process way to run `cppbot`, **without changing what is
uploaded**:

1. **A C ABI around the existing brain**, in a new file (for example
   `cppbot/inproc.cpp`), compiled only for local simulation:
   ```c
   void* bc_new(const char* init_text, unsigned long long seed);
   const char* bc_step(void* h, const char* turn_block);  // returns the full reply incl. ENDTURN
   void bc_free(void* h);
   ```
   One handle = one dragon = one fresh brain. **All state must live in the
   handle** (no globals or statics that carry between dragons; audit
   `v6.hpp` / `v6_brain.hpp` for `static` and file-scope state). The reply
   must be byte-identical to what `main.cpp` writes for the same input.
2. **Build it as a shared library** (`.dll` on Windows via the local
   mingw/clang; `.so` on Linux) from the same sources and `params.hpp` as the
   bot directory, with the same optimisation flags `unswbc` uses for native
   builds. Build once per bot directory and cache it (the tuner makes a new
   bot directory per candidate: 14 builds per generation is fine; building per
   game is not). Build before the worker pool starts (see
   `bcsim.match.prebuild`) to avoid the Windows build race.
3. **A loader in `bcsim/match.py`**: `load_bot` returns an in-process C++ bot
   (via `ctypes`) when the directory is a C++ bot and `BCSIM_CPP_INPROC=1`
   (default off at first). It plugs into `play()` the same way
   `InProcessBot` does (`spawn` creates a handle, `reply` calls `bc_step`,
   `death` frees it). Keep the result hash = content hash of the bot
   directory, as today.
4. **Timing semantics.** The release build (`PARITY=false`) stops searching on
   a wall-clock budget (`SOFT_S`/`HARD_S`). In-process and native it is far
   faster than wasm, which is already true of today's native process build,
   so keep the behaviour identical to the process build. Do not add new
   clocks.

## 3. Acceptance

- **Parity:** with `BCSIM_CPP_INPROC=1` vs `=0`, identical games (winner,
  rounds, lengths, deaths dict and replay bytes) for `versions/v7-base` vs
  `opponents/splitter`, vs `versions/v6` and vs itself on all 11 official
  maps, both sides, seeds 1-3. Use `PARITY=true` in `params.hpp` for this
  check so wall-clock cutoffs cannot differ; then spot-check the release
  build on a few maps.
- **Isolation:** two dragons stepping interleaved give the same actions as
  each run alone (proves no shared state).
- **Speed:** report seconds per game for C++ vs `versions/v6` and C++ vs
  C++ on default_small, Devil and big_empty, process vs in-process.
- **Upload unchanged:** `main.cpp` and the bot directory still build and play
  under `unswbc run --sandbox` exactly as before; `inproc.cpp` must not be
  picked up by the judge build (check `bot.toml`'s `include` globs; keep the
  new file outside the uploaded directory or excluded).
- Unit tests for the loader; existing tests still pass.

## 4. Hand back

Push the branch with the code, a short section in `V7_EXPERIMENT.md`
(parity result, speed table, how to enable), and leave the switch off by
default. The local PC then enables it for tuning and wraps the sparring C
bots the same way (their code stays local and must never be pushed).
