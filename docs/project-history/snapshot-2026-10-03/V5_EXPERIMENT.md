# V5 strategy experiments — 2026-09-24

V5 is experimental. The live `mybot` was not changed or submitted. Each local
experiment freezes the bot copies, map copies, hashes, replays, and comparisons
under `results/`. The source-of-truth implementations live in `framework/v5_*.py`
and `experiments/v5/brain.py`.

## Evaluation caveat

The `seed` passed to `bcsim.match.play` seeds bot RNG, **not the map engine**.
For these deterministic bots, repeated seeds produced identical replay events.
Consequently, duplicate seed runs are not independent evidence, and the usual
seed-block bootstrap confidence intervals in the generated summaries must not
be read as ladder uncertainty. Counts below use one outcome per distinct
map/side/opponent condition where repeats were identical. Fresh opponents,
real map variation, and website games remain necessary.

From now on, any bot-change evaluation includes both sides of all eleven
distinct official maps, even when a change targets one map. The shared list
and coverage check live in `bcsim/official_suite.py`. The default full-change
runner uses eight workers on this host with bounded RAM checks. A 16-worker
portal experiment exhausted available RAM with nicked and was completed by
resuming only its missing games at six workers. Small map-only probes remain
diagnostics, not promotion evidence.

## Deferred tuning work

After the nicked v34 mechanism experiments, run a controlled parameter sweep
of the current v5 split cutoff, minimum split length, king election/start,
Trauma hotspot pull, and 24-feature linear movement weights. Screen cheaply,
then require all eleven maps on both sides against frozen v5, additive v4 and
nicked v34 before accepting a setting. Earlier king-start and trap experiments
show that a parameter can help one matchup while harming another; do not tune
against a single map or duplicate deterministic seeds.

## Full 11-map screen of the latest v5 combination

Frozen run: `results/20260924-233609-full-change-bb86e5/`. The unchanged
Trauma scout + round-400 king played all eleven maps on both sides against
additive v4, frozen v3, and the stronger audited `nicked` bot: 66 games, eight
workers, 335 seconds, no match errors, maximum recorded worker RSS 287 MiB.
Aggregate results were 15–7 versus additive, 14–8 versus v3, and 5–17 versus
nicked. This is an exploratory full-map baseline, not a release gate.

Each cell below is v5 W-L on that map's two sides. The full generated report is
`results/20260924-233609-full-change-bb86e5/map_matrix.md`.

| Map | Additive v4 | v3 | nicked |
|---|---:|---:|---:|
| Default Small | 2–0 | 2–0 | 0–2 |
| Trophy | 0–2 | 1–1 | 0–2 |
| Queen Of Spades | 1–1 | 1–1 | 0–2 |
| Default | 2–0 | 2–0 | 0–2 |
| Devil | 1–1 | 0–2 | 0–2 |
| stronghold | 0–2 | 1–1 | 2–0 |
| Trauma | 2–0 | 2–0 | 0–2 |
| Schooltime | 2–0 | 1–1 | 0–2 |
| Big Empty | 1–1 | 2–0 | 0–2 |
| Arena | 2–0 | 1–1 | 1–1 |
| Colosseum | 2–0 | 1–1 | 2–0 |

The full map view reverses some tempting interpretations from the small
screens: v5 beats additive on Trauma but loses there to nicked, while it beats
nicked on stronghold but loses there to additive. Trophy and Devil need
specific attention. Do not promote based on the aggregate 15–7 or 14–8 alone.

## Portal-memory and sparse pocket-explorer ablation (25 Sep)

Claude's `V5_VS_NICKED_BRIEF.md` made nicked v34 the first target and identified
portals, economy and survival as likely bottlenecks. We tested a sparse
round-0–120 explorer on the 48×24 maps plus per-dragon bounded routing through
portal pairs actually observed (`framework/v5_portal_push.py`), without copying
third-party code. The action-only probe at
`results/20260924-235440-v5-portal-probe-b63cb1/behavior.json` confirmed a
real action change on both sides of Trauma, Default and Queen. Default pearls
rose markedly in that tiny probe, but none of those six nicked games flipped.

The required full 11-map screen is
`results/20260924-235840-full-change-a01a46/`. It scored **10–12 versus the
frozen scout+king v5, 13–9 versus additive, and 3–19 versus nicked**. Trauma
was 0–2 against each of the three opponents. This policy is **rejected**;
extra pearl collection in a diagnostic is not evidence of a better match bot.
The first 49 games were saved when a 16-worker attempt hit the 4 GiB available-
RAM guard. A six-worker resume played only the 17 missing jobs; the completed
66-game log, summary and per-map matrix are under `completed/` and
`map_matrix.md`. No game errors occurred. The default future full-suite setting
is back to the observed memory-safe eight workers, not the old one-worker
throttle.

## Local trap-guard ablation (25 Sep)

We applied the existing local trap chooser before hotspot routing, leaving
the rest of scout+king v5 unchanged (`TRAP_GUARD`). A four-game action probe
against nicked on Default Small and Trauma confirmed that the policy really
changed actions on both sides, but lost all four games. The full 11-map,
both-sides comparison is `results/20260925-001343-full-change-a0dc40/`:
**12–10 versus frozen scout+king v5, 12–10 versus additive v4, and 3–19 versus
nicked v34**. The scout+king control had previously scored 5–17 versus
nicked, so this is **not promoted**. It improved the direct v5 matchup on
Queen of Spades, Devil, Trauma and Schooltime, but went 0–2 versus v5 on
Trophy, Big Empty and Arena. Against nicked it split Stronghold, won both
Colosseum sides and lost both sides of the other nine maps. The first 44
games were preserved when the run was interrupted; a six-worker resume
played the 22 missing games, producing a complete error-free 66-game log,
summary and map matrix under `completed/` and `map_matrix.md`.

## Remembered pearl-spawn economy ablation (25 Sep)

An opt-in per-dragon memory of visible spawn countdowns and recent pearls
(`framework/v5_economy.py`) routed through known ordinary edges when no pearl
was reachable within three local steps. Its 96-node search avoided assuming
that hidden occupancy or portal exits were safe. A six-game action probe on
Default, Schooltime and Big Empty changed action streams on both sides of all
three maps, with no runtime errors, but lost all six nicked games. Big Empty
finished with more total length than frozen v5 on both sides; Schooltime
finished with much less.

The required full 11-map comparison is
`results/20260925-113359-full-change-053960/`: **11–11 versus scout+king v5,
8–14 versus additive v4, and 1–21 versus nicked v34**, 66 games, no match
errors. It lost both nicked sides on every map except a 1–1 Colosseum split.
This policy is **rejected**. It remains isolated behind `ECONOMY = True` in
the variant builder; neither the frozen baseline nor live bot changed. The
per-map matrix and replays are in that result directory.

## Queen opening audit and map-gated founder route (25 Sep)

The frozen v5-vs-nicked Queen replays show **no founder deaths before round
50**. Our team has two dragons and total length 6 on side A, or three dragons
and total length 8 on side B, while nicked reaches 7 and 8 dragons
respectively. The mechanism is poor
early pearl acquisition, not an opening wipeout. The map has two 50-round
spawn clusters near x=13–18/y=1–3 and x=6–11/y=31–33; most other spawn
tiles have a 1000-round gap. The original founders traverse the low-yield
perimeter and middle corridors rather than holding these clusters.

An opt-in, exact-start-gated founder route (`framework/v5_queen_opening.py`)
sent the four known Queen founders toward separate clusters. The first probe
reached the target region but immediately left it; a revised candidate kept
safe moves inside a cluster when possible. Both probes changed action streams
on both sides yet left our team at two dragons and total length 6 at round
50 on both sides, and lost both nicked games. The revised candidate's
required full 11-map comparison is
`results/20260925-114947-full-change-08d46d/`: **10–12 versus frozen v5,
14–8 versus additive v4, 5–17 versus nicked v34**, no game errors. Queen
itself was 0–2 against all three controls. The route is **rejected** and
stays off in all promoted variants. The opening failure likely needs
dynamic spawn timing/contest and safe loitering, not just a coordinate pull.

## Visible-head hard guard ablation (25 Sep)

An opt-in final-step guard (`framework/v5_head_guard.py`) retained the selected
move unless it entered a cell a visible friendly or enemy head could reach
next, and a legal alternative existed. This isolates Claude's P3 head-risk
proposal from the rejected trap penalty. A four-game action probe on Default
Small and Trauma changed decisions on all four sides and won one Default Small
side against nicked, while losing both Trauma sides.

The full eleven-map comparison is
`results/20260925-115956-full-change-cb0cd7/`: **12–10 versus frozen v5,
14–8 versus additive v4, 4–18 versus nicked v34**, 66 games and no match
errors. Versus nicked it improved Default Small from 0–2 to 1–1, but reduced
Stronghold from 2–0 to 1–1 and Arena from 1–1 to 0–2. Trauma was still 0–2.
The global guard is **rejected**. Its opt-in switch remains off; neither the
frozen baseline nor live bot was changed.

## Round 2 exploration-score ablation (25 Sep)

Claude's Round 2 brief identified unseen-area exploration, avoidance of a
dragon's own recent trail, and early teammate fan-out as missing terms in the
v3 action objective. `framework/v5_exploration.py` combines those terms with
the learned 24-feature v3 score while keeping immediate moves legal and the
terrain search to at most 48 remembered cells per candidate. The new scorer
replaces the base mover's choice in an opt-in v5 variant; it is not a fixed
target override. The Default/Queen probe changed actual action streams on
both sides. At round 200, Default side B grew from total length 31 to 37,
but side A fell from 64 to 38; Queen showed no useful growth gain.

The required full eleven-map comparison is
`results/20260925-122111-full-change-0499e5/`: **7–15 versus frozen v5,
12–10 versus additive v4, 5–17 versus nicked v34**, 66 games without match
errors. It beat nicked on both Default Small sides and one Trauma side, but
lost both Stronghold sides and the Arena side that baseline v5 could win.
Default and Queen remained 0–2. This fixed-weight combination is **not
promoted**; its losses against frozen v5 warrant separating/tuning the
exploration, revisit, and fan-out terms before any future release test.

## Round 2 big-board split-brake ablation (25 Sep)

An independent opt-in policy (`framework/v5_population.py`) suppressed
ordinary v3 splits only on boards with at least 2,000 tiles: at population
48+, or after round 300 while population was at least 24. The original v3
split eligibility remained the legality gate. A four-game Big Empty and
Schooltime probe changed actions on both sides but lost all four nicked
games. At round 450, Big Empty total length fell from 503 to 266 on side A
and from 455 to 249 on side B; Schooltime fell from 171 to 92 and from 137
to 92. The team had dwindled to the 24-dragon floor in each probe game.

The full eleven-map comparison is
`results/20260925-123353-full-change-4c85a0/`: **12–10 versus frozen v5,
12–10 versus additive v4, 5–17 versus nicked v34**, 66 games without match
errors. Schooltime and Big Empty were 0–2 against both additive and nicked.
This fixed schedule is **rejected**. Its opt-in switch remains off; the
deferred split-parameter sweep should account for retained total length and
food production, not merely count fewer deaths or more long individuals.

## Results so far

| Ablation | Distinct local outcomes | Interpretation |
|---|---:|---|
| Naive all-dragon hotspot seeking | 2–6 vs additive v4 (4 maps × 2 sides) | Rejected: excessive congestion and kelp deaths. |
| No-split hotspot collector | 3–5 vs additive v4 | Rejected: scout grows to 9 then dies in a one-way corridor. |
| Split-and-export Trauma scout | 2–0 on Trauma vs additive v4; 1–1 mirror on Stronghold | Promising map-specific access, not a general promotion. |
| Sparse early king | 7–5 vs additive v4 (6 maps × 2 sides) | Mixed: 0–2 on Stronghold and Trophy. Election can still choose a crowded dragon that dies shortly afterward. |
| Early local feeding + rendezvous | 6–6 vs frozen early-king; 9–3 vs additive v4 | No isolated gain over early king. Twelve deliberate feed actions across the 12 direct-control games; too sparse to explain the broader wins. |
| Remove public sonar and its routing | 5–7 vs additive v4 | No evidence to drop sonar wholesale, despite the public location leak. |
| Stricter king safety package | 5–7 vs frozen early-king; 5–7 vs additive v4 | Rejected: additional crowding/exit filtering and friendly-head avoidance did not improve outcomes. |
| King protection from round 350 | 7–5 vs frozen round-400 king; 5–7 vs additive v4; 5–5 vs round 400 on five held-out maps | Matchup- and map-dependent, not a general improvement. Big Empty and Trauma beat round 400 twice each; Schooltime lost twice. |
| Trauma scout + round-400 king | 2–2 vs additive v4 (Trauma 2–0, Stronghold 0–2); 0–2 vs nicked on Trauma | No demonstrated synergy. Against nicked, its complete event streams were identical to the scout-only bot on both sides: the king policy had no behavioral effect in those games. |

The Trauma scout reaches the fast pearl tiles near round 24. In the two
additive-v4 games it held those tiles for hundreds of turns, splitting there
126 and 133 times and collecting 451 and 473 pearls. Those are two side
outcomes, not eight independent seed wins. Against frozen v3 it won both
Trauma sides; against the stronger `sparring/nicked` bot it lost both, as did
additive v4. In the nicked match our candidate collected more pearls but
finished with a much shorter longest dragon. The limiting problem is conversion
of pearl access into surviving length, not just access.

The feed replay audit used `bcsim/v5_feed_audit.py` to reconstruct each action:
the new `should_feed` predicate was true 12 times and produced 12 suicide
actions. Final kings did consume friendly-corpse pearls, but the trace does
not establish those specific 12 deaths as the source. The neutral direct
comparison and Schooltime losses argue against promoting this change yet.

## Current work and next gate

The stricter safety variant is preserved in its frozen bot snapshot. Frozen
comparisons at `results/20260924-221605-v5-king-safety-0c6649/` show 5–7
against both the old early-king and additive controls. It still lost both
Stronghold and Trophy sides to additive and both Trauma sides to the old king,
so it is **not promoted**. `framework/v5_king.py` was restored to the original
election criteria afterward. Its two mechanisms were bundled; a future ablation
could isolate the friendly-head move guard from the overly restrictive election
filter. The trial's 24 games completed with no match errors, though a report
writer initially failed when it tried to create `comparison.json` twice; the
saved comparison was completed from the generated game summaries without
rerunning matches.

The round-350 candidate in `results/20260924-222647-v5-king-350-937025/`
uses that original election policy. It beat its round-400 counterpart 7–5,
but lost 5–7 to additive. Its longest dragon was only one or two segments
longer in the two Big Empty and two Trauma direct games, and four to seven
segments shorter in Schooltime. The frozen five-map holdout at
`results/20260924-223513-v5-king-350-holdout-8687c3/` was 5–5, with each
map splitting by side. Earlier protection does not pass a general promotion
gate.

The combination at `results/20260924-223816-v5-combo-809e43/` preserved the
scout's Trauma wins versus additive but did not improve Stronghold or nicked.
On nicked, the combined and scout-only event streams were byte-for-byte
equivalent in both side pairings, confirming that the king component had no
behavioral effect in those matches. The bottleneck remains reliably creating
and protecting a long king, then converting nearby friendly corpses into its
length. Next experiments should diagnose when king election never fires,
isolate late kelp/head-on losses, and test a more active but safe feeder
rendezvous. Only after these improve distinct opponents should the work move
to judge CPU/sandbox verification and a release decision.
