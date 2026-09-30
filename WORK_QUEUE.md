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

1. **Defect + tune-candidate ablate** (`results/20260930-073741-ablate-f5f4ba`,
   running): hubsep, v3portal, both, v12tune, v12gen5 vs v10i (= v10h).
   Decision table per variant: current pool, guard maps, per opponent (report
   nicked v92/v75/lab separately from the easy leviathan3/v7-base), actual wins
   and paired CI. Gains mostly from leviathan3/v7-base do not count.
2. **Robustness check for finalists + control**: 15 originals + 10 perturbed
   (`maps/perturbed/*_p1`), both sides, same seeds for every bot; report
   original and perturbed deltas separately. Also replay the tune's final
   generation conditions with the frozen v10h (hard conditions vs policy drift).
   New perturbations (`_p2`) for final confirmation, not `_p1` again.
3. Confirm any winner on fresh seeds before promotion (and judge sandbox check).

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

- Audit replay schemas (public replays redact sonar and pearl timers), refresh
  the v3 linear ranker on audited data, then a small MLP; judge by held-out
  games, not imitation accuracy. CUDA 12.6-era PyTorch for Maxwell, or CPU.
