"""Known-map 48x24 portal/hotspot probe, isolated from the general bot.

This is an upper-bound strategy experiment based on the two local maps with
matching geometry. It is not a general policy for unseen ranked maps.
"""

import bc
import action_value
import tactics


def eligible(init, obs, team):
    if (init.width, init.height) != (48, 24) or obs.round >= 300:
        return False
    x, y = obs.head
    return (team == "A" and x <= 20) or (team == "B" and x >= 27)


def torus_distance(x, y, tx, ty):
    dx, dy = abs(x - tx), abs(y - ty)
    return min(dx, 48 - dx) + min(dy, 24 - dy)


def choose(init, obs, team, model, original):
    if not eligible(init, obs, team) or not original.startswith("MOVE "):
        return original
    if obs.length > 5:
        return original  # keep larger dragons away from unknown portal exits
    x, y = obs.head
    outside = (team == "A" and x <= 10) or (team == "B" and x >= 37)
    # These are entry approaches, not hidden portal destinations. The paired
    # hotspot maps share this outer-wall layout; observe the edge before entry.
    target = ((10, 0) if team == "A" else (37, 23)) if outside else \
             ((11, 12) if team == "A" else (36, 11))
    options = action_value.candidates(obs, team)
    if not options:
        return original
    danger = tactics.danger_cells(obs, team)
    options = [d for d in options if obs.step(bc.CENTER, d) not in danger] or options
    # Only a short scout may deliberately cross an unknown exit. Ordinary
    # movement cannot discover a portal's destination from its near edge.
    if outside:
        crossing = "E" if team == "A" else "W"
        if obs.edge(bc.CENTER, crossing) >= 0 and obs.length <= 3 and \
                bc.CENTER not in danger:
            return "MOVE " + crossing
    _, rows = action_value.features(obs, team, options)
    before = torus_distance(x, y, *target)
    def value(i):
        d = options[i]
        dest = obs.step(bc.CENTER, d)
        after = torus_distance(obs.x[dest], obs.y[dest], *target)
        local_food = sum(obs.pearl[k] for k in obs.bfs(dest))
        return (action_value.score(rows[i], model) +
                0.8 * (before - after) + 0.15 * local_food,
                d == original[-1])
    return "MOVE " + options[max(range(len(options)), key=value)]
