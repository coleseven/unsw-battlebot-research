# Fundamentally different strategies (2026-09-24)

Research only; nothing was run against any bot. Companion to
[COMPETITOR_RESEARCH.md](COMPETITOR_RESEARCH.md), which covers what current bots
do. This file covers *different* ways to play and build, for exploration on a
second machine (GTX 980).

Every bot seen so far, ours included, plays one archetype: **swarm then grow**.
Split at length 4 into length-2 children, collect, and hope someone is long at
round 500. The ideas below are alternatives, or additions that change the game
the bot is playing.

## Rules that open strategic space

From the official docs (game.battlecode.au/docs):

- **Scoring:** survive; then longest *living* dragon; then total team length;
  else draw. The game ends immediately when one team is eliminated.
- **Death drops food:** a dead dragon turns every second segment into a pearl,
  ⌈L/2⌉ pearls in total. Pearl countdowns are not changed.
- **Self-kill is possible:** a turn with no valid action (or no output) is
  suicide. There is no explicit suicide command; the default action is suicide.
- **Head-on kills both** dragons regardless of length.
- **Split:** the child is the rear segments reversed, acts later in the same
  round, and needs length >= 2 on both sides. Team cap 64.
- **Pearl spawns:** each tile's countdown is visible when in view; spawns only
  on an empty tile; the reset gap is random in a hidden per-tile range. **On a
  symmetric map, mirror tiles share one countdown.**
- **Maps are guaranteed symmetric** (mirror or 180° rotation), 10-64 per side.
- **Sonar** goes in a straight line from the head and is delivered to the first
  dragon hit, which can be an enemy.
- **Sprint:** each extra step costs one segment; collisions checked per step.

## Game-strategy archetypes

### 1. Consolidation by sacrifice ("feeding the king")

At the end, convert the swarm's total length into the longest dragon. Small
dragons walk next to a chosen king and die (empty turn), dropping ⌈L/2⌉ pearls
each for the king to eat.

- **Why it fits our losses:** 31 of our last 39 losses went to round 500 and were
  lost on longest dragon by a median of 4. In several we had far more total
  length (Big Empty M146956: total 697 vs 475, longest 34 vs 59). Converting a
  small part of the swarm would flip many of these.
- **Efficiency:** about 50% (⌈L/2⌉ pearls per L length), minus pearls the king
  cannot reach before round 500 or the enemy steals. A length-2 dragon gives 1
  pearl; a length-3 gives 2 (the best ratio).
- **Coordination without shared memory:** king = the longest dragon a sacrificer
  can see (ties by lowest id); sacrifice only when adjacent to the king's
  predicted path and after round ~460. Sonar could call feeders, but it only
  reaches the first dragon in a straight line.
- **Costs:** lowers total length (the second tiebreak); feeding near enemies
  feeds them. Needs a king that is safe to route.
- **Evidence it is used:** unclear. In the 26 top-team games, 880 small-dragon
  deaths were empty turns (engine default "suicide"), concentrated in 7 games and
  spread across the whole game, not the end. That could be deliberate
  (sacrifice, or suicide when boxed in) or crashes; replays cannot distinguish.
  Their pearls went 96% to the same team, but so did 98% of kelp-death pearls,
  so this does not show feeding.

### 2. Titan with escorts

A few dragons (for example one titan plus 4-8 escorts) instead of 64. Escorts
body-block around the titan and take head-on trades for it.

- Our population experiment found splitting beats no splitting against our own
  bots, so a pure monolith is likely weak. The open question is the middle:
  small squads where each dragon is safer and one is always large.
- Pairs naturally with sacrifice: the escorts are the feed.

### 3. Predator: win by elimination

Aim to end the game before round 500. Head-on kills both, so a team with more
dragons wins a war of attrition by trading 1-for-1 (a Lanchester-style
numbers argument). Small dragons trade with long enemies (net gain); bodies are
placed in front of enemy heads.

- Top-bot winners ended 14 of 26 games by elimination, mostly on small maps
  (Default Small, Trophy, Devil, Queen Of Spades).
- Kills drop pearls near the killer: a Halite III-style fight economy.
- Map-dependent: likely strong on 16x16 and 25x25, weak on 64x64.

### 4. Territory and enclosure (Tron)

Use long bodies as moving walls to cut enemies off from pearl-rich regions or
seal them into pockets. Evaluate moves by Voronoi territory (cells we reach
first) with chambers split at articulation points (see the Tron winner's
write-up). Harder on the wrapping board; stronger on kelp-heavy maps
(stronghold, Trauma).

### 5. Spawn farming with a map book

The ladder uses a small fixed map pool, and every replay carries the full map
text. A bot can fingerprint the map on turn 0 (size plus visible kelp/portals)
and load the whole static map: kelp, portal pairs, and every spawning tile with
its mirror partner. That removes the 7x7 limit for terrain and planning.

- Farming: schedule visits to spawn tiles by countdown (a timed routing problem),
  keep "gardener" dragons circling rich hubs, and use mirror symmetry (a
  countdown seen on our side predicts the mirrored tile's spawn).
- nicked hard-codes a few hub coordinates by map size; nobody seen does a full
  map book.
- Risk: new maps at the Sprint/Qualifier. The fallback must be the generic bot.
  Also confirm with the organisers that embedding public map data is allowed.

### 6. Split as a tactic

A split instantly places the rear half as a new dragon facing the other way:
an escape (the reverse split used by nicked and Leviathan), or a wall dropped in
front of an enemy head. The child acts later in the same round.

### 7. Adapting to the opponent

Detect the opponent's style from what is visible (many small heads versus a few
long bodies) and switch between the archetypes above. TX140907 prototyped this
(counter graphs per map), but has not enabled it.

### 8. Sonar information warfare

Enemies receive our sonar when they are the first dragon hit, and we receive
theirs. Encrypt anything we send; enemy messages can be read or ignored. ctmes
measured no gain from sonar at all, so expect little value here.

## Technical paradigms

| Approach | What it is | Compute | Fit here |
|---|---|---|---|
| Heuristic + automated tuning | Parametric policy; CMA-ES or genetic search over weights; round-robin selection; SPRT confirmation (ctmes) | CPU, embarrassingly parallel | Best return per hour. Each archetype above becomes a parameter set |
| Search with a hand evaluation | Shallow per-dragon search (2-3 plies) with Voronoi/chamber evaluation (Tron winner, Battlesnake) | CPU at runtime; must fit 100M points | Strong for safety and trapping; budget limits depth |
| Imitation learning | Learn top players' moves from replays (v3) | Small GPU or CPU | Done; strong baseline. Copies habits, not reasons |
| Privileged teacher, then student | Offline teacher with full map state and search labels actions; a window-only student imitates it ("Learning by Cheating") | CPU for teacher labels, GPU for student | Fits our assets: exact full-state reconstruction from replays |
| Self-play reinforcement learning | Shared per-dragon policy on local observations, centralized critic on full state (MAPPO / CTDE) | Needs a fast simulator; GPU for updates | Highest ceiling, highest cost; nets must stay tiny for the judge |
| Neuroevolution / evolution strategies | Optimize policy weights directly on win rate | CPU | Simpler than RL, no gradients through the game; scales with cores |
| League / population training | Keep a pool of past selves and outside bots as opponents (AlphaStar league) | CPU | Prevents overfitting to one opponent; use `sparring/` |
| Search + network (AlphaZero) | Tree search guided by a policy/value net | Too costly for 64 dragons per turn | Only plausible for a single king |

## Setting up the GTX 980 machine

- **The GPU only helps training.** The judge runs Python 3.13 + NumPy only on
  CPU, at 100M points per dragon-turn (v3 already peaks at 65-85M). Deployed
  models must be tiny and run in NumPy. For evolution, tuning and self-play, the
  bottleneck is **simulation speed on CPU cores**, not the GPU.
- **PyTorch on Maxwell (sm_52):** the CUDA 12.8/12.9 wheels dropped Maxwell and
  Pascal from PyTorch 2.8. The CUDA 12.6 wheels still include them, but will not
  be published from PyTorch 2.15. Use a cu126 build no newer than 2.14, and check
  `torch.cuda.get_arch_list()` includes `sm_50` or `sm_52`: a Windows cu126 2.8
  issue reported missing Maxwell kernels. 4 GB of VRAM is plenty for
  the network sizes the judge can afford.
- **A fast simulator is the enabler** for RL, evolution and large tuning runs.
  The official engine (wasm) plus Python bots runs ~12 games/s on 15 workers.
  A NumPy/Numba or C++ re-implementation of the rules, checked against the real
  engine with our replay reconstruction (`bcsim.reconstruct`, already verified
  on ~39k turns), would let one machine play orders of magnitude more games.
  Keep the real engine as the final judge.

## Suggested exploration order

1. **Consolidation by sacrifice.** Cheapest to test, aimed directly at the
   dominant loss mode (round-limit losses by a few segments). Parameters: start
   round, king rule, feeder radius, minimum king length.
2. **Map book** (fingerprint, then full static map). Unlocks spawn farming,
   routing, and safe long-range planning. Needs an organiser check and a
   fallback.
3. **Predator mode on small maps**, compared by map size.
4. **A fast simulator**, then CMA-ES over these archetypes (and mixes of them).
5. **Teacher-student distillation** or self-play RL, once the simulator exists.

## References

- UNSW Battlecode rules: https://game.battlecode.au/docs (structure, pearls, death, splitting, sonar, execution order)
- Tron post-mortem (Voronoi, articulation points): https://www.a1k0n.net/2010/03/04/google-ai-postmortem.html
- Chen et al., Learning by Cheating (privileged teacher to student): https://arxiv.org/abs/1912.12294
- Yu et al., The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games (MAPPO): https://arxiv.org/abs/2103.01955
- Vinyals et al., AlphaStar league training (Nature 2019): https://www.nature.com/articles/s41586-019-1724-z
- Hansen, The CMA Evolution Strategy: A Tutorial: https://arxiv.org/abs/1604.00772
- Halite III winner bot (fight economy): https://github.com/teccles-halite/halite3-bot
- PyTorch: Maxwell/Pascal removed in CUDA 12.8/12.9 builds: https://dev-discuss.pytorch.org/t/cuda-toolkit-version-and-architecture-support-update-maxwell-and-pascal-architecture-support-removed-in-cuda-12-8-and-12-9-builds/3128
- PyTorch: CUDA 12.6 wheels end at 2.15: https://dev-discuss.pytorch.org/t/notice-cuda-12-6-wheels-will-no-longer-be-published-from-pytorch-2-15-drops-maxwell-pascal-volta/3432
- PyTorch issue, Windows 2.8 cu126 Maxwell kernels: https://github.com/pytorch/pytorch/issues/160575
