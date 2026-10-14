"""Local protected-grower and safe cash-in rules for v6."""

import bc
import core_search


def protected(obs, born_round, P):
    return ((born_round == 0 and obs.round >= P.FOUNDER_PROTECT_ROUND) or
            (obs.round >= P.PROTECT_ROUND and obs.length >= P.PROTECT_LEN))


def visible_target(mem, obs, team, did, P):
    if obs.round < P.FEED_ROUND or obs.length > P.FEED_MAXLEN:
        return None
    segments = {}
    heads = []
    for k, part in enumerate(obs.occ):
        if part is None or part[0] != team or part[1] == did:
            continue
        segments[part[1]] = segments.get(part[1], 0) + 1
        if part[2]:
            heads.append((k, part[1], part[3]))
    needed = max(P.FEED_KING_MIN, 2 * obs.length)
    candidates = []
    for k, other_id, facing in heads:
        if segments[other_id] < needed:
            continue
        head = mem.cell(obs.x[k], obs.y[k])
        front = mem.nav.destination(head, facing)
        dist = core_search.torus_distance(mem.cell(*obs.head), head,
                                          mem.width, mem.height)
        candidates.append((dist, -segments[other_id], head, front, k))
    if not candidates:
        return None
    _, _, head, front, local = min(candidates)
    return head, front, local


def should_feed(mem, obs, team, target, P):
    if target is None:
        return False
    head, front, local = target
    own = mem.cell(*obs.head)
    distance = core_search.torus_distance(own, head, mem.width, mem.height)
    if not P.FEED_DMIN <= distance <= P.FEED_DMAX or own == front:
        return False
    if P.FEED_ENEMY_CHECK:
        for k in obs.enemy_heads(team):
            enemy = mem.cell(obs.x[k], obs.y[k])
            if core_search.torus_distance(enemy, head, mem.width, mem.height) <= 2:
                return False
    return True
