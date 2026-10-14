# Trap follow-up with a gaming-friendly compute limit

The previous trap variant gained six net validation wins, all accounted for
by Arena. This follow-up asks whether that signal repeats and transfers to
nearby layouts. The bot itself is unchanged; the sprint experiment is parked.

## Resource policy

One Python process plays matches sequentially at Windows Below Normal
priority. Wasmtime's Rayon pool is limited to one thread before engine
initialization. No GPU or model training is used. Between matches, the runner
checks available system memory and its own resident memory. It stops and
preserves partial results if available memory falls below 4 GiB or its own
resident size exceeds 1 GiB. This does not cap Civ VI or alter another app's
priority, affinity, settings, firmware, or clocks.

These controls reduce competition for resources; they are not a guarantee of
zero stuttering, zero transient memory spikes, or hardware/driver stability.
The memory check happens between games, not continuously during a match.

At the initial resource check this PC reported 8 physical cores, 16 logical
CPUs, 31.9 GiB RAM, and 24.0 GiB available; Civ VI was not running then.
That snapshot is not a guarantee of memory available after starting a game.

## Fixed design

- Frozen trap versus frozen round-450 baseline, directly head-to-head.
- Twelve new bot seeds, 6000-6011, both sides: 24 games per map, 120 total.
- Original Arena: repeat the prior positive signal.
- Original Schooltime: retain a map on which the earlier aggregate regressed.
- Arena baffles: add symmetric short interior wall segments.
- Arena pockets: add symmetric partial enclosures without disconnected food.
- Arena slow-food: same geometry and starts, twice the pearl countdown range.
- No policy or threshold changes based on results, and no opponent-pool search.

Generated maps preserve the original starting dragons and spawnable cells.
They are distinct by semantic signature, have connected resource cells, and
the actual engine accepts them without correction notices. Official maps
are also checked for engine notices, but may intentionally contain separate
regions: Schooltime is not subjected to the synthetic connectivity constraint.

The Arena-derived layouts are a related family, NOT independent samples of
all competition maps. Per-map side-paired results are exploratory and do not
justify broad promotion by themselves. More seeds on these maps do not fix
the lack of diverse map families.

## Reproduce

```powershell
.venv\Scripts\python.exe -B -m bcsim.trap_followup --seeds 12
```

Implementation: `bcsim/trap_followup.py`; map tests:
`tests/test_trap_followup.py`. Outputs include frozen bots and maps, a plan,
code/engine hashes, incrementally saved games, resource samples, per-map
comparisons, and a summary in a fresh `results/*-trap-followup-*/` directory.
No changes are made to the live bot, older snapshots, or the training corpus.

## Completed results

Saved in `results/20260922-175423-trap-followup-a1e642/`:

| Map | Trap wins-losses | Match score |
|---|---:|---:|
| Arena | 19-5 | 79.2% |
| Schooltime | 17-7 | 70.8% |
| Arena baffles | 16-8 | 66.7% |
| Arena pockets | 6-18 | 25.0% |
| Arena slow food | 12-12 | 50.0% |

Overall: 70-50, 58.3%, but the map dependence is more important than that
aggregate. The original Arena signal replicated; the policy failed badly on
partial enclosures and gained nothing with slower food. Do not promote it
globally. These are diagnostic leads, not proof of the failure mechanism.

All 120 matches completed without errors or code-hash changes in 242 seconds.
Observed worker RSS rose from about 103 to 730 MiB; minimum sampled available
RAM was 21.6 GiB. Long subsequent runs will recycle worker processes in bounded
batches rather than assume this growth plateaus. The 63-test suite passed.
