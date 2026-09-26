# V4 sonar feasibility experiment

The preceding protected-grower and local-feeding screen did not improve v3.
This independent experiment asks whether sonar can supply the missing
coordination signal, not whether it is already a better ladder bot.

Sonar carries a public unsigned 32-bit packet: magic/version, team bit,
7-bit post-move x and y, 7-bit approximate sender length, and a 2-bit check.
Dragons of length at least six broadcast after round 400. `beacon` sends but
ignores packets for movement; `route` also remembers the strongest valid
teammate beacon for up to eight rounds and gives safe ordinary moves toward
its coordinate a small score bonus after round 450. Both keep the exact
grower/feeding policy from the preceding experiment. Sonar can reach an enemy
first; the packet contains no secret map or team state.

Predeclared screen: Schooltime and stronghold, one seed, both sides, one
in-process worker. Feed baseline, beacon-only, and routing each play v3 (12
games); routing also plays beacon-only (four games). Saved replays must show
beacon-only preserving the baseline match outcomes while delivering at least
one ping to a friendly dragon. Routing results are exploratory. Successful
delivery is not a v4 promotion: fresh maps, stronger opponents, replay action
audit and judge CPU checks remain required. No four-worker process-bot load
is used after the host crash.

## Screen result (2026-09-24)

Frozen run: `results/20260924-133212-v4-sonar-e451f4/`. All 16 games
completed in one in-process worker without a recorded error. Against v3,
the feed baseline went 1-3, beacon-only 1-3, and beacon-plus-routing 2-2.
Routing versus beacon-only also went 2-2. These are only four games per
comparison on two maps and one seed, not evidence of a reliable win-rate gain.

Replay events record 1,125 beacon-only pings: 385 hit a friendly dragon,
110 hit an enemy, and 630 missed. The routing bot sent 1,198 pings: 410
friendly hits, 125 enemy hits, and 663 misses. Reconstructed recipient
observations contain the packet values (for example, 42 nonempty inboxes in
the Schooltime beacon game with the candidate on side A). Packets are public:
the enemy can receive our approximate length and post-move position too.

The beacon-only control is particularly clean. In each of the four paired
games against v3, **every dragon action was identical** to the no-sonar feed
baseline, not just the final result. The action traces contained 49,034,
49,157, 30,866, and 30,597 actions respectively. This confirms sending
beacons alone does not change movement in the local harness. Routing first
changed a candidate move at round 479/450 on Schooltime (sides A/B) and
475/450 on stronghold, so the movement mechanism is active after the
predeclared round-450 threshold.

Decision: sonar delivery and the beacon-only control pass feasibility.
Routing does alter moves, but is not promoted: the tiny matched screen is
inconclusive, and feed baseline itself remains below v3. No team-safety
experiment or live-bot change is included. Next test should isolate whether
received beacons improve deliberate feeding versus simply pulling small
dragons into traffic, on fresh maps and stronger opponents, followed by
judge CPU validation before any v4 candidate is promoted.
