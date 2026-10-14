# Where we are, and the next useful experiments

Reviewed 3 October 2026. Analysis only: no bot changes, training, runtime replacement or submission in this review. The official 1.2.9 wheel was downloaded for inspection, not installed.

## Recommendation

**Keep v11q. Repair the evaluation setup, then replace the queen's approximate escape test with a more faithful controller and cooperative worker yielding. Stop broad safety-weight sweeps.**

We have made meaningful progress, but the recent experiments mostly adjust penalties around the same limited decision model. The next gains are more likely to come from modeling the actual danger and changing teammate behavior than from making the queen more afraid of everything nearby.

The public snapshot during this review put [777](https://game.battlecode.au/teams/590) at **rank 115, rating 1553**, with [rank 100](https://game.battlecode.au/leaderboard?page=10) at **1598**. The 45-point gap is a moving target, not a conversion into a required local win count. The experiment log records v11q as the uploaded incumbent; the public profile alone does not identify its files.

## What worked, and what did not

| Experiment | Evidence | Decision |
|---|---|---|
| Pearl-focused extra free moves | Confirmation 474 versus 447 wins/792; known maps gained, reconstructed Sprint maps tied | Retain |
| Light queen protection plus short escape search | Confirmation 490 versus 492/792, but surviving queens 79 versus 24; head-to-head 80/120 versus v10o and 73/120 versus v11ms | Retain v11q |
| Bigger/faster worker economy | Later split thresholds produced large losses | Do not globally delay splitting |
| Broad queen mode and early growth | More surviving or larger queens did not compensate for lost games; keep6 had 27 surviving queens versus 56 | Do not equate queen growth with winning |
| Queen hunt | Confirmation 549 versus 563/924 | Not adopted |
| Worker travel | 552 versus 563/924 | Not adopted |
| Keep-away and wider worker guard | Q11: 563 and 545 versus 572/924, despite modest survival gains | Not adopted |

These are reported results from [FEATURE_EXPERIMENT.md](FEATURE_EXPERIMENT.md), not new runs. The confirmation failures matter more than the promising screens.

The strongest live diagnosis is the logged 162-game v11q sample: **31 losses when only the enemy queen survived, versus four wins when only ours survived**. Longest-dragon results were 33 wins/33 losses; elimination favored us 27/16; both-queen length favored us 10/8. Queen survival is the largest deficit in that sample. This is a classification of outcomes, not evidence that saving a queen would automatically flip all 31 games.

## 1. Fix the benchmark before choosing the next winner

The official site announced updated maps and the Sprint maps on 2 October; 1.2.9 is now available. Our explicit queen runtime still pins **1.2.3**. [Official updates](https://game.battlecode.au/updates)

I compared all 22 maps bundled in the 1.2.9 wheel with our 15 historical maps and seven reconstructed Sprint maps. The saved comparison is [map-comparison.json](results/review-20261003/map-comparison.json).

- **Dragon starting configurations differ on eight:** Colosseum, Autarky, Prisoners Dilemma, Islands, Slithery Fight, Stripes, Trophy and Around UNSW.
- **Parsed edge geometry differs on five:** Colosseum, Default, Default Small, Schooltime and Trophy.
- Pearl-source counts differ on several important maps: Autarky 188→196, PD 88→84, Islands 290→330, Slithery 339→331, Trophy 625→547. The raw TILE records also differ for the Sprint maps; their former timers were estimates.

This does not erase the previous results. It means their measured effect may not transfer to the current starts, corridors and food supply. In particular, queen-opening deaths on an old starting position cannot settle a policy choice for a revised one.

**Next deliverable:** preserve the old environment and frozen results; establish a separately identified current runtime, exact bundled maps and hashes; verify them against recent server layouts. Use the official Sprint files rather than estimates for current evaluation. Re-run rule/parity fixtures and benchmark v11q before any tuning. Do not install underneath an active job.

The queue currently names 17 current maps, while `ranked_maps()` still returns the historical 15. `current_pool_maps()` adds reconstructed Sprint maps. Make current, historical and reconstructed coverage explicit in every run. A changed constant is insufficient if the runner still loads the old files.

The old map books need special attention: revised spawn starts and food can leave geometry recognition looking plausible while its resource assumptions are wrong. Audit book validity and run a targeted book-on/off comparison on changed maps. Do not blindly remove the previously successful book everywhere.

## 2. Repair the queen escape model, not just its depth

I inspected the frozen `versions/v11q/v6_brain.hpp`, as well as the current source. `queen_escape` is useful, but its description as an exact search overstates what it models:

1. **Food does not change the simulated body.** Every simulated step drops the tail. Eating should retain it. A route can therefore appear to escape through a cell that remains occupied after growth.
2. **Threats are expanding toroidal distance circles.** Walls, neck direction and traversable routes do not constrain that reach estimate. It can overstate danger behind barriers and miss portal shortcuts. Visible segment count can also understate enemy speed.
3. **Other bodies remain static throughout the horizon.** This hides cells that will become available and omits cells newly occupied by moving workers. Both errors matter in a crowd.
4. **Leaving the visible window is credited as surviving the full horizon.** An uncertain exit should not be ranked as equivalent to a demonstrated safe continuation.
5. **A successful horizon is effectively binary.** The caller clamps full-line count to one and keeps the old preference when survival ranks tie. A fragile single corridor and multiple independent exits can look equivalent.
6. **The tactical choice is not necessarily the final action.** Extra pearl steps can be appended after selection. In v11q, `CPP_QUEEN=0`, so the multistep conditional permits queen extra steps despite `CPP_MULTISTEP_QUEEN=0`. The safety assessment must apply to the final complete action.

These are code-level limitations, not a measurement of how many ladder losses each caused. Increasing depth 3→5 searches these assumptions more deeply; it does not correct them.

**First prototype:** branch-specific body and consumed-food state, correct current-tail collision, explicit turn/substep timing, and final-action validation. Separate unknown space from known-safe space. Use wall/portal-aware threat reach, with an uncertainty treatment for incomplete enemy bodies. Treat other-unit future occupancy as scenarios rather than pretending all bodies are permanently frozen.

Do not start with a full-game minimax. Start with the queen's next action and a few plausible responses. Score survival, escape alternatives and resource cost separately. Reserve deeper work for ambiguous dangerous states. Retain a tested fallback within the judge budget.

**Decisive diagnostic:** take 30–50 locally reproducible failures, inspect the 5–15 turns before death, and find the first state where the corrected controller chooses differently. Check whether that changes the subsequent failure. Public replay reconstruction may omit private information, so use public games to identify patterns and locally captured exact observation histories for controlled interventions. Never label every wall death as a planning bug: some positions are already forced losses.

## 3. Make workers actively yield to the queen

The logged ladder death sample attributed 18 of 83 queen deaths to our own dragons, including 14 head-ons. A radius-two penalty failed confirmation, so simply clearing a larger circle is not the next experiment.

Test a **short route reservation**, not a permanent exclusion zone:

- Queen announces a short intended route/escape corridor with origin round and expiry.
- Workers that receive it avoid ending on the queen's next head cell and avoid occupying its only usable exit when another acceptable action exists.
- Workers distinguish the queen's actual body from an intended route; they do not assume a reservation makes an occupied cell traversable.
- If intent is absent or stale, use a conservative local visible-queen rule. Sonar is directional and can be blocked; successful receipt cannot be assumed.
- Prefer changing the responsible worker's action over forcing the queen into an inferior route. Keep the restriction narrow enough to preserve food access and reproduction.

Queens act before their workers, which gives this idea a useful timing structure: workers can receive queen sonar later in that round and preserve space for the next queen turn. Validate communication and action ordering with fixtures. Route intent must describe the position after the issued action, not accidentally reuse pre-move coordinates.

First compare local yielding alone, reservation alone and their combination. Measure own-worker queen kills, legal queen exits one turn ahead, worker food intake and wins. Reject a policy that merely moves the death category from friendly collision to enemy collision or starvation.

## 4. Try a small queen refuge controller

This is the next structural hypothesis if corrected local tactics still get trapped: a length-2/3 queen maintains a safe circuit in a defensible area while workers run the economy. It deliberately postpones growth until survival and access are credible. The logged stronger-team sample also had median surviving queen length three, so a small queen is not inherently a failed strategy.

Choose refuge candidates by traversable cycles, multiple exits, approach corridors, crowding and access to modest food. Maintain a fallback exit and periodically re-evaluate; a fixed loop becomes predictable and can be intercepted. Do not interpret large flood-fill area as a safe circuit or use only map-name scripts.

Compare three roles: incumbent mobile queen, temporary refuge while crowded, and persistent refuge with an escape trigger. Start with temporary refuge. Only after survival improves should we revisit threshold growth or scheduled feeding. Prior growth experiments show that feeding a vulnerable queen can make the investment less useful.

## 5. Change the opponent panel and promotion rule

The panel still contains several versions of the same old strategic family. Adding v11q helps, but a panel whose queens usually die underprices queen survival and may overvalue secondary longest-dragon play.

Keep the old opponents as economy/combat guards. Add controlled queen-aware specialists: small refuge queen, active growth queen, queen raider, and strong worker economy. These can initially be variants of our own controller; label their shared lineage rather than counting them as independent strategies. Use current public ladder replays to check whether their behavior resembles the failures we actually face.

Promote on actual win/draw outcomes across the current maps, both sides and fresh seeds, with family-balanced reporting. Queen survival is a diagnostic, not a substitute objective. Report the four queen-alive combinations separately and separate elimination from round-limit outcomes. Reserve untouched confirmation conditions; repeated reuse of the same confirmation set turns it into training data.

The local evidence and live evidence should inform each other. A gain against unadapted opponents is weak ladder evidence. Conversely, a survival increase accompanied by a reliable loss across a representative queen-aware panel should still be rejected.

## Order of work

| Order | Work | Completion gate |
|---|---|---|
| 1 | Current runtime, exact map refresh, book audit, v11q baseline | Rule/parity tests and complete current-map baseline with hashes |
| 2 | Correct queen simulation and final-action safety | Real-engine fixtures plus demonstrated reductions in reproducible failures |
| 3 | Local yielding and short route reservations | Fewer teammate-caused queen losses without economy/win regression |
| 4 | Temporary queen refuge/circuit policy | Improvement against queen-aware specialists and fresh full-suite confirmation |
| 5 | Selective growth/collection | Survival already credible; retained queen growth adds actual wins |
| Later | NN endpoint/role evaluator | Correct transition model and useful teacher first; R5 stays stopped |

Do not repeat global split-delay, generic stronger attraction, larger keep-away radii, or the rejected hunt/travel settings without a new mechanism and a concrete failure case. No evidence yet justifies restarting a large neural training run. The immediate research asset should be a small, reliable set of queen-danger scenarios and an evaluation panel that rewards the behavior the current ladder requires.
