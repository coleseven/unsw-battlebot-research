# Research continuation — publication edition, 14 October 2026

This completes the interrupted October 6 review against the work that subsequently landed. It is a research handoff, not an implementation or a new performance claim. Read [PROJECT_WRITEUP.md](PROJECT_WRITEUP.md) and [the later history chapter](docs/project-history/07_V12_AND_CLOSEOUT.md) first. **v12z is the latest adopted local control.** No new strength tests or bot changes were performed for publication.

## Questions already answered

The October 4 harvesting proposal did not pass its diagnostic gate: failures concerned access to food rather than sequencing nearby pickups. Path-aware exploration and a stronger exploration term produced v12x. Do not restart harvesting as if that diagnosis never happened.

| Later work | Outcome | Consequence |
|---|---|---|
| D15 broad sprint masks | Rejected, including against the sprinter | Do not repeat the forbidden-cell union |
| D16 small-enemy-only mask | −6.6 pp | Narrowing the same mask did not rescue it |
| D16/D18 paid flight and queen-sparing fallback | Small, initially unconfirmed | Components later tested in a stronger combination |
| D17 preserving long starting founders | Mixed, +0.2 pp | No generic founder split delay |
| D19 sprint escorts | Neutral/negative | Distance-based escort not established useful |
| D20 queen exploration exemption | −1.8 pp | Broad queen roaming suppression failed |
| D21/D22 queen sprint attacks | Confirmed; attack alone +3.8 pp in D22 | Already implemented, not future work |
| D22 attack + flight + queen-sparing fallback | +5.7 pp; adopted as v12z | Preserve this control |

The corrected October 6 audit gives **104/117** rammers visible at the queen's preceding turn, **39/117** within two cells then, and **75/117** attacks using paid steps. Earlier figures mixed positions and lengths from different moments. These events came from the old mixed 532-game cohort, not a new v12z sample. See [corrected replay evidence](results/strategy-review-20261006/queen-ram-audit.json).

That cohort included two unranked series, verified on the public pages: [Human Learning, 17 games](https://game.battlecode.au/visualiser?match=1223999) and [180 Deg, 10 games](https://game.battlecode.au/visualiser?match=1225935). Removing their 24 wins leaves **264/505**, rather than 288/532. This subtraction does not establish that every remaining five-game battle was ranked. Future exports need an explicit ranked flag and submission provenance.

## 1. Current-map and opponent transfer

New map names appeared by October 12 and were absent from the books. Keep the old 17-map suite as a regression set; obtain authoritative new layouts and rules for a separate current-map manifest. Do not repeat the foodless-map error by treating redacted replay terrain as a complete spawn definition.

Compare v12z with and without available map-specific knowledge on verified layouts. Measure time to productive territory, worker starvation, portal traversal, queen exposure and wins. Include unseen and perturbed geometry. Recognizing additional map names alone will not establish generalization.

If access failures recur, test a short **interruptible route objective**: cross a particular bottleneck, establish a foothold, then clear its exit. Local collision handling remains active; abandon the objective on contradictory evidence. Measure completed useful arrivals, not just distance progress. This differs from another global exploration multiplier or permanent camping. Temporally extended, interruptible policies are formalized by [Sutton, Precup and Singh, 1999](https://www.sciencedirect.com/science/article/pii/S0004370299000521); the paper does not establish which objective will work here.

## 2. Compare complete tactical actions before committing

The source review found splits can return before later attack/escape logic. v12z already attacks queens and uses paid flight; the remaining hypothesis is **better full-action comparison**, not enabling sprinting again.

Compare the incumbent, a few legal one/two-step moves, and the available split. Apply the entire proposed move, including body changes, before considering enemy replies. Intermediate steps within one move are not separate opponent turns. Evaluate realizable short kill paths against the resulting position, rather than unioning all reachable cells into forbidden terrain.

Distinguish certain self-collision, a realizable head-kill response, uncertain danger outside observation, and a demonstrated short escape. Preserve graded preferences when every action is risky and retain the incumbent when information is inadequate. Visible enemy segments do not necessarily reveal full length; keep uncertainty explicit.

First inspect a fixed balanced corpus of current-version ram losses and safe encounters. Count recognized attacks, already-doomed positions, and legal alternatives that survive the immediate response. If alternatives rarely exist at the last decision, inspect the prior turn. Do not begin a large weight sweep before establishing action-selection opportunities.

Sprint boundary fixtures matter. Payment is checked before collision; a length-two dragon cannot pay an extra step unless an earlier free step has increased its length. Free allowance is fixed at action start; food, portals, occupied tails and paid shrinkage change subsequent transitions. A `length - 1` radius is not a full legal-action model. Verify against the engine. [Official execution order](https://game.battlecode.au/docs/execution-order).

Opponent-model robustness is motivated by [Johanson, Zinkevich and Bowling, 2007](https://proceedings.neurips.cc/paper/2007/hash/6e7b33fdea3adc80ebd648fffb665bb8-Abstract.html). Their guarantees do not transfer automatically to this truncated partially observed search. Begin with a few explicit response scenarios, a fixed comparison rule, and incumbent fallback.

## 3. Isolate friendly-fire changes

The existing queen-sparing fallback also changes enemy-ram choices in other trapped states. D14 was not a pure safety invariant: saved pairing shows **83 losses became wins and 73 wins became losses**. v12z's combination now has positive evidence, so retain it as the control.

A further experiment can isolate “the incumbent fatal move hits our queen” and choose a verified non-queen fatal destination, including portal exits. Test against v12z's existing fallback, not old v11t. Queen-into-worker collisions need a different intervention. Avoid rebuilding a standing escort after D19's failure.

If replay review finds interception opportunities, require a worker to reach the actual attack lane **before the attacker's ID-ordered turn**, preserving the queen's exit. Count feasible opportunities before building messaging. Short space-time reservations relate to [Silver, Cooperative Pathfinding, 2005](https://ojs.aaai.org/index.php/AIIDE/article/view/18726), whose assumptions about known agent routes are stronger than this game's delayed, unauthenticated sonar permits.

## 4. Test behaviors, not just more sibling versions

Keep the old panel for regression, but classify opponents by demonstrated sprint hunting, ordinary hunting, economy racing, portal aggression, corridor blocking and late collection. Multiple nicked versions are correlated; our own specialists are not independent external strategies.

Verify that each opponent exercises its intended behavior. Hold out an implementation of an important behavior. When a new defense improves, test a counter-response that exploits its cost, such as surrendering food access while retreating. This is a modest application of population/response-oracle reasoning from [Lanctot et al., 2017](https://proceedings.neurips.cc/paper_files/paper/2017/hash/3323fe11e9595c09af38fe67567a9394-Abstract.html), not a request for their entire deep-RL system.

## 5. Learning only after a useful teacher

R5 already used real alternative-action continuations. “Counterfactual training” alone is not a new proposal. A restart requires a demonstrably stronger, narrowly activated teacher, legal observations and reliable baseline-action identity.

Label short outcomes separately: legal ram availability, near-term survival, traps and paid length. Split by whole game, map and opponent family; include safe states and false alarms. Start with a linear ranker. Test a small MLP only if needed, followed by frozen full-game validation. [Chang et al., Learning to Search Better than Your Teacher, 2015](https://proceedings.mlr.press/v37/changb15.html) motivates rollouts beyond reference imitation, not a promise of game strength.

The spare i5/16 GB/GTX 980 machine can initially handle bounded replay reconstruction and teacher labels. A neural self-play rewrite or GPU purchase should not be a prerequisite. Trustworthy labels matter more than training capacity here.

## Next-cycle acceptance criteria

Freeze v12z's parameters, use untouched seeds and both sides, verify maps, and prespecify the opponent mix. Change one behavior at a time. Report paired wins/draws, map/family results, activation frequency and sandbox cost. Keep diagnostics separate from promotion trials. A combined candidate needs an incremental comparison against the actual combined incumbent.

For live review, preserve upload identity, timestamp/timezone, ranked status, map, opponent and side. Separate custom series and uncertain version boundaries. Rating streaks and showcase games are not confirmation. The record supports further development, but does not establish top-100 strength or a guaranteed route to it.
