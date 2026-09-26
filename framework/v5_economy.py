"""Bounded, observation-only routing toward remembered pearl spawns.

Memory belongs to one dragon. It does not infer hidden occupancy or unseen
portal exits, and it only overrides an ordinary move when local food is scarce.
"""

import heapq

import bc
import navigation
import tactics


class Policy:
    def __init__(self, init):
        self.memory = navigation.Memory(init.width, init.height)
        # cell -> (ready_round, last_seen_round, observed_pearl_count)
        self.spawns = {}
        self.last_expanded = 0

    def update(self, obs):
        memory = self.memory
        memory.update(obs)
        for cell, k in memory.visible.items():
            if obs.pearl[k]:
                self.spawns[cell] = (obs.round, obs.round, obs.pearl[k])
            elif obs.pearl_in[k] >= 0:
                self.spawns[cell] = (obs.round + obs.pearl_in[k], obs.round, 0)
            else:
                self.spawns.pop(cell, None)
        # Old sightings are too unreliable to direct a dragon across the map.
        self.spawns = {cell: data for cell, data in self.spawns.items()
                       if obs.round - data[1] <= 40}

    def choose(self, obs, team, original):
        self.update(obs)
        self.last_expanded = 0
        if not original.startswith("MOVE ") or len(original) != 6:
            return original
        # Existing evaluator already sees food in the 7x7 window. Preserve
        # urgent local collection and reserve long routing for a food desert.
        local_paths = obs.bfs()
        if any(obs.pearl[k] and path[0] <= 3
               for k, path in local_paths.items()):
            return original
        memory = self.memory
        start = obs.y[bc.CENTER] * memory.w + obs.x[bc.CENTER]
        blocked = {cell for cell, k in memory.visible.items()
                   if obs.occ[k] is not None and cell != start}
        safe = tactics.safe_moves(obs, team)
        good = {d for d, value in safe.items() if value > -10}
        if not good:
            return original
        best_cost = {start: 0}
        queue = [(0, 0, start, "")]
        choice = None
        selected = original[-1]
        while queue and self.last_expanded < 96:
            cost, hops, cell, first = heapq.heappop(queue)
            if cost != best_cost.get(cell):
                continue
            self.last_expanded += 1
            if first and cell in self.spawns:
                ready, seen, pearls = self.spawns[cell]
                age = obs.round - seen
                wait = max(0, ready - obs.round - hops)
                # Fresh visible pearls outrank uncertain predicted respawns.
                uncertainty = 0 if age == 0 else 2 + age // 10
                value = cost + wait + uncertainty - min(3, pearls)
                option = (value, first != selected, first)
                if choice is None or option < choice:
                    choice = option
            if hops >= 14:
                continue
            for d in bc.DIRS:
                dest = memory.destination(cell, d)
                if dest is None or dest in blocked:
                    continue
                if not first:
                    if d == bc.OPPOSITE[obs.facing] and obs.length > 1:
                        continue
                    if d not in good:
                        continue
                new_cost = cost + 1 + (1 if dest not in memory.visible else 0)
                if new_cost < best_cost.get(dest, 100000):
                    best_cost[dest] = new_cost
                    heapq.heappush(queue, (new_cost, hops + 1, dest, first or d))
        # A stale/remote target should not displace the local evaluator.
        if choice is not None and choice[0] <= 14:
            return "MOVE " + choice[2]
        return original
