# Work queue

Ordered; one heavy game job at a time. Sources: TOP_100_RESEARCH.md (29 Sep),
OVERNIGHT_REVIEW_2026-09-30.md (30 Sep), FEATURE_EXPERIMENT.md for results.
Incumbent: **v10h** (`results/v10h-bot`, v10 + CPP_BOOK_MAP + CPP_FEED_SHIFT_LARGE 40).
Keep **v10g** (book map only) as a second control: the book gain is confirmed,
the feed shift is marginal.

## Done

- 30 Sep defect + tune-candidate ablate: nothing beats v10h (hubsep +0.011,
  v3portal -0.043, both -0.033, v12tune -0.091, v12gen5 -0.087 on the pool;
  both tune candidates worst vs nicked v92). No finalists, so the robustness
  check is moot for these; hubsep kept as an option for combinations.
- Item 4 implemented as CPP_KB_V2 (default off); ablate running
  (results/v12-kb2-dir.txt).

- 30 Sep kb2 confirmation: gains only vs easy opponents (strong three 55 vs
  56/180). Feed reach (reach4/6, kb2+reach4): all within noise, slightly
  negative vs v92.
- **v92 loss anatomy** (630 base games vs v92, 30 Sep runs): (a) longest-dragon
  tiebreak with equal or more total length (Autarky longest 12 vs 26, total
  86 vs 52; Big Empty 55 vs 77; Slithery 36 vs 54; Schooltime 36 vs 60): the
  feed pull W_CASH/(1+d) is ~3 points far away, drowned by v3. Testing
  CPP_KING_GRAD (per-step walking-distance pull to the feeding target).
  (b) early elimination: Prisoners Dilemma 0/42 (wiped out in 41, median
  round 221; our population never grows, v92 cycles 81 wall deaths/game),
  Default Small, Arena, Trophy. **PD opening/population is its own item.**

- 30 Sep endgame conversion: king gradient (no effect: longest unchanged);
  feed trace showed our late feeding volume is 3-10x below v92's; letting
  length <= 12 feed + king gradient 10 (sum12) raised our longest dragon vs
  v92 by ~2.5 in two runs but the win gain did not replicate (+14, then -1).

## Now

1. **CPP_SONAR_HUB full-suite ablate** (`results/v12-sonarhub-dir.txt`,
   running): sonarhub, sonarhub + W_HUB x3 vs v10m (= v10h). PD probe: 5/12
   vs v92 with it (base 0/42), pearls 50 -> 161-226 per game. Confirm on fresh
   seeds if it helps overall, then judge sandbox and an upload candidate.
2. Robustness check (originals + perturbed, same seeds) for any finalist.

## Next (structural)

4. **King protocol with identity and freshness (K1/K2)**: announcement carries
   king id and the origin round (relays keep the original age), deterministic
   election ties, invalidate contradicted locations; feeders bind to that id,
   never to "a friendly head near the beacon cell". Test king death, movement,
   relay loops, emergency-split succession. Protocol 3 (64-bit sonar) is an
   option if 32 bits are too tight (full parser incl. ECHOES).
5. **Collection-aware feeding (F1/F2)**: feed only where the recipient can
   reach the corpse pearls (ceil(L/2), on alternating cells) before the
   deadline and before enemies; recipient gets a bounded collection priority.
   Then compare a rendezvous policy with the current chase. Only then retune
   timing (F3). Food accounting must follow split lineage (bcsim/feed_trace.py).
6. **Endgame-only interventions**: identical to the incumbent until round R,
   then the change (clean comparison from the same economy). Late king
   protection belongs here, not early protection (length-4 protection: -0.185).
7. **Opening diagnosis on Trophy/Trauma/Default**: do founders reach productive
   regions, do dragons take redundant routes; change route allocation only if
   the diagnostics support it.
8. **Selective tactical lookahead (T1)** for valuable dragons (threat, emergency
   split, cheap trades on enemy kings); correct tail rule and food state; not
   the old beam made deeper.
9. Destination-aware portal scoring (remembered landing info + uncertainty),
   only if the neutral CPP_V3_PORTAL treatment shows portals matter.

10. **Our own better move ranker (self-taught, "R5")**. The v3 ranker is our
    most important term (W_V3 9 instead of 24.7: -0.175; removing it -0.36),
    but it is a 24-feature linear model fitted in the v3 era, it only sees the
    7x7 window, and imitating nicked v92's moves made us worse (R4: -0.044 at
    better imitation accuracy, 30 Sep). So learn from our own bot's outcomes,
    not from another bot's choices:
    - **States**: sampled decisions from our incumbent's games vs the strong
      panel on all 15 maps (DAgger-style: later rounds sample states the new
      ranker itself visits).
    - **Labels by counterfactual rollouts**: replay the same seeded game to
      round t (deterministic), force the dragon's move m via a wrapper bot,
      let our bot play on for K rounds (or to the end), and score each legal
      move by the outcome (dragon survival and length, team length/longest,
      game result). Engine snapshots are not needed; prefix replay is. Check
      the forced-move wrapper reproduces the original game exactly first.
    - **Features**: the 24 v3 features plus portal-destination info (with an
      unknown flag), hub/goal/king-target direction and walking distance,
      teammate heads, round phase, role (founder, king, feeder).
    - **Model**: linear first (drop-in for model.hpp), then a small MLP (<=1-2k
      params) if linear gains; C++ inference must stay well under the judge
      budget (now ~8M of 100M points).
    - **Gate**: the usual paired full-suite ablate (6 opponents, 15 maps, 3
      seeds) plus fresh-seed confirmation; promote on wins vs the strong three,
      not on label accuracy. Budget: ~10k states x 4 moves x ~1.5 s per
      rollout = about 1.5 h at 12 workers per labelling round.
    - Runs on this PC (the GTX 980 machine may not be set up): labelling
      and confirmation games are heavy jobs and go through the guard lock
      like everything else, one at a time; model fitting is small (CPU or
      this PC's GPU).

## Method changes for future tuning

- Incumbent evaluated on every generation's shared conditions (paired progress).
- Screen broadly, then spend extra seeds only on surviving candidates
  (successive-halving style); fixed development panel, separate untouched
  confirmation panel.
- Tune a feature's own few knobs after it is confirmed; modest bounds around
  the incumbent; no broad 17-dim overnight sweep; do not reuse old covariance
  after a strategy change by default.
- Promote on actual wins; aligned score, length and economy explain results.
- More opponent-family diversity (nicked builds are one family).

## Spare machine (GTX 980)

- Not assumed available (user, 30 Sep): plan all work for this PC. If it is
  set up later: replay-schema audit and model training could move there.
