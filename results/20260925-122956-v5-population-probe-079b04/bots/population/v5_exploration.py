"""Observation-only exploration score combined with the learned v3 mover.

The per-dragon memory stores only terrain it has actually seen. A bounded
search rewards a move that exposes a nearby unknown frontier; it never treats
unknown occupancy as safe for the immediate move.
"""

from collections import deque

import bc
import action_value
import navigation


class Policy:
    def __init__(self, init):
        self.memory = navigation.Memory(init.width, init.height)
        self.visits = {}
        self.expanded = 0

    def update(self, obs):
        self.memory.update(obs)
        cell = obs.y[bc.CENTER] * self.memory.w + obs.x[bc.CENTER]
        self.visits = {k: v for k, v in self.visits.items()
                       if obs.round - v <= 24}
        self.visits[cell] = obs.round

    def frontier(self, start, blocked, round_no):
        memory = self.memory
        queue = deque([(start, 0)])
        seen = {start}
        rewards = []
        count = 0
        while queue and count < 48:
            cell, depth = queue.popleft()
            count += 1
            age = round_no - memory.seen[cell]
            if age > 0:
                if memory.seen[cell] < 0:
                    rewards.append(1.0 / (depth + 1))
                elif age >= 20:
                    rewards.append(0.35 / (depth + 1))
            if depth >= 8:
                continue
            for direction in bc.DIRS:
                dest = memory.destination(cell, direction)
                if dest is not None and dest not in blocked and dest not in seen:
                    seen.add(dest)
                    queue.append((dest, depth + 1))
        self.expanded += count
        rewards.sort(reverse=True)
        return (rewards[0] if rewards else 0.0) + 0.2 * sum(rewards[1:7])

    def choose(self, obs, team, model):
        options = action_value.candidates(obs, team)
        if not options:
            return "MOVE " + obs.facing
        if len(options) == 1:
            return "MOVE " + options[0]
        _, rows = action_value.features(obs, team, options)
        memory = self.memory
        blocked = {cell for cell, k in memory.visible.items()
                   if obs.occ[k] is not None}
        heads = [k for k, part in enumerate(obs.occ)
                 if part and part[2] and part[0] == team and k != bc.CENTER]
        self.expanded = 0

        def score(i):
            direction = options[i]
            k = obs.step(bc.CENTER, direction)
            cell = obs.y[k] * memory.w + obs.x[k]
            frontier = self.frontier(cell, blocked, obs.round)
            last = self.visits.get(cell, -10000)
            recent = max(0.0, (20 - (obs.round - last)) / 20)
            neighbours = sum(1.0 / max(1, abs(k // 7 - h // 7) +
                                        abs(k % 7 - h % 7))
                             for h in heads
                             if abs(k // 7 - h // 7) + abs(k % 7 - h % 7) <= 2)
            fanout = 2.0 if obs.round < 40 else 0.4
            return (action_value.score(rows[i], model) +
                    3.0 * frontier - 2.0 * recent - fanout * neighbours,
                    direction == obs.facing)

        best = max(range(len(options)), key=score)
        return "MOVE " + options[best]
