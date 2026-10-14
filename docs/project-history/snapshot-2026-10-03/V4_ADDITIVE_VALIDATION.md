# Additive bot upload-readiness check

The user indicated the currently active website bot is v2, so this is a
pragmatic upload-readiness check rather than a demand for a statistically
conclusive v3 improvement. The candidate is the unchanged, frozen clean
v3+feeding+sonar bot from `20260924-172250-v4-additive-9c22dc`.

Predeclared: four maps not used in the additive screen (Devil, Trauma,
Queen of Spades, Colosseum), both sides, one worker. Compare against v3
at seeds 44002 and 44003 (16 games), then against v2 at seed 44002 (eight
games). Separately run one full game with the candidate in the judge sandbox
to measure CPU points and detect runtime errors. A winning v3 score, clear
v2 edge, no match errors, and passing sandbox would justify recommending a
user-controlled upload. This is still a small local sample, not proof of
ranked-ladder strength. No bot will be submitted automatically.

## Outcome (2026-09-24)

Frozen run: `results/20260924-174513-v4-additive-validation-d407dd/`.
All 24 in-process games completed without errors. On the four new maps,
the additive bot went 8-8 versus v3 over two seeds and both sides. It went
8-0 versus frozen v2 over one seed and both sides. The v3 result is highly
map-dependent: 4-0 on Devil, 0-4 on Colosseum, and 2-2 each on Trauma and
Queen of Spades. Thus the predeclared *winning v3 score* condition was not
met; we cannot claim an improvement over v3. The direct v2 comparison is
positive on every map, albeit still a small local sample.

The full judge-sandbox game on Devil against v3 completed to round limit
with no runtime errors or exceptions. The candidate won 75-35 total length.
Across 16,637 metered candidate turns, maximum use was 64,725,813 CPU
points (p99 41,639,586), below the 100,000,000-point limit; peak recorded
bot memory was 21,954,560 bytes. This is one full game, not a worst-case
guarantee on every map. The sandbox game and all match data are saved in
the frozen run directory.

Recommendation in light of the user's stated priority: the clean additive
bot is ready for a **user-controlled trial upload replacing v2**, because it
beat v2 8-0 in this fresh local comparison and passed a full sandbox game.
Do not describe it as stronger than v3, and do not submit automatically.
