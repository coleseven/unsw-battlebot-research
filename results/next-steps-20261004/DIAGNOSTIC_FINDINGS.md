# Diagnostic findings: worker economy (NEXT_STEPS_2026-10-04, section 3)

4 October 2026. Control: v11t behaviour (C10 base, `results/20261003-224713-ablate-d440c5`,
hash-verified equal to `versions/v11t`; see `v11t_manifest.json`). Analysis of reconstructed
replays (an analyst view, not bot inputs). No bot change was evaluated here.

## Method

- **Case selection**: `select_cases.py` chose 24 cases deterministically before any replay was
  viewed (rules in its docstring): 12 elimination losses (4 each Stripes, Trophy, Dilemma, cycling
  opponent families and sides), 6 both-dead losses (3 with a total-length advantage, 3 without:
  Portals, Islands, weakhold, Tower Defense) and 6 wins on the same map against the same opponent
  (or the same family where no such win exists: Trophy v75 and Dilemma v75 have none).
- **Replays**: `case_replays.py` replayed all 24 deterministically; all 24 reproduced the recorded
  winner. Replays are in `cases/replays`.
- **Economy reconstruction**: `economy_diag.py` → `economy_cases.json`, tabulated by
  `economy_table.py`. Per side and 20-round window: pearls eaten (natural spawner tile versus
  elsewhere), living worker-turns, adjacent pearls passed over, worker-turns more than 20 own turns
  after last eating, spawner coverage (spawner tiles within 3 of a head), splits, deaths by cause,
  and the first round from which our length / dragon count stays below the opponent's.
- **Probes** (single games, diagnostic only, never promotion evidence) against the passive
  `opponents/turtle`, both sides, seed 771001 (`probe/`).

## Findings by map

### Stripes (4 elimination losses, 2 controls): production failure from round 0

- In the first 120 rounds of all four losses we ate **0–2 pearls in total and never split**; the
  opponents ate 26–139 and split 12–53 times. Our length and dragon count stay at 4 and 2 for
  70 rounds; the persistent deficit starts at round 10–27. Both controls also starved (4 and 21
  pearls); they were won by other means.
- Food per worker-turn is ~0.01 for us against 0.05–0.13 for the opponent: a genuine yield
  failure, not a population effect.
- Stripes has only 12 fast spawners (respawn gap 1), all in two-wide pockets fenced by kelp bands
  and entered through short portals or detours; 42 spawners have gap 500.
- **First divergence** (probe, v11q versus v11t against turtle; v11q is our previous version and
  differs only in the queen escape search):
  - v11q's queen walks into the pocket holding the fast spawners at (11–12, 1), eats twice and
    splits at round 11. Its child then farms a 7-cell loop through that pocket, eating every 7–9
    turns and splitting every ~10 rounds. v11q's workers ate 69 and 39 pearls in rounds 0–119.
  - **v11t's queen turns back at (14, 1)**: the corrected escape search rejects the pocket path.
    It never eats or splits, and no farming worker is born. v11t's workers ate **0** in rounds
    0–119, on both sides.
  - This matches the head-to-head (v11t 0/8 against v11q on Stripes) and C5's map delta (Stripes
    28→25, Tower Defense 30→20 when the corrected search was added).
- **Worker 2 (founder), in both versions**, circles a 2×3 loop at (17–18, 3–5) for 120+ rounds
  without eating, beside a kelp-fenced spawner block. Two likely lures:
  - `search_one`'s food term is the maximum food value met within 200 expanded nodes.
  - Its exploration-goal progress term scores each reached cell by **straight-line** distance to
    the goal. Behind a wall, the best cell is the one pressed against the wall nearest the goal.
- Turning off the queen guard penalty, or allowing queen extra steps, did not change the probe
  (0 worker pearls).

### Portals (2 both-dead losses): production failure from round 0

- We ate **0 pearls in rounds 0–59** in both cases; the opponent ate 43. The map has 104 fast
  spawners spread across it, in 2×2 clusters entered through portals.
- Probe: with all books on we ate 5 / 0 pearls in rounds 0–59; with all books off, 28 / 24.
  Turning off only `PORTAL_BOOK` reproduced the books-off result (28 / 24); hub book and map fill
  made no difference.
- The book's Portals pairs **match the 1.2.9 map exactly**, so the book data is not wrong. The
  divergence comes from how knowing the portals changes movement. In both probes no dragon stepped
  through a portal in rounds 0–59, and paths diverge after ~10 moves.
- C1's per-map table (books off): Portals 14/24 versus 12/24 (+2), Queen of Spades 5 versus 18,
  Default 12 versus 19. The books help overall and on several maps; Portals alone is weak evidence
  from 24 games.

### Trophy (4 elimination losses, 2 controls): early population race

- Food per worker-turn over rounds 0–119 is about equal for both sides: ours 0.05–0.08, theirs
  0.06–0.07; in our wins 0.065–0.07 against 0.08. The deficit is in **worker-turns**: the
  opponent has 2–4× as many, from more splits (43–67 against 5–22).
- The race is decided early. In the losses, the opponent's length goes 7→17 by round 20 and
  roughly doubles every 10 rounds; in our wins we are the side that does this. In rounds 0–19
  against v92 as side A we ate 1 against 11.
- Head-on deaths in the first 120 rounds are equal on both sides (trades).

### Dilemma (4 elimination losses, 2 controls): not an economy loss

- Lengths stay level (14–19 each) for 70 rounds in losses and controls alike, and food per
  worker-turn is similar. The persistent deficit begins at round 104–235: a late
  fight/territory/kelp-death collapse (W deaths 6–13 in 120 rounds on both sides).

### Both-dead losses (Islands, weakhold, Tower Defense)

- Islands: equal or better economy (we ate 179–210 against 166–167 in 120 rounds). We lost more
  dragons to kelp (35–36 W deaths against 2–3) and lost on longest length late: a delivery or
  survival problem, not production.
- weakhold and Tower Defense: tiny economies on both sides (2–6 pearls per 40 rounds). These are
  slow maps where the endgame decides.

## Decision gate (section 3)

The gate asks for repeated missed collection or return opportunities preceding collapse in at
least two target maps, appearing less in controls.

- **Missed collection precedes collapse on Stripes and Portals** (zero intake from round 0), and
  partly on Trophy (rounds 0–19). It is not less common in the Stripes controls, which starve too.
- **Its form is access, not sequencing.**
  - Food behind kelp, in portal-entered pockets, or a straight-line goal on the far side of a wall
    holds dragons in place.
  - On Stripes, the queen's corrected search refuses the one pocket path that founds the economy.
  - Once a dragon is inside a fast pocket, both versions already farm it with a tight
    collect-and-return loop (v11q worker 4).
  - A 2–4 turn harvest planner would not reach food that is 10–15 steps away around a wall.
- Trophy's yield per worker-turn is equal; it loses on population (split count and early first
  pearls). Dilemma and Islands are not production failures.

**Conclusion: the harvesting gate is not met in its intended form.** The first irreversible
divergence is **reaching** productive food, not exploiting food already within reach. The concrete
failures are:

1. **Straight-line goal progress behind walls**, which strands a worker (Stripes worker 2).
2. **The corrected queen search refusing a pocket entry that founds the economy** on
   small-start maps (Stripes; likely Tower Defense, −10 in C5).
3. **The Portals start**, where portal-book knowledge changes early routing for the worse (one
   probe; C1 +2/24 books off). This needs a multi-seed probe before any change.

## Recommended next experiments (one at a time, off-by-default switches, v11t parameters fixed)

1. **Path-aware exploration progress.** Distances to the goal by BFS over remembered terrain,
   unknown edges assumed open, kelp blocking, known portals followed. They replace the
   straight-line distance in `search_one`'s progress term. Measure first-60-round intake on
   Stripes and Portals, the worker-turns without eating, and wins over the full panel.
2. **Existing `CPP_PATH_DIST`** (path distance for hub, feeding and hunting pulls; built for v7
   and never evaluated under queen rules) as a separate variant in the same screen.
3. **Queen founding**: a narrowly triggered exception letting the queen take a pocket entry with a
   proven exit while the team has no worker income. Only after (1), and only with a regression
   case from this Stripes probe.
4. **Portals**: a multi-seed, both-side probe of `PORTAL_BOOK` on Portals alone before considering
   any change.

Harvest sequencing (section 4) stays queued behind these. If an access fix lands and Trophy-style
population races remain, revisit it together with "harvest one turn versus split now".

## Late-game conversion (section 5 prerequisite)

All 548 both-queens-dead games of the C10 base (254 losses, 294 wins) were replayed
deterministically, and all 548 reproduced the recorded winner (`late_cases.json`,
`late/replays`). Analysis scripts: `collector_diag.py` → `collector_cases.json`, and
`endgame_spread.py`.

- **Classes of the 254 losses.**
  - Could not deliver (160): our end total length exceeds their final longest, but no
    dragon of ours ever exceeded it.
  - Could not produce (76): end total 15 against their longest 27.5. These are mostly
    weakhold, Tower Defense and Maze.
  - Delivered then died (18): our dragon was longer than their final longest after
    round 300 and then died. Mostly weakhold and Islands.
- **Delivery efficiency is the same in wins and losses.** A donation is a worker's empty
  action, which drops its pearls; every donation had a teammate within the feeding range
  of 4. Donated pearls went:
  - losses: 38% to the intended recipient, 48% to other teammates, 8% to the enemy, 6%
    never eaten;
  - wins: 39%, 46%, 8%, 7%.
  - Pickup-aware drop placement therefore has no specific target here.
- **Volume and transport differ.**
  - Winners donate 42.5 times per game against 29.3 in losses (25.4 against 21.7 after
    round 400 in the could-not-deliver class).
  - In could-not-deliver losses our worker material at rounds 420 / 460 / 480 is 84.5 /
    78 / 66, of which **51 / 49 / 44.5 is more than 12 cells from our king** and only
    3 / 3 / 2 within 6.
  - Our king grows 16 → 20.5 → 23 over those rounds, while theirs grows 20 → 27.5 → 33.
  - In wins our king grows 18.5 → 24 → 28 at the same rate, and theirs only 10.5 → 14.
  - The longest-length race is decided after round 400: in losses the median margin goes
    −2 → −5 (round 450) → −10 (end); in wins 0 → +2 → +10.
- **Diagnosis.** Of Astra's three options, the evidence matches "collection begins too
  late despite persistent surplus". The surplus exists, but most of it is too far from
  the king to arrive before round 500. Small workers all start feeding at a fixed round
  (FEED_ROUND 403, minus 40 on large maps), whatever their distance from the king.
- **Experiment.** `CPP_FEED_TRAVEL`: a small worker's feeding start moves earlier by
  1 round per cell of distance to the beaconed king, capped at 60. Near workers keep the
  current timing. D4 screen: base results/v11t10-bot, 408 games.
