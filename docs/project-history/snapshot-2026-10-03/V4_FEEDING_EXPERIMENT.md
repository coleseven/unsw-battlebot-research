# V4 protected-grower and local-feeding experiment

## Replay audit, September 24

`bcsim/feed_trace.py` reconstructs body positions and tags each pearl-creation
event as a natural spawn or a specific dragon's corpse. It then attributes
every consumption event to its most recent creation event and identifies the
team's final longest dragon (tie: lowest id). It does not infer intent.

Six distinct round-limit wins from three top-team submissions on Default,
Schooltime, Big Empty and stronghold were audited. Their final longest
dragons' own-corpse shares of pearls eaten after round 400 were 62.5%, 78.6%,
57.6%, 100%, 74.5%, and 69.6%, respectively. The tracer reported no unknown
pearl origins, overwrites, or consumption without a moving actor in those
games. Some final kings were born after round 400, so the comparison follows
the same dragon backward, giving length zero before its birth. Three saved v3
games were also audited: its final kings ate 2, 2, and 9 pearls after 400,
finishing length 5, 4, and 12. V3 does consume some incidental own-corpse
pearls; that alone does not make a deliberate feeding policy.

The source events verify substantial late resource transfer in the leading
bots, but cannot distinguish intentional feeding from deaths caused by a
shared route or congestion. The independent tracer supports the scouting
report's mechanism, not its claim of deliberate coordination.

Reproduce the six traces with:

```
.venv\Scripts\python.exe -B -m bcsim.feed_trace data/replays/158767.replay data/replays/158771.replay data/replays/158574.replay data/replays/158763.replay data/replays/157404.replay data/replays/158769.replay
```

## Policy and screen, frozen before matches

`grower` is v3 movement and split size with a deterministic quarter of
dragon IDs stopping splitting at round 400; the rest remain at v3's 450.
The role hash is copied from our earlier v2 grower trial, where this idea did
not validate. `feed` is byte-identical except that after round 465, a length
2-3 dragon may take the engine's no-action death only when a visibly long
teammate can step straight onto its head's drop cell, at least 12 teammates
are alive, and no enemy head is visible within three cells of either head.
The predicate intentionally favors precision over activation frequency.

Use four familiar round-limit-prone maps: Default, Schooltime, stronghold,
Big Empty. One bot seed, both sides, three pairings: grower versus v3, feed
versus grower, feed versus v3. Eight games per pairing, 24 total. All bots run
in-process, strictly one worker with bounded recycling after the earlier host
crash during four concurrent third-party process-bot matches. The screen is
exploratory; a combined finalist requires >50% in all three pairings and no
errors, then fresh maps/opponents, exact replay and CPU-budget checks before
any v4 freeze. No source from competitors is copied into our bot. No live bot,
frozen v3, or submission is changed by this experiment.

## Screen result

The frozen run at `results/20260924-131752-v4-feed-48a467` completed all
24 games with no match errors, using one in-process worker. Scores were
grower 3-5 versus v3, feed 4-4 versus grower, and feed 3-5 versus v3.
The predeclared exploratory screen rule was not met; neither policy advances.
The grower swept Big Empty but lost both sides on Default and stronghold.

Across the eight feed-versus-grower games, the feed bot had seven no-action
deaths. The replay tracer found five pearls from those deaths eaten by its
*final* longest dragon (two on Default, three on stronghold); it found none
in the other games. This verifies some intended transfers actually happened,
but they did not move the match score. The predicate is too local/rare to
establish an advantage, and an arbitrary quarter-ID grower remains fragile.
The low sample and four familiar maps also preclude a broad negative claim
about coordinated feeding. Sonar-based coordination is the next separate
experiment, not a retroactive modification to this screen.
