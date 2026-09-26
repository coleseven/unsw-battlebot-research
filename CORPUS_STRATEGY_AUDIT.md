# Strategy patterns in the downloaded public games

Descriptive audit: `results/20260922-234132-corpus-strategy-de8cf0/summary.md`.
Full event-derived data, recorded battle metadata, and replay hashes are in
the adjacent `audit.json`. No networking, private source access, or training
was used. The raw replay/dataset corpus is unchanged.

Selection: twelve complete downloaded battles, ordered by the lower of the
two recorded Elo values, with distinct submission pairs. Sixty games cover
nine submissions from seven teams. The lower-rated player in each selected
battle had a recorded rating between 1,926 and 2,004. These are historical
scraper snapshots, NOT verified current ladder ratings.

Observed patterns:

- Length 4 was the most common split length for every sampled submission.
- Two-segment offspring were the most common child size for every submission.
  One submission always used two-segment offspring in these games.
- Sprint shares ranged from 0% to 1.82% of move actions, depending on the
  submission. This favors investigating selective uses before pervasive sprints.
- Every submission made some splits from round 450 onward. This does not tell
  us whether it had other dedicated growers, local exceptions, or a later cutoff.

These observations support experiments, not imitation by assumption. The
sample is selected, opponents/policies repeat, and we do not know their code
or which other decisions made them strong. Frequent actions are not proven
causes of wins. None of these games is counted in our bot's win-rate tests.

The reproduction-size experiment was specified and launched independently
before these aggregate patterns were available. It includes length-4 splitting
as a controlled candidate, not a post-validation modification.

An earlier report at `20260922-233553-corpus-strategy-3d71b9` has the same
displayed action-frequency table but incorrectly summed per-game maxima in
unused aggregate JSON fields. The later report above corrects peak population
and maximum sprint-length aggregation. The earlier artifact is retained and
superseded, not additional evidence.

Reproduce a new descriptive report:

```powershell
.venv\Scripts\python.exe -B -m bcsim.corpus_strategy
```
