"""Observation-gated Queen opening: send founders to the fast spawn clusters."""

import bc
import action_value
import tactics


STARTS = {
    ("A", 0): ((5, 11), (15, 2)),
    ("A", 2): ((2, 9), (8, 32)),
    ("B", 1): ((19, 23), (8, 32)),
    ("B", 3): ((22, 25), (15, 2)),
}


def distance(point, target, width, height):
    dx = abs(point[0] - target[0])
    dy = abs(point[1] - target[1])
    return min(dx, width - dx) + min(dy, height - dy)


class Policy:
    def __init__(self, init):
        self.width, self.height = init.width, init.height
        self.key = (init.team, init.id)
        self.target = None
        self.arrived = False

    def choose(self, obs, team, model, original):
        if (self.width, self.height) != (25, 35) or self.key not in STARTS:
            return original
        if obs.round == 0:
            start, target = STARTS[self.key]
            if obs.head == start:
                self.target = target
        if (self.target is None or self.arrived or obs.round >= 80 or
                obs.length > 6 or not original.startswith("MOVE ") or
                len(original) != 6):
            return original
        before = distance(obs.head, self.target, self.width, self.height)
        if before <= 2:
            self.arrived = True
            return original
        safe = tactics.safe_moves(obs, team)
        options = [d for d, value in safe.items() if value > -10]
        if not options:
            return original
        _, rows = action_value.features(obs, team, options)
        def value(i):
            d = options[i]
            k = obs.step(bc.CENTER, d)
            after = distance((obs.x[k], obs.y[k]), self.target,
                             self.width, self.height)
            return (action_value.score(rows[i], model) + 3.0 * (before - after),
                    d == original[-1])
        best = options[max(range(len(options)), key=value)]
        return "MOVE " + best
