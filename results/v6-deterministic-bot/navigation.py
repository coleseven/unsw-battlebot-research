"""Bounded per-dragon terrain memory; hidden occupancy is never called safe."""

import heapq
import bc
import tactics


class Memory:
    def __init__(self, width, height, portals=False):
        self.w, self.h, self.n = width, height, width * height
        self.portals = portals
        self.edges = [None] * (2 * self.n)  # horizontal, then vertical canonical edges
        self.ends = {}
        self.seen = [-10000] * self.n
        self.visited = {}
        self.food = {}
        self.visible = {}
        self.expanded = 0

    def remember(self, key, value):
        if self.edges[key] == value:
            return
        self.edges[key] = value
        if value >= 0:
            self.ends.setdefault(value, set()).add(key)

    def update(self, obs):
        w, h, n = self.w, self.h, self.n
        x0, y0 = obs.x[0], obs.y[0]
        for r, row in enumerate(obs.hedge):
            base = ((y0 + r) % h) * w
            for c, value in enumerate(row):
                self.remember(base + (x0 + c) % w, value)
        for r, row in enumerate(obs.vedge):
            base = n + ((y0 + r) % h) * w
            for c, value in enumerate(row):
                self.remember(base + (x0 + c) % w, value)
        self.visible = {obs.y[k] * w + obs.x[k]: k for k in range(49)}
        self.food = {k: v for k, v in self.food.items() if obs.round - v[2] <= 8}
        for cell, k in self.visible.items():
            self.seen[cell] = obs.round
            if obs.pearl[k] or 0 <= obs.pearl_in[k] <= 12:
                self.food[cell] = (obs.pearl[k], obs.round + obs.pearl_in[k], obs.round)
            else:
                self.food.pop(cell, None)
        self.visited = {k: v for k, v in self.visited.items() if obs.round - v <= 8}
        self.visited[obs.y[24] * w + obs.x[24]] = obs.round

    def edge_key(self, cell, d):
        x, y = cell % self.w, cell // self.w
        if d == "N":
            return cell
        if d == "S":
            return ((y+1) % self.h)*self.w + x
        if d == "W":
            return self.n + cell
        return self.n + y*self.w + (x+1) % self.w

    def destination(self, cell, d):
        key = self.edge_key(cell, d)
        value = self.edges[key]
        if value is None or value == bc.KELP:
            return None
        if value >= 0:
            ends = self.ends.get(value, ())
            if not self.portals or len(ends) != 2:
                return None
            other = next(k for k in ends if k != key)
            if (other < self.n) != (key < self.n):
                return None  # do not invent mixed-orientation portal rules
            target = other % self.n
            if d in "ES":
                return target
            x, y = target % self.w, target // self.w
            return y*self.w + (x-1) % self.w if d == "W" else ((y-1) % self.h)*self.w+x
        x, y = cell % self.w, cell // self.w
        return ((y+bc.DY[d]) % self.h)*self.w + (x+bc.DX[d]) % self.w

    def choose(self, obs, team, original):
        self.expanded = 0
        if not original.startswith("MOVE ") or len(original.split()[1]) != 1:
            return original
        safe = tactics.safe_moves(obs, team)
        good = {d for d, value in safe.items() if value > -10}
        paths = obs.bfs()
        baseline = next((cost for cost, k in tactics.pearl_targets(obs, paths)
                         if paths[k][1] in good), None)
        start = obs.y[24]*self.w + obs.x[24]
        blocked = {cell for cell, k in self.visible.items() if obs.occ[k] is not None}
        danger = {obs.y[k]*self.w + obs.x[k] for k in tactics.danger_cells(obs, team) if k >= 0}
        best = {start: 0}
        queue = [(0, 0, start, "")]
        target, frontier = None, None
        selected = original.split()[1]
        # Bounded weighted search, not a survival proof or full dynamic-body search.
        while queue and self.expanded < 96:
            cost, hops, cell, first = heapq.heappop(queue)
            if cost != best.get(cell):
                continue
            self.expanded += 1
            if first:
                sighting = self.food.get(cell)
                if sighting:
                    pearl, ready, stamp = sighting
                    if pearl or ready <= obs.round + hops + 1:
                        score = cost + (0 if pearl else 2) + (0 if cell in self.visible else 3)
                        option = (score, first != selected, first)
                        if target is None or option < target:
                            target = option
                if self.seen[cell] > -10000 and any(self.edges[self.edge_key(cell, d)] is None for d in bc.DIRS):
                    score = cost + (8 if cell in self.visited else 0)
                    option = (score, first != selected, first)
                    if frontier is None or option < frontier:
                        frontier = option
            if hops >= 12:
                continue
            for d in bc.DIRS:
                dest = self.destination(cell, d)
                if dest is None or dest in blocked:
                    continue
                portal = self.edges[self.edge_key(cell, d)] >= 0
                if not first:
                    if d == bc.OPPOSITE[obs.facing] and obs.length > 1:
                        continue
                    if portal:
                        if dest in danger:
                            continue
                    elif d not in good:
                        continue
                newcost = cost + 1 + (2 if portal else 0) + (0 if dest in self.visible else 1)
                if newcost < best.get(dest, 100000):
                    best[dest] = newcost
                    heapq.heappush(queue, (newcost, hops+1, dest, first or d))
        if target is not None and (baseline is None or target[0] + 1 < baseline):
            return "MOVE " + target[2]
        if baseline is None and target is None and frontier is not None:
            return "MOVE " + frontier[2]
        return original
