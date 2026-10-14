# Brief for Codex: make v5 beat nicked (v34, then v44)

Written 2026-09-25 by Claude (research role) for Codex (bot builder).
Goal set by the user: **beat `sparring/nicked` (v34) locally, then
`sparring/nicked_v44`**. Everything below is from replays already on disk and
from reading nicked's public source. Nothing here was run against any bot.

Do not copy nicked's code: the repo has no license. The behaviours below are
described so they can be implemented independently in our framework. The numbers
quoted from nicked are reference points for our own tuning, not values to paste.

## 1. What actually happens against nicked (v34)

Every local game against nicked on disk (v3 control, mature/opportunity growers,
additive v4, export scout, v5 scout_king) was lost, except Colosseum (a map no
longer in rotation). Distinct games:

| Map | Result | Final (alive/longest/total) us v nicked | What went wrong |
|---|---|---|---|
| Default | L, round limit | 15/7/48 v 41/16/189 | **Economy:** 164 pearls v 466. Even until r100, then nicked's total grows 81 → 146 by r400 while ours stays ~61 |
| Default Small | L, eliminated r383-444 | 0 v 42/3/95 | 44-49 **kelp** deaths; pearls 186 v 317 |
| Queen Of Spades | L, eliminated r205-477 | 0 v 32/4/77 | **Opening collapse:** 2 dragons and 10 pearls by r50 (nicked: 7 dragons, 20 length). Cause not yet diagnosed |
| Trauma | L, round limit (all variants) | ~13/4/30 v 28-41/8-13/95-148 | **Portal pocket** (below); 84-141 kelp deaths; population flat at ~13 while nicked goes 13 → 44 |

Two facts matter more than any king logic:

- **nicked's winning longest dragon is only 8-16.** Against v34 we do not lose a
  king race; we lose on economy and survival (fewer pearls, more deaths, fewer
  dragons), and on small maps by elimination.
- **Many of our variants never changed the game.** v3, mature, opportunity and
  additive produced *byte-identical* Trauma games against nicked, and scout_king
  was identical to export_scout. Before running a full evaluation, diff event
  streams against the control to confirm the change actually changes behaviour.

### The portal pocket

Reachable area from team A's start, computed from the map files:

| Map | Without portals | With portals |
|---|---|---|
| Trauma (48x24) | 264 tiles, **10 spawn tiles** | 1,144 tiles, 142 spawn tiles |
| stronghold (48x24) | 264 tiles, 99 spawn tiles | 1,152 tiles, 210 spawn tiles |
| Schooltime (60x40) | 1,858 tiles, 296 spawn tiles | 2,062 tiles, 322 spawn tiles |
| Default (32x32) | 830 tiles | 1,024 tiles |
| Queen, Trophy, Devil, Default Small, Big Empty | effectively no gain | |

v3/v4/v5 movement treats portals as walls. On Trauma that starves the whole
team inside a 10-spawn-tile pocket for 500 rounds.

## 2. How nicked plays

**v34** (the snapshot used in all local games above):
- **Memory:** remembers terrain, portal pairs, pearls, spawn countdowns and when
  each tile was last seen.
- **Move choice:** each move is scored by a search over up to 300 remembered
  cells. The score includes pearl value (visible pearls weighted above
  remembered ones), predicted spawns (countdown minus rounds since seen, within
  40 rounds), an exploration bonus for unseen cells, a strong penalty on cells
  enemy or teammate heads can reach, a corridor penalty (cells with fewer than
  2 free neighbours), a trap penalty when reachable room is under
  `2 x length + margin` (the margin is doubled after round 400), and a lethal
  penalty when room is under `length + 2`.
- **Portals:** scouted deliberately early; an unseen exit gets an increasing
  penalty later; a portal whose exit is known to be occupied is never taken.
- **Hunting:** short dragons target the cell in front of enemy heads.
- **Kings:** dragons of length 12 or more; smaller teammates yield pearls to a
  king within 3 tiles.
- **Escape:** a reverse split (`SPLIT length-2`) when no safe move exists.
- **Sonar:** broadcasts pearl clusters and large threats.

**v44** (current) adds:
- **Founder anchors:** dragons alive at round 0-1 split length-2 children until
  round 250, then stop and grow. They are protected: 1.5x space margin, 2x
  head-on and portal penalties, no hunting. They only split again if the team
  falls below 24.
- **Long-dragon protection:** any dragon of length 5 or more after round 80
  stops splitting, weights pearls 2.5x, and plays safer after round 450.
- **Swarm schedule:** the swarm splits at length 4 until round 250 only, with a
  cap of 48 dragons.
- **Cash-in from round 420:** a dragon of length 5 or less that sees a teammate
  of length 6 or more (at least twice its length) moves toward it, avoiding the
  cell in front of its head. When 2-4 tiles away (Manhattan), and not in that
  front cell, it sends no action and dies, so its pearls land near the big
  dragon. There is no enemy check and no exact-adjacency requirement.
- **Map knowledge:** the hard-coded hub coordinates from v34 are gone.

## 3. Changes, in priority order

Each item is one ablation on top of current v5 (or additive v4 if v5 changes
turn out neutral), evaluated as in section 4.

### P1. Portals as real passages
Keep a per-dragon memory of portal pairs as they are seen. Include known portal
edges in the route graph and in the trap/room check. For the first ~80-100
rounds, add a pull toward portals and unexplored portal exits; after that,
penalise portals whose exit has not been seen recently. Never enter a portal
whose exit is known to be occupied, including by our own tail.
*Why first:* it is the only fix for Trauma and stronghold, and those maps
account for most of the kelp deaths.
*Earlier result to reuse carefully:* `NAVIGATION_EXPERIMENT.md` (portal memory
on v2 movement) failed promotion against v2. Against nicked the need is direct,
so re-test it against nicked, not against v2.
*Measure:* pearls and spawn tiles reached on Trauma and stronghold; alive count
at round 300.

### P2. Pearl economy beyond the 7x7 window
Remember pearls and spawn countdowns per dragon (predicted spawn = countdown
minus rounds since seen). Route to the best remembered or predicted target with
a BFS over remembered terrain, with a budget of a few hundred nodes. Add an
exploration term for unseen cells. Spread out: penalise stepping within 2 cells
of teammates, much more strongly in the first 20-40 rounds.
*Why:* Default is 164 v 466 pearls with even fighting.
*Measure:* pearls per game against nicked on Default, Schooltime and Big Empty.

### P3. Survival: kelp, traps and heads
- **Room check:** require reachable room of at least `2 x length + margin` over
  remembered terrain, treating a body segment `k` steps from the tail as free
  after `k` moves. Double the margin after round 400.
- **Trap penalties:** penalise corridor cells (fewer than 2 free neighbours).
  Treat room under `length + 2` as lethal.
- **Head danger:** hard-exclude cells that enemy **or teammate** heads can enter
  next turn, when any alternative exists. v4's guard screen was neutral against
  weak opponents; re-test it against nicked.
- **Reverse-split escape:** when no safe move exists, `SPLIT length-2`.

*Why:* 44-141 kelp deaths per game on Trauma and Default Small.
*Measure:* kelp deaths and own-team deaths per game.

### P4. Queen Of Spades opening
We have 2 dragons at round 50. Pull a v3-vs-nicked Queen replay
(`results/20260924-114923-v4-grower-352a0f/.../control_v3-vs-nicked-queen_of_spades_*`)
and find what kills the founders in the first 50 rounds: `python -m bcsim.analyze <replay>`
with `--game`, or the replay viewer. Fix before tuning anything else on Queen.

### P5. Split schedule
Test the split cutoff at {250, 350, 450} crossed with a population cap of
{48, 64}, with a floor that resumes splitting when the team drops below ~24.
nicked v44 uses 250/48; the top-10 median is ~470 with heavy late feeding.
Choose per map size if the data supports it (larger maps favour earlier growth
and earlier feeding: Big Empty feeding starts ~r363 across the top 10).

### P6. Kings and feeding (needed for v44 and the ladder, less for v34)
- **King selection that exists early:** use founders (alive at round 0-1)
  and/or any dragon of length 5+ after round ~80 as protected growers. They stop
  splitting, get a pearl-weight multiplier, and wider safety margins (more room,
  head-risk and portal penalties). Replace v5's hash-elected 1/8 at round 400:
  too late, and it can elect a crowded dragon.
- **Feeding volume:** from round ~400-420, a dragon of length 5 or less that sees
  a teammate of length 6 or more (at least twice its length) moves toward it
  (weight falling with distance, never into the cell in front of its head). When
  2-4 tiles away, and not in that front cell, send an empty turn. Consider
  skipping the feed when an enemy head is within ~2 of the king (nicked has no
  check; measure both ways).
- *Why:* v5 made 12 feed actions in 12 games; top teams' kings eat 20-30
  own-corpse pearls after round 400 (`TOP_TEAMS_SCOUTING.md`). The exact-adjacency
  predicate is too rare to matter.
- *Measure:* the king's own-corpse pearls after round 400
  (`python -m bcsim.feed_trace <replays>`), and king length at r450 and r499.

### P7. Head-on trade policy
Allow deliberate head-on trades only for short dragons (length 3 or less)
against longer enemies. Dragons of length 5 or more should avoid any cell an
enemy head can reach. In v4's first 27 site games (unranked), the dragon we lost
was the longer one in 50% of head-on trades.

## 4. Evaluation protocol

- **Opponents:** `sparring/nicked` (v34) first, then `sparring/nicked_v44`
  (which needs its `params.py`; both passed the static review in
  `sparring/TRIAGE.md`), with additive v4 as a regression control. Build
  third-party bots with one worker to avoid the Windows build-cache race you
  hit earlier.
- **Maps: 11**, both sides. The 9-map ranked rotation (Default Small, Trophy,
  Queen Of Spades, Default, Devil, stronghold, Trauma, Schooltime, Big Empty)
  **plus Arena (11x11) and Colosseum (16x16)**, which left the ranked rotation
  around 23 Sep but are kept so the bot stays generally good, including on
  small cramped maps. Map files: `maps/` and `maps/server/` (Arena exists in
  both; use one copy). Games are deterministic, so **one seed = 22 distinct
  games per opponent**. Repeating seeds adds no information.
- **Gate:**
  - Against v34, win at least 12 of 22 with no map at 0-2.
  - Then against v44, same gate.
  - Not worse than additive v4 on the same 22.
  - Report the 9 rotation maps and the 2 extra maps separately as well, so a
    gain on Arena/Colosseum cannot hide a loss on the ranked rotation.
  - Report `bcsim.analyze --json` stats: pearls, deaths by cause, own-team
    deaths, and king curve.
- **Behaviour-change check:** before each full run, diff the new bot's event
  stream against the control on 2-3 maps; if identical, the change did not fire.
- **CPU:** memory plus search adds cost. v4 already peaks at ~65M of 100M
  points. Add a self-meter: stop optional work (long searches, routing) past
  ~45 ms, and fall back to the cheap safe move past ~65 ms. Confirm with the
  judge sandbox on Big Empty and Schooltime (largest maps, most dragons).

## 5. Suggested order of work

P1 portals, then P3 survival, then P2 economy: these three should flip Trauma,
stronghold, Default and Default Small against v34. Arena and Colosseum are
small, cramped maps decided early by elimination (Colosseum is currently the
only map where v3 movement beats nicked, 2-0), so check that P1-P3 do not
cost them. Then P4 (Queen opening),
then P6 kings/feeding and P5 split schedule for v44 and the ladder. P7 is small
and can ride along with P3.

## Sources

- Local replays against nicked: `results/20260924-114923-v4-grower-352a0f`,
  `results/20260924-115357-v4-grower-374d2b`, `results/20260924-121059-v4-phase-e23595`,
  `results/20260924-215614-export_scout`, `results/20260924-215724-additive`,
  `results/20260924-223816-v5-combo-809e43`.
- nicked source: `sparring/nicked` (v34, commit badc527ffd),
  `sparring/nicked_v44` (v44, commit b932513ce3). Security review: `sparring/TRIAGE.md`.
- Ladder evidence: `TOP_TEAMS_SCOUTING.md`, `COMPETITOR_RESEARCH.md`.

## 6. Round 2 (25 Sep): why P1-P4 did not move the nicked score

Codex's full-suite ablations (`V5_EXPERIMENT.md`) each scored 1-5 wins of 22
against nicked v34 (baseline v5: 5-17). Re-reading the baseline v5-vs-nicked
replays (`results/20260924-233609-full-change-bb86e5/full/replays`):

- **Pearl totals are even overall** (v5 621 per game, nicked 625), but the
  losses come from two different failures:
  - **Starvation on small/medium maps.** Default side B: v5 holds 13 dragons
    from r100 to r200 making ~3,800 moves, yet total length stays at 26-31 and
    it eats 37 pearls all game; nicked grows 33 -> 124 by r200 (507 pearls).
    Queen 9 v 490 pearls, Trophy 188 v 689, Devil 66 v 317.
  - **Mass loss on big maps.** Big Empty: v5 is at the 64-dragon cap from r100,
    peaks at 554 total length near r300, then *shrinks* to 368 while nicked
    grows to 1,013 (both ate ~1,600 pearls). Schooltime: v5 eats more (1,660 v
    840) but has 300-349 kelp deaths, i.e. boxed-in dragons with no legal move.
- **The missing piece is exploration, not memory.** v3's 24 features have no
  term for unseen or not-recently-visited area, and the economy ablation only
  routed to spawns already seen. With no food in view, a v5 dragon has no
  reason to go somewhere new. nicked's per-move score adds a bonus for unseen
  cells reachable within its search, a penalty for revisiting its own recent
  cells, and strong early fan-out away from teammates.
- **Single nudges on the v3 ranker cannot express this.** Each ablation was a
  thin override applied after the learned ranker; the base mover's objective
  stayed "nearest visible food, else local drift". Changing the objective
  itself is a bigger step than any one override.

Suggested next experiments, each still judged on the full 11-map suite:

1. **Exploration term in the move score:** reachable unseen (or not seen for N
   rounds) cells within a bounded search from each candidate move, plus a
   recent-visit penalty on this dragon's own trail, plus stronger teammate
   fan-out in the first ~40 rounds. Diagnostic before the full suite: Default
   and Queen pearls at r200 (target: nicked's ~120 total length by r200).
2. **Population control on big maps:** stop ordinary splitting around r250-350
   and/or cap at ~48, so pearls become longer dragons instead of 64 short ones
   that collide. Diagnostic: Big Empty total length at r450 (v5 503, nicked 856).
3. **Consider a new mover rather than more overrides:** a search-based scorer
   (bounded BFS over remembered terrain with pearl, predicted-spawn,
   exploration, trap and head-risk terms), with the learned v3 score as one
   term, then tune its weights by CMA-ES against nicked v34 on the 11 maps.
   This is how nicked, ctmes and Kraken are all built.
