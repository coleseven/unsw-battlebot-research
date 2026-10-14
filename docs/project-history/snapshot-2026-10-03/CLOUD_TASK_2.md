# Cloud task 2: spend the C++ speed (2026-09-26)

For the cloud Claude Code session. Read `CLOUD_HANDOFF.md`, `V7_CPP_PORT_PLAN.md`
(section 5) and `V7_EXPERIMENT.md` first. **Never run `unswbc submit`; do not
merge into `master`.**

## 1. Start from the right branch

Your port (branch `claude/happy-brown-0mwwlo`) has been **merged into
`v6-release-and-port-prep`** on the local PC and pushed. **Pull that branch and
branch from it** (for example `claude/v7-speed`). Do not continue from your old
branch. The merged branch adds:

- **v6.1 parameters.** `framework/core_params.py` now has `ATTACK_MIN_GAIN = 1`,
  `HUNT_MIN_GAIN = 2`, `W_HUB = 60.0`, and `cppbot/params.hpp` was regenerated
  from it. The C++ bot is v6.1. No other bot logic changed.
- **A line-ending fix.** `.gitattributes` had a UTF-8 byte-order mark before
  `* -text`, so it never matched and Windows checkouts turned into CRLF. It is
  now plain `* -text`, and `bcsim.gen_cpp` writes LF on every host. Keep all
  files LF.
- **The CMA-ES tuner** (`bcsim/tune.py`). It rewrites `inline constexpr` /
  `constexpr` / `#define` numbers in `cppbot/params.hpp` by name. Tuning runs
  on the local PC.

Local results for the port so far: judge CPU suite and matching confirmed.
The full-suite strength test against Python v6.1 and the sparring bots is
running locally. You do not need to run it.

## 2. The task

The C++ bot uses at most about 7M of the judge's 100M points per dragon-turn;
Python v6.1 needs up to about 83M. Turn that headroom into strength with these
**separate** features. Each must sit behind its own parameter whose default
keeps today's behaviour, so the existing matching check (`bcsim/parity.py`)
still passes 100% with every new switch off.

1. **A real CPU meter and a larger search.** On the judge, `std::chrono` and
   `clock()` advance with CPU points spent (0.1 s = 100M points).
   - Add a points-based budget: `CPP_SOFT_POINTS` (stop expanding; start 60M)
     and `CPP_HARD_POINTS` (take a cheap safe move; start 80M), measured from
     the start of the turn.
   - Split the remaining budget evenly across legal moves, as the Python
     "fair search" does. Never let the first move use it all.
   - Then allow much larger `N_SEARCH` and `DEPTH_MAX` (for example `N_SEARCH`
     up to 5,000, `DEPTH_MAX` up to 40), capped by the meter.
   - Switch: for example `CPP_BUDGET = 0` (off keeps today's fixed N_SEARCH).
2. **Path distances instead of straight lines.** One budgeted BFS per turn from
   our head over remembered terrain (with book portals) gives true path
   distances. Use them for the hub pull (`HUB_FAR_MULT` fallback), the
   exploration goal, the feeding pull toward the king, and hunting.
   Switch: `CPP_PATH_DIST = 0`.
3. **Lookahead over our own moves.** A short beam over our next moves that
   simulates our own body (growth when eating, the tail moving) and marks cells
   enemy heads could reach, scored with the existing `score_moves` terms at the
   leaves. The known reference point is Leviathan (a C++ ladder bot), which
   uses width 24, depth 14. Start smaller (width 8, depth 6) and grow while
   the meter allows. Switch: `CPP_BEAM = 0`, plus `CPP_BEAM_WIDTH` and
   `CPP_BEAM_DEPTH`.

Put every new number in `framework/core_params.py` with a `# C++ only` comment
(the Python core ignores them), then regenerate with `python -m bcsim.gen_cpp`,
so `params.hpp` stays generated and tunable.

## 3. What to measure in the cloud

- **Matching:** with all new switches off, `python -m bcsim.parity` still gives
  100% identical actions (a short run over all 11 maps is enough).
- **Judge CPU, per feature and combined:** sandbox games on the largest maps
  (Big Empty, Schooltime) and one small one (Default Small), both sides.
  Report max, p99 and first-turn points. Hard requirement: zero over-budget
  turns.
- **Quick strength screens against what you have:** the frozen Python bots
  (`versions/v6`, the v6.1 bot built by `python -m bcsim.v6_initial`),
  `versions/v3` and `opponents/`. Screens only; the deciding tests against the
  sparring bots (nicked v34/v44, ctmes) run on the local PC.

## 4. Hand back

Push your branch with:

1. The code, each feature behind its switch, all defaults off.
2. `V7_EXPERIMENT.md` updated: what each switch does, parity result with the
   switches off, CPU tables per feature, and your screen results.
3. A **suggested setting** for each switch to test locally (for example
   `CPP_BUDGET=1, N_SEARCH=2000, DEPTH_MAX=30`).

The local PC then runs the full 11-map suite against the sparring opponents
for each feature, decides which to keep, and tunes the kept ones with
`bcsim/tune.py`.
