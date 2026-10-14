# Clean v3 + feeding + sonar experiment

Question: was the earlier combined bot's weak showing caused by changing its
split schedule, rather than by feeding or sonar? The new `additive` bot is a
snapshot of frozen v3 with a thin wrapper. It calls v3's original `turn` for
the split/move decision. The only exceptions are the previously tested
late-game local no-action feeding predicate and the previously tested sonar
beacon plus route override for short dragons after round 450. There is no
grower role or earlier split cutoff. The existing experimental `old_route`
keeps that grower change.

Predeclared screen: four familiar round-limit maps (Big Empty, Default,
Schooltime, stronghold), seed 44001, both sides, one in-process worker.
`additive` and `old_route` each face unchanged v3 for eight matched games;
then `additive` faces `old_route` directly for eight games. All bot/map/source
hashes are frozen in the run plan, and saved replays allow split/action and
feeding audits. The matched v3 pool estimates whether removing the grower
change helps. The direct pairing is a consistency check, not a replacement
for the matched comparison.

This is exploratory, not a promotion gate: four familiar maps and one seed
cannot establish ladder strength. A candidate needs fresh maps/opponents and
a judge CPU-budget check before any v4 freeze. The live bot and frozen v3 are
not changed, and no website submission is made.

## Result (2026-09-24)

Frozen run: `results/20260924-172250-v4-additive-9c22dc/`. All 24 matches
completed without a match error. In the eight matched games versus v3,
`additive` went 5-3 and `old_route` went 4-4. Directly against `old_route`,
`additive` went 5-3. The matched advantage of additive over old route was
+12.5 percentage points, but its map-cluster 95% interval was -25 to +50
points; with four familiar maps and one seed this does not establish an
improvement. Additive swept Schooltime and split its other three v3 maps;
old route swept Big Empty and Schooltime but lost both sides on Default and
stronghold.

Replay events confirm additive was not an inert copy of v3. In its eight
v3 games it sent 10,068 sonar pings; 5,203 hit allies, 4,357 hit enemies,
and 508 missed. It also had three deliberate no-action deaths after round
465, consistent with the local feeding predicate. The old route bot had
eight such deaths in its corresponding v3 games. Sonar packets are public;
the large enemy-hit count is a meaningful information-leak risk against
opponents that decode our packet. These event counts verify activation,
not that either mechanism caused the wins.

Decision: keep the clean additive snapshot as an experimental candidate,
but do not promote it to `versions/v4` or the live bot. Its small positive
screen is encouraging enough for a fresh-seed/map and stronger-opponent
follow-up; it is not yet a validated ladder improvement.
