# Team 777 at UNSW Battlecode 2026: every version of the bot, what it did and what we learned

Written 12 October 2026. This is the narrative account of the whole project, from the
first greedy bot on 22 September to the last upload on 7 October, with the ladder
position as it stood on 12 October. It is written as source material for a video: each
chapter covers one version of the bot, says exactly what that version was, what was
tested, what worked and what did not, and names matches that show the idea (or the
weakness) on screen.

**How this relates to the other documents.** `PROJECT_HISTORY.md` and
`docs/project-history/` are Astra's audited archive; they cover 22 September to
3 October and are the place to check a number's provenance. `FEATURE_EXPERIMENT.md` is
the running experiment log from v7 onward, including everything after Astra's cutoff
(v12s, v12x, v12z). This document tells the story in order and does not replace either.
Nothing in Astra's files was changed to write it.

**Two kinds of match are cited.**

- **Live ladder games.** Each has a link to the official viewer
  (`https://game.battlecode.au/visualiser?match=<battle id>`). A battle is five games;
  the text names the map so you can pick the right game.
- **Showcase replays.** 132 games played for this writeup between frozen versions of our
  own bot: each version against the one before it, both sides, one seed, under the rules
  of its era. They are in `showcase/replays/` and are named
  `<side A>-vs-<side B>-<map>-s20261012.replay`. Open them in VS Code like any local
  replay. The same seed and bots always replay the same game
  (`showcase/make_showcase.py` regenerates them). `showcase/timeline.py <replay>` prints
  the round-by-round numbers quoted here.

Showcase replays are illustrations, chosen because they show a mechanism clearly. They
are one seed each and are not evidence of strength; a newer version sometimes loses them.
The evidence is the multi-seed, multi-opponent experiments quoted in each chapter.

**Reading the numbers.** "A vs B of N" is always candidate wins against control wins over
the same N games (same maps, sides, seeds and opponents). "pp" is percentage points of
win score. A "screen" is a first test (400 to 550 games); a "confirmation" is a second
test on seeds the candidate has never seen (1,000 to 1,200 games). A range in brackets
is a bootstrap interval.

---

## 1. The whole story in one page

A solo entrant, team "777", played the UNSW Battlecode 2026 ladder (21 September to
17 October, about 1,000 teams). The bot went through 17 frozen versions and 11 uploads in
16 days of development.

The arc has three parts:

1. **Learn the old game (22 to 30 September).** The game was won by the longest living
   dragon at round 500. The bot learned to multiply (v2), to move well (v3), to plan with
   one search instead of stacked rules (v6), to run 10 times cheaper in C++ (v7), and to
   pour its swarm into one "king" at the end (v10). Rating went from 1500 to about 1670,
   rank 133 of roughly 930.
2. **The rules change (1 October).** The organisers made each team's first dragon a
   **queen**: at round 500 the longest surviving queen wins. Ratings were reset. A bot
   built to breed a swarm and feed a king now had to keep one specific small dragon alive.
3. **Learn the new game (1 to 7 October).** The queen learned not to feed herself to her
   own workers (v11q), then to search for escapes correctly (v11t). Two replay diagnoses
   fixed whole maps (v12s, v12x). The last version (v12z) copied what the ladder was
   doing to us: small workers that spend a body segment to sprint into the enemy queen.

**Where it ended.** On 12 October the team was **rank 153 of 1,001 at rating 1604**, with
3,421 game wins. The closest approach to the top 100 was **rank 108 of 973** on
3 October, 31 rating points short. The rating needed for rank 100 rose from 1533 on
2 October to 1813 on 12 October; ours rose from 1445 to 1604 over the same days.

**Five things the project taught, in order of how much they mattered.**

1. **Economy first.** Letting dragons split was the largest gain ever measured here:
   78% of games won against 34%. Nothing later came close.
2. **The scoring rule decides the strategy.** Under "longest dragon" the answer was king
   feeding. Under "longest queen" it was queen survival and queen killing. The rule
   change on 1 October made the previous best idea irrelevant overnight.
3. **Caution almost always lost.** Trap avoidance, wider threat zones, guards, refuges,
   split restrictions and sprint-aware fear all made dragons survive less or win less.
   More than a dozen such ideas were tested. The only safety work that paid was making
   the queen's escape search correct, not making it more fearful.
4. **Testing errors cost more than strategy errors.** A wall-clock bug made a 0/22 bot
   look like a 12/22 bot. A single-seed tuning win reversed on three seeds. Seven "new"
   maps turned out to have no food in them. Each was caught, but only by distrust.
5. **Watching games beat turning knobs.** Every gain after 3 October came from reading
   one replay closely and finding a specific wrong decision. The broad retunes and
   learned models tried in the days before had found nothing.

---

## 2. The game in two minutes

Two teams of **dragons** (snakes) share a grid that wraps at the edges. Between cells
there can be **kelp** (a wall) or a **portal** (a paired doorway to somewhere else on the
map). **Pearls** appear on fixed spawner tiles; eating one makes a dragon one segment
longer. Each tile respawns after its own hidden delay, so some tiles are worth far more
than others.

What makes the game hard:

- **Each dragon is its own program.** It sees a 7 by 7 window around its head and shares
  no memory with its teammates. The only communication is **sonar**: a 32-bit message
  fired in a straight line to the first dragon it hits, friend or enemy.
- **Splitting.** A dragon of length 4 or more can split; the rear segments become a new
  dragon facing the other way. A team can hold 64 dragons.
- **Death.** Hitting a wall, a body or having no legal move kills a dragon. A head-on
  collision kills both dragons, whatever their lengths. A dead dragon leaves pearls on
  half its segments. A dragon that outputs nothing dies on the spot, which teams use
  deliberately to **feed** a teammate.
- **Sprinting.** A dragon may take extra steps in one turn; each extra step costs it a
  segment.
- **Budget.** Each dragon gets 100 million "CPU points" per turn on the judge, with
  Python 3.13 and NumPy or compiled C++.

A game lasts 500 rounds, or ends at once if a team has no dragons left.

**Scoring until 30 September:** elimination, else the **longest living dragon**, then
total team length.

**Scoring from 1 October ("Slay Queen"):** the two starting dragons with id 0 and 1 are
the **queens**. At round 500 the longest surviving queen wins; a dead queen scores zero.
If both are dead (or tied) the old rule applies. Every dragon also got free extra steps:
one quarter of its length, rounded up. A child never inherits queen status.

A ranked **battle** is five games on five maps. Rating moves with the share of games won.

---

## 3. Every version at a glance

| Version | Frozen | What it added | Uploaded? | Headline evidence |
|---|---|---|---|---|
| v1 | 22 Sep | Greedy pearl chaser, no splitting | No | 81/180 vs scripted bots; 4/36 vs a splitter |
| v2 | 22–23 Sep | Split at length 4 into 2+2, cap 64, stop at round 450 | Yes, 22 Sep | 386 vs 317 of 432; 117–27 direct |
| v3 | 24 Sep | Learned 24-feature move ranker | No (packaged) | 126–50 vs v2; 445 vs 393 of 528 |
| v4-additive | 24 Sep | Late feeding and sonar beacon on v3 | Yes, 24 Sep | 8–8 vs v3; 8–0 vs v2 |
| v5 | 25 Sep | Scout and early-king wrappers | Never released | 5/22 vs nicked |
| v6 | 25 Sep | One unified search with memory | Yes, 26 Sep | 21/22 vs v3; 16/22 vs nicked v34 |
| v6.1 | 25 Sep | Map books, aggression, hubs, exploration goals | Folded into v7 | 16/22 vs v6 |
| v7 | 26 Sep | C++ port, first tuned parameters | No (reversed) | 14/22 on one seed, 29/66 on three |
| v7-base | 26 Sep | C++ port, untuned | Yes, 27 Sep | Exact parity with Python on 481,092 turns |
| v9 | 28 Sep | 16 parameters re-tuned, portal scouting | Yes, 28 Sep | 153 vs 124 of 270 |
| v10 | 28 Sep | King beacon, big dragons also feed | Yes, ~29 Sep | 237 vs 210 of 360 |
| v10h | 30 Sep | Map completion, earlier feeding on big maps | Yes, 30 Sep | 316 vs 280 of 540 |
| v10o | 1 Oct | Sonar hub sharing for lost dragons | Yes, 2 Oct | 563 vs 542 of 900 |
| v11ms | 2 Oct | Free extra steps to grab a pearl | No | 474 vs 447 of 792 |
| v11q | 2 Oct | Light queen, 3-step escape search | Yes, 2 Oct | Queen alive 79 vs 24; 80/120 vs v10o |
| v11t | 3 Oct | Corrected queen search | No | 571 vs 534 of 1,020; 75/136 vs v11q |
| v11u | 3 Oct | Queen refuge | No (rejected) | 392 vs 358, then 641 vs 627 |
| v12s | 5 Oct | Queen plays as a worker early on tiny maps | No | Stripes 53 vs 25 of 132 |
| v12x | 5 Oct | Exploration that beats the ranker's pull | Yes, 5 Oct | +4.7 pp [+0.6, +8.9]; 60/102 vs v11t |
| v12z | 7 Oct | Sprint rams on enemy queens, paid queen flight | Yes, 7 Oct | +5.7 pp [+2.4, +9.1]; 91/136 vs v12x |

Content hashes and verified zips for each frozen version are in `versions/*/FROZEN.txt`.

---

## 4. v1: the greedy snake (22 September)

**What it was.** The starter Python bot with small repairs. Each dragon looked at its
7 by 7 window, ran a breadth-first search to the nearest visible pearl, estimated free
space with a flood fill, and avoided cells next to an enemy head. It had no memory, did
not use portals on purpose, never split and never talked to teammates.

**What was tested.** Before any strategy work, a small laboratory was built: an arena
that plays two bots on a map, frozen snapshots of every version, five scripted opponents
(greedy, hunter, splitter, turtle, wanderer), a replay decoder and content hashes so a
result always names the exact code that produced it.

**What worked.** The laboratory. It was used for every later decision.

**What did not.** The bot. It scored 81 of 180 against the scripted opponents and
**4 of 36 against the splitter**, a script that does nothing clever except split. After
the evaluation was repaired the splitter result was 2 wins to 16.

**Matches to show.**

- `showcase/replays/old/v1-vs-splitter-trophy-s20261012.replay`. v1 starts with two
  dragons and never has more. The splitter first splits at round 27, has 13 dragons at
  round 100 and 22 at round 175, when v1's last dragon dies. The whole first lesson is in
  this game: one careful snake cannot hold a board against a crowd.
- `showcase/replays/old/splitter-vs-v1-default-s20261012.replay`. The counterexample.
  The splitter ends with 22 dragons and 116 total length, and loses, because its longest
  dragon is 7 and v1's single survivor is 16. This is the old scoring rule in one
  picture, and it is the trap the next version walks into.

---

## 5. v2: multiply (22–23 September, first upload)

**What it was.** v1's mover with three population rules, each adopted after its own
experiment:

1. **Split whenever the team is under the cap of 64.** Reproduction against no
   reproduction: 78.3% of games won against 34.2% on reserved maps.
2. **Stop splitting at round 450** so the last 50 rounds grow dragons instead of
   dividing them: 90.0% against 79.2%, and 33–7 against the splitter.
3. **Split at length 4 into two dragons of length 2**, the smallest legal split.
   Thresholds 4, 6, 10 and 12 scored 28–8, 26–10, 11–25 and 8–28.

The confirmation was 386 wins against 317 of 432 across the pool, and 117–27 directly
against the previous build. On eight brand-new generated maps it won 124–4.

**What else was tested and failed at this stage.**

- **Looking three steps ahead for traps:** +5.0 pp with an interval of −2.5 to +15.8;
  every net extra win came from one map (Arena), and a related "pockets" map went 6–18.
- **Emergency two-step sprints** out of danger: 1,885 sprints, none fatal, no gain
  (−0.8 pp).
- **A quarter of the team held back as growers:** 74–70, not better than chance.
- **Last-resort portal jumps:** 131–109 and encouraging, then 53.1% on replication.
- **Persistent terrain memory with portal routing:** 70 wins, 2 draws, 72 losses against
  v2. Default went from 36–12 to 48–0 while Queen of Spades went from 33–15 to 18–29.

The pattern that repeats for the rest of the project appears here first: a mechanism
can work exactly as designed and still not win more games.

**How it did live.** v2 ran on the ladder from 22 to 24 September. A review of 71 games
found 32 wins and 39 losses. **31 of the 39 losses reached round 500 and were lost on
the longest dragon, by a median of 4 segments.** The team was eating and splitting more
than its opponents and losing about 101 of its own dragons per game against their 44.

**Matches to show.**

- `showcase/replays/old/v2-vs-v1-schooltime-s20261012.replay`. v2 splits on round 0,
  splits 61 times in the first 100 rounds, has 25 dragons at round 100 and eliminates v1
  at round 113.
- `showcase/replays/old/v2-vs-v1-default-s20261012.replay`. The weakness. v2 finishes
  with 29 dragons and 94 total length. Its longest dragon is 3 or 4 for 400 rounds and
  reaches 10 only after splitting stops. v1's one surviving dragon is 16, so **v1 wins**.
- Live, Big Empty, match 146956: we finished with 697 total length against 475 and lost,
  because our longest dragon was 34 and theirs was 59.

---

## 6. v3: learn to move from better players (24 September)

**What it was.** v2's population rules with a new mover. For every legal step a dragon
computes 24 hand-built numbers (things like nearby food, open space and how close other
heads are) and a **linear model with 25 parameters** turns them into a score. The model
was trained to imitate strong teams: 68,099 decisions sampled from 60 high-rated ladder
games (12 battles, split by whole battle into train, development and test sets).

**What was tested.** Three movers with the same inputs: a hand-written heuristic, the
linear model and a small neural network (16 hidden units, 417 parameters).

| Mover | Agreement with the strong teams' moves | Screen against v2 (88 games) |
|---|---|---|
| Heuristic | not applicable | 63–25 |
| Linear | 58.1% | 67–21 |
| Neural network | 59.3% | 63–25 |

**What worked.** The linear model. Confirmation was 126–50 against v2 and 445 against
393 of 528 across three opponents. On 16 generated layouts it scored 210 wins, 32 draws
and 14 losses. Three days later a feature ablation found this small model to be the most
valuable single component of the whole bot (removing it cost more than removing the food
term).

**What did not.** The neural network imitated slightly better and played no better. The
"mature grower" roles tested alongside it (400 against 393 of 528) were not adopted.

**Status.** Frozen and packaged, never uploaded on its own; it went live inside v4.

**Matches to show.**

- `showcase/replays/old/v2-vs-v3-trophy-s20261012.replay`. Both sides use the same split
  rules. v3 has 35 dragons to 11 at round 100 and 64 to 9 at round 300. The only
  difference is where each dragon steps.
- `showcase/replays/old/v3-vs-v2-trophy-s20261012.replay`. Same map, sides swapped. v3
  ends with 42 dragons and 143 total length against 9 dragons and 46, and **loses 9 to
  10 on the longest dragon**. Better movement did not touch the weakness that was
  costing live games.

---

## 7. v4 and v5: teach the swarm to cooperate (24–25 September)

The live review of v2 changed the question from "how do we get more dragons" to "how do
we turn many dragons into one long one". The top of the ladder was already doing it.

**Matches to show (other teams, late September).** These are worth showing before our own
attempts because they define the target.

- SSS on Slithery Fight, game 687878
  ([battle](https://game.battlecode.au/visualiser?match=687878)): its eventual king is
  54 long at round 400 and 93 at the end. Of the 39 pearls it eats late, 35 come from its
  own team's corpses. It wins 93 to 19 on longest with barely half the opponent's total
  length (172 against 343).
- Cutlery on Schooltime, game 797338
  ([battle 797334](https://game.battlecode.au/visualiser?match=797334)): one dragon grows
  from 15 at round 400 to 43 at the finish; 17 of those 28 pearls are from its own
  teammates' bodies.
- 3.14159265 on Slithery Fight, game 797661
  ([battle 797659](https://game.battlecode.au/visualiser?match=797659)): wins 71 to 34 on
  longest with 177 total length against 296 and 23 dragons against 54.

### v4-additive (uploaded 24 September)

**What it was.** v3 plus two cooperative mechanisms:

- **Late feeding.** Near the end, a small dragon next to a longer teammate outputs
  nothing, dies, and leaves its pearls for the longer one.
- **Sonar beacon.** The longest dragon broadcasts its position and approximate length in
  a 32-bit message with a small checksum; late in the game teammates that hear it walk
  toward it.

**What was tested.** Each piece alone, then together, in small screens.

**What worked.** The plumbing. Beacons were sent and received (1,125 pings in one test,
385 reaching a teammate) and kings did eat pearls from fed teammates.

**What did not.** Strength. The combined package scored **8–8 against v3** and 8–0
against v2. It was uploaded as an improvement over the live v2, with the explicit note
that it had not been shown to beat v3. Also rejected here: friendly-head filters (fewer
friendly deaths, 1.1 pp fewer wins), a quarter-team grower schedule (3–5), and emergency
portal jumps (160 jumps into unseen exits, 62 dead the same round).

### v5 (never released)

**What it was.** v4 with strategy wrappers layered on top: a scout that crosses a portal
to reach rich food, and a sparse "king" chosen at round 400.

**What was tested.** Eleven maps, both sides, three opponents, and seven follow-up ideas.

**What worked.** In isolation, the scout: in two games on one map its line of dragons
collected 451 of the team's 473 pearls and made 126 of its 133 splits.

**What did not.** Everything, against a real opponent. v5 scored 15 of 22 against v4,
14 of 22 against v3 and **5 of 22 against "nicked"**, a strong public bot that became our
main sparring partner. All seven follow-ups failed: portal memory with a pocket explorer
(3/22 against nicked), a local trap guard (3/22), remembered spawn economy (1/22), a
map-specific opening route (5/22), a hard guard around visible heads (4/22), exploration
scoring (5/22) and a split brake on large maps (5/22).

The lesson was structural. Each wrapper overrode the mover in some situation, the
overrides fought each other, and results were not even consistent between opponents.
Stacking rules on v3 had run out.

---

## 8. v6: one brain instead of a stack of rules (25–26 September)

**What it was.** A rewrite of how a dragon chooses a step. Each dragon keeps a private
**memory of the world** (terrain, portals, where food appears). For each legal step it
runs **one bounded search** over that remembered map and produces a single score that
combines food, open space, enemy and friendly heads, portal routes and the v3 model's
opinion. Splitting, king protection and feeding stayed as explicit rules on top.

**What was tested, and the bug that nearly sank it.** The first screens looked strong:
17 of 22 against v5 and 12 of 22 against nicked. Then two almost identical variants gave
different results on a map neither should have affected. The cause was the search budget:
it was measured in **wall-clock time on the test machine**, which is much faster than the
judge's CPU meter. Locally the search finished; on the judge it would not.

With a clock calibrated to the judge, the same bot scored **2 of 22, 1 of 22 and 0 of
22**. In one profiled game the time cutoff fired on 16,940 of 19,461 turns: the first
candidate step was eating nearly the whole budget and the others got nothing.

**What worked.**

- **Sharing the budget fairly across the legal steps** brought it back to 16, 17 and 12
  of 22 under the honest clock.
- **A split-floor fix.** A rule that refilled low populations was letting protected
  kings split at length 4; kings were built and immediately cut in half.
- The frozen v6 then scored **21 of 22 against v4, 21 of 22 against v3, 16 of 22 against
  nicked v34 and 8 of 22 against the newer nicked v44**, peaking at 81.9 million of the
  100 million CPU points.

**v6.1** added four things on the same core: a **portal book** and a **hub book** (the
bot recognises a known map from the geometry it sees and then knows where portals lead
and where the rich food is), **aggression** (small dragons may trade head-on with enemy
heads and hunt bigger targets) and **exploration goals** (head for unseen or stale
areas). Together: 16 of 22 against v6, 22 of 22 against v3, 18 of 22 against nicked v34.

**What did not.** A scout allowed to try unknown portals, a pull toward post-portal food,
fixed-size searches without a time cutoff (over the CPU limit on the largest map) and two
escape-check variants.

**Matches to show.**

- `showcase/replays/old/v6-vs-v3-schooltime-s20261012.replay`. The size of the jump. v6
  ends with 581 total length against 35 and a longest dragon of 49 against 12. At round
  200 it already holds a 33-long dragon while keeping 56 dragons alive. In the last 100
  rounds 48 of its small dragons feed the king.

---

## 9. v7 and v7-base: the C++ port, and a tuning win that was not real (26–27 September)

**What it was.** v6.1 rewritten in C++, decision for decision. The port matched Python's
iteration order, tie-breaks and floating-point order so that both would pick the same
move from the same position.

**What was tested.**

- **Parity.** 295,997 turns against the splitter and 185,095 against the hunter, on all
  11 maps and both sides, with **zero mismatched moves**.
- **Cost.** About 7 million CPU points per turn against Python's 80 million.
- **Spending the saved budget.** A larger search, portal-aware path distances, both
  together, and a beam search scored 8, 10, 6 and 8 of 22 against the plain port.
  Fourteen times more headroom bought nothing.
- **Automatic tuning.** An evolutionary optimiser (CMA-ES) tuned 21 parameters. Its best
  candidate won 14 of 22 against nicked v44, where the untuned port won 9. It was frozen
  as **v7**.

**The reversal.** That same day the organisers' toolkit (unswbc 1.1.0) began giving every
match its own pearl-spawn seed. Until then, every local "game" on a map had been the
same game. Replayed on three seeds:

| Bot | vs nicked v44 (66) | vs v6 (66) | Head to head (66) |
|---|---|---|---|
| Tuned v7 | 29 | 42 | 30 |
| Untuned v7-base | 32 | 43 | 36 |

The tuned bot had learned one particular sequence of pearl spawns. **v7-base**, the plain
port, was uploaded on 27 September and went 53–37 in its first live games, taking the
rating from 1500 to about 1575.

**What the ablation showed.** With seeds now meaningful, 18 feature groups were removed
one at a time over 4,560 games. Removing the v3 learned model hurt most, then food, then
spawn anticipation, then hubs. Removing the trap and "defend" terms **helped** on the
main pool, then did not hold up on other opponents (252 against 244 of 360, with Queen
of Spades falling from 15 wins to 8). Nothing was removed.

**Operations.** This is also when the test machine blue-screened twice and the compiler
crashed, each time with two heavy jobs stacked. The fixes were a machine-wide lock (one
heavy job at a time, at most 12 workers), a build cache that stopped recompiling every
bot in every worker, and, once Windows' memory test flagged bad regions, removing a RAM
overclock.

There is nothing to show on screen for the port itself: v7-base and v6 play the same
moves. That is the point of it.

---

## 10. v8 experiments and v9: tuning that held up (27–28 September)

**The prompt.** New public builds of nicked (v75, then "lab") beat v7-base 33 and 32 of
40 on the current maps. On Prisoners Dilemma, nicked collected 59 pearls in the first 100
rounds to our 8.

**v8 was a family of switches, not a release.** Tested: scouting portals by how long ago
they were last seen (kept), trap weights that depend on map type (not kept), Voronoi-style
territory targeting (not kept) and sharing food-hub locations by sonar (hurt at this
stage; it returns later as v10o).

**What v9 was.** v7-base with **16 parameters re-tuned** by a better-instrumented
optimiser (CMA-ES with learning-rate adaptation, three training opponents, original and
perturbed maps, and the distribution's mean tested as a candidate each generation), plus
the portal-age scouting switch. v9 is the mean of generation 5.

**What was tested.** A held-out comparison against v7-base on opponents and seeds the
optimiser never saw: **153 wins against 124 of 270**. On the ten maps the ladder was then
using, 99 against 77 of 180.

**What worked.** Tuning, once the evaluation was honest: several seeds, several opponents,
and a held-out check before believing anything.

**What did not.** Running longer. Later generations drifted; an average of generations 8
to 14 scored 153 against 153. Tuning was stopped and generation 5 kept.

**How it did live.** Uploaded 28 September. Rating 1579 to 1626; 66 of 128 games (52%).

**Matches to show.** `showcase/replays/old/v9-vs-v7-base-trophy-s20261012.replay` (v9
finishes with 139 total length against 15 and a longest dragon of 33 against 10) and the
same map with sides swapped (v9 eliminates v7-base at round 417). One seed; the evidence
is the 270-game comparison.

---

## 11. v10: make a king (28–29 September)

**The prompt.** v9's live losses looked like v2's, one level up: more total length than
the opponent, shorter longest dragon.

**What it was.** v9 plus two changes to the end-game:

- **King beacon.** The longest dragon announces itself by sonar so teammates out of
  sight know where the king is.
- **Big-dragon feeding.** Previously only the smallest dragons fed. Now larger workers
  also give themselves to the king late in the game.

**What was tested.**

| Variant on v9 | Wins of 360 |
|---|---|
| v9 | 210 |
| King beacon | 218 |
| **Beacon and big feeding** | **237** |
| Dead-end penalty | 213 |
| All three | 228 |

Held-out validation: 207 against 198 of 270.

**What did not work.** Every attempt to reduce the swarm's own death rate: a minimum
amount of room before splitting (229 and 242 against 247), a gentle dead-end penalty
(234), a parent telling its child about a dead end by sonar (247, no change) and that
combined with the room rule (221). Newborn deaths looked wasteful in replays and turned
out to be the price of a productive economy.

**How it did live.** Uploaded around 29 September. A review of 155 games from this period
found 79 wins and 76 losses.

**Matches to show.**

- `showcase/replays/old/v10-vs-v9-schooltime-s20261012.replay` and
  `showcase/replays/old/v9-vs-v10-schooltime-s20261012.replay`. A controlled
  demonstration. The two games are **identical for 400 rounds** (same dragon counts and
  lengths at every 100-round mark) because v10 changes only the ending. Then they
  diverge: on side A, v10's king finishes at 50 where v9's finished at 45; on side B,
  36 where v9's finished at 29.
- Live success, Default against Oxbridge Rejects, game 647761
  ([battle](https://game.battlecode.au/visualiser?match=647761)): we win 40 to 31 on
  longest; our king eats 34 pearls from teammates that fed it after round 400.
- Live failures, Slithery Fight against CookAgent, games 563874 and 557811
  ([battle 563873](https://game.battlecode.au/visualiser?match=563873),
  [battle 557809](https://game.battlecode.au/visualiser?match=557809)): 266 total length
  against 161 and a loss, 21 to 51 on longest; then 262 against 207 and a loss, 20 to 40.
  Feeding existed; it was too little and too late.
- Live near miss, Schooltime against codih, game 572261
  ([battle](https://game.battlecode.au/visualiser?match=572261)): lost 22 to 23 on
  longest with 273 total length against 150.

---

## 12. v10h: know the map (29–30 September), and the two learning projects that failed

**What it was.** v10 plus:

- **Map completion.** The bot already recognised known maps and knew their portals and
  food hubs. Now, once it recognises a map, it also fills in every remaining wall and
  opening from the book, so its search plans over the real geometry instead of the few
  cells it has personally seen.
- **Earlier feeding on large maps.** Feeding starts 40 rounds earlier when the map is
  big, because the walk to the king is longer.

**What was tested.** Map completion: 378 against 335 of 540 on the screen and 316
against 280 of 540 on confirmation, positive against all six opponents. The feeding
shift: 688 against 654 over two runs.

Why map completion beat every "pull harder toward the food" idea: in traces from Trophy,
the learned model's opinion differed by 10 to 30 points between two steps while the hub
pull differed by about 1, and the pull pointed in a straight line through walls. Knowing
the walls changed what the search could reach; a bigger weight on a bad direction did not.

**What did not work in these two days.** A long list, all tested on the same 540-game
panel or larger:

- Two broad parameter retunes ("v11" and "v12" at the time): 205 against 207, and 317
  and 324 against 339.
- Founder dragons anchored near the start for 80 or 150 rounds: neutral.
- A stronger pull toward far hubs: +0.044, then −0.056 on fresh seeds.
- A step-by-step gradient toward the hub or the king: neutral to bad.
- Protecting a growing dragon from length 4: 285 against 329.
- A better beacon (identity and freshness): 323 against 314, then 308 against 303.
- Checking that a fed pearl is reachable; letting much larger dragons feed (362 against
  348, then 322 against 323 on confirmation).

**R4: imitate a stronger player.** The v3 model was refitted on about 650,000 decisions
from 300 games of nicked v92, the strongest bot available. It predicted v92's moves
better than the old model (60.7% against 57.9%). In games it was **worse in every form**:
333, 326 and 291 wins against the old model's 347.

**R5: learn from our own what-ifs.** A full pipeline was built to replay a game from a
chosen decision with a different move forced, see whether the result changed, and train
a correction to the mover from those outcomes (64 inputs per move, 1,075 fully labelled
decisions from 88 games). Final-result labels were too noisy to learn from: a model
trained on deliberately shuffled labels still showed part of the "gain", so some of it
came from deviating at all, not from learning anything. In games,
the more the learned correction was allowed to override the bot, the worse it played:
**184, 234 and 263 wins against 270 of 528**. It stayed off.

Both results say the same thing about this bot at this stage: predicting a good player's
move, or the outcome of one changed move, is not the same as choosing better inside a
system built around a different search, split policy and feeding rule.

**Sprint 1 tournament (1 October).** v10h was seeded 131 of 591 teams in a best-of-seven
knockout on seven maps nobody had seen. It had a bye, beat Split and Stack 6–1 and lost
the next series to Citadel Insecurities (logged as 1–6 with a win on Stripes and a draw
on weakhold; the exact count needs checking against the bracket). In that series it lost
Maze 62 to 64 on longest and was out-eaten on Tower Defense 62 pearls to 771.

**The foodless-maps scare.** Tested locally on the seven new maps, v10h scored 58 of 168
and lost even to old weak bots. An investigation was started into why the bot had
"collapsed" on unseen maps. The real cause: the scraper had extracted the maps **with no
pearl spawners at all** (Tower Defense: 24 draws in 24 games, zero pearls eaten). With
spawners reconstructed from real games, v10h scored 82 of 168 and beat the weak bots
comfortably.

**Ladder position.** 30 September: rank 149 at 1624 of 928 teams. 1 October, 02:39 UTC:
**rank 133 at 1671**, with rank 100 at 1723.

**Matches to show.**

- `showcase/replays/old/v10-vs-v10h-schooltime-s20261012.replay`. v10h's king finishes
  at 64 against v10's 25. v10h's first feeding deaths come in rounds 300 to 399 (15 of
  them); v10's come only after round 400.

---

## 13. The rules change, and v10o (1–2 October)

On 1 October the organisers changed the game (section 2): queens decide round 500, every
dragon gets free extra steps, ratings reset to 1500 and every submission was switched
off until re-uploaded. Three things followed at once for this project:

- Everything measured before that day used the old objective and could not be assumed
  to carry over.
- The local toolkit was the old engine. A separate copy of the new engine was installed
  and six rule tests written before any new experiment was trusted.
- The live bot was a swarm-and-king machine with no idea that one of its dragons was
  special.

### v10o

**What it was.** v10h plus **sonar hub sharing**: a dragon that is at least 30 rounds old
and still knows no rich food area adopts one it hears about by sonar from a teammate. It
was designed under the old rules for one failure: on Prisoners Dilemma, founders sometimes
never saw a pearl countdown and wandered with no target.

**What was tested.** Sharing with everyone: 337 against 343, because it fixed Prisoners
Dilemma (15 to 20 wins of 36) and broke Slithery Fight (24 to 16) and Portals (21 to 17).
Newborns were being dragged away from food they were about to find. Restricting adoption
by age fixed that:

| Adopt only after age | Screen (control 333) | Confirmation of 900 (control 542) |
|---|---|---|
| 15 rounds | 331 | not run |
| 30 rounds | 340 | **563** |
| 60 rounds | 342 | 552 |

**What worked.** A small, repeatable overall gain. **What did not:** the dramatic
Prisoners Dilemma fix it was built for did not survive into the confirmation.

**How it did live.** v10o was uploaded around 00:48 UTC on 2 October as the first bot
after the reset, an old-rules bot in a new-rules game. Its first 50 games made the
problem plain. Both queens were dead at round 500 in 38 games (we won 25). Only the
opponent's queen was alive in 10 games, and **we won none of those**. Our queen survived
2 games of 50; theirs survived 11. Over its whole time on the ladder v10o won 171 of 345
games against opponents averaging 1449; the rating sat near 1445 with rank 100 at 1533.

---

## 14. v11ms and v11q: the queen stops volunteering (2 October)

**The baseline.** Under the new rules with the old bot: 200 wins of 360, our queen alive
at the end in 10 games, and a typical queen dead by round 85.

### What was tried first, and failed

The obvious plan was to treat the queen like the old king: protect her, feed her, keep
her long.

- **Queen protected and fed, king beacon off:** 148 wins against 200, with 28 queens
  alive against 10. More queens survived and many more games were lost.
- **Bigger workers to use the new free steps** (split at 7 or 11 instead of 4): 100 and
  83 wins against 216. The split-at-4 economy was still the engine of everything.
- **A wider danger zone around enemy heads:** 169 and 170 wins against 207, queens alive
  32 against 9.

### v11ms (not uploaded)

**What it was.** v10o plus one use of the new free steps: when a pearl is visible and an
extra free step reaches it, take it.

**What was tested.** 236 against 209 of 360, then a confirmation of **474 against 447 of
792**. Against v10o directly, 62 of 120.

### v11q (uploaded 2 October, about 21:04 UTC)

**What it was.** v11ms plus two things for the queen only:

- **Light queen.** The old feeding logic saw the queen as just another small dragon and,
  late in the game, had her kill herself to feed the king. The light queen never feeds
  herself to anyone, and she keeps a little distance from her own workers.
- **Escape tactics.** A three-step look-ahead that simulates her body and the reach of
  nearby heads. It keeps the normal move unless another line survives longer.

**What was tested.**

| Variant | Wins of 360 | Queens alive |
|---|---|---|
| v11ms behaviour | 223 | 13 |
| Tactics only | 218 | 19 |
| Light only | 226 | 22 |
| **Light and tactics** | **228** | **37** |
| plus a wider worker guard | 217 | 51 |
| plus extra threat margin | 204 | 14 |

The confirmation was a tie on wins, **490 against 492 of 792**, with queens alive 79
against 24. It was adopted on the direct matches: **80 of 120 against v10o** (queens
alive 20 against 2) and **73 of 120 against v11ms** (20 against 1). The test panel was
made of old-rules bots that lose their own queens, which hides the value of keeping
yours; against a bot that also keeps its queen, survival decides the game.

**What did not work after v11q** (each on 420 to 924 games):

- Letting the queen grow or be fed selectively: 269 and 270 against 268.
- A queen that runs from danger, or values food three times more: 251 and 246 against 254.
- Keeping the queen at length 6: 226 against 254, queens alive 27 against 56. A longer
  queen is a bigger target and dies more.
- **Hunting the enemy queen** (first attempt): 265 against 262, then 549 against 563 on
  confirmation. This idea comes back in v12z in a different form and works.
- Using spare free steps to travel toward food hubs: 557 against 560; workers only, 552
  against 563.
- Deeper escape search (4 or 5 steps): 251 and 249 against 256.
- Stronger keep-away from enemies: 563 against 572 with queens alive 104 against 94;
  with a wider guard, 545 with 107. Again more queens, fewer wins.

**How it did live.** In the first 82 games: 34 wins. Where only our queen survived we
won 7 of 7; where only theirs survived we won 0 of 15. Our queen was alive at the end in
18% of games against v10o's 4%. Around midnight UTC on 3 October the team was **rank 108
of 973 at 1529, with rank 100 at 1560**: the closest it ever came. Over its whole run
v11q won 533 of 1,080 games (49.4%) against opponents averaging 1521.

Astra's review of 95 of those games found 44 wins and 51 losses. Elimination was the
worst class (6 wins, 18 losses). Our queen died 81 times: 39 against walls, 32 to enemy
head-ons and 9 to our own dragons.

**Matches to show.**

- `showcase/replays/queen/v11q-vs-v11ms-schooltime-s20261012.replay`. The new rule and
  the fix in one game. Both queens sit at length 3 for 390 rounds. At **round 398 v11ms's
  queen dies by doing nothing**: its feeding logic has just handed the queen to the king.
  v11ms finishes with the longer dragon, 56 to 43, and loses, because v11q's length-3
  queen is still alive.
- Live, Schooltime, 3 October: six wins in six games, the queen ending at length 3 every
  time. Small and alive beats long and dead.
- Live weakness, Maze, games 981445 and 980023
  ([battle 981442](https://game.battlecode.au/visualiser?match=981442),
  [battle 980020](https://game.battlecode.au/visualiser?match=980020)): the queen walks
  the same corridor in both games, splits at round 11 and dies at round 13 in the same
  cell.
- Live weakness, Devil, game 973653
  ([battle 973650](https://game.battlecode.au/visualiser?match=973650)): one of our own
  workers kills our queen at round 27.
- Live weakness, the economy, in
  [battle 975838](https://game.battlecode.au/visualiser?match=975838): Tower Defense
  (3 dragons against 26 at round 100) and Trophy (6 against 29).
- Live, Autarky, game 981446 (battle 981442): 118 total length against 60 and a loss on
  longest dragon, 19 to 25.

---

## 15. v11t: fix the queen's model of the world (3 October)

**First, the maps.** A review on 3 October found that the official maps had been updated
(toolkit 1.2.9) and differed from the local copies, and that the ladder now rotated 17
maps: ten old ones and the seven from the Sprint. All later tests use the official files.
On them, v11q scored 242 of 408; with map books off, 216. The books still earned their
keep.

**What v11t was.** v11q with the queen's escape search rewritten to model the game
correctly. The first version had been built in a hurry, and a source review found it was
wrong in specific ways:

- When the queen eats, her tail does not move; the old search assumed it did.
- Threats were measured in straight lines, through walls; now they follow real paths.
- "I cannot see past here" was treated like "I know this is open"; now the two differ.
- It now counts how many separate escape lines survive, not just whether one does.
- The move the search approved is the move actually played (they could differ before).

**What was tested.** Three runs with different seeds and panels:

| Run | Games | Control wins / queens alive | Corrected search |
|---|---|---|---|
| C2 screen | 476 | 273 / 101 | **291 / 158** |
| C3 (with a worker-yield rule) | 476 | 255 / 91 | **285 / 175** |
| C5 confirmation | 1,020 | 534 / 207 | **571 / 346** |

C5's interval was +0.070 [−0.003, +0.141], just touching zero; the decision rested on
three positive runs in a row. Directly against v11q: **75 of 136, queens alive 48
against 26**. CPU cost peaked at 8.4 million points.

Four opponents built from our own lineage joined the panel here (a careful queen, a
raider that hunts queens, a growth queen, an economy bot), because the public bots did
not play the queen game at all.

**What worked.** Queen survival rose by two thirds with wins rising too, for the first
time. Every earlier survival gain had cost wins.

**What did not.**

- **v11u, a "refuge" for a crowded queen** (pull her toward open cells): 392 against 358
  of 680 on the screen, a clear +34. Then 67 of 136 against v11t directly, and 641
  against 627 of 1,122 on confirmation, +0.026 [−0.045, +0.097]. Not adopted. This is
  the cleanest example in the project of a screen that looked decisive and was not.
- **Splitting only with enough exits.** A replay audit of 674 queen deaths found 358
  against walls, 241 of them within two rounds of the queen splitting. The natural fix,
  "do not split in a tight spot", scored 377 and 382 against 402, with fewer queens
  alive. Splitting down to length 2 was protecting her; the audit had found where queens
  die, not why.
- **Fear of sprinting enemies** (assume every nearby head can sprint): 370 and 373
  against 394.
- **A trapped worker avoids dying on its own queen:** 645 against 647, queens alive 371
  against 356. Harmless and neutral; kept on the shelf (it ships in v12z).
- **Bodyguard workers** that trade with enemy heads near the queen: 381 and 379 against
  385. The situation almost never arises.

**A weakness found at freeze.** In the 136-game match against v11q, v11t scored **0 of 8
on Stripes** and 1 of 8 on Tower Defense. The next chapter is about why.

**Status.** Recommended for upload and never uploaded as far as the record shows; v11q
stayed live until v12x.

**Matches to show.**

- `showcase/replays/queen/v11t-vs-v11q-tower_defense-s20261012.replay`. v11t's queen
  finishes alive at length 8. v11q's queen dies against a wall at round 305.
- `showcase/replays/queen/v11t-vs-v11q-australia-s20261012.replay`. v11t's queen alive
  at 5; v11q's dies at round 489, eleven rounds from the end.
- `showcase/replays/queen/v11q-vs-v11t-stripes-s20261012.replay`. The weakness. v11t has
  **two dragons and a total length between 4 and 6 for 240 rounds**. Its first split is
  at round 176. v11q splits at round 38, has 25 dragons at round 200 and eliminates v11t
  at round 240.

---

## 16. v12s: one portal, one map (4–5 October)

**The diagnosis.** Twenty-four of v11t's games were chosen by fixed rules before anyone
looked at them (12 elimination losses, 6 other losses, 6 wins as controls) and replayed
with an economy tracker. On Stripes, in all four losses, **we ate between 0 and 2 pearls
in the first 120 rounds and never split**; the opponents ate 26 to 139.

Stripes is a 24 by 12 map. Only 12 of its spawners are fast, and they sit in two-wide
pockets fenced by kelp and entered through short portals. A side-by-side probe against a
passive opponent showed the first moment the two versions differ:

- **v11q's queen** walks into the pocket, eats twice and splits at round 11. Her child
  then farms a 7-cell loop inside the pocket, eating every 7 to 9 turns. v11q's workers
  ate 69 and 39 pearls in the first 120 rounds.
- **v11t's queen** walks to the pocket entrance and turns back. Her workers ate **0**.

The entrance is a **portal step**. The corrected search followed only open edges, so it
scored the step through the portal as certain death and overrode it every time. The
better queen search had removed the one move that starts the economy on that map.

**What was tested.**

- Trusting portal steps alone: 207 against 212; it changed nothing.
- Trusting portals and making the search less eager to override: Stripes went from 4 of
  24 to **16 of 24**, and other maps paid for it (Default 9 against 16, Islands 7
  against 12). Overall +1.5 pp, not adopted.
- The same but only when no enemy is in view: 199 and 219 against 230. "No enemy in
  view" is not safety; enemies arrive after the queen has committed to a corridor.
- **Queen plays as a worker for the first 40 rounds**, on every map: 230 against 221 on
  the screen, 647 against 634 on confirmation (+1.2 pp, not confirmed overall). But
  Stripes went **40 against 20 of 66**, while Queen of Spades went 31 against 44.

**What v12s was.** v11t plus "the queen plays as a worker for the first 40 rounds" **only
on maps of at most 300 cells**. In the rotation that is Stripes alone. On the other 16
maps v12s was verified to play move-for-move identically to v11t (64 of 64 games
identical). On Stripes with six fresh seeds: **53 wins against 25 of 132**.

**Also tested these two days and rejected.** Path-aware distance for exploration goals
alone (+3.7 pp on the screen, +0.6 pp on confirmation, 659 against 652 of 1,122);
path-aware hub distance; and **starting the walk to the king earlier for distant
feeders**. That last one came from a solid diagnosis: across 160 "more material but
shorter king" losses, 44.5 of 66 segments of worker length were still more than 12 cells
from the king at round 480. The fix scored +2.9 pp [+0.5, +5.6] on the screen and
+0.4 pp [−1.2, +2.0] on confirmation. The problem is real; leaving up to 60 rounds
earlier does not solve it.

**Status.** Frozen, never uploaded; it was folded into v12x the same day.

**Match to show.** Live, after the fix went up inside v12x: Stripes against Tony S (1633),
game 1162940 ([battle 1162937](https://game.battlecode.au/visualiser?match=1162937)).
First split at round 37, 9 dragons to 3 at round 100, win by elimination at round 119
with the queen alive.

---

## 17. v12x: why the dragons would not leave home (5 October)

**The diagnosis.** On weakhold, v11t won **1 of 48 games against the nicked family**.
Replays showed our dragons spending 92% of rounds 30 to 199 in the empty zones where
they start. Nicked threaded a maze to the fast spawners in the centre by about round 53.

Six plausible fixes did nothing (no trap penalty, path-aware goals, a stronger pull to
unseen cells, no exploration goal at all, a dead-end look-ahead, searching through
unknown edges). So a debug build printed the score of every candidate step, term by term.
With no food in reach:

- the **learned v3 model** contributed 70 to 106 points, differing by about 15 between
  steps;
- exploration contributed less than 1 point;
- progress toward the exploration goal contributed at most 10.

The most valuable component of the bot, the move ranker trained on 24 September, was
deciding every food-less step, and its taste was for staying in open, familiar ground.
Exploration was being outvoted fifteen to one.

**What v12x was.** v11t plus three switches:

1. **Exploration multiplier.** When a step's search finds no food and no hub, its
   progress toward the exploration goal counts 30 times more.
2. **Path-aware goal distance.** That progress is measured along a real path through
   remembered terrain (unknown edges assumed open), not in a straight line through walls.
3. **v12s's small-map queen rule.**

Share of time our dragons spent in the centre of weakhold in the probe (one game from
each side): 0.08 and 0.09 before; 0.42 and 0.44 with a ten-times multiplier and path
distance; **0.62 and 0.49 at thirty times**. Nicked: 0.68.

**What was tested.** Screen: 238 against 213 of 408 (+6.2 pp). Confirmation on untouched
seeds: **684 against 631 of 1,122, +4.7 pp [+0.6, +8.9]**, and 60 of 102 against v11t
directly. By map: Tower Defense 52 against 28, weakhold 45 against 24; slightly down on
Australia (38 against 42), Autarky (35 against 39) and Prisoners Dilemma (26 against 30).
CPU cost 12.1 million points.

**How it did live.** Uploaded 5 October (10:04 local time; the first battle with the new
bot is at 14:24 UTC). Over the next two days: **415 of 772 games (54%) against opponents
averaging 1567, and the rating went from 1512 to 1601.** Tower Defense was won 81% of
the time (30 of 37), Maze and Schooltime 67%. weakhold, close to unwinnable before,
finished at 47% (18 of 38).

**What the live games showed next.** How games were decided, wins against losses:

| How the game ended | Won | Lost |
|---|---|---|
| Elimination | 120 | 101 |
| Only our queen alive | 81 | 0 |
| **Only their queen alive** | 0 | **111** |
| Both queens alive | 35 | 48 |
| Both queens dead | 179 | 97 |

In the first 532 of those games, **117 of the 244 losses had our queen killed by an
enemy head-on**. In 75 of those the
rammer had paid for extra steps: a small dragon of length 2 or 3 giving up a segment to
reach her. A check of the queen's last move before each ram found that in 74 cases she
had stayed outside every visible enemy's free reach, as designed, and was killed by a
paid sprint anyway. Only 8 times did she step avoidably into reach. The corrected search
was doing its job; the ladder had found the gap around it.

**What did not work against it** (each on 476 to 1,224 games):

- Assuming enemies can sprint, in three forms: −1.3 pp, −1.8 pp, and limited to small
  heads **−6.6 pp [−11.6, −2.0]**. Marking more cells as forbidden collapses the queen's
  options; she dies sooner.
- Bodyguards (+0.0) and workers that intercept rammers near the queen (+0.0 and −2.0).
- Halving or quartering the ranker's weight everywhere: +1.3 pp and −3.2 pp.
- Keeping a long starting dragon whole instead of splitting it at round 0, aimed at
  Prisoners Dilemma where opponents were eating 38 pearls a game from our own fast
  column against our 9: +0.2 pp, better on two maps and worse on two.
- Exempting the queen from the new exploration: −1.8 pp.
- Paying a segment for a two-step queen escape, alone: +1.7 pp [−0.9, +4.4]. With the
  trapped-worker rule: +1.6 pp [−1.6, +4.7]. Small, positive every time, never
  significant.

**Matches to show.**

- `showcase/replays/queen/v11t-vs-v12x-weakhold-s20261012.replay`. v11t has 4 dragons
  and total length 8 at round 100, and 5 dragons and 10 at round 400. v12x has 13
  dragons at round 100 and 27 at round 400.
- Live, weakhold against aisakastrats, game 1157721
  ([battle 1157718](https://game.battlecode.au/visualiser?match=1157718)). Our queen
  dies in a dead end at round 9. The team has 2 dragons at round 100, then 8, 18 and 29
  at rounds 200, 300 and 400 while the opponent shrinks from 4 to 1. Win by elimination
  around round 413. A dead queen does not matter if nobody is left to out-score you.
- Live, Tower Defense against meowest (1743), game 1233668
  ([battle](https://game.battlecode.au/visualiser?match=1233668)): 25 dragons against 2
  at round 100; win by elimination around round 312.
- **Live weakness, Autarky against Oswald, game 1152241**
  ([battle 1152239](https://game.battlecode.au/visualiser?match=1152239)). The single
  best illustration of the new game. We lead all game: 36 dragons to 12 at round 200. At
  **round 250 a length-5 enemy takes three steps, one of them paid, and rams our queen**.
  We go on to 56 dragons and 185 total length at round 400 and feed 84 dragons into a
  38-long king. They finish with two dragons and 28 total length. **They win**, because
  one of the two is their queen. A second game against the same team, 1151142
  ([battle 1151138](https://game.battlecode.au/visualiser?match=1151138)), shows it
  again: 125 total length against 17, queen rammed at round 85, lost.
- Live weakness, Prisoners Dilemma against Imagine Winning, game 1158437
  ([battle 1158434](https://game.battlecode.au/visualiser?match=1158434)). We start with
  21 total length and have 7 at round 100 while they have 39; one dragon left at round
  200 against 31; eliminated around round 348.

---

## 18. v12z: do unto others (6–7 October, last upload)

**The idea.** Every defence against sprint rams had failed. A sparring opponent had been
built to reproduce the ladder's behaviour locally: v12x with one extra rule, workers
sprint into a visible enemy queen. That opponent **beat v12x 39 games to 29**. The
attack was stronger than the bot it was attacking, so it was tested as our own feature.

**What v12z was.** v12x plus three rules:

1. **Sprint-ram hunting.** A worker that can reach a visible enemy queen's head this
   turn, using its free steps plus **at most one paid step**, rams her. Both die; a
   worker of length 2 or 3 is traded for the game's deciding piece.
2. **Paid queen flight.** A queen of length 3 or more may pay one segment for a two-step
   escape to a cell that small enemies cannot reach this turn and that has at least two
   exits.
3. **A trapped worker spares the queen.** A worker with no legal move rams an adjacent
   enemy head if there is one; otherwise it dies anywhere except on our queen.

**What was tested.**

| Run | Games | Control | Candidate | Change |
|---|---|---|---|---|
| D21 screen, 1 paid step | 544 | 283 | 305 | +4.0 pp [+0.6, +7.4] |
| D21, 2 or 3 paid steps | 544 | 283 | 297 | +2.6 pp |
| D22 confirmation, rule 1 only | 1,224 | 671 | 717 | +3.8 pp [+1.6, +5.9] |
| **D22 confirmation, all three rules** | 1,224 | 671 | **741** | **+5.7 pp [+2.4, +9.1]** |

With all three rules our queen was alive at the end of 445 games against 363, and the
opponent's in 129 against 211. Australia went 53 against 37 and Autarky 50 against 35,
the two worst live maps. Maze (45 against 51) and Schooltime (42 against 45) slipped.
One paid step was better than two or three: beyond one, the rammers cost more than they
kill. CPU cost 12.4 million points.

The direct match against v12x was not part of the original tests. It was played for this
writeup on four fresh seeds, 17 maps, both sides: **v12z won 91 of 136, with queens
alive 65 against 22** (`showcase/games-h2h-v12z.json`). It was weakest on Stripes and
Trophy (3 of 8 each).

**Was it really uploaded?** The ladder shows a new submission starting at about 23:10 UTC
on 7 October (rating swings per battle jump, as they do after every upload). Its
behaviour identifies it. In 150 games from the v12x period our dragons never paid for a
step. In a sample of 100 games after the upload, they paid for steps in 62 games, the
queen fled with a paid step 64 times, and **we rammed the enemy queen 43 times (25 with
a paid step) against 35 rams on ours**. In the v12x sample it was 29 rams by us against
54 on ours. Games where only our queen survived went from 10% of games to 19 of 100;
games where only theirs survived from 14% to 6 of 100.

**How it did live.** This is the sober part. The rating jumped to 1763 within three
hours and touched **1807**, then fell back as the matchmaking found stronger opponents:
45% of games won on 8 October against opponents averaging 1665. From the upload to
12 October the bot won **948 of 1,995 games (47.5%) against opponents averaging 1632**,
and the rating finished at **1604**, where v12x had left it. By the usual Elo arithmetic
that record is worth about 1615, against about 1590 for v12x's record: a real but small
step, far smaller than the local +5.7 pp suggested.

Two things were moving underneath it:

- **The field.** The rating needed for rank 100 was 1560 on 3 October and 1813 on
  12 October.
- **The maps.** By 11 and 12 October, 25 of the 70 sampled games were on 13 maps the bot
  had never seen (Athena, Atlantis, Caution, Detention, Ezam, Hive, Maelstrom, Metro,
  Ouroboros, Thermopylae, Trolley Problem, its "Buffed" variant, and Whale Song). The
  map books that carried v10h mean nothing there. In the sample the bot won 12 of 25 on
  new maps and 51 of 75 on known ones; small numbers, same direction.

**Matches to show.**

- `showcase/replays/queen/v12z-vs-v12x-australia-s20261012.replay`. At **round 172 a
  length-3 v12z worker takes two steps, one paid, and rams v12x's queen.** v12x ends
  with the longer dragon (32 to 20) and loses to a queen of length 4.
- `showcase/replays/queen/v12z-vs-v12x-autarky-s20261012.replay`. v12z's queen sits at
  length 2 all game. v12x's queen is rammed at round 346. v12x finishes with 93 total
  length against 59 and a longest dragon of 17 against 8, and loses. This is the Oswald
  game from the other side.
- **Live, Australia against linux-container (1702), game 1395660**
  ([battle 1395659](https://game.battlecode.au/visualiser?match=1395659)), minutes
  after the upload. Their length-3 dragon sprints into our queen at round 244. At
  **round 343 our length-4 worker sprints into theirs.** With both queens dead the old
  rule applies, and we win 26 to 24 on longest dragon while holding 121 total length
  against 356.
- **Live, Ouroboros against Um_nik da real goat (1797), game 1812278**
  ([battle](https://game.battlecode.au/visualiser?match=1812278)). A map the bot had
  never seen, against an opponent that sprints 50 times per hundred rounds. Our queen is
  rammed at round 182. Their queen grows to length 36. At **round 458 a length-9 worker
  of ours pays one step and rams her.** We win on longest dragon, 102 to 54, with 211
  total length against 616.
- Live, Australia against No Idea, game 1400680
  ([battle 1400678](https://game.battlecode.au/visualiser?match=1400678)): ram at round
  157, then our queen grows to 13 and the king to 54.
- Live, Autarky against zzz3nith was here (1645), game 1403145
  ([battle 1403141](https://game.battlecode.au/visualiser?match=1403141)): the last move
  of the game is a paid ram on their length-10 queen, the final dragon they had.
- **Live weakness that remains, Autarky against the meowl, game 1816214**
  ([battle 1816211](https://game.battlecode.au/visualiser?match=1816211)), 12 October.
  56 dragons to 4 at round 400; 119 total length to 23 at the end; longest 41 to 7. Lost.
  Our queen was rammed by a paid sprint at round 214 and theirs was never caught. v12z
  learned to throw the punch; it never learned to slip one.
- `showcase/replays/queen/v12x-vs-v12z-tower_defense-s20261012.replay`. A reminder that
  the newer bot does not win every game: v12x out-breeds v12z here (32 dragons to 10 at
  round 400) and wins with its queen alive at 8. On this one showcase seed v12z won only
  4 of 12; over four other seeds, 91 of 136.

---

## 19. What never worked

Grouped by idea, across the whole project. Each line was a controlled test; details and
run folders are in the two logs.

| Idea | Forms tried | Typical result |
|---|---|---|
| **Make dragons more careful** | Trap look-ahead, friendly-head filters, hard guards, dead-end penalties, minimum room to split, wider threat zones, keep-away, refuge, split-exit rule, sprint-aware threats | Fewer deaths of the kind targeted; equal or fewer wins. −6.6 pp at worst |
| **Protect or grow the special dragon early** | Early kings, protect from length 4, queen protected and fed, queen kept at length 6 | 285 against 329; 148 against 200; queens alive 27 against 56 |
| **Fewer, bigger dragons** | Split at 6 to 12, growers, split brakes on big maps | Lost heavily every time (100 and 83 against 216) |
| **Pull harder** | Stronger hub pull, per-step gradients to hub or king, hotspot seeking | A first positive that reversed, or congestion |
| **Spend spare CPU** | Bigger search, beam search, deeper queen search | 6 to 10 of 22 against the plain port; deeper queen search slightly worse |
| **Retune everything** | Three broad CMA-ES campaigns after v9 | Gains on easy opponents only, or losses |
| **Learn a better mover** | Neural ranker (v3), refit on a stronger teacher (R4), counterfactual correction (R5) | Better imitation, worse or much worse play |
| **Fix the late game harder** | Better beacons, reachability checks, larger feeders, earlier departure | Mechanism moved, wins did not |
| **Bodyguards and escorts** | Workers trade near the queen; workers intercept rammers | Neutral: the trigger almost never fires, or costs what it saves |
| **Portals as emergency exits** | Last-resort jumps, emergency portal wrappers | 62 of 160 jumpers dead the same round |

What did work is a much shorter list: splitting small and often (v2), a tiny learned
ranker (v3), one unified search (v6), honest multi-seed tuning once (v9), feeding a king
(v10), knowing the map (v10h), not sacrificing the queen (v11q), modelling her escapes
correctly (v11t), letting exploration outvote the ranker when there is no food (v12x) and
trading a worker for the enemy queen (v12z).

---

## 20. How the testing went wrong, and what fixed it

The method that every late result relies on:

- **Paired games.** Candidate and control play the same map, side, seed and opponent, so
  the difference between them is the only thing that varies.
- **A screen, then a confirmation on untouched seeds.** A candidate needs both, and a
  practical gain of about +2 pp, to be adopted.
- **A mixed panel.** Up to twelve opponents: several builds of the public bot "nicked",
  other public bots, our own older versions, and specialists built from our own code to
  play styles the public bots do not (queen hunters, sprinters). Third-party bots were
  used only as opponents; no code was taken from them.
- **Switches.** Every feature sits behind an off-by-default switch, and each new build
  with its switch off is checked to play identically to the frozen control before the
  switch is tested.
- **Frozen versions.** Every release is a hashed folder and a verified zip.

It was built up from mistakes:

| What went wrong | When | What it cost | The fix |
|---|---|---|---|
| Duplicate maps counted twice | 22 Sep | 96 games excluded after the fact | Map identity by content |
| Search budget in wall-clock time | 25 Sep | A 0/22 bot measured as 12/22 | Clock calibrated to the judge |
| Every local game on a map was the same game | until 26 Sep | A tuned bot chosen on one spawn sequence | Per-match seeds; several seeds per test |
| Two heavy jobs at once, unstable RAM | 28 Sep | Three blue screens, lost runs | One job at a time, 12 workers, no overclock |
| Seven new maps extracted with no food | 1 Oct | A day chasing a "collapse" that was not there | Fixed the scraper; rebuilt spawners from real games |
| Local maps out of date | 1–3 Oct | Two days of queen-era tests on old and reconstructed maps | Official files, hashed |
| Panel of bots that all lose their queens | 2–5 Oct | Queen survival undervalued; no opponent sprinted | Queen-aware specialists, then a sprinter |
| Believing a screen | throughout | Refuge +34, goal path +3.7 pp, feed travel +2.9 pp all vanished | Nothing is adopted without the second run |

The last row is the one to dwell on. From 3 October onward, seven screens showed a gain
of 2 pp or more. Three survived confirmation (the corrected queen search, exploration,
sprint rams). Four did not (refuge, goal path, feed travel, queen-early on every map).

---

## 21. The ladder, start to finish

| When | Live bot | Rating | Rank | Rating at rank 100 |
|---|---|---|---|---|
| 27 Sep | v7-base | 1500 to ~1575 | | |
| 28 Sep | v9 | 1579 to 1626 | | |
| 30 Sep | v10h | 1624 | 149 of 928 | ~1700 |
| 1 Oct, 02:39 UTC | v10h | 1671 | 133 | 1723 |
| 1 Oct | Rules change, ratings reset to 1500 | | | |
| 2 Oct | v10o | ~1445 | | 1533 |
| 3 Oct, ~00:00 UTC | v11q | 1529 | **108 of 973** | 1560 |
| 3 Oct, later | v11q | 1553 | 115 | 1598 |
| 5 Oct | v12x uploaded | ~1520 | | |
| 7 Oct | v12x | ~1600 | | |
| 8 Oct | v12z, first hours | 1763, peak 1807 | | |
| 9–10 Oct | v12z | 1628 to 1652 | | |
| 12 Oct | v12z | **1604** | **153 of 1,001** | 1813 |

Live record by version, ranked five-game battles only:

| Live bot | Games won | Share | Average opponent |
|---|---|---|---|
| v10o | 171 of 345 | 49.6% | 1449 |
| v11q | 533 of 1,080 | 49.4% | 1521 |
| v12x | 472 of 895 | 52.7% | 1572 |
| v12z | 948 of 1,995 | 47.5% | 1632 |

A team's rating settles where it wins about half its games, so these shares say less
than the opponent column: each version held its own against a stronger field than the
last. On 12 October the top team stood at 2616 and every team in the top ten was
written in C++.

**The honest summary.** The bot improved at every step by its own measurements and
finished about where it had been a week earlier relative to everyone else. From 2 to
12 October the rating needed for rank 100 rose by about 27 points a day; the bot's rose
by about 16.

---

## 22. What was left on the table

Problems that were diagnosed and not solved:

- **Dodging a sprint ram.** Half of live losses. Fear-based masks fail. The untested idea
  is to score a handful of specific enemy replies separately instead of forbidding every
  reachable cell.
- **Prisoners Dilemma's home column.** Opponents eat from our fast spawners; we do not
  hold them.
- **Late-game transport.** Two thirds of surplus worker length is too far from the king
  to arrive by round 500.
- **Maps with no book.** A third of games by the end. The bot's best single feature
  under the old rules was knowing the map.
- **A panel that looks like the ladder.** Local gains of 4 to 6 pp became much smaller
  live. The sparring opponents were public bots and our own relatives; the top teams'
  behaviour was only ever seen in replays.

---

## 23. Showcase reel

One suggested running order, each a single game that carries its chapter.

| # | Shows | Match | The moment |
|---|---|---|---|
| 1 | Why one snake loses | `old/v1-vs-splitter-trophy` | 22 dragons close in; v1's last dies at round 175 |
| 2 | The longest-dragon rule | `old/v2-vs-v1-default` | 29 dragons lose to one dragon of 16 |
| 3 | Better moves, same flaw | `old/v3-vs-v2-trophy` | 42 dragons, 143 length, lose 9 to 10 |
| 4 | What the best teams did | SSS, [687878](https://game.battlecode.au/visualiser?match=687878) | King grows 54 to 93 on teammates' pearls |
| 5 | One brain | `old/v6-vs-v3-schooltime` | 581 total length against 35 |
| 6 | Making a king | `old/v10-vs-v9-schooltime` and its mirror | Identical to round 400, then 50 against 45 |
| 7 | Feeding too late | [battle 563873](https://game.battlecode.au/visualiser?match=563873), Slithery Fight | 266 length loses to 161; longest 21 to 51 |
| 8 | The queen rule | `queen/v11q-vs-v11ms-schooltime` | Round 398: a queen feeds herself to her king |
| 9 | A better search breaks a map | `queen/v11q-vs-v11t-stripes` | Two dragons for 240 rounds |
| 10 | Leaving home | `queen/v11t-vs-v12x-weakhold`; live [1157718](https://game.battlecode.au/visualiser?match=1157718) | 27 dragons against 5; queen dead at round 9 and a win anyway |
| 11 | **The ram, received** | Live [1152239](https://game.battlecode.au/visualiser?match=1152239), Autarky | Round 250; 108 length loses to 28 |
| 12 | **The ram, returned** | Live [1395659](https://game.battlecode.au/visualiser?match=1395659), Australia | Round 244 theirs, round 343 ours |
| 13 | Against a big name | Live [1812278](https://game.battlecode.au/visualiser?match=1812278), Ouroboros | Round 458: a length-9 worker takes a length-36 queen |
| 14 | Where it ended | Live [1816211](https://game.battlecode.au/visualiser?match=1816211), Autarky | 119 length loses to 23 on 12 October |

Local files are under `showcase/replays/` with the suffix `-s20261012.replay`.

---

## 24. Sources

- Experiment log, v7 to v12z: `FEATURE_EXPERIMENT.md`.
- Audited history to 3 October (Astra): `PROJECT_HISTORY.md`, `docs/project-history/`.
- Research on other teams: `TOP_100_RESEARCH.md`, `TOP_5_STRATEGIC_ANALYSIS_2026-09-30.md`,
  `TOP_TEAMS_SCOUTING.md`, `COMPETITOR_RESEARCH.md`, `LIVE_GAME_REVIEW_2026-10-03.md`.
- Diagnostics: `results/next-steps-20261004/DIAGNOSTIC_FINDINGS.md`,
  `results/live-review-20261005/REVIEW.md`, `results/strategy-review-20261006/`.
- Frozen bots: `versions/` (each with `FROZEN.txt`) and `battlebot-*.zip`.
- For this writeup: `showcase/` (scripts, game summaries, replays),
  `results/final_ladder_battles.json` (950 battles, 30 September to 12 October),
  `results/final_leaderboard_team590.json`, `results/live-review-final/` (100 games after
  the last upload).

**Limits of this account.** Live games are attributed to a version by upload time, since
the site stopped reporting submission ids on 28 September; v12z's identity rests on its
behaviour in replays, not on a hash. Ranks other than those in the table were not
recorded. The Sprint 1 series score needs checking. Figures for v1 to v6 come from
Astra's archive and were measured on an older engine in which repeated games were not
independent.
