# V6 core plan: one search-based move score, tuned against nicked

Written 2026-09-25 by Claude (research role) for Codex (bot builder).
Read with `V5_VS_NICKED_BRIEF.md` (evidence) and `V5_EXPERIMENT.md` (your results).

Do not copy code from `sparring/` (no licenses). Where this plan cites nicked's
behaviour or numbers, they are reference points; implement independently and
let tuning choose the values.

## 0. Why a new core instead of more v5 ablations

Every v5 ablation was judged by wins out of 22 against nicked v34. Measured by
**final total-length share margin** instead (`(ours - theirs) / (ours + theirs)`
of team total length at the last round, 0 = even, -1 = eliminated; averaged
over the 22 games), none of them moved the gap:

| v5 variant (22 games vs nicked v34) | Wins | Mean final share margin | Mean longest gap at end |
|---|---|---|---|
| baseline v5 (scout + round-400 king) | 5 | -0.52 | -5.6 |
| portal | 3 | -0.53 | -4.8 |
| trap guard | 3 | -0.56 | -7.0 |
| economy | 1 | -0.76 | -10.7 |
| Queen route | 5 | -0.52 | -5.4 |
| head guard | 4 | -0.48 | -3.8 |
| exploration | 5 | -0.50 | -5.0 |
| split brake | 5 | -0.57 | -7.2 |

-0.5 means nicked ends with about 3x our total length. The best change moved the
margin by 0.04. Baseline per-map final share margins (average of both sides):
Arena 0.00, Big Empty -0.46, Colosseum +0.76, Default -0.76, Default Small -1.00,
Devil -1.00, Queen -1.00, Schooltime -0.50, stronghold -0.26, Trauma -0.55,
Trophy -0.95.

Two structural reasons:

1. **The objective never changed.** The v3 linear ranker (24 window features,
   imitation-trained) chooses toward visible food, else local drift. Every v5
   module is a post-hoc override of that choice.
2. **Overrides conflict.** `experiments/v5/brain.py` applies up to ten modules
   in sequence (population, exploration, trap guard, hotspot, Queen route,
   sonar route, feeding route, portal, economy, king guard, head guard); each
   can overwrite the previous one's move without seeing its reasons.

The strong bots we have read (nicked, Leviathan, seadragon) all make one
decision per turn from one score that combines food, exploration, space, head
danger and portals, computed by a bounded search over remembered terrain. V6
does the same, keeps v3's learned score as one term, and then **tunes the
weights automatically** instead of by hand.

## 1. What to keep from v5, what to drop

Keep (copy the files into the v6 bot snapshot unchanged unless stated):

| Keep | From | Used for |
|---|---|---|
| `bc.py` | `versions/v3` | protocol, `Obs`, `Brain`, `fallback` |
| `tactics.py` | `versions/v3` | `danger_cells`, `safe_moves`, `room` (fallback path only) |
| `action_value.py` + `action_model.py` | `versions/v3` | the learned v3 score as one weighted term (`W_V3`), and the emergency fallback mover |
| `navigation.py` (`Memory`) | `framework/navigation.py` | per-dragon terrain memory and `destination()` through portals. **Construct with `portals=True`** |
| `v4_sonar.py` beacon/decode | `framework/v4_sonar.py` | optional, behind parameter `SONAR` (your ablation found removing it neutral: 5-7) |
| split legality and the danger guard | `versions/v3` split rule | "never split with the head in `danger_cells`" stays a hard rule |

Drop from the v6 path (they are replaced by terms in the single score; keep the
files for history, but v6 must not import them): `v5_hotspot` (Trauma-only
scout), `v5_queen_opening`, `v5_economy`, `v5_exploration`, `v5_population`,
`local_safety` trap guard, `v5_head_guard`, `v5_portal_push`, `v5_king`
(hash election), `v4_feeding` and `v5_feeding` (replaced by section 2.4).

## 2. The v6 bot, module by module

New files, all in `framework/` (then `python -m bcsim.sync` where applicable)
plus `experiments/v6/brain.py`. Every tunable number lives in one generated
`core_params.py` (like `v5_config.py`), so the tuner can write a candidate
without touching code.

### 2.1 `framework/core_memory.py`: what one dragon remembers

`class WorldMemory` wraps `navigation.Memory(width, height, portals=True)` and
adds, all keyed by absolute cell index `y * width + x`:

- `spawn[cell] = (predicted_ready_round, seen_round)`: when a visible tile has
  `pearl_in >= 0`, store `obs.round + obs.pearl_in[k]`. Mirror symmetry is an
  optional later extension; do not add it in the first version.
- `pearl[cell] = seen_round` for visible pearls; delete when the tile is seen
  without a pearl; expire after `PEARL_TTL` rounds (default 8).
- `occupied[cell] = (team, id, is_head, facing, seen_round)` from `obs.bodies`
  (absolute coordinates; visible parts only); expire after `OCC_TTL` rounds
  (default 2). Never treat an unseen cell as occupied or as safe: unseen cells
  are simply "unknown" (the search can walk them at an extra cost).
- `trail`: this dragon's head cells, newest last, with the round of each visit
  (keep the last 60). Because v6 never sprints, the last `obs.length` trail
  cells are exactly our body, including parts outside the window.
- `update(obs)` is called **once at the start of every turn**, before any
  decision, including split and feed turns (v5 skipped memory updates on some
  non-move turns; do not repeat that).

### 2.2 `framework/core_search.py`: the single move score

`def score_moves(mem, obs, team, did, P) -> dict[str, float]` (`P` =
`core_params`). For each first move `d` in `NESW`:

1. **Legality (hard):** not the reverse of `obs.facing` when `length > 1`;
   `obs.passable(CENTER, d)`; the destination is not occupied, except by our
   own tail cell when not eating. A portal move is allowed only if both ends of
   that portal are known in `mem` and its exit cell is not known occupied. If
   no move is legal, return `{}` (the caller falls back, section 2.5).
2. **Time-aware blocking:** for our own body, the segment `k` steps from the
   tail is free after `k + 1` moves; other remembered occupied cells are
   blocked for the whole search.
3. **Bounded BFS** from the destination over `mem.destination()`, at most
   `N_SEARCH` expansions (tune; start 200) and depth `DEPTH_MAX` (start 16). A
   cell is enterable at depth `t` if its free time is at most `t`. Unknown cells
   cost 1 extra step.
4. **Terms,** computed from the BFS (`dist` = BFS depth to the cell):
   - `food = max(W_PEARL / (1 + dist))` over visible pearls; the same with
     `W_MEM_PEARL` for remembered pearls; `W_SPAWN / (1 + dist + 0.2 * wait)`
     for predicted spawns with `0 <= wait = ready - round - dist <= H_SPAWN`.
     Take the max over all three.
   - `explore = W_UNSEEN * unseen_reached / N_SEARCH + W_STALE * stale_reached / N_SEARCH`,
     where unseen = never seen and stale = not seen for at least `STALE_ROUNDS`.
   - `room`: the number of cells reached (the BFS stops counting at `need`).
     `need = min(SPACE_MULT * length + SPACE_MARGIN, SPACE_CAP)`, with the
     margin multiplied by `ENDGAME_SPACE_MULT` when `round >= 400`.
     `trap = -W_TRAP * max(0, need - room)`; add `-W_LETHAL` if
     `room < length + 2`.
   - `exits`: legal onward moves from the destination, not counting the way
     back. `-W_DEADEND` if 0, `-W_CORRIDOR` if 1.
   - `heads`: `-W_HEAD_ENEMY * max(1, length / 4)` if an enemy head can step
     onto the destination next turn; `-W_HEAD_TEAM` for a teammate head; and
     `-W_AHEAD` if the destination is one of the two cells straight ahead of
     any head.
   - `revisit = -W_REVISIT * max(0, 1 - (round - last_visit) / REVISIT_ROUNDS)`
     from `trail`.
   - `fanout = -W_FAN(round) * teammate_heads_within_2`, where
     `W_FAN = W_FAN_EARLY` before `FAN_ROUNDS`, else `W_FAN_LATE`.
   - `portal = -W_PORTAL` for a portal move; `-W_PORTAL_UNSEEN` if the exit has
     not been seen for `PORTAL_STALE` rounds; for the first `SCOUT_ROUNDS`
     rounds, add `+W_PORTAL_SCOUT` instead (pull toward exploring portals).
   - `v3 = W_V3 * action_value.score(row_d, action_model.MODEL)`, where `row_d`
     is the v3 feature row for `d`. Compute features only for legal moves.
   - `straight = W_STRAIGHT` if `d == obs.facing`.
   - A **protected** dragon (section 2.4) multiplies `W_TRAP`, `W_LETHAL`,
     `W_HEAD_ENEMY` and `W_PORTAL_UNSEEN` by `PROTECT_MULT`.
5. Return `score[d] = food + explore + trap + exits + heads + revisit + fanout + portal + v3 + straight`.
   Choose the max; break ties by the v3 term, then by `d == obs.facing`.

### 2.3 `framework/core_split.py`: population

`def should_split(obs, mem, P, protected) -> str | None` returns `"SPLIT n"`
or `None`:

- Never if `protected`, or if `bc.CENTER in tactics.danger_cells(obs, team)`.
- Split if `obs.length >= SPLIT_AT` (start 4), with child `CHILD` (start 2),
  and `obs.unit_count < min(CAP, init.unit_limit)`, and
  `round <= SPLIT_UNTIL_SMALL` on maps under `AREA_SPLIT` tiles (start 1000),
  `round <= SPLIT_UNTIL_LARGE` otherwise.
- **Floor:** after the cutoff, split again only if `unit_count < FLOOR`.
- A split can leave the child with no exit; keep v3's legality checks
  (`can_split` equivalent) exactly as they are.

### 2.4 `framework/core_king.py`: kings and feeding

- **Protected (king candidate):** a dragon is protected if it was born at
  round 0 (a founder) and `round >= FOUNDER_PROTECT_ROUND`, or if
  `round >= PROTECT_ROUND` and `obs.length >= PROTECT_LEN`. Protected dragons
  do not split (except an emergency floor split when `unit_count < FLOOR`),
  weight food by `PROTECT_FOOD_MULT`, and use the safety multiplier above.
- **Feeding:** from round `FEED_ROUND`, a dragon with
  `obs.length <= FEED_MAXLEN` that can see a teammate head whose visible
  segment count is at least `max(FEED_KING_MIN, 2 * obs.length)`:
  - is pulled toward that head: add `W_CASH / (1 + manhattan)` to each move's
    score, and `-W_LETHAL` for the cell straight in front of that head;
  - returns the empty action `""` (engine suicide, drops ⌈L/2⌉ pearls) when
    the Manhattan distance to the head is between `FEED_DMIN` and `FEED_DMAX`
    (start 2 and 4), it is not in the cell straight in front of the head, and
    (parameter `FEED_ENEMY_CHECK`) no enemy head is within 2 cells of the king.
- **Target volume:** the king should eat 20-30 own-corpse pearls after round
  400 on round-limit maps (top-10 teams; see `TOP_TEAMS_SCOUTING.md`). Measure
  with `python -m bcsim.feed_trace`.

### 2.5 `experiments/v6/brain.py`: turn order

```
turn(obs):
    t0 = time.perf_counter()
    mem.update(obs)                              # always first
    read sonar messages (if SONAR)
    if feed rule fires: return ""                # 2.4
    s = core_split.should_split(...)             # 2.3
    if s: return s
    if elapsed(t0) > HARD_S: return v3 choice    # action_value.choose(...)
    scores = core_search.score_moves(...)        # 2.2, with the feeding pull
    if not scores: reverse-split escape if length >= 4: return f"SPLIT {length - 2}"
                   else return self.fallback(obs)
    action = "MOVE " + best
    append SONAR beacon (if SONAR)
    return action
```

- **CPU meter:** check `time.perf_counter()` inside the BFS loop. Past
  `SOFT_S` (start 0.045 s), stop expanding and score with what has been
  searched. Past `HARD_S` (start 0.065 s) before the search, use the v3 choice.
  These are wall-clock guesses; the judge measures points, so calibrate the two
  numbers with `unswbc run ... --sandbox` on Big Empty and Schooltime (largest
  maps, most dragons) before tuning. v4 already peaks at about 65M of 100M
  points, mostly in v3 feature extraction.
- Keep all state on `self` (CLAUDE.md).

## 3. Parameters (initial values and tuning ranges)

Initial values are reasonable hand guesses, some informed by what nicked
exposes publicly. The tuner owns the final values. Normalise every parameter
to [0, 1] inside the tuner; integers are rounded after de-normalising.

| Group | Parameter | Start | Range |
|---|---|---|---|
| Search | `N_SEARCH`, `DEPTH_MAX` | 200, 16 | 80-400, 8-24 |
| Food | `W_PEARL`, `W_MEM_PEARL`, `W_SPAWN`, `H_SPAWN` | 80, 20, 30, 40 | 20-200, 0-80, 0-100, 10-80 |
| Explore | `W_UNSEEN`, `W_STALE`, `STALE_ROUNDS` | 8, 3, 30 | 0-40, 0-20, 10-80 |
| Space | `SPACE_MULT`, `SPACE_MARGIN`, `SPACE_CAP`, `ENDGAME_SPACE_MULT` | 2, 8, 100, 2 | 1-3, 2-20, 40-160, 1-3 |
| Traps | `W_TRAP`, `W_LETHAL`, `W_DEADEND`, `W_CORRIDOR` | 10, 100, 60, 8 | 1-40, 30-300, 0-200, 0-40 |
| Heads | `W_HEAD_ENEMY`, `W_HEAD_TEAM`, `W_AHEAD` | 60, 60, 20 | 10-200, 0-200, 0-80 |
| Movement | `W_REVISIT`, `REVISIT_ROUNDS`, `W_FAN_EARLY`, `W_FAN_LATE`, `FAN_ROUNDS`, `W_STRAIGHT` | 3, 20, 8, 1.5, 30, 0.5 | 0-15, 5-60, 0-20, 0-8, 0-80, 0-3 |
| Portals | `W_PORTAL`, `W_PORTAL_UNSEEN`, `PORTAL_STALE`, `W_PORTAL_SCOUT`, `SCOUT_ROUNDS` | 8, 60, 3, 40, 100 | 0-40, 0-200, 1-20, 0-100, 0-200 |
| Learned | `W_V3` | 10 | 0-40 |
| Split | `SPLIT_AT`, `CHILD`, `CAP`, `FLOOR`, `SPLIT_UNTIL_SMALL`, `SPLIT_UNTIL_LARGE`, `AREA_SPLIT` | 4, 2, 56, 24, 450, 300, 1000 | 3-6, 2-3, 32-64, 8-40, 150-480, 150-480, 400-2000 |
| Kings | `FOUNDER_PROTECT_ROUND`, `PROTECT_ROUND`, `PROTECT_LEN`, `PROTECT_MULT`, `PROTECT_FOOD_MULT` | 250, 80, 5, 1.5, 2 | 100-450, 50-400, 4-12, 1-3, 1-3 |
| Feeding | `FEED_ROUND`, `FEED_MAXLEN`, `FEED_KING_MIN`, `W_CASH`, `FEED_DMIN`, `FEED_DMAX`, `FEED_ENEMY_CHECK` | 410, 5, 6, 80, 2, 4, 1 | 350-470, 2-6, 5-12, 0-200, 1-3, 2-6, {0, 1} |
| Other | `SONAR` | 1 | {0, 1} |

## 4. Success criteria: how training and testing are scored

### 4.1 Per-game margin `m` (the tuning signal)

Wins alone are too coarse at 5 of 22. Use a continuous margin computed from the
replay timeline (`bcsim.analyze` stores alive/total/longest every 10 rounds):

```
share(t) = (T_us(t) - T_opp(t)) / max(1, T_us(t) + T_opp(t))    # team total length at round t
m = mean of share(t) for t = 10, 20, ..., 500
    # after an elimination, rounds up to 500 count as -1 (we were eliminated)
    # or +1 (they were), so early collapses are penalised in proportion
```

Also record per game: result (W = 1, D = 0.5, L = 0), final longest-dragon gap,
final total-length share, and elimination round. Add this as a small reusable
function (for example `bcsim/margin.py`, `game_margin(stats, side)`) and a CLI
that prints it for a results directory. **Compute it for the v5 baseline run
(`results/20260924-233609-full-change-bb86e5`) first**; that is the number to
beat.

### 4.2 Tuning objective `F` (one number per candidate)

```
m_map = mean of m over that map's two sides
F = mean over maps of m_map + 0.25 * min over maps of m_map
```

The min term stops the tuner from buying average gains with a collapse on one
map. Any match error, crash-fallback turn or invalid-action death sets
`F = -inf` for that candidate. A candidate whose sampled CPU meter triggered the
`HARD_S` fallback on more than 2% of its turns also gets `F = -inf` (it is
spending the budget, not deciding).

### 4.3 Train / test split

Games are deterministic, so seeds add nothing and **the test set must be
different opponents**, not different seeds. Maps cannot be held out (CLAUDE.md
requires all 11 for every bot change).

- **Train (the tuner sees these):** nicked v34 (`sparring/nicked`) and
  additive v4. Both sides, 11 maps.
- **Test (never used for tuning or selection):** nicked v44
  (`sparring/nicked_v44`), ctmes (`sparring/ctmes`), frozen v3, the frozen
  v5 baseline, and Leviathan once it builds through the judge clang. Both
  sides, 11 maps.

### 4.4 Tuning loop

- **Tool:** a new `bcsim/tune_core.py`, run through `bcsim.bounded.run` (RAM
  checks) at `official_suite.DEFAULT_WORKERS`. Each candidate is a bot snapshot
  whose only difference is `core_params.py`. Use the `cma` pip package as a
  training-only dependency (not installed yet: `.venv\Scripts\python -m pip install cma`);
  the bot must never import it.
- **CMA-ES settings:** start at section 3's values, `sigma0 = 0.25` in
  normalised space, population 12, at most 25 generations. Checkpoint after
  every generation (mean, sigma, covariance, every evaluated vector with its
  `F` and per-game margins) so it can resume after a crash or RAM stop.
- **Two stages per generation:**
  - **Screen:** each candidate plays nicked v34 on the 5 hardest maps (Default
    Small, Devil, Queen Of Spades, Trophy, Big Empty), both sides: 10 games.
    `F_screen` uses the formula in 4.2 over those 5 maps. This is a diagnostic
    probe, allowed by CLAUDE.md.
  - **Full:** the generation's top 2 by `F_screen` play the full train set
    (nicked v34 and additive v4, 11 maps, both sides: 44 games). The
    generation's reported best is the best full `F` (nicked games weighted 2:1
    against additive games).
  - CMA-ES updates on `F_screen`; the full runs exist to catch screen
    overfitting. If the full `F` of screen leaders falls for 3 generations in a
    row while `F_screen` rises, stop and widen the screen to all 11 maps.

### 4.5 Gates, in order (a candidate must pass each to continue)

| Gate | Test | Pass condition |
|---|---|---|
| G0 architecture probe | Hand-default v6 (section 3 values) vs nicked v34 on the 5 hardest maps, both sides | Mean `m` improves over the v5 baseline on those same 10 games by at least 0.15. If it does not, stop and diagnose before building the tuner: the architecture, not the weights, is wrong |
| G1 train | Tuned candidate vs nicked v34, 22 games | At least 12 wins and no map 0-2 |
| G2 regression | vs additive v4, 22 games | At least 13 wins, and full `F` at least that of the v5 baseline against additive |
| G3 held-out test | vs nicked v44, ctmes, v3, v5 baseline (and Leviathan if built), 22 games each | v44: at least 11 wins; ctmes and v3: at least 16 wins, no map 0-2; v5 baseline: at least 12 wins. Report `m` per map for every opponent |
| G4 CPU | Judge sandbox full games (`unswbc run ... --sandbox`) on Big Empty and Schooltime | Max at most 85M points, p99 at most 60M, zero invalid-action deaths |
| G5 release | Upload | Only with the user's explicit go-ahead (CLAUDE.md) |

Report every gate with: W-D-L, per-map `m` for both sides, final longest-dragon
gap, deaths by cause (kelp, head-on, own-team), pearls, and the king's own-corpse
pearls after round 400. Store all replays and the parameter vector.

## 5. Order of work

1. `bcsim/margin.py` and the v5 baseline margins (section 4.1).
2. `core_memory.py` with unit tests on recorded observation blocks: portal
   destinations, trail-derived body, spawn prediction, occupancy expiry.
3. `core_search.py` and `experiments/v6/brain.py` with hand defaults;
   calibrate the CPU meter in the sandbox.
4. `core_split.py` and `core_king.py`.
5. **Gate G0.** Do not build the tuner until the architecture moves the margin.
6. `bcsim/tune_core.py`, then run CMA-ES (overnight; the second PC can run a
   second CMA-ES chain from a different start or with a different screen map
   set).
7. Gates G1 to G4 on the best full-`F` candidate. Freeze it as `versions/v6`.

## 6. Should we imitate the best downloaded bot instead?

Short answer: **find out which bot is best (cheap, useful either way), but do
not make imitation the main path.** Use the best bot as the tuning opponent.

- **Which bot is best:** only nicked v34 (8-2 against v3) and ctmes (3-8
  against v3) have been measured. Run the Python round-robin from
  `OPPONENT_LADDER.md` (v3, additive v4, v5 baseline, ctmes, nicked v34,
  nicked v44, devkadaba, zylotomous 2 and 3, nambot) on the 11 maps, and add
  Leviathan when it builds. That orders the ladder and picks the train and
  test opponents above.
- **Why not copy its moves as the policy:**
  1. We already did imitation. v3 is a clone of top-ladder players' moves (58-66%
     agreement), and it is the ceiling we are stuck at. A clone of nicked would
     have the same limit.
  2. nicked decides from memory (remembered pearls, spawn timers, portal
     pairs), which our 7x7 window features cannot see, so a window-feature clone
     cannot reproduce its decisions. It would learn its habits, not its reasons.
  3. Pure imitation compounds errors: once the clone drifts into states nicked
     never visits, it has no good examples. Fixing that needs interactive
     relabeling (DAgger: run our bot, ask nicked what it would do in our
     states), which means running nicked as a labeler at scale.
  4. At best it caps us at nicked's strength. We do not know nicked's ladder
     rating, and nothing suggests it is one of the top-10 teams.
  5. Training on its outputs is legally grey (no license) and is the user's
     decision.
- **Where imitation can help later:** after the v6 memory exists, the learned
  `W_V3` term could be refit on memory-aware features from top-ladder replays
  (legitimately public games), or on our own tuned v6 acting as teacher. That
  is a refinement of one term, not the core.
