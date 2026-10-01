# New mover (R5): stage log

Plan: [NEW_MOVER_PLAN.md](NEW_MOVER_PLAN.md). This file is the handoff: current
stage, frozen hashes, gates passed, next action, exact run directories.

## Current stage

**M1 (identity/parity), in progress.** Next action: read the identity gate
result (`results/mover-m1-identity.json`, log `results/mover-m1-identity.log`);
then the zero-strength residual switch in C++ and per-candidate feature logging.

## M0: frozen experiment contract (30 Sep 2026, git aa2cbb5)

- Incumbent (base policy for labels and comparisons): **v10h**,
  `versions/v10h`, bot hash `f9d00cd150ff2c53` (v10 + CPP_BOOK_MAP 1 +
  CPP_FEED_SHIFT_LARGE 40; live on the ladder since 30 Sep ~21:59 UTC).
  1 Oct: sonar adoption age 30 passed confirmation -> candidate v10o
  (`versions/v10o`, hash 7623b9aa5ef6172b). If the user uploads v10o, the
  mover is rebased onto it explicitly before any labels are collected (none yet).
- Engine: unswbc 1.1.0 (seeded pearl spawns; same seed replays identically).
  Our C++ bots run in-process with BCSIM_DETERMINISTIC_V6=1, BCSIM_CPP_INPROC=1.
- Opponent panel (hashes): cpp_nicked_v92 `602ed8c414fbde08`, cpp_nicked_v75
  `1c66e312e0f142fb`, nicked_v44 `5f9efb7e03ba029b`, nicked_lab
  `902a04976020ece2` (the nicked family: one strategic family), cpp_leviathan3
  `fb5e2bc2b5915d86`, v7-base-bot `bec48091e76579a1`.
- Evaluation: all 15 ranked maps both sides (`official_suite.ranked_maps()`),
  current pool first, the other five as a guard; confirmation adds the 10
  `maps/perturbed/*_p1` layouts (25 layouts). Promotion on paired wins vs the
  strong panel (v92, v75, lab), not on label accuracy or aligned score.
- Compute: this PC only; one guarded heavy job at a time, at most 12 workers.

## M1: identity / parity

- `bcsim.match.play(..., hook=...)`: optional reply hook (None = unchanged
  play). The hook sees each bot reply after the bot produced it, so the bot's
  private state has updated normally; `bcsim/mover_teacher.py` `Force`
  rewrites only the MOVE line of one dragon at one round (other lines such as
  sonar are kept).
- Identity gate (`python -m bcsim.mover_teacher --identity`): 3 games (Portals
  v10h vs v92, Schooltime lab vs v10h, Trophy v10h vs v7-base); checks no hook
  vs pass-through hook vs forcing the chosen move (5 decisions per game, rounds
  >= 40 and >= 300) all give the identical event stream (actions, tiles,
  moves, splits, deaths, sonar; CPU points ignored), and that forcing another
  direction diverges. Status: queued behind the running confirmation.
- To do: CPP mover residual switch (off/zero = exact incumbent), 64-feature
  logging from live memory, Python/C++ feature parity fixtures.
