"""One bounded score for food, exploration, room, heads and movement.

Unknown terrain can be explored only across an observed open edge. Unknown
occupancy is neither assumed blocked nor certified safe. The current own tail
is never an immediate legal move: the engine checks collision before release.
"""

import heapq
import time

import bc
import action_value


def torus_distance(a, b, width, height):
    ax, ay = a % width, a // width
    bx, by = b % width, b // width
    dx, dy = abs(ax - bx), abs(ay - by)
    return min(dx, width - dx) + min(dy, height - dy)


def own_free_times(mem, obs):
    body = mem.trail_body(obs.length)
    if body is None:
        return {}
    # Current tail becomes available after the first move, not during it.
    return {cell: obs.length - i + 1 for i, cell in enumerate(body)}


def blocked(mem, cell, arrival, team, did, own_free):
    part = mem.occupied.get(cell)
    if part is None:
        return False
    if part[0] == team and part[1] == did:
        return arrival < own_free.get(cell, 10**9)
    return True


def legal_moves(mem, obs, team, did, attacks=None):
    """Immediate one-step legality, with known paired portals only.

    When `attacks` is a dict, an ordinary step onto a visible enemy head is also
    returned (head-on kills both dragons) and recorded as attacks[dir] = id.
    """
    start = mem.cell(*obs.head)
    out = {}
    for direction in bc.DIRS:
        if obs.length > 1 and direction == bc.OPPOSITE[obs.facing]:
            continue
        edge = obs.edge(bc.CENTER, direction)
        if edge == bc.KELP:
            continue
        dest = mem.nav.destination(start, direction)
        if dest is None:
            continue
        if edge == bc.OPEN:
            local = obs.step(bc.CENTER, direction)
            if local < 0:
                continue
            part = obs.occ[local]
            if part is not None:
                if attacks is None or part[0] == team or not part[2]:
                    continue
                attacks[direction] = part[1]
        elif dest in mem.occupied:
            continue
        out[direction] = dest
    return out


def head_threats(mem, obs, team, did):
    enemy, friendly, ahead = set(), set(), set()
    mates = []
    for cell, part in mem.occupied.items():
        side, pid, is_head, facing, seen = part
        if not is_head or seen != obs.round or pid == did:
            continue
        if side == team:
            mates.append(cell)
        for direction in bc.DIRS:
            if direction == bc.OPPOSITE[facing]:
                continue
            dest = mem.nav.destination(cell, direction)
            if dest is not None:
                (friendly if side == team else enemy).add(dest)
        next_cell = mem.nav.destination(cell, facing)
        if next_cell is not None:
            ahead.add(next_cell)
            second = mem.nav.destination(next_cell, facing)
            if second is not None:
                ahead.add(second)
    return enemy, friendly, ahead, mates


def food_value(mem, obs, cell, hops, P):
    value = 0.0
    visible = mem.nav.visible.get(cell)
    if visible is not None and obs.pearl[visible]:
        value = P.W_PEARL / (1 + hops)
    elif cell in mem.pearl:
        value = P.W_MEM_PEARL / (1 + hops)
    spawn = mem.spawn.get(cell)
    if spawn is not None:
        wait = spawn[0] - obs.round - hops
        if 0 <= wait <= P.H_SPAWN:
            value = max(value, P.W_SPAWN / (1 + hops + 0.2 * wait))
    return value


def search_one(mem, obs, team, did, dest, direction, P, own_free, t0, budget):
    best = {dest: 0}
    queue = [(0, 1, dest)]  # weighted cost, actual arrival step, cell
    expanded = unseen = stale = 0
    food = hub = 0.0
    hub_area = mem.hub_area
    goal = mem.goal
    progress = 0.0
    if goal is not None:
        width, height = mem.width, mem.height
        base = torus_distance(mem.cell(*obs.head), goal, width, height)
    while queue and expanded < P.N_SEARCH:
        if time.perf_counter() - t0 > budget:
            break
        cost, arrival, cell = heapq.heappop(queue)
        if cost != best.get(cell):
            continue
        expanded += 1
        food = max(food, food_value(mem, obs, cell, arrival - 1, P))
        if goal is not None:
            # tiles gained toward the goal along this search path
            gained = base - torus_distance(cell, goal, width, height) - P.GOAL_STEP_COST * (arrival - 1)
            if gained > progress:
                progress = gained
        if hub_area:
            v = hub_area.get(cell)
            if v:   # reached a hub area along a real (portal-aware) path
                hub = max(hub, v / (1 + (arrival - 1) / P.HUB_SCALE))
        seen_round = mem.nav.seen[cell]
        unseen += seen_round < 0
        stale += seen_round >= 0 and obs.round - seen_round >= P.STALE_ROUNDS
        if arrival >= P.DEPTH_MAX:
            continue
        for step in bc.DIRS:
            next_cell = mem.nav.destination(cell, step)
            if next_cell is None or blocked(mem, next_cell, arrival + 1,
                                            team, did, own_free):
                continue
            new_cost = cost + 1 + (mem.nav.seen[next_cell] < 0)
            if new_cost < best.get(next_cell, 10**9):
                best[next_cell] = new_cost
                heapq.heappush(queue, (new_cost, arrival + 1, next_cell))
    exits = 0
    for step in bc.DIRS:
        if step == bc.OPPOSITE[direction]:
            continue
        next_cell = mem.nav.destination(dest, step)
        if next_cell is not None and not blocked(mem, next_cell, 2, team,
                                                 did, own_free):
            exits += 1
    return {"food": food, "hub": hub, "progress": progress, "unseen": unseen, "stale": stale,
            "room": len(best), "exits": exits, "expanded": expanded}


def score_moves(mem, obs, team, did, P, model, protected=False,
                cash_target=None, started=None):
    """Return one combined numeric score for every legal immediate move."""
    hunter = not protected and obs.length <= P.HUNT_MAXLEN
    attacker = not protected and obs.length <= P.ATTACK_MAXLEN
    attacks = {} if attacker else None
    moves = legal_moves(mem, obs, team, did, attacks)
    if not moves:
        return {}
    started = time.perf_counter() if started is None else started
    # enemy dragons in view this round: visible segment count (a lower bound
    # on length) and head cells
    enemy_len, enemy_heads = {}, []
    for cell, part in mem.occupied.items():
        if part[4] == obs.round and part[0] != team:
            enemy_len[part[1]] = enemy_len.get(part[1], 0) + 1
            if part[2]:
                enemy_heads.append((cell, part[1]))
    scores = {}
    for direction, pid in (attacks or {}).items():
        gain = enemy_len.get(pid, 1) - obs.length
        if gain >= P.ATTACK_MIN_GAIN:
            scores[direction] = P.W_ATTACK + P.W_TRADE * gain
        moves.pop(direction)
    if not moves:
        return scores
    directions = list(moves)
    _, rows = action_value.features(obs, team, directions)
    v3 = {d: action_value.score(row, model) for d, row in zip(directions, rows)}
    enemy, friendly, ahead, mates = head_threats(mem, obs, team, did)
    # longest visible enemy that can step onto each cell next turn
    reach = {}
    for cell, pid in enemy_heads:
        for step in bc.DIRS:
            dest = mem.nav.destination(cell, step)
            if dest is not None:
                reach[dest] = max(reach.get(dest, 0), enemy_len.get(pid, 1))
    own_free = own_free_times(mem, obs)
    latest_visit = {cell: round_no for cell, round_no in mem.trail}
    start = mem.cell(*obs.head)
    protection = P.PROTECT_MULT if protected else 1.0
    margin = P.SPACE_MARGIN * (P.ENDGAME_SPACE_MULT if obs.round >= 400 else 1.0)
    need = min(P.SPACE_MULT * obs.length + margin, P.SPACE_CAP)
    remaining = max(0.0, P.SOFT_S - (time.perf_counter() - started))
    per_direction = remaining / len(moves)
    for direction, dest in moves.items():
        terms = search_one(mem, obs, team, did, dest, direction, P,
                           own_free, time.perf_counter(), per_direction)
        room = min(terms["room"], need)
        value = terms["food"] * (P.PROTECT_FOOD_MULT if protected else 1.0)
        value += (P.W_UNSEEN * terms["unseen"] +
                  P.W_STALE * terms["stale"]) / P.N_SEARCH
        value -= protection * P.W_TRAP * max(0, need - room)
        if room < obs.length + 2:
            value -= protection * P.W_LETHAL
        if terms["exits"] == 0:
            value -= P.W_DEADEND
        elif terms["exits"] == 1:
            value -= P.W_CORRIDOR
        # a hunter hit by a longer enemy head is a favourable trade
        threat = reach.get(dest, 0)
        if dest in enemy and not (hunter and threat >= obs.length + P.HUNT_MIN_GAIN):
            value -= protection * P.W_HEAD_ENEMY * max(1, obs.length / 4)
        if hunter and obs.round >= P.HUNT_ROUND:
            value += max((P.W_HUNT / (1 + torus_distance(dest, cell, mem.width, mem.height))
                          for cell, pid in enemy_heads
                          if enemy_len.get(pid, 1) >= obs.length + P.HUNT_MIN_GAIN),
                         default=0.0)
        if mem.goal is not None:
            # exploration goal, stronger in a poor area, weak for kings
            poor = mem.local_rate is not None and mem.local_rate < P.POOR_RATE
            value += (P.W_GOAL * terms["progress"] * (P.POOR_MULT if poor else 1.0)
                      * (P.KING_GOAL_MULT if protected else 1.0))
        if mem.hubs:
            # pull toward pearl hubs: by search path where the search reached a
            # hub area (follows portals), else a weaker straight-line pull;
            # weaker where teammates already crowd the hub
            crowd = 1 + max(sum(torus_distance(hub, m, mem.width, mem.height) <= 3
                                for m in mates) for hub, _ in mem.hubs)
            far = P.HUB_FAR_MULT * max(
                v / (1 + torus_distance(dest, hub, mem.width, mem.height) / P.HUB_SCALE)
                for hub, v in mem.hubs)
            value += P.W_HUB * max(terms["hub"], far) / crowd
        if obs.length >= P.DEFEND_LEN:
            near = sum(torus_distance(dest, cell, mem.width, mem.height) <= 2
                       for cell, _ in enemy_heads)
            value -= protection * P.W_DEFEND * near * obs.length / 4
        if dest in friendly:
            value -= P.W_HEAD_TEAM
        if dest in ahead:
            value -= P.W_AHEAD
        last = latest_visit.get(dest)
        if last is not None:
            value -= P.W_REVISIT * max(0, 1 - (obs.round - last) / P.REVISIT_ROUNDS)
        near_mates = sum(torus_distance(dest, head, mem.width, mem.height) <= 2
                         for head in mates)
        value -= (P.W_FAN_EARLY if obs.round < P.FAN_ROUNDS else P.W_FAN_LATE) * near_mates
        portal = mem.nav.edges[mem.nav.edge_key(start, direction)] >= 0
        if portal:
            value -= P.W_PORTAL
            if obs.round - mem.nav.seen[dest] > P.PORTAL_STALE:
                value -= protection * P.W_PORTAL_UNSEEN
            if obs.round < P.SCOUT_ROUNDS:
                value += P.W_PORTAL_SCOUT
        if cash_target is not None:
            head, front, _ = cash_target
            value += P.W_CASH / (1 + torus_distance(dest, head,
                                                    mem.width, mem.height))
            if dest == front:
                value -= P.W_LETHAL
        value += P.W_V3 * v3[direction]
        value += P.W_STRAIGHT * (direction == obs.facing)
        scores[direction] = value
    return scores
