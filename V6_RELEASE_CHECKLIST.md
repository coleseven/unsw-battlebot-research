# V6 release checklist (2026-09-25)

Written by Claude (research role) for Codex, after reading `V6_EXPERIMENT.md`.
Goal: replace the live bot (v4, submission 5204; team site id 590, rated about
1478, rank ~183) with v6 safely. Upload only with the user's go-ahead.

## Where v6 stands

| Candidate | vs v5 | vs additive v4 | vs nicked v34 | nicked F | Judge CPU (Big Empty, 1 game) |
|---|---|---|---|---|---|
| Original v6 (`results/20260925-132108-v6-g0-791c56/bots/v6`) | 17/22 | 17/22 | 12/22 | -0.089 | max 81.36M, p99 60.71M |
| Narrow-escape v6 (`results/v6-narrow-escape-bot`) | 17/22 | 18/22 | 11/22 | -0.033 | max 80.75M, p99 62.40M |
| (reference) v5 baseline | | | 5/22 | -0.499 | |

**Correction to `V6_CORE_PLAN.md`:** gate G1 (beat nicked 12 of 22 with no map
at 0-2) was written as the research target. It is not the right bar for a
ladder release. Nothing on the ladder requires beating nicked. The release bar is:

1. clearly stronger than the live bot (v4), on all 11 maps;
2. no regressions against held-out opponents; and
3. **zero judge CPU deaths.**

v6 already meets the first (17-18/22 against additive v4, with a large margin
gain). The second is untested and the third is under-tested. Queen, stronghold
and Trauma against nicked are improvement work for after release, not
blockers.

## How the judge clock works (from the official Timeouts docs)

- On the judge, `time.perf_counter()` **advances with CPU points spent**
  (100M points read as 0.1 s). Games are reproducible, and the wall-clock guard
  in v6 is an exact, deterministic point meter there. Keep it.
- A turn that exhausts 100M points **delivers nothing and the dragon dies**.
  There is no partial credit and no fallback reply.
- The first turn is not exempt: your own imports and setup are charged to it.
  Heavy setup must be lazy or spread across turns. This is why the fixed-node
  variants died in rounds 0-2.
- Output writes cost 2.5M points plus 4,000 per byte; parsing a round costs
  about 10M in Python. Keep logging off.
- The local in-process arena uses real wall time, so the same guard is
  **non-deterministic locally**. That is the evaluation flaw you found, not a
  judge problem.

## Release steps, in order

### R1. Make local evaluation deterministic without changing judge behaviour

Choose one approach and document it:

- **(a)** In local in-process runs only, give the bot a budget clock that
  counts deterministic work (expanded nodes times a cost calibrated from the
  sandbox, plus a fixed charge per v3 feature row). On the judge, read
  `time.perf_counter()` as now. Detect the environment by a harness-set flag,
  never by guessing.
- **(b)** Or, locally, scale the guard so it essentially never fires in
  in-process runs, and first measure in the sandbox how often it fires on the
  judge. If it fires on under 1% of turns, local results are then a good
  approximation of judge play.

Either way, rerun the candidate's 11-map screens once so that the two v6
candidates can be compared on deterministic results.

### R2. CPU safety on every map (blocking)

For the chosen candidate, run judge-sandbox full games (`unswbc run ... --sandbox`,
or your sandbox harness) on **all 11 official maps, both sides**, against
additive v4 (22 games). If time is short, the minimum is Big Empty,
Schooltime, stronghold, Trauma and Default, both sides; the others are
smaller. Record per game: max, p99, number of turns where the guard fired, and
first-turn cost.

Pass:
- **no turn over budget** (zero CPU deaths, including rounds 0-2);
- max at most 90M on every game;
- the post-guard work is bounded: `max - HARD_S point value` is at most 25M
  on every game. If the guard fires at 65M and the max is 81M, 16M of work
  runs after the check. Find what that is (feature rows, sonar, output) and
  move it before the check, or make it conditional.

The 85M/60M figures in the plan were headroom guesses. The hard requirement is
zero over-budget turns across these 22 games, with the max check above as the
safety margin.

### R3. Held-out regression (blocking)

Same candidate, 11 maps, both sides, 22 games each, against opponents never
used to tune or choose v6: frozen v3, ctmes (`sparring/ctmes`) and nicked v44
(`sparring/nicked_v44`). Pass: at least 14/22 against v3 and ctmes, no map at
0-2 against either, and a nicked v44 result reported (not gated). Report the
trajectory margin per map.

### R4. Pick the release candidate

After R1-R3, choose between original and narrow-escape v6 by: zero CPU deaths
first, then held-out wins and margin, then the result against additive v4.
Freeze the winner as `versions/v6` with `python -m bcsim.arena freeze` (or your
snapshot tool) and record the hash.

### R5. Package check

- Build the upload zip exactly like the previous releases (bot files at the
  archive root). Check that `paths.foreign_imports` is empty and that the zip's
  extracted bot hash equals the frozen hash.
- Run one end-to-end CLI game with the extracted zip, for example
  `unswbc run maps/default.map <extracted v6> versions/v3 --sandbox`, to check
  the real toolkit path, not just the harness.
- The toolkit reports `unswbc` 1.0.1 is available (we have 0.3.10). Read its
  changelog before release: if the judge's sandbox or price list changed, redo
  R2 with the new version.

### R6. Upload and monitor (user's go-ahead required)

- After upload, the user or Claude can track v6 with:
  `python -m bcsim.scrape --team 590 --unranked --submission <new id> --max-battles 40 --pages 2`
  then `python -m bcsim.scout --team 590 --unranked --submission <new id> --battles 40`.
- Check the first ranked games for CPU deaths: in `bcsim.analyze`, v6's
  deliberate feeding shows as `empty_turn_deaths`; any `no-move` death that is
  *not* an empty turn, or any turn flagged TLE or exceeded, means a CPU or
  invalid-action death. One is a stop-and-fix signal.
- **Rollback rule:** if CPU deaths appear, or if the rating is more than 60
  below v4's level after 30 ranked battles, make v4 (submission 5204) the active
  submission again and investigate.

## After release (not blockers)

- Queen, stronghold and Trauma against nicked (0-2 each), and Default for
  narrow-escape.
- The CMA-ES tuner from `V6_CORE_PLAN.md` section 4.4. It becomes practical
  once R1 makes local runs deterministic.
- King-feeding volume check with `bcsim.feed_trace` against the top-10 target
  (20-30 own-corpse pearls to the king after round 400).
