# Handoff to the cloud C++ port session (2026-09-26)

Read this before continuing `V7_CPP_PORT_PLAN.md`. It lists everything that
changed on branch `v6-release-and-port-prep` after the commit you started from
(`1525ffc`), and what the local PC needs back from you.

## 1. What changed since `1525ffc`

**Bot logic: nothing.** No file in `framework/`, `experiments/` or `versions/`
changed except three numbers in `framework/core_params.py`:

| Parameter | Was | Now |
|---|---|---|
| `ATTACK_MIN_GAIN` | 0 | **1** (ram an adjacent enemy head only when it is strictly longer) |
| `HUNT_MIN_GAIN` | 1 | **2** (hunt only enemies at least 2 longer) |
| `W_HUB` | 20.0 | **60.0** (hub pull) |

If your port reads its parameters from `core_params.py` (as the plan says),
regenerate them and you are done. If you hard-coded any of these three,
update them.

These defaults are now the **v6.1 candidate** (`results/v61b-goal-bot` on the
local PC). On the full 11-map suite it scored 16/22 against uploaded v6, 22/22
against additive v4, 18/22 against nicked v34, 8/22 against nicked v44, and
held out 22/22 against v3 and 20/22 against ctmes. **Port target = this
branch's current `framework/` + `experiments/v6/brain.py` with these
defaults.** The earlier defaults are not the target any more.

Other new files (not bot code):

- `bcsim/tune.py` + `tests/test_tune.py`: the CMA-ES tuner (section 3).
- `V6_EXPERIMENT.md`: the v6.1 section explains every new feature (portal
  book, aggression, hub book, learned hubs, exploration goal) with results.

## 2. What the local PC now has (so you don't need to)

- **A C/C++ compiler:** GCC 14.2 and clang 19 (WinLibs). `unswbc run` and the
  `bcsim` harness build and run C++ bots natively. A C++ bot plays a full
  Default game in about 12 s through `bcsim.match`.
- **The judge sandbox for C++:** `unswbc run ... --sandbox` builds C++ with the
  toolkit's shipped judge clang (wasm32-wasi) and meters CPU points. Checked
  with the official C++ starter: 3.6-3.8M points per turn. Toolkit 0.3.10.
- **The sparring opponents** (`sparring/`: nicked v34, nicked v44, ctmes and
  others): git-ignored, third-party and unlicensed. **Do not recreate or
  download them in the cloud.** Strength tests against them happen on the
  local PC.

So your job is to **port and prove it matches exactly**. Final strength, CPU
and release checks happen locally.

## 3. Requirements so the local tuner works on your port

`bcsim/tune.py` edits one parameter file per candidate copy of the bot and
rebuilds it. For the C++ bot:

1. Put **every tunable number in one file**, `cppbot/params.hpp`, one per line,
   exactly as either
   `constexpr double NAME = 60.0;` / `constexpr int NAME = 200;` or
   `#define NAME 16`. The tuner rewrites the number by `NAME` with a regex, so
   no expressions (`= 2 * X`), no `inline`, and no line breaks inside a setting.
2. **Use the same names as `framework/core_params.py`** (for example `W_HUB`,
   `N_SEARCH`, `SPLIT_UNTIL_LARGE`). The same search-space file then works for
   both bots.
3. Booleans (for example `GOAL`, `HUB_BOOK`) as `constexpr int NAME = 1;` (0 or 1).
4. The bot must build from its folder alone with the files listed in
   `bot.toml` (`unswbc run` builds the folder; the harness snapshots only bot
   files).
5. No time-based behaviour in matching mode (section 3 of the port plan). For
   normal play, meter CPU the way the judge does: on the judge, `std::chrono`
   and `clock()` advance with CPU points spent (0.1 s = 100M points).

## 4. What to hand back

Push a branch (for example `v7-cpp-port`) containing:

1. `cppbot/` (the C++ bot, building with `unswbc run`), with `params.hpp`
   generated from `framework/core_params.py` at this branch's defaults.
2. The params generator script (so the local PC can regenerate after any
   Python-side change).
3. `bcsim/parity.py` and a short `V7_EXPERIMENT.md` with the matching result:
   dragon-turns compared per map, mismatches found and fixed, and the final
   pass count. Target: 100% identical actions on at least 20k dragon-turns
   over all 11 maps.
4. Anything the local PC must run first (for example "regenerate params, then
   run `python -m bcsim.parity ...`").

Do not merge into `master`, and do not run `unswbc submit`.

## 5. What happens after you push (local PC)

1. Re-run the matching check locally.
2. Judge CPU suite on all 11 maps and both sides for the C++ bot.
3. Full-suite strength against v6.1, nicked v34/v44, ctmes and v3.
4. CMA-ES tuning of `params.hpp` with the extra search budget C++ allows.
5. Release decision by the user (the user uploads).
