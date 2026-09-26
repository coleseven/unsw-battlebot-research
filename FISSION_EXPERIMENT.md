# Reproduction-size experiment

This is independent of movement tuning. All candidates keep the original
frozen movement, cap 64, head-threat split guard, and round-450 cutoff.

The baseline splits in half at length 8. The coarse alternatives are balanced
splits at lengths 4, 6, 10, or 12, plus length-8 splitting with a two-segment
child. Earlier splitting tests coverage/turn-count advantage; small offspring
test whether preserving parent size repays a weaker newborn.

Both parent and child must retain at least two segments. The child reverses
the old tail and acts later in the same round. These are official mechanics,
not assumptions about simultaneous Snake movement.
[Official splitting rules](https://game.battlecode.au/docs/splitting)

The wrapper's length-8 balanced configuration is tested against the original
baseline in the real engine and produces identical outcomes. Thresholds,
unit caps, split sizes, and the round-450 cutoff have direct regression tests.

Experiment: `results/20260922-232921-fission-5df835/`.

- Screen: six policies including baseline, nine official maps, seeds 9000-9001,
  both sides, direct baseline opponent: 216 games.
- Select the highest scoring new policy, ties in saved mode order, provided
  its score exceeds 50%. No movement combination during this test.
- Validation: selected policy and control against baseline/splitter/hunter,
  nine maps, seeds 10000-10007, both sides: 864 games.
- Performance gate: 95% map-cluster lower bound above 50% directly against
  baseline AND paired pool-score improvement lower bound above zero.
- Replay and judge-runtime checks required before promotion.

Maps and opponents are familiar; seeds are fresh. This is local-pool evidence,
not a claim about ranked opponents. No submission is performed.

## Screen completed

| Change | Wins-losses vs baseline | Score |
|---|---:|---:|
| Split at 4 | 28-8 | 77.8% |
| Split at 6 | 26-10 | 72.2% |
| Split at 10 | 11-25 | 30.6% |
| Split at 12 | 8-28 | 22.2% |
| Length-8 split, child size 2 | 21-15 | 58.3% |

Length 4 advances unchanged, hash `9f29ab4138b51d26`. Screening is selection,
not final evidence. A separate descriptive audit of 60 already-downloaded
high-rated games also found length-4 splitting common; that is a supporting
research lead, not evidence our implementation beats those teams.

## Validation passed; frozen as versions/v2

The exact tested bot is now frozen at `versions/v2`, hash
`9f29ab4138b51d26`. `mybot`, v1, all older experiment snapshots, and the raw
training corpus remain unchanged. Nothing was submitted or committed.

| Opponent | Previous baseline W-L | Split-at-4 W-L |
|---|---:|---:|
| Round-450 baseline | 72-72 | 117-27 |
| Splitter | 109-35 | 134-10 |
| Hunter | 136-8 | 135-9 |
| Total | 317-115 (73.4%) | 386-46 (89.4%) |

Paired pool gain: **+15.97 percentage points**, 95% map-cluster interval
**[+6.71, +24.54]**. Direct baseline score: **81.25%**, map-cluster interval
**[65.97%, 94.44%]**. Both predeclared performance gates passed.

This is not uniformly better: Queen of Spades regressed from 31-17 to 27-21
across the pool, and the direct matchup there was 6-10. Hunter lost one net
game. All 46 candidate validation losses were round-limit length losses;
elimination losses fell from 43 to zero. Individual dragon deaths increased
with the much larger reproductive population; those counts are not team losses.

## New-map transfer and verification

Eight new connected, symmetric layouts vary size, kelp density, pearl density,
and pearl timing. Their four procedural families are related and contain no
portals; they do not represent the entire competition distribution. The policy
was unchanged and not tuned on their results.

Saved at `results/20260922-235151-novel-maps-db3a9c/`: **124-4 (96.875%)**
against the round-450 baseline. The approximate family-cluster 95% interval
is **[92.97%, 100%]**. Every map scored at least 81.25%; the transfer gate passed.

- Official validation: all 864 replay results/standings verified;
  **4,150,627** candidate actions reproduced exactly without exception fallback.
- New maps: all 128 replays verified; **722,699** candidate actions reproduced.
- No invalid-action deaths, recorded timeout flags, or late splits in these audits.
- Full-game judge runtime: 1,208 candidate turns, no errors, maximum
  **31,248,216 CPU points** and **21,561,344 bytes** (20.56 MiB).
- Another 24 cold/warm candidate probes, including maximum observed population,
  length and density, passed; maximum **30,961,586 points**, same memory.
- The 75-test regression suite passed. Runtime probes are not a worst-case guarantee.

Next research target: preserve one or more late-game growers without sacrificing
the early swarm's elimination pressure. Compare a few fixed earlier cutoffs and
per-dragon grower roles against v2; do not modify v2 or tune against these saved
transfer results. Earlier population/endgame experiment CLIs and tests now use
the frozen v1 movement by default, so changing the active bot cannot silently
change those historical experiment controls.

```powershell
.venv\Scripts\python.exe -B -m bcsim.fission --workers 2
.venv\Scripts\python.exe -B -m bcsim.fission --validate results/20260922-232921-fission-5df835 --workers 6
```
