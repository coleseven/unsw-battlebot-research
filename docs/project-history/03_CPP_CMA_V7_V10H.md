# 3. C++, feature ablation and CMA-ES: v7–v10h

[Project history](../../PROJECT_HISTORY.md) · [Previous](02_V4_V6.md) · [Next: learning and rules reset](04_LEARNING_RESEARCH_RESET.md)

## Porting the verified behavior

The C++ port preserved the Python v6.1 decision path before adding new behavior. Python's PARITY mode removed wall-clock cutoffs while retaining fixed search caps. Generated C++ headers contained parameters, the frozen v3 model and map books. The implementation matched iteration order, tie-breaking, heap ordering and floating-point operation order where those affected decisions.

Parity results were **295,997 turns against splitter** and **185,095 against hunter**, all 11 maps and both sides, **zero mismatched dragons**. Four live cross-checks also produced identical games. The matching judge build stayed below **7.1M points per turn**, compared with roughly 80M for Python. This justified the port as a measured runtime improvement, not an assumed language advantage.

The initial C++ port omitted sonar: the then-current v6 logic decoded and discarded received beacons, so omitting that output did not change its action line. Later C++ king/hub protocols were separate additions.

Source: [v7 port log](snapshot-2026-10-03/V7_EXPERIMENT.md), with design in [port plan](snapshot-2026-10-03/V7_CPP_PORT_PLAN.md) and the three preserved cloud handoff documents.

## Spending the speed did not automatically improve decisions

Three switches added a point-budget meter, portal-aware path distances, and a body-aware beam. With all switches off, **297,348 further turns** matched Python. The combined larger-search/path build peaked at **23.6M** on Big Empty, safely below the hard limit. Small four-map screens looked promising against older bots.

The saved full-map results are less favorable and are important additions to the narrative:

| C++ variant | Wins /22 versus v7-base | Wins /22 versus nicked |
|---|---:|---:|
| Larger search | 8 | 17 |
| Path distances | 10 | 15 |
| Search/path combination | 6 | 17 |
| Beam | 8 | 11 |

These are old-engine single-condition comparisons, not modern multi-seed confirmation. They explain why measured CPU headroom did not immediately become a stronger release. Sources are the four `20260925-235406/235407-full-change-*` comparisons in the [run register](RUN_REGISTER.md). The main v7 log concentrated on implementation and initial screens; the archive retains both.

## First CMA-ES release and its reversal

The first full C++ tuning run, `20260926-001535-tune-79f3f9`, searched 21 parameters with population 12 on five screen maps against nicked v34 and Python v6.1. It recorded 14 generations, indexed 0–13. The selected **generation-7 c05** used `N_SEARCH=357`, `DEPTH_MAX=12`, with the new search switches off.

Its original 11-map validation won **14/22 against nicked v44**, 20/22 ctmes, 15/22 v6 and 12/22 untuned C++. Untuned C++ had won 9/22, 21/22 and 16/22 against those first three opponents. It was frozen as **v7**, hash `b033b4202f624d25`; sampled sandbox peak was 7.0M.

Then unswbc **1.1.0** introduced actual per-match pearl-spawn seeds. The harness passed its seed to the engine, and a three-seed recheck changed the recommendation:

| Bot | Nicked v44 /66 | ctmes /66 | v6 /66 | Direct matchup /66 |
|---|---:|---:|---:|---:|
| Tuned v7 | 29 | 60 | 42 | 30 |
| Untuned v7-base | 32 | 59 | 43 | 36 |

The old single-layout gain did not survive. **v7-base**, hash `bec48091e76579a1`, became the recommended upload. This is one of the clearest examples of a release recommendation being reversed by better evaluation.

The [tuning register](TUNING_REGISTER.md) also preserves shorter starts, interrupted runs and plans with no logged evaluations. A directory name containing “tune” is not evidence that a complete optimization ran.

## In-process C++ simulation

A C ABI outside the submitted bot exposed one independent handle per dragon. The local harness used it through ctypes to avoid one OS process per dragon. It was not a replacement game engine and did not change the upload package.

Compiler/flags mattered: a different native compiler changed score ties and diverged. The accepted path used the same compiler/flags as the toolkit and a guarded build signature. **198/198 configurations** matched process mode in winners, lengths, deaths and replay bytes across three opponents, 11 maps, both sides and three seeds. Python opponents required the deterministic calibrated clock for a meaningful comparison.

Measured Linux speedups were roughly **1.5–2.1× for C++ versus C++**, smaller against the expensive Python opponent. Windows compatibility and build-race repairs followed. Later scope was restricted to our compatible C++ lineage; arbitrary sparring C++ bots stayed in subprocesses.

## Feature ablation: what was actually carrying strength

The feature-efficiency program tested 18 leave-one-group-out variants. The original total-length objective disagreed with final results in **36/180** sampled games. It was replaced for that era by an “aligned” score: half result, quarter final longest share, quarter trajectory total-length margin, with wins reported separately.

The experiment distinguished a then-current ten-map ladder pool from five regression maps. Stage 1 used 15 maps, two opponents and four seeds: **4,560 games** across base and 18 variants.

| Removed group | Current-pool aligned change | Reading at that time |
|---|---:|---|
| v3 learned score | −0.355 | Most damaging removal |
| Food | −0.255 | Essential |
| Spawn anticipation | −0.123 | Essential |
| Hubs | −0.115 | Important on current pool |
| Room/trap | +0.131 | Harmful on training pool, different behavior on guard maps |
| Defend | +0.025 pool; +0.056 overall | Candidate to remove |
| Several exploration, revisit, fan-out, hunt and protection groups | Small uncertain changes | Not individually established as useful or useless |

Fresh-seed stage 2 confirmed **dropping trap and defend** on the training pool: +0.131 aligned, 161 versus 147 wins. Dropping many neutral groups together lost part of the gain; they stayed.

Held-out opponents weakened the finding: **252/360 versus 244/360**, aligned +0.040 [−0.026,+0.106], with Queen of Spades falling from 15 to eight wins in the current-pool table. The simplified B1 was not upload-worthy alone. The useful conclusion was topology- and opponent-dependence, not “remove safety everywhere.”

Source for this and subsequent feature work: [feature experiment log](snapshot-2026-10-03/FEATURE_EXPERIMENT.md).

## v8 experiments and the successful v9 tuning campaign

New public sparring builds exposed a larger gap: nicked v75 won **33/40** against v7-base on the current pool, and nicked_lab won 32/40. The v7-base live cohort was 53–37, but several maps showed an early economy stall.

Initial suspicion centered on unknown portals. The expanded portal book did not fix Prisoners Dilemma: its fast food was near the start, and nicked collected 59 pearls in the first 100 rounds while ours collected eight. Portal access and food exploitation were separate bottlenecks.

The v8 family added portal-age/scouting spread, topology-conditioned trap weights and Voronoi-like targeting. Hub sonar was implemented but hurt PD against v75 at that stage. All-off parity held for 88 games. Hidden-spawn map extracts were separated from valid test maps.

CMA tooling then gained learning-rate adaptation, an evaluated distribution-mean candidate each generation, paired original/perturbed map sampling, warm-start covariance and fixed settings. Binary switches were tested outside CMA. In a 2×2 A/B, portal-age was retained (+0.068 current-pool aligned, interval spanning zero, with supporting within-generation observations); Voronoi remained off.

The **v9** campaign used 16 dimensions, cmaes-lra, population 12 plus a mean candidate, and three training opponents. The generation-5 mean's held-out comparison against v7-base gave:

| Panel | v9 wins | v7-base wins | Aligned delta |
|---|---:|---:|---|
| All 15 maps | 153/270 | 124/270 | +0.174 [+0.083,+0.265] |
| Current ten-map pool | 99/180 | 77/180 | +0.187 [+0.088,+0.290] |
| Guard maps | 54/90 | 47/90 | +0.147 [−0.044,+0.346] |

The improvement was large against nicked_lab and Python v6, but slightly negative against nicked v44 on the current pool. Sandbox peak was **7.3M**. v9 was frozen at `7bad14b4e4fd110b`.

Later means drifted without clear progress. Averaging generations 8–14 produced **153 versus 153 wins** on the held-out set and aligned −0.001 [−0.070,+0.068]. Tuning stopped; the earlier v9 stayed.

## v10: concentration helped; broad death reduction did not

The first v9 ladder analysis showed losses with more total length but a shorter longest dragon. The C++ king beacon and big-dragon feeding addressed that conversion problem.

| Variant over v9 | Wins /360 | Aligned delta |
|---|---:|---|
| Base v9 | 210 | — |
| King beacon | 218 | +0.021 [−0.012,+0.052] |
| Beacon plus big feeding | **237** | **+0.085 [+0.032,+0.138]** |
| Dead-end penalty 400 | 213 | −0.003 |
| All three | 228 | +0.047 |

Follow-up restrictions over the beacon/feeding candidate were negative: minimum split room eight won 229 versus base 247; room16 242; gentle dead-end penalty 234; parent-to-child dead-end sonar briefing 247; briefing plus room8 221. The record interpreted many newborn deaths as a cost of productive reproduction. The measured conclusion is narrower: these tested restrictions did not improve wins.

Held-out v10 validation won **207/270 versus 198/270**, aligned +0.036 [+0.003,+0.073]. Sandbox peak was 7.6M. **v10** was frozen with beacon and big feeding, without those death-reduction additions.

## September 29–30: successful map knowledge amid failed retunes

| Experiment | Key result | Decision |
|---|---|---|
| Disable hub book | −0.103 aligned on original book maps; perturbed +0.048 uncertain | Keep book |
| Replace book hubs with observations | −0.104 current originals; perturbed near zero | Keep prior; observe override off |
| v11 broad retune | Held-out 205 versus 207; training fresh-seed 232 versus 212 but losses versus v75 and easy-opponent concentration | Not adopted |
| Founder anchors at 80/150 | Approximately neutral across 450 games | Not adopted |
| Stronger far-hub pull | Initial +0.044, then **−0.056** on fresh seeds | First lead did not confirm |
| Complete identified map's open edges | Screen **378 versus 335/540**; confirmation **316 versus 280/540**, positive across six opponents | Adopted as v10g |
| Per-step hub gradient | Weight15 hurt badly; weight8 near neutral | Not adopted |
| Protected-floor/rescue schedules | Roughly neutral; barely triggered before split-at-four | Not adopted |
| Protect from length four | 285 versus 329; combinations 250/247 | Rejected: early growth displaced the worker economy |
| Large-map feeding shift40 | 344 versus 325, then 344 versus 329; combined 688 versus 654 | Adopted in v10h; current-pool effect less decisive than map completion |
| v12 broad retune | Final mean 317 and gen5 324 versus 339; worse against v92 | Rejected |
| Learned-hub separation fix | 342 versus 339, small mixed effect | Defect identified, benefit unestablished; not adopted |
| Portal-aware input correction to v3 scorer | 330 versus 339; both defects 332 | Not adopted |
| King beacon v2 identity/freshness | 323 versus 314, confirmation 308 versus 303; gains mainly easy opponents | Not adopted alone |
| Reachable feeding check, four/six steps | 333/325 versus 329; combination 326 | No robust gain; not adopted |
| Per-step king gradient | 318/319/316 versus 327 | No useful effect |
| Broader feeding, max length 12 | First 362 versus 348; confirmation 322 versus 323 | Mechanism moved, broad win gain did not confirm |
| Broader feeding, max length 64 | First 355 versus 348; confirmation 316 versus 323 | Not adopted |

Trophy traces explained why map completion could outperform stronger pull weights: the v3 score differed by 10–30 points between moves while the hub term changed by about one; straight-line pull also ignored blocked routes. Knowing traversable geometry changed the reachable plan, rather than merely increasing a weak directional preference.

Nicked v92 raised the benchmark again: v10 won only 8/40 on the current pool in one comparison. A 630-game diagnostic located almost universal PD elimination losses and major longest-dragon deficits on other maps. Feeding traces found our king often received its share when transfers happened, but transfers were too rare. The larger-feeder experiments partially changed that mechanism, yet failed replication on overall wins.

**v10h** retained the map completion and large-map feeding shift. Its ZIP was frozen, sandbox peak **7.9M**, and the log records it active by September 30 21:59 UTC. The next chapter follows the attempted learned replacement and age-gated communication change.

## Operational failures that shaped this period

Parallel heavyweight jobs, repeated C++ compilation and unstable memory coincided with BSODs and GCC crashes. The project introduced a machine-wide experiment lock, serial build locking, worker caps and a corrected build signature. Windows memory diagnostics later reported bad regions; the log records removal of the RAM overclock. The durable experiment rule became one heavy job at a time, at most 12 workers, with memory guards and resumable results. This history records the diagnosis as documented; it does not independently identify a hardware root cause.
