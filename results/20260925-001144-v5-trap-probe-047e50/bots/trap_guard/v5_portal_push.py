"""Sparse early portal exploration plus bounded remembered-portal routing.

Only short explorers are pulled toward the known 48x24 pocket exits. Once a
dragon has seen both endpoints of a portal, the existing bounded navigation
memory can include it as a passage for food/frontier routing on any map.
"""

import bc
import action_value
import navigation
import portal_escape
import tactics


def explorer(team, did):
    founder = 2 if team == "A" else 3
    return did >= founder and (did - founder) % 8 == 0


def pocket_route(init, obs, team, did, model, original):
    if ((init.width, init.height) != (48, 24) or obs.round >= 120 or
            obs.length > 4 or not explorer(team, did) or
            not original.startswith("MOVE ") or len(original) != 6):
        return original
    x, y = obs.head
    if not ((team == "A" and x <= 10) or (team == "B" and x >= 37)):
        return original
    target = (10, 0) if team == "A" else (37, 23)
    crossing = "E" if team == "A" else "W"
    if obs.edge(bc.CENTER, crossing) >= 0 and \
            portal_escape.exit_score(obs, crossing) > 0:
        return "MOVE " + crossing
    options = action_value.candidates(obs, team)
    if len(options) < 2:
        return original
    danger = tactics.danger_cells(obs, team)
    options = [d for d in options if obs.step(bc.CENTER, d) not in danger]
    if not options:
        return original
    _, rows = action_value.features(obs, team, options)
    before = abs(x - target[0]) + abs(y - target[1])
    best = max(range(len(options)), key=lambda i: (
        action_value.score(rows[i], model) +
        1.2 * (before - (abs(obs.x[obs.step(bc.CENTER, options[i])] - target[0]) +
                         abs(obs.y[obs.step(bc.CENTER, options[i])] - target[1]))),
        options[i] == original[-1]))
    return "MOVE " + options[best]


class Policy:
    def __init__(self, init):
        self.memory = navigation.Memory(init.width, init.height, portals=True)

    def choose(self, init, obs, team, did, model, original):
        self.memory.update(obs)
        routed = pocket_route(init, obs, team, did, model, original)
        if routed != original:
            return routed
        if any(len(ends) == 2 for ends in self.memory.ends.values()):
            return self.memory.choose(obs, team, original)
        return original
