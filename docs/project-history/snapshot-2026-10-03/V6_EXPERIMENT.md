# V6 search-core experiment log

## Frozen hand-default core (2026-09-25)

The v6 mover uses one bounded search score over remembered terrain, food,
space, heads, portal paths, and the v3 learned action score. Split, protection,
and feeding are explicit decisions. The initial frozen bot is
`results/20260925-132108-v6-g0-791c56/bots/v6`; the full evaluation is
`results/20260925-132931-full-change-982835/`. The live `mybot` was not changed.

- Five-map G0 against nicked: 6/10 wins; mean trajectory margin -0.076 vs
  frozen v5's -0.547, delta +0.471. G0's +0.15 architecture gate passed.
- All 11 maps, both sides: 17/22 vs frozen v5 scout-king, 17/22 vs additive,
  12/22 vs nicked. No match errors.
- Trajectory-margin F (mean + 0.25 * worst map): +0.301 vs v5, +0.323 vs
  additive, -0.089 vs nicked. The frozen v5 baseline F vs nicked is -0.499.
- Against nicked, Queen, Stronghold, and Trauma were 0/2 each. Thus the G1
  12-win count passed but the no-0/2-map requirement failed; v6 is **not**
  promoted.
- The Big Empty judge-sandbox run showed max 81.36M CPU points and p99
  60.71M, against proposed thresholds of 85M and 60M. No crash logs were
  observed. The harness flags explicit empty-turn feeding deaths as no-action
  deaths, so its invalid-action count needs classification before G4 can pass.

## Portal diagnosis and scout experiment

In the frozen full-set nicked replays, v6 used zero portals on both sides of
Trauma and Stronghold; nicked used 22/118 on Trauma and 45/83 on Stronghold.
On Trauma, v6 gathered 31/28 pearls versus nicked's 415/785 in the same two
games. The core only considered portals whose *both* ends were already seen,
which makes a one-way escape from a spawn pocket unlikely to be discovered.

The next candidate adds an early, short, unprotected scout role (one of eight
new dragons). An unpaired portal edge seen during bounded search contributes a
frontier score; a scout may cross an adjacent unpaired portal if the visible
exit is empty or the exit is unseen. That latter case is a deliberate risk
limited to expendable scouts. Other dragons keep the known-pair-only rule.
The scout is still scored in the same unified mover, not a final-action
override. Source changes are in `framework/core_search.py`,
`framework/core_params.py`, `experiments/v6/brain.py`, and snapshot packaging.
The candidate is frozen at `results/v6-portal-scout-bot`; its all-map evaluation
is `results/20260925-165427-full-change-6aff76/`. It tied the initial v6's
17/22 vs scout-king, 17/22 vs additive, and 12/22 vs nicked, but shuffled
several map outcomes. Its F vs nicked was -0.090, slightly worse than -0.089.
It caused some Stronghold crossings (17-18 instead of zero), but only two
crossings per side on Trauma. This is not a promotable standalone change.

The next route-bias variant retains those bounded scouts and gives them a
one-step distance-progress score toward the known 48x24 spawn-pocket exit
while they are still inside the pocket. This is restricted to a map-size and
observed-coordinate condition and only to the early scout role; it is an
experiment, not a generic permanent map override. It needs a full-map screen.

Route-bias was frozen at `results/v6-pocket-route-bot` and screened in
`results/20260925-170438-full-change-1b70b0/`. It scored 17/22 vs v5,
18/22 vs additive, and 13/22 vs nicked, with nicked F -0.067. Queen,
Stronghold, and Trauma remained 0/2 against nicked; Default regressed to
0/2. The specified founder scouts had already entered the Trauma portal by
round 9 *without* the route term, and each survived the full game but never
split after crossing. Merely adding entry-route pressure is not a solution.

An unrelated-map replay comparison exposed an evaluation flaw: the scout-only
and route-bias Schooltime actions were identical to round 196, then diverged
despite the route term being disabled on Schooltime. V6's shared wall-clock
search cutoff can change the number of expanded nodes under host scheduling.
The next frozen candidate removes that cutoff and uses only the fixed
`N_SEARCH` node cap. A full Big Empty judge-sandbox CPU check is required
before an all-map strength test; `results/v6-deterministic-bot` is that
candidate.

The fixed-200-node candidate exceeded the judge CPU limit on Big Empty in
rounds 0-2 (`results/v6-deterministic-sandbox.json`) and was rejected before
strength testing. A fixed-96-node candidate failed in the same early pattern
(`results/v6-deterministic96-sandbox.json`). Rechecking the original frozen v6
in the same sandbox reproduced the earlier 20,376-turn run exactly, with no
CPU errors (`results/v6-original-sandbox-recheck.json`). The portal-scout bot
with the wall-time guard also completed 20,437 metered turns with no CPU
errors (`results/v6-portal-scout-sandbox.json`), max 80.71M and p99 60.30M.
The runner's nonzero exit in both full games came from intentional empty-turn
feeding deaths, not an observed CPU error. The fixed-node rewrite is rejected;
the safe wall-time cutoff is restored. Deterministic evaluation remains an
open infrastructure issue, and narrow win differences require replication.

The new post-portal hypothesis is that a scout that escapes but never grows
cannot colonize the high-spawn area. An initial-observation check distinguishes
Trauma's sparse starting pocket from Stronghold. Only its founder scout gets
a score toward the known hotspot after crossing; the original pre-portal
route and other dragons are unchanged. The check was confirmed against a
recorded round-0 observation. The frozen bot is
`results/v6-trauma-hotspot-bot`; full-map screen:
`results/20260925-172503-full-change-de9339/`.

That screen finished 17/22 vs v5, 17/22 vs additive, and 13/22 vs nicked.
Trauma still lost both sides to all three opponents. A recorded founder scout
crossed the portal, then died to kelp at round 54 without splitting after
crossing. The hotspot term is rejected and removed from source.

The next variant instead adds a three-step, non-reversing escape test for each
immediate move. Cell-only BFS can count a thin corridor as room by turning
around, while a length-2+ dragon cannot reverse. The escape test penalizes
paths with no continuation before depth three, with future own-body release
and remembered occupancy handled by the same blocking helper as search.
Unit tests include a synthetic forced corridor. Frozen candidate:
`results/v6-forced-escape-bot`. Its judge CPU screen must pass before a full
11-map strength screen.

The unconditional lookahead completed a Big Empty sandbox game without hard
CPU errors, but max 85.53M and p99 63.99M missed the planned 85M/60M
headroom targets (`results/v6-forced-escape-sandbox.json`). It also had lower
final length than the control in that game. It was rejected before a full
strength screen. The next revision runs this check only when the destination
has at most one onward exit, retaining the intended corridor case at lower
CPU cost.

The narrowed guard completed Big Empty under the hard CPU limit, with no CPU
errors and max 80.75M points, but p99 62.40M still misses the planned 60M
headroom target (`results/v6-narrow-escape-sandbox.json`). A full strength
screen is running at `results/20260925-174256-full-change-ac5a2a/` because
its Big Empty outcome was better than the unconditional guard. It is not yet
promotable under G4.

That full screen finished 17/22 vs v5, 18/22 vs additive, and 11/22 vs
nicked, with zero match errors. Its nicked trajectory F improved to -0.033
(mean +0.107, worst Queen -0.562), compared with route-bias F -0.067.
Nevertheless G1 fails on the win count and 0/2 maps: Queen, Default,
Stronghold, and Trauma. The candidate is retained as a frozen datapoint, not
promoted. Its CPU p99 also still fails G4's 60M headroom target. The source
currently represents this experimental candidate, while `mybot` remains
unchanged.

The sandbox harness now classifies a `\nENDTURN\n` reply as an intentional
empty action, and separates those feeding deaths from missing/invalid replies
in new artifacts. This avoids falsely failing CPU integration tests because
the bot deliberately cashes in a feeder. Previously saved sandbox artifacts
retain their original classification.

All map/side results here are one deterministic game per map and side against
each opponent, not independent random-seed evidence. Do not upload v6 yet.

## Handover to Claude, 25 Sep evening (Codex out of tokens)

Reconstructed from `results/` (the log above ended before these runs):

- `bcsim/local_v6_clock.py` gives in-process runs a deterministic,
  judge-calibrated work clock (`BCSIM_DETERMINISTIC_V6=1`). In the Big Empty
  sandbox profile the soft cutoff fired on 16,940 of 19,461 moving turns, so
  the budget binds almost every turn on the judge.
- Under that clock the earlier candidates collapse: original v6 went 2/22,
  1/22 and 0/22 against v5, additive and nicked
  (`results/20260925-182609-full-change-a85586`); narrow-escape 1/22, 1/22,
  0/22 (`...182711-full-change-1505bb`). Their earlier 17/22 came from host
  wall time being faster than the judge. Judge-sandbox games agree: both lost
  their Default and Default Small sandbox games.
- **Fair-search v6** (`results/v6-fair-search-bot`, hash `09044969872c49c4`)
  splits the remaining soft budget evenly across legal moves instead of
  letting the first searched move use it all. Deterministic full suite
  (`...184725-full-change-858372`): 16/22 against v5, 17/22 against additive,
  12/22 against nicked v34. It won both Default Small sandbox games (max 81.0M,
  p99 57.4M, first turn up to 73.5M points).
- Held-out opponents (`results/20260925-190333-full-change-62d036`):
  16/22 against v3, 17/22 against ctmes, 7/22 against nicked v44.
  **stronghold and Trauma were 0-2 against every opponent, including v3 and
  ctmes.**

### Split-floor bug and fix

`core_split.should_split` let any dragon (including protected kings) split
whenever `unit_count < FLOOR` (24), at any round. On Trauma, where v6 stays
under ~14 dragons, everything re-split at length 4 all game (longest 3; lost to
v3 3 vs 5 on longest). On stronghold, late feeding thinned the team below 24
and the fed king re-split (longest fell to 5-7 against v3's 10).

Fix (source of truth `framework/core_split.py`, new `FLOOR_UNTIL = 400` in
`framework/core_params.py`): protected dragons never split after the cutoff,
and the low-population refill ends at `FLOOR_UNTIL`. Unit tests updated
(`tests/test_core_search.py`; the two tests of narrow-escape-only features were
removed). `framework/core_search.py`, `framework/core_params.py` and
`experiments/v6/brain.py` were reset to the fair-search versions (they still
held the rejected narrow-escape variant), and `bcsim/v6_initial.py` no longer
packages the unused `portal_escape.py`. Candidate: `results/v6-floorfix-bot`
(hash `4959b003957277f5`; differs from fair-search only in `core_split.py` and
`FLOOR_UNTIL`).

Running: full 11-map deterministic suite against fair-search, additive v4,
nicked v34, v3, ctmes and nicked v44
(`results/20260925-191302-full-change-a71535`), and the 22-game judge CPU
suite (`results/20260925-191314-v6-cpu-cc9c2f`). The CPU suite's summary
writer was fixed to overwrite its per-game summary (it crashed after 2 games
of the earlier fair-search run).

### Floor-fix results and release candidate (25 Sep)

Deterministic full suite, all 11 maps, both sides, 132 games, zero match
errors (`results/20260925-191302-full-change-a71535`):

| Opponent | Floor-fix v6 | Fair-search v6 (before) | Maps at 0-2 after |
|---|---|---|---|
| fair-search v6 | 16/22 | - | none |
| additive v4 (live) | 21/22 | 17/22 | none |
| nicked v34 | 16/22 | 12/22 | Queen, Trauma |
| v3 | 21/22 | 16/22 | none |
| ctmes | 21/22 | 17/22 | none |
| nicked v44 | 8/22 | 7/22 | Trophy, Queen, Trauma, Schooltime, Big Empty, Arena |

Judge CPU suite, 22 sandbox games covering every map and side against
additive v4 (`results/20260925-191314-v6-cpu-cc9c2f/summary.json`):
**PASS**. Zero over-budget turns, zero invalid-action deaths, zero guard
fallbacks; max 81.9M points (Big Empty), first turn at most 73.8M, p99 53-62M.
The live Timeouts docs (checked 25 Sep) still say 100M points per turn, first
turn charged for imports, and a 48 MB memory limit; v6 peaked at about 22 MB.

Frozen as `versions/v6` (hash `4959b003957277f5`). Upload package
`battlebot-v6.zip` (SHA-256
`61bf7fcad9470ac69a8a6c3d4fc7f1721c5b742d56e31bff479d3daf1a6df374`); its
extracted files hash to the frozen bot and have no foreign imports.

Known weaknesses for the next round: nicked v44 (8/22), and Queen and Trauma
against nicked v34. The `unswbc` toolkit here is 0.3.10; PyPI has up to
1.1.0 (no changelog published). The documented judge limits are unchanged, but
re-run the CPU suite after any toolkit upgrade.

## v6.1 (26 Sep): portal book, aggression, hubs, exploration

All runs: deterministic judge-calibrated clock, all 11 maps, both sides, zero
match errors unless noted. Opponents: uploaded v6 (`versions/v6`, submission
6688), additive v4 (live before v6), nicked v34, nicked v44.

- **Portal book** (`framework/v6_portal_book.py`, `bcsim/portal_book.py`):
  official-map portal pairs, applied only after a dragon has seen one end with
  the same id and edge. Every crossing matches engine geometry
  (`tests/test_portal_book.py`). Portal steps per game rose on stronghold
  (1 -> 22), Default, Queen and Schooltime, but not Trauma: the move was legal,
  but nothing beyond the portal scored. Alone it was about even with v6
  (12/22; `results/20260925-204545-full-change-13b847`; a lighter unseen-exit
  penalty was not better: `...204546-full-change-911c3e`).
- **Aggression** (`core_search`): short non-king dragons may step onto an
  adjacent enemy head (head-on kills both), hunt longer enemy heads, and long
  dragons keep 2 tiles from enemy heads. First settings (even trades allowed)
  tripled favourable trades and all but ended losing ones, but even trades
  exploded, pearls fell 568 -> 422 and body kills 11.6 -> 4.0 against nicked;
  net about even (`...210224-full-change-b3cbea`).
- **Hub book** (`framework/v6_hub_book.py`, `bcsim/hub_book.py`): up to 12
  hubs per map from the map files' per-tile respawn gaps, only on maps with real
  hot spots; map identified in-game by its kelp/portal layout (all 11 maps
  identified from real observations, `tests/test_hub_book.py`). The hub pull
  follows search paths (through book portals), with a weaker straight-line
  fallback; learned hubs from observed countdowns on unknown maps. At W_HUB 20
  the time near hubs only rose 18% -> 22% (`...210224-full-change-4838d6`).
- **Exploration goal** (`core_memory.update_goal`): stale or unseen 8x8 blocks
  as per-dragon goals, pursued along search paths; x2.5 in poor areas (mean
  1/(1 + max countdown) of tiles in view below 0.01); weak for kings.

Tuned combination **v6.1b + exploration** (`results/v61b-goal-bot`, hash
`a208ae7f66bbd144`: ATTACK_MIN_GAIN 1, HUNT_MIN_GAIN 2, W_HUB 60, GOAL on;
`results/20260925-212727-full-change-b01abd`):

| Opponent | v6.1b + exploration | uploaded v6 |
|---|---|---|
| uploaded v6 | 16/22 | - |
| additive v4 | 22/22 | 21/22 |
| nicked v34 | 18/22 | 16/22 |
| nicked v44 | 8/22 | 8/22 |

No map at 0-2 against v6 or additive; against nicked v34 only Queen. These
are now the defaults in `framework/core_params.py`. Pending: judge CPU suite
(`results/20260925-214041-v6-cpu-f74d3d`), held-out v3/ctmes
(`...214042-full-change-ba75fb`), and the same combination without the goal
(`...212726-full-change-52675f`, resumed after a worker crashed with a
CPython/wasmtime thread-state fault; not a bot error).
