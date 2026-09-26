# V4 experiments — teammate-head safety on frozen v3

Started September 24 after reading the revised `COMPETITOR_RESEARCH.md`.
`versions/v3` hash `69382825b699723d` is the immutable baseline. No change to
its split policy, linear model, score function, live `mybot`, or submitted ZIP.
No competitor source is copied into our bot.

## First ablation, frozen before matches

The v3 move ranker permits a visible empty step that another friendly head
could enter. Two variants remove these destinations from v3's existing move
candidates only when an alternative remains. `guard_all` considers every
visible teammate head; `guard_later` considers heads with a higher id that have
not acted this round. Both exclude a teammate's impossible reverse move and
retain v3's choice if every candidate is threatened. The linear weights and
ordinary-move constraint remain identical to v3.

Screen on the eleven existing maps, two new bot RNG seeds, both sides against
the unchanged splitter and hunter. The same opponent/map/seed/side blocks are
played by a v3 control and both guards. Direct guard-versus-v3 games use one
seed on each side of each map; these bots are deterministic, so repeating a
seed would not create new information. Screen totals: 264 pooled plus 44 direct
games. Save all replays and fail on any error or changed source/map hash.

Advance the guard with the largest positive paired pool gain only if its direct
v3 score is at least 50%. This is an exploratory screen, not promotion. A
positive finalist must then pass fresh-opponent and new-layout comparison with
a positive map-clustered 95% lower bound, exact replay auditing, and judge
sandbox budget checks. No `versions/v4` will be frozen merely for winning the
screen. Later phases can independently test growers, body-aware escape, and
reverse split; do not blend them into this ablation.

## Sparring preparation

The `ctmes` snapshot has a custom `brain.py` but no `bc.py`; the old local
harness misclassified it as our in-process protocol. The loader now requires
both modules for that protocol. One local smoke match on Default Small ran
to round 500 without an adapter error (v3 won once); this is not a strength
estimate. Source snapshots remain git-ignored under `sparring/` and require a
separate mixed-opponent evaluation before they can guide tuning.

## Guard screen result

The frozen screen at `results/20260924-113203-v4-abbee0` completed all 308
planned games without match errors. Against splitter/hunter, both guards lost
1.14 percentage points to their paired v3 control. Directly against v3,
`guard_all` went 9-13 and `guard_later` went 13-9. Neither satisfies the
predeclared positive pooled-gain rule; neither is a v4 finalist. Guarding did
reduce recorded teammate-head deaths, but the weak pool was near saturation
(v3 won 80 of 88), and deaths alone did not predict wins. The direct games are
few and map-cluster uncertainty is large. This screen does not establish that
all teammate-risk modeling is bad; it rejects these two hard-filter variants.

## Independent grower screen, frozen before matches

The next ablation retains v3's split size, split cutoff, candidate set and
learned movement score, but allows the existing hysteretic `mature` and
`opportunity` roles to suppress splitting. These are the unchanged thresholds
from the older v2 experiment, now layered over v3 movement, not the guard.
Each dragon tracks its role on its own `Brain` instance.

Use four familiar maps (Default Small, Default, Queen of Spades, Trauma),
one bot RNG seed and both sides against pinned `ctmes` and `nicked` source
snapshots. Include a matched v3 control, plus direct grower-versus-v3 games:
48 pooled and 16 direct games. This intentionally targets the screen's weak-
opponent ceiling, but is still a small exploratory screen. An eligible grower
needs positive paired mixed-pool gain and at least 50% direct v3 score; if
both qualify, choose the higher pooled gain. Fresh layouts/opponent versions,
replay audit and sandbox budget checks remain prerequisites for freezing v4.

The first attempted mixed-opponent execution was invalid: parallel project
compilation of `ctmes` raced over its `.unswbc-build` bytecode cache on
Windows. Its partial `games.jsonl` contains an error and is excluded. The
local subprocess adapter now launches Python snapshots with an existing
`main.py` directly, without shared compilation. The screen is restarted under
a new result directory and frozen plan; no game from the invalid run counts.

## Grower screen result and next hypothesis

The restarted screen at `results/20260924-115357-v4-grower-374d2b` completed
all 64 planned games without errors. The v3 control won 5/8 against the pinned
`ctmes` bot and 0/8 against pinned `nicked`. The `mature` variant had an exact
zero paired win-score difference and 4-4 directly against v3; all 16 paired
pool games also had identical final standings and death counts. Its trigger
appears effectively inert while v3 splits at length four. The `opportunity`
variant was 5-3 directly against v3, but lost one win against `ctmes` and
finished 4/16 in the mixed pool versus v3's 5/16. Its paired difference was
-6.25 percentage points; the four-map 95% cluster interval was [-18.75, 0]
points. Neither variant passes its positive pooled-gain rule. No v4 is frozen.

Next experiment should test a grower policy that can adopt a role before the
population reaches 16, or improve v3 movement/escape against the much
stronger `nicked` snapshot. That is a new hypothesis, not a retroactive change
to this screen. A larger, varied pool and fresh maps are needed before
claiming ladder improvement. The CPU-budget fallback from the research
remains untested and should be addressed before submission.

## Phase cutoff versus reserve growers, predeclared before matches

The pinned `nicked` source stops routine splitting at round 300; v3 stops at
450. In the four-map v3-versus-nicked screen, four of eight v3 losses were
eliminations, while the other four ended with a longest-dragon deficit. This
motivates two *new* isolated policies, both retaining v3 movement and split
size: `global_300` stops all dragons splitting at 300, while `reserve_300`
stops dragons with `id % 7 == 0` at 300 and lets the rest split until 450.
The latter is deliberately coarse and can be biased by global ID allocation;
the experiment tests whether keeping a swarm around a few growers is worth
exploring, not whether this is an optimal election protocol.

Screen matched v3 control and both candidates on six familiar maps (Default
Small, Default, Queen of Spades, Trauma, Colosseum, Schooltime), both sides,
one bot seed versus pinned `ctmes` and `nicked`: 72 pooled games. Add 24 direct
candidate-versus-v3 games. Select only positive paired pool gain with at least
50% direct v3 score; highest paired gain wins, with an exact tie favoring the
smaller `reserve_300` change. This is exploratory, not promotion. Process-bot
RNG is not controlled by the harness seed, so the paired blocks match context
but not opponent random streams. Any finalist must pass fresh layouts and
opponent versions, replay auditing, and sandbox CPU checks before a v4 freeze.

Important interpretation correction made *after the plan was frozen*: the
`nicked` snapshot's `SPLIT_UNTIL = 300` constant is unused. Its live split
function enters endgame mode at round 400 and stops splitting only while the
team has at least 20 dragons (with a separate king-length condition). Recorded
replays confirm that it still splits after round 300. The ongoing 300-cutoff
screen remains an isolated policy test, but must not be described as imitating
`nicked`. A separate future test should isolate the active population-floor
rule. No thresholds in the already frozen screen are changed.

The phase screen was interrupted by a host Windows bugcheck at approximately
12:12 on September 24 while four subprocess-bot matches ran concurrently.
Only 12 of 72 pooled games were logged, with no game errors. There are no
direct games or comparison; this partial run is not selection evidence. The
event log reported bugcheck `0x50`, but it does not establish cause. Do not
restart the same four-worker load without a separate safety decision.
