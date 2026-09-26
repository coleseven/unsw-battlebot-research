# Newborn survival diagnostic

This is a descriptive audit of existing replays, not a split-policy experiment.
It uses the 144 frozen-v2 mirror matches in the grower validation (nine maps,
eight seeds, both sides), measuring only the `control_450` side of each game.
Artifacts: `results/20260923-084317-growers-5ac330/split-mortality-control_450/`.

- 28,044 recorded births; 26,985 children had length 2.
- 159 children died before receiving their first turn.
- 27,885 children received a first turn; 1,243 died during that turn: **4.46%**.
- Those immediate deaths comprised 380 kelp collisions, 526 other-body
  collisions, and 337 head-to-head collisions. Head trades need not be bad.
- 1,414 died during their birth round; 5,676 died before age five rounds.
- 1,835 children remained alive at game end.

The short-lifetime counts are not survival-rate estimates because the game
ending censors observation. They also do not measure the value of each birth:
children can score, fight, or reproduce before dying. In particular, 4.46%
first-turn mortality does not mean withholding those splits would improve
match score.

This narrows the immediate-child-safety opportunity. A future conservative
split guard could test only proven static traps, but its benefit must be
measured against the loss of reproductive tempo. This diagnostic alone does
not justify changing the successful split-at-4 policy.

```powershell
.venv\Scripts\python.exe -B -m bcsim.split_mortality results/20260923-084317-growers-5ac330 --workers 4
```

The command checkpoints replay analysis and refuses to overwrite its final
summary. Unit tests cover pre-turn death, first-turn death, later death,
round-age boundaries, team filtering, and living/censored children.
