"""Observation-only features shared by linear and neural action rankers.

Only ordinary, visible, empty moves are candidates. Portals, sprints and
intentional trades are outside this first experiment. Space is a static
estimate, not a guarantee about the next turn. No hidden replay state enters.
"""

import math

import bc
import tactics

FEATURES = (
    "food_nearness", "soon_food", "food_count", "spawn_count", "space",
    "exits", "dead_end", "straight", "friendly_near", "enemy_near",
    "enemy_reach", "friendly_reach", "later_enemy_reach", "own_near",
    "boundary", "short_path", "length", "round", "population",
    "food_x_length", "space_x_length", "friendly_x_population",
    "exits_x_length", "boundary_x_no_food",
)


def candidates(obs, team):
    safe = tactics.safe_moves(obs, team)
    good = {d: s for d, s in safe.items() if s > -10}
    return list(good or safe)


def features(obs, team, directions=None):
    directions = candidates(obs, team) if directions is None else directions
    myself = obs.occ[bc.CENTER]
    did = myself[1] if myself else -1
    reach = {"enemy": set(), "friendly": set(), "later": set()}
    for k, part in enumerate(obs.occ):
        if not part or not part[2] or part[1] == did:
            continue
        kind = "friendly" if part[0] == team else "enemy"
        for d in bc.DIRS:
            if obs.edge(k, d) != bc.OPEN:
                continue
            n = obs.step(k, d)
            if n >= 0:
                reach[kind].add(n)
                if kind == "enemy" and part[1] > did:
                    reach["later"].add(n)
    result = []
    length = min(obs.length, 64) / 64
    population = obs.unit_count / 64
    for d in directions:
        start = obs.step(bc.CENTER, d)
        paths = obs.bfs(start, blocked={bc.CENTER})
        food = max((1 / (dist + 1) for k, (dist, _) in paths.items() if obs.pearl[k]), default=0)
        soon = max((1 / (dist + 2) for k, (dist, _) in paths.items()
                    if 0 <= obs.pearl_in[k] <= dist + 1), default=0)
        exits = sum(obs.passable(start, nd) for nd in bc.DIRS)
        nearby = [part for k, part in enumerate(obs.occ) if part and
                  abs(k // 7 - start // 7) + abs(k % 7 - start % 7) <= 2]
        friendly = sum(p[0] == team and p[1] != did for p in nearby) / 13
        enemy = sum(p[0] != team for p in nearby) / 13
        own = sum(p[1] == did for p in nearby) / 13
        boundary = sum(k // 7 in (0, 6) or k % 7 in (0, 6) for k in paths) / 24
        # A three-step simple path through CURRENT empty cells. This is not
        # moving-body search and deliberately does not infer tail release.
        def continuation(k, visited, depth):
            if depth == 0:
                return 0
            best = 0
            for nd in bc.DIRS:
                n = obs.step(k, nd)
                if n >= 0 and n not in visited and obs.passable(k, nd):
                    best = max(best, 1 + continuation(n, visited | {n}, depth - 1))
                    if best == depth:
                        break
            return best
        space = len(paths) / 49
        result.append([
            food, soon, sum(obs.pearl[k] for k in paths) / 49,
            sum(obs.pearl_in[k] >= 0 for k in paths) / 49, space,
            exits / 3, float(exits == 0), float(d == obs.facing), friendly, enemy,
            float(start in reach["enemy"]), float(start in reach["friendly"]),
            float(start in reach["later"]), own, boundary,
            continuation(start, {bc.CENTER, start}, 3) / 3,
            length, obs.round / 500, population, food * length, space * length,
            friendly * population, exits / 3 * length, boundary * (food == 0),
        ])
    return directions, result


def score(row, model):
    if model["kind"] == "linear":
        return sum(x * w for x, w in zip(row, model["weight"])) + model["bias"]
    hidden = [math.tanh(sum(x * w for x, w in zip(row, weights)) + bias)
              for weights, bias in zip(model["w1"], model["b1"])]
    return sum(x * w for x, w in zip(hidden, model["w2"])) + model["b2"]


def choose(obs, team, model):
    directions = candidates(obs, team)
    if not directions:
        return "MOVE " + obs.facing  # same forced fallback as v2
    if len(directions) == 1:
        return "MOVE " + directions[0]
    _, rows = features(obs, team, directions)
    best = max(range(len(rows)), key=lambda i: (score(rows[i], model), directions[i] == obs.facing))
    return "MOVE " + directions[best]
