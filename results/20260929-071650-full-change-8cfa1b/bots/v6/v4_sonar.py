"""Small public king-beacon packet and optional safe-move routing."""

import bc
import action_value

MAGIC = 0xBC000000


def encode(team, x, y, length):
    if team not in "AB" or not all(0 <= v < 128 for v in (x, y, length)):
        raise ValueError("sonar field out of range")
    side = int(team == "B")
    check = (side ^ x ^ y ^ length) & 3
    return MAGIC | (side << 23) | (x << 16) | (y << 9) | (length << 2) | check


def decode(value, team, width, height):
    if not isinstance(value, int) or value < 0 or value > 0xFFFFFFFF or value >> 24 != 0xBC:
        return None
    side = (value >> 23) & 1
    x, y, length = (value >> 16) & 127, (value >> 9) & 127, (value >> 2) & 127
    if side != int(team == "B") or x >= width or y >= height or length < 6:
        return None
    if (side ^ x ^ y ^ length) & 3 != value & 3:
        return None
    return x, y, length


def distance(x, y, target, width, height):
    tx, ty = target
    dx, dy = abs(x - tx), abs(y - ty)
    return min(dx, width - dx) + min(dy, height - dy)


def routed_move(obs, team, model, target, width, height):
    directions = action_value.candidates(obs, team)
    if not directions:
        return "MOVE " + obs.facing
    if len(directions) == 1:
        return "MOVE " + directions[0]
    _, rows = action_value.features(obs, team, directions)
    before = distance(*obs.head, target, width, height)
    def value(i):
        k = obs.step(bc.CENTER, directions[i])
        after = distance(obs.x[k], obs.y[k], target, width, height)
        return (action_value.score(rows[i], model) + 1.25 * (before - after),
                directions[i] == obs.facing)
    return "MOVE " + directions[max(range(len(rows)), key=value)]


def beacon(obs, team, action):
    """Post-move coordinates for an ordinary one-step move; no split beacon."""
    if not action.startswith("MOVE ") or len(action) != 6 or obs.length < 6 or obs.round < 400:
        return None
    direction = action[-1]
    k = obs.step(bc.CENTER, direction)
    if k < 0 or obs.edge(bc.CENTER, direction) != bc.OPEN:
        return None
    return encode(team, obs.x[k], obs.y[k], min(obs.length, 127))
