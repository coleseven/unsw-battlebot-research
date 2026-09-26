# Late growth and grower-role experiment

Baseline: frozen `versions/v2`, hash `9f29ab4138b51d26` (split at length 4,
stop splitting at round 450). Its preceding validation had zero elimination
losses, but 46 round-limit length losses. The new experiment targets that
weakness without changing movement, food routing, split size, or population cap.

## Policies fixed before screening

| Policy | Reproduction stops |
|---|---|
| Control v2 | Everyone at 450 |
| stop425 | Everyone at 425 |
| stop400 | Everyone at 400 |
| stop350 | Everyone at 350 |
| quarter350 | Roughly 1/4 at 350; others at 475 |
| quarter400 | Roughly 1/4 at 400; others at 475 |

Roles use a deterministic integer hash of dragon ID and team. They consume
no movement RNG and require no shared state or sonar. Every newborn calculates
its own role. This is NOT a globally elected champion, nor a guarantee that
one-quarter of the survivors will be growers. Growth-role dragons can die.

Tests cover cutoff boundaries, unit limits, approximate role balance across
teams and ID parities, unchanged RNG initialization, and exact real-engine
equivalence to v2 when configured with its original cutoff.

## Protocol

Run: `results/20260923-084317-growers-5ac330/`.

- Screen: six policies, nine official maps, two new seeds (15000-15001), both
  sides, directly against frozen v2: 216 games.
- Select the best new policy by screen score; ties prefer stop425, stop400,
  stop350, quarter350, then quarter400. It must exceed 50% to advance.
- Validate exactly one unchanged policy with seeds 16000-16007. Candidate
  and control each face v2, splitter, and hunter across nine maps/both sides:
  864 games.
- Require a 95% map-cluster lower bound above 50% against v2 and a paired
  pool-gain lower bound above zero. Replay and judge-runtime checks follow.

The maps and scripted opponents are familiar; this is a fresh-seed test, not
unseen-map or ladder evidence. No active-bot change, submission, or commit is
part of this experiment. Frozen v2 stays available regardless of the result.

## Result: not promoted

The screen selected `quarter350` (21 wins, 15 losses; 58.33%), hash
`eba788af5f0d162c`. The unchanged policy did not pass fresh-seed validation:

- Direct v2: 74 wins, 70 losses (51.39%); map-cluster 95% interval
  **40.97-60.42%**.
- Paired opponent pool: 347/432 wins versus control's 343/432. Gain
  **0.93 percentage points**, map-cluster 95% interval **-2.78 to +4.17 pp**.
- Both policies had 11 elimination losses. Candidate length losses fell from
  78 to 74, but that small difference is not persuasive evidence of improvement.
- All 163 matched control games ending before the first changed round had
  identical recorded outcomes, lengths, deaths, and duration.

An independent complete Queen of Spades judge-sandbox game reached round 500
with 2,513 candidate decisions, no runtime errors, a maximum 28,102,296 CPU
points, and 21,561,344 bytes memory. This verifies execution, not strength.
Replay fidelity checks are recorded separately in the run directory.

All 864 validation replays passed metadata/action checks; **3,911,558**
candidate actions matched exactly with exception fallback disabled. The
2,367 splits at round 450 or later are expected: non-growers reproduce until
475. Another 24 cold/warm candidate probes passed with a maximum
**31,338,426 CPU points**, 21,561,344 bytes, and zero failures.

Interpretation: the small screening advantage did not replicate. Randomly
assigning growers is not yet a demonstrated solution to the length endgame.
Do not combine it with other improvements on the assumption that it helps.

```powershell
.venv\Scripts\python.exe -B -m bcsim.growers --workers 6
.venv\Scripts\python.exe -B -m bcsim.growers --validate results/20260923-084317-growers-5ac330 --workers 6
.venv\Scripts\python.exe -B -m bcsim.growers --audit results/20260923-084317-growers-5ac330 --workers 6
.venv\Scripts\python.exe -B -m bcsim.growers --budget results/20260923-084317-growers-5ac330
```
