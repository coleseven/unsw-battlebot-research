# Work queue

Ordered; one heavy game job at a time. Sources: TOP_100_RESEARCH.md (29 Sep),
OVERNIGHT_REVIEW_2026-09-30.md (30 Sep), FEATURE_EXPERIMENT.md for results.
Incumbent: **v10h** (`results/v10h-bot`, v10 + CPP_BOOK_MAP + CPP_FEED_SHIFT_LARGE 40).
Keep **v10g** (book map only) as a second control: the book gain is confirmed,
the feed shift is marginal.

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
