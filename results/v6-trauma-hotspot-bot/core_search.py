"""One bounded score for food, exploration, room, heads and movement.

Unknown terrain can be explored only across an observed open edge. Unknown
occupancy is neither assumed blocked nor certified safe. The current own tail
is never an immediate legal move: the engine checks collision before release.
"""

import heapq
import time

import bc
import action_value
import portal_escape


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


def legal_moves(mem, obs, team, did, portal_scout=False):
    """Immediate one-step legality, with known paired portals only."""
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
            if (portal_scout and edge >= 0 and
                    portal_escape.exit_score(obs, direction) > 0):
                out[direction] = None
            continue
        if edge == bc.OPEN:
            local = obs.step(bc.CENTER, direction)
            if local < 0 or obs.occ[local] is not None:
                continue
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


def search_one(mem, obs, team, did, dest, direction, P, own_free, t0,
               portal_scout=False):
    best = {dest: 0}
    queue = [(0, 1, dest)]  # weighted cost, actual arrival step, cell
    expanded = unseen = stale = 0
    food = 0.0
    frontier = 0.0
    while queue and expanded < P.N_SEARCH:
        if time.perf_counter() - t0 > P.SOFT_S:
            break
        cost, arrival, cell = heapq.heappop(queue)
        if cost != best.get(cell):
            continue
        expanded += 1
        food = max(food, food_value(mem, obs, cell, arrival - 1, P))
        seen_round = mem.nav.seen[cell]
        unseen += seen_round < 0
        stale += seen_round >= 0 and obs.round - seen_round >= P.STALE_ROUNDS
        if portal_scout:
            for step in bc.DIRS:
                edge = mem.nav.edges[mem.nav.edge_key(cell, step)]
                if edge is not None and edge >= 0 and len(mem.nav.ends[edge]) < 2:
                    frontier = max(frontier, P.W_PORTAL_FRONTIER / (1 + cost))
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
    return {"food": food, "unseen": unseen, "stale": stale,
            "room": len(best), "exits": exits, "expanded": expanded,
            "frontier": frontier}


def score_moves(mem, obs, team, did, P, model, protected=False,
                cash_target=None, started=None, portal_scout=False,
                hotspot_scout=False):
    """Return one combined numeric score for every legal immediate move."""
    moves = legal_moves(mem, obs, team, did, portal_scout)
    if not moves:
        return {}
    started = time.perf_counter() if started is None else started
    directions = list(moves)
    ordinary = [d for d in directions if moves[d] is not None]
    _, rows = action_value.features(obs, team, ordinary)
    v3 = {d: action_value.score(row, model) for d, row in zip(ordinary, rows)}
    enemy, friendly, ahead, mates = head_threats(mem, obs, team, did)
    own_free = own_free_times(mem, obs)
    latest_visit = {cell: round_no for cell, round_no in mem.trail}
    start = mem.cell(*obs.head)
    scores = {}
    pocket_target = None
    if portal_scout and (mem.width, mem.height) == (48, 24):
        x, _ = obs.head
        if team == "A" and x <= 10:
            pocket_target = mem.cell(10, 0)
        elif team == "B" and x >= 37:
            pocket_target = mem.cell(37, 23)
    hotspot_target = None
    if hotspot_scout and (mem.width, mem.height) == (48, 24):
        x, _ = obs.head
        if team == "A" and 11 <= x <= 20:
            hotspot_target = mem.cell(11, 12)
        elif team == "B" and 27 <= x <= 36:
            hotspot_target = mem.cell(36, 11)
    protection = P.PROTECT_MULT if protected else 1.0
    margin = P.SPACE_MARGIN * (P.ENDGAME_SPACE_MULT if obs.round >= 400 else 1.0)
    need = min(P.SPACE_MULT * obs.length + margin, P.SPACE_CAP)
    for direction, dest in moves.items():
        if dest is None:
            scores[direction] = P.W_PORTAL_UNKNOWN * (
                1.0 if portal_escape.exit_score(obs, direction) == 2 else 0.75)
            continue
        terms = search_one(mem, obs, team, did, dest, direction, P,
                           own_free, started, portal_scout)
        room = min(terms["room"], need)
        value = terms["food"] * (P.PROTECT_FOOD_MULT if protected else 1.0)
        value += terms["frontier"]
        if pocket_target is not None:
            value += P.W_POCKET_ROUTE * (
                torus_distance(start, pocket_target, mem.width, mem.height) -
                torus_distance(dest, pocket_target, mem.width, mem.height))
        if hotspot_target is not None:
            value += P.W_HOTSPOT_ROUTE * (
                torus_distance(start, hotspot_target, mem.width, mem.height) -
                torus_distance(dest, hotspot_target, mem.width, mem.height))
        value += (P.W_UNSEEN * terms["unseen"] +
                  P.W_STALE * terms["stale"]) / P.N_SEARCH
        value -= protection * P.W_TRAP * max(0, need - room)
        if room < obs.length + 2:
            value -= protection * P.W_LETHAL
        if terms["exits"] == 0:
            value -= P.W_DEADEND
        elif terms["exits"] == 1:
            value -= P.W_CORRIDOR
        if dest in enemy:
            value -= protection * P.W_HEAD_ENEMY * max(1, obs.length / 4)
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
