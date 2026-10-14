"""Local, conservative feeder-to-king rendezvous experiment."""

import bc
import action_value
import tactics


def distance(a, b):
    ar, ac = divmod(a, 7)
    br, bc_ = divmod(b, 7)
    return abs(ar - br) + abs(ac - bc_)


def visible_kings(obs, team, own_id):
    segments = {}
    heads = []
    for k, part in enumerate(obs.occ):
        if not part or part[0] != team or part[1] == own_id:
            continue
        segments[part[1]] = segments.get(part[1], 0) + 1
        if part[2]:
            heads.append((k, part[1], part[3]))
    return [(k, did, facing, segments[did]) for k, did, facing in heads
            if segments[did] >= 6]


def enemy_near(obs, team, cells, radius=3):
    return any(part and part[2] and part[0] != team and
               any(distance(k, c) <= radius for c in cells)
               for k, part in enumerate(obs.occ))


def should_feed(obs, team, own_id):
    """Die only where a visible large ally can collect, never under threat."""
    if obs.round < 440 or obs.length not in (2, 3, 4) or obs.unit_count < 12:
        return False
    for head, _, facing, size in visible_kings(obs, team, own_id):
        if size < obs.length + 3 or enemy_near(obs, team, (bc.CENTER, head)):
            continue
        if any(d != bc.OPPOSITE[facing] and
               obs.edge(head, d) == bc.OPEN and
               obs.step(head, d) == bc.CENTER for d in bc.DIRS):
            return True
    return False


def route(obs, team, own_id, model, original):
    """Nudge a short dragon toward a visible king's *safe approach* cell."""
    if (obs.round < 430 or obs.length not in (2, 3, 4) or
            obs.unit_count < 12 or not original.startswith("MOVE ") or
            len(original) != 6):
        return original
    kings = [(k, size) for k, _, _, size in visible_kings(obs, team, own_id)
             if not enemy_near(obs, team, (bc.CENTER, k))]
    if not kings:
        return original
    head = max(kings, key=lambda x: (x[1], -distance(x[0], bc.CENTER)))[0]
    if distance(head, bc.CENTER) <= 1:
        return original  # adjacent feeding predicate, not routing, handles it
    paths = obs.bfs()
    approach = [obs.step(head, d) for d in bc.DIRS
                if obs.edge(head, d) == bc.OPEN and
                obs.step(head, d) in paths and
                obs.occ[obs.step(head, d)] is None]
    if not approach:
        return original
    target = min(approach, key=lambda k: paths[k][0])
    options = action_value.candidates(obs, team)
    if len(options) < 2:
        return original
    threatened = tactics.danger_cells(obs, team)
    options = [d for d in options if obs.step(bc.CENTER, d) not in threatened]
    if not options:
        return original
    _, rows = action_value.features(obs, team, options)
    route_dir = paths[target][1]
    best = max(range(len(options)), key=lambda i: (
        action_value.score(rows[i], model) + (1.0 if options[i] == route_dir else 0.0),
        options[i] == original[-1]))
    return "MOVE " + options[best]
