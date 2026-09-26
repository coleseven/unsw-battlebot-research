# Competitor and strategy research (2026-09-24)

Research only: nothing here was run against any bot, and no competitor code was
executed. Written for whoever builds the next bot (currently Codex). Every claim
about a competitor comes from reading their public source or notes; every claim
about us comes from `versions/v2`, the experiment write-ups, or `bcsim.analyze`.

## 1. How we actually lose (ranked replays)

Tool: `python -m bcsim.analyze` (see README). Numbers below are the 71 newer
ranked games of submission `3974` (32W 39L); the first four 9-game battles
(6W 30L) were against stronger opponents and are excluded here.

- 31 of 39 losses reach round 500 and are lost on longest dragon by a median of
  only **4**. Only 8 are eliminations.
- In round-limit **wins**, the opponent's longest stays at ~5 and our round-450
  growth overtakes it (to ~12 at the end). In **losses**, the opponent is already
  ~11 by round 400; our growth reaches ~8. Our total length is flat at ~30 from
  round 300 while theirs climbs to ~95.
- We eat **more** pearls (655/game vs 465) and split more (192 vs 136). Length is
  lost to deaths, not starvation: 574 length/game vs 336.
- Death causes (share of our deaths): head-on 46%, kelp 35%, body 18%, self 2%.
  **~101 of our deaths per game are into our own dragons** (vs 44 for opponents).
- Our long dragons die twice as often: 6.7 per game at length >= 10 vs 3.2, 213 of
  472 after round 400. Causes: self 157, own body 110, own head-on 78; enemy only 86.
- Queen Of Spades is 1-9 (mostly close round-limit losses). CPU is fine: max
  36.5M of 100M points.

Scoring order (official docs): survive; then longest living dragon; then total
team length; else draw. A dead dragon turns every second body segment into a pearl.

## 2. Sources

Public GitHub repos of teams in this competition. None has a license (all rights
reserved): use ideas, never code. Local copies for reading are in git-ignored
`sparring/`, pinned by commit, with a static security review in
`sparring/TRIAGE.md` (all clean; prebuilt `.exe` files deliberately not fetched).

| Repo | Team | Lang | Notes |
|---|---|---|---|
| nicked1205/battlecode-unsw-2026 | ? | Py | Very active (v34 on 24 Sep). Kings, hunters, sonar, map hub flags. |
| TX140907/UNSWBC- | "An IQ too high?" (~1680 on 22 Sep) | C++ | Leviathan/Kraken: beam search, per-map/per-side tuned params. Notes in Vietnamese. |
| devkadaba-maker/BattleCode | ? | Py + C++ | Flagship + collector/hunter roles; 153-game loss audit. |
| Aarav0010/botpro | ? | C++ | seadragon: measured topology/safety changes (75% -> 93%). |
| ctmes/battlecode | ? | Py | CMA-ES tuned (25 params, ~3,000 games); architecture close to ours. |
| zylotomous/bc2026 | ? | Py | Random queen/killer roles, pearl bidding, CPU self-metering. |

devkadaba's own loss audit found the same problem we have: 82 of their 91
round-limit losses were decided on longest dragon.

## 3. v2 versus the field: technical strategy

v2 is ~150 lines: greedy BFS to the nearest visible pearl, a one-step safety
filter, split at length 4 until round 450.

| | v2 | Competitors |
|---|---|---|
| Memory | None; the 7x7 window each turn | Persistent terrain, portal pairs, pearl sightings, tile staleness, own full body (nicked, Leviathan, zylotomous) |
| Move choice | First step of the path to the nearest pearl, if "safe"; else explore | Weighted score per move (pearl value, space, exits, danger, hunting, team spacing); Leviathan/seadragon beam search width 24, depth 14 |
| Trap check | Flood fill inside the window, capped at length + 4; cells on the window edge are never flagged | Length-scaled reachable area + exits at 1 and 2 steps + bottleneck/dead-end penalties; seadragon also checks the tail is reachable |
| Head-on danger | **Enemy heads only** | Enemy **and teammate** heads (nicked, ctmes, seadragon). seadragon measured enemy-only as worse: deaths roughly doubled |
| Portals | Treated as walls | Remembered pairs; early scouting; penalise unseen exits; use as escape |
| Sprint / sonar | Never used | Sprint as an emergency escape (Leviathan); sonar for pearl clusters, threats, targets (nicked, devkadaba). ctmes measured no gain from sonar |
| When trapped | Moves forward and dies | Reverse split: `SPLIT length-2`, so the rear becomes a new dragon walking out from the old tail (nicked, Leviathan) |
| CPU | ~15M points/turn | Self-metering: drop optional work at ~45 ms, cheap safe move at ~65 ms (zylotomous; they measure ~15M points of overhead before a turn's code runs) |
| Tuning | Hand constants + controlled experiments | CMA-ES + round-robin selection (ctmes); per map size **and starting side** tables (Kraken `trained_policy.hpp`) |

The replay data matches the table: ignoring teammate heads fits ~101 own-team
deaths per game; the window-only trap check that trusts the window edge fits 35%
kelp deaths.

## 4. v2 versus the field: game strategy

| | v2 | Competitors |
|---|---|---|
| Split | At length 4 into two length-2 dragons until round 450 | Mostly the same length-4 / child-2 pattern (also the most common in our corpus audit) |
| Endgame | Stop splitting at 450 | Growers chosen earlier: kings at length >= 12 that teammates yield pearls to within 3 tiles (nicked); children with `id % 7 == 0` never split (ctmes, founders stop at 25-49 units); growth priority from round 350 (Leviathan); flagships stop splitting at length 8 on big maps (devkadaba) |
| Team size | Up to 64 | Map-dependent: 40 on >= 3,000-tile maps (devkadaba); 56 open / 40 confined (Kraken) |
| Combat | Avoid only | Small dragons trade head-on with longer enemies; aim for the tile in front of an enemy head so it hits our body (nicked); separate head-risk weights for "we are longer" vs "we are much shorter" (ctmes) |
| Exploration | Toward likely pearl spawns in the window | Remembered hubs per map (nicked hard-codes coordinates by map size), early fan-out, border and retrace penalties (zylotomous) |

## 5. Our experiments in that light

Grower roles, persistent navigation memory, portal escape and guarded movement
were each tested as a single layer over v2's greedy movement. Grower, navigation
and guarded movement failed; the portal follow-up helped on generated maps but
missed the official-map promotion gates. Competitors make the same ideas work
alongside far stronger scoring and safety.

Hypothesis, untested: v2's movement and safety were the bottleneck (a grower that
walks into its own teammates does not get long), so these ideas may deserve a
retry on a stronger base. Newer framework files (`framework/action_value.py`,
`framework/adaptive_roles.py`) already move toward per-move features for a learned
ranker and locally triggered growth roles.

## 6. Techniques from similar games

| Game | What top teams did | Relevance |
|---|---|---|
| Tron, Google AI Challenge 2010 | Winner used a Voronoi territory score (cells each player reaches first), split space into chambers at articulation points instead of raw flood fill, found that a better evaluation beat deeper search, and switched to survival mode once separated | Formal version of the exits/bottleneck idea behind seadragon's gain; ctmes has a Voronoi term (`voro`). Chamber analysis targets kelp/pocket deaths |
| Battlesnake | Flood fill baseline, then paranoid minimax with alpha-beta (~7 plies) or MCTS | With up to 64 dragons and a per-turn budget, only a shallow (2-3 step) search including nearby heads is realistic |
| Kaggle Hungry Geese (multi-snake on a torus, the closest match) | Top solutions: policy/value network trained largely by self-play RL (HandyRL), bootstrapped from imitation, plus tree-search lookahead and flood-fill features | We have decoded top-ladder replays, exact turn reconstruction and a GPU. Limit: judge is NumPy-only at 100M points/turn, so networks must be small |
| Lux AI Season 1 | Public replays of the best agent were used by other teams to train imitation models; top two used RL and pulled ahead | Imitation from ladder leaders is a fast strong baseline; RL is how leaders separated |
| MIT Battlecode | Shared comms for permanent facts; early symmetry detection (maps are symmetric); search cut off before the budget | Maps here are guaranteed symmetric (mirror or 180 rotation), so one half predicts the other: kelp, portals, pearl spawns. No competitor seen uses this |
| Halite III | Winner assigned targets as a team rather than per ship; aggressive in 1v1, with resources dropped by collisions pulling ships into fights | Pearl bidding between teammates (zylotomous does this); dead dragons drop pearls on every second segment, so kills feed nearby dragons |

## 7. Recommended priorities

1. **Safety that includes teammates and map shape:** avoid teammate heads,
   exits at 1-2 steps, bottleneck/chamber detection, reachable-tail check, and a
   trap check that does not trust cells at the window edge. Targets our two
   largest death causes; seadragon measured 75% -> 93% from this area.
2. **Named growers from mid-game** (king/flagship style, possibly tuned per map),
   applied only once item 1 is in place.
3. **Automated tuning** (CMA-ES, round-robin selection, SPRT confirmation)
   against a mixed pool, parameterised by map size and possibly starting side.
4. **Learned move scoring** from top-ladder replays, used as the evaluation
   inside a short search rather than as the whole bot.
5. **Low-cost extras:** reverse-split escape, teammate pearl bidding, symmetry
   inference.

## 8. Sparring pool (not yet used)

`sparring/` holds six Python and seven C++ competitor bots, source only. If they
are used as opponents: run C++ only via the toolkit's judge clang to wasm32-wasi
(the `--sandbox` path), never build seadragon/portoff with `-DSEAD_*` (enables
debug file writes), re-triage after any re-pull, and mix the pool to avoid
overfitting to snapshots (nicked alone went through 34 versions in three days).
Python bots currently run one process per dragon in `bcsim.match`; an in-process
adapter for helper-based bots would be needed for arena-speed evaluation.

## 9. v3 against this research

`versions/v3` (hash `69382825b699723d`, see `HYBRID_EXPERIMENT.md`) keeps v2's
split policy exactly and replaces movement with a linear ranker over 24 window
features, imitation-trained on 60 top-ladder games. Candidates are still v2's
`tactics.safe_moves` set. Locally: 126-50 vs v2, 88% on new generated layouts.

**Where v3 matches the research**
- Learned move scoring from top-ladder replays: the Lux AI / Hungry Geese route
  (priority 4), with an honest train/dev/test split by battle.
- Some topology and crowding signals as features: exits, dead end, 3-step
  continuation, friendly/enemy nearby, teammate/enemy head reach.
- Elimination losses fell 10 -> 3 and round-limit losses 125 -> 80 in
  confirmation; friendly head deaths per action fell 28%.

**Learned weights (features are roughly 0-1 scaled)**
food_nearness +4.16, soon_food +2.67, food_x_length +2.52, friendly_near -2.32,
short_path +1.72, enemy_near -1.63, friendly_x_population -1.42, exits +1.24,
dead_end -0.74, friendly_reach -0.69, enemy_reach -0.29, later_enemy_reach -0.27;
round, length and population ~0.

**Gaps against the research**
1. **Teammate heads are still only a soft cost.** The hard filter (v2
   `danger_cells`) excludes enemy-head cells only. A teammate head's reach costs
   0.69, against 4.16 for an adjacent pearl, so the ranker will take a pearl into a
   cell a teammate head can also enter. seadragon treats both as danger and
   measured enemy-only avoidance as doubling deaths. Absolute friendly head
   deaths went *up* in v3's diagnostic (1,452 -> 1,644).
2. **Same window-limited trap check.** Space and exits are computed inside the
   7x7 window; there is no memory, no reachable-tail check, no chamber analysis,
   and no kelp knowledge beyond the window. Kelp was 35% of our ranked deaths.
3. **No phase awareness.** The round/length/population weights are effectively
   zero, so movement is identical at round 50 and round 480; the endgame is
   still only "stop splitting at 450". This is the main ranked loss mode (31 of
   39 recent losses are round-limit, median longest gap 4). Competitors pick
   growers from round ~200-350 or by length/ID. The mature-role variant failed
   its gate on v2 movement; worth retrying on v3 movement (section 5).
4. **Imitating the teacher's moves without its reasons.** Teachers act on memory,
   sonar and search that v3's window features cannot see; agreement is 58-66%.
   Cloning captures their food-first habits without their long-horizon safety.
   Hungry Geese and Lux leaders used imitation as the start, then self-play RL
   or search.
5. **Used as the whole policy, not inside a search.** No lookahead over
   our own moving body and nearby heads (research: evaluation inside a shallow
   2-3 step search).
6. **Still absent:** portals, sprint escape, reverse-split escape, sonar,
   pearl bidding, intentional trades, map symmetry, per-map/side parameters.
   Default regressed (40-8 -> 35-13); Trauma stays weak (15-33).
7. **CPU headroom is thin.** Sampled sandbox peaks were 65-85M of 100M points
   (v2 used ~37M on the ladder) and v3 has no self-metering. Competitors cut
   optional work at ~45 ms and fall back to a cheap move at ~65 ms. A
   worst-case turn on a crowded large map is the risk; "no valid action" is
   death.
8. **Evaluation opponents are weak.** Gains are measured against v2, splitter
   and hunter. The ranked opponents it must beat use kings, trades and deep
   search; the `sparring/` pool would test those directly.

**Suggested order, building on v3:** hard teammate-head avoidance in the
candidate filter; a CPU self-meter with a cheap fallback; round/phase-aware
growers on top of v3 movement; then a shallow search using the ranker as its
evaluation.

## References

- a1k0n, Google AI Challenge post-mortem: https://www.a1k0n.net/2010/03/04/google-ai-postmortem.html
- Battlesnake useful algorithms: https://docs.battlesnake.com/guides/useful-algorithms
- coreyja, Minimax in Battlesnake: https://coreyja.com/posts/BattlesnakeMinimax/Minimax%20in%20Battlesnake/
- Hungry Geese 2nd place: https://www.kaggle.com/competitions/hungry-geese/writeups/goosebumps-goosebumps-solution-2nd-place
- Hungry Geese 3rd place slides: https://speakerdeck.com/hoxomaxwell/kaggle-hungry-geese
- Hungry Geese 11th place (NN+MCTS): https://www.kaggle.com/competitions/hungry-geese/writeups/the-wisdom-of-manjushri-if-three-ducks-approach-11
- Lux AI S1 lessons: https://github.com/Lux-AI-Challenge/Lux-Design-S1/issues/142
- Toad Brigade (Lux AI S1): https://www.kaggle.com/competitions/lux-ai-2021/writeups/toad-brigade-toad-brigade-s-approach-deep-reinforc
- Battlecode 2023 postmortem: https://battlecode.org/assets/files/postmortem-2023-gone-fishin.pdf
- Battlecode 2025 postmortem: https://battlecode.org/assets/files/postmortem-2025-confused.pdf
- teccles Halite III bot: https://github.com/teccles-halite/halite3-bot
- UNSW Battlecode docs: https://game.battlecode.au/docs
