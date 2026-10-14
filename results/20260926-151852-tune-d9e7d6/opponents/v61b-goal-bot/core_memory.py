"""Per-dragon, observation-only world memory for the v6 search core."""

import bc
import navigation
import v6_hub_book
import v6_portal_book


class WorldMemory:
    def __init__(self, width, height, params):
        self.width, self.height = width, height
        self.nav = navigation.Memory(width, height, portals=True)
        self.params = params
        self.spawn = {}       # cell -> (predicted_ready_round, last_seen_round)
        self.pearl = {}       # cell -> last_seen_round
        self.occupied = {}    # cell -> (team, id, is_head, facing, last_seen_round)
        self.trail = []       # (absolute_head_cell, round), oldest first
        self.last_round = None
        # Official-map portal pairs; used only to complete a pair after this
        # dragon has itself seen one end with the same id at the same edge.
        self.book = (v6_portal_book.BOOK.get((width, height), ())
                     if getattr(params, "PORTAL_BOOK", False) else ())
        self.book_done = set()
        # Official-map pearl hubs: a map stays a candidate only while every
        # visible edge (open vs kelp/portal) matches its static layout.
        self.hub_maps = ([(int(bits, 16), hubs) for bits, hubs in
                          v6_hub_book.BOOK.get((width, height), ())]
                         if getattr(params, "HUB_BOOK", False) else [])
        self.hubs = []
        self.hub_area = {}
        # spawn tile -> largest countdown seen: an instant estimate of how
        # slowly it respawns (a short-timer tile is rich)
        self.timer_max = {}
        self.local_rate = None   # mean estimated respawn rate of tiles in view
        # exploration: last round each SECTOR x SECTOR block was seen, and this
        # dragon's current goal cell
        sec = getattr(params, "SECTOR", 8)
        self.sec_w, self.sec_h = -(-width // sec), -(-height // sec)
        self.sector_seen = [-10000] * (self.sec_w * self.sec_h)
        self.goal = None
        self.goal_round = -10000

    def cell(self, x, y):
        return y * self.width + x

    def update(self, obs):
        """Update exactly once per turn, including split and feed decisions."""
        if self.last_round == obs.round:
            raise ValueError("world memory updated twice in one round")
        self.last_round = obs.round
        self.nav.update(obs)
        if self.book:
            self.apply_book()
        visible = self.nav.visible
        if self.hub_maps:
            self.identify_map(obs, visible)
        sec = getattr(self.params, "SECTOR", 8)
        rates = []
        for cell, k in visible.items():
            self.sector_seen[(cell // self.width // sec) * self.sec_w +
                             (cell % self.width) // sec] = obs.round
            timer = obs.pearl_in[k]
            if timer >= 0:
                if timer > self.timer_max.get(cell, -1):
                    self.timer_max[cell] = timer
                rates.append(1.0 / (1 + self.timer_max[cell]))
        self.local_rate = sum(rates) / len(rates) if rates else None
        if getattr(self.params, "LEARN_HUBS", False) and not self.hub_maps:
            self.learn_hubs(obs)
        for cell, k in visible.items():
            if obs.pearl_in[k] >= 0:
                self.spawn[cell] = (obs.round + obs.pearl_in[k], obs.round)
            else:
                self.spawn.pop(cell, None)
            if obs.pearl[k]:
                self.pearl[cell] = obs.round
            else:
                self.pearl.pop(cell, None)
            self.occupied.pop(cell, None)
        for team, did, x, y, facing, is_head in obs.bodies:
            cell = self.cell(x, y)
            self.occupied[cell] = (team, did, is_head, facing, obs.round)
        self.pearl = {cell: seen for cell, seen in self.pearl.items()
                      if obs.round - seen <= self.params.PEARL_TTL}
        self.occupied = {cell: part for cell, part in self.occupied.items()
                         if obs.round - part[4] <= self.params.OCC_TTL}
        head = self.cell(obs.x[bc.CENTER], obs.y[bc.CENTER])
        self.trail.append((head, obs.round))
        if len(self.trail) > 60:
            self.trail = self.trail[-60:]

    def apply_book(self):
        """Add a portal's far end when every book map agrees on it."""
        for pid, keys in self.nav.ends.items():
            if pid in self.book_done or len(keys) != 1:
                continue
            key = next(iter(keys))
            partners = {pair[1] if pair[0] == key else pair[0]
                        for pair in (m.get(pid) for m in self.book)
                        if pair is not None and key in pair}
            self.book_done.add(pid)
            if len(partners) == 1:
                keys.add(partners.pop())

    def identify_map(self, obs, visible):
        w, h, n = self.width, self.height, self.width * self.height
        x0, y0 = obs.x[0], obs.y[0]
        seen = []
        for r, row in enumerate(obs.hedge):
            base = ((y0 + r) % h) * w
            seen += [(base + (x0 + c) % w, v != bc.OPEN) for c, v in enumerate(row)]
        for r, row in enumerate(obs.vedge):
            base = n + ((y0 + r) % h) * w
            seen += [(base + (x0 + c) % w, v != bc.OPEN) for c, v in enumerate(row)]
        self.hub_maps = [(bits, hubs) for bits, hubs in self.hub_maps
                         if all(((bits >> key) & 1) == closed for key, closed in seen)]
        choices = {tuple(hubs) for _, hubs in self.hub_maps}
        self.set_hubs(list(choices.pop()) if len(choices) == 1 else [])

    def set_hubs(self, hubs):
        if hubs == self.hubs:
            return
        self.hubs = hubs
        w, h = self.width, self.height
        self.hub_area = {}
        for hub, value in hubs:
            x, y = hub % w, hub // w
            for dy in (-2, -1, 0, 1, 2):
                for dx in (-2, -1, 0, 1, 2):
                    cell = ((y + dy) % h) * w + (x + dx) % w
                    if value > self.hub_area.get(cell, 0.0):
                        self.hub_area[cell] = value

    def learn_hubs(self, obs):
        """No book map fits: hubs from respawn rates estimated from countdowns."""
        P = self.params
        if obs.round % P.LEARN_EVERY or not self.timer_max:
            return
        rate = {c: 1.0 / (1 + t) for c, t in self.timer_max.items()}
        w, h = self.width, self.height
        local = {}
        for c in rate:
            x, y = c % w, c // w
            local[c] = sum(rate.get(((y + dy) % h) * w + (x + dx) % w, 0.0)
                           for dy in (-2, -1, 0, 1, 2) for dx in (-2, -1, 0, 1, 2))
        mean = sum(local.values()) / len(local)
        best = max(local.values())
        hubs = []
        for c, v in sorted(local.items(), key=lambda kv: -kv[1]):
            if len(hubs) >= 4 or v <= 0 or v < 2 * mean:
                break
            if all(max(min(abs(c % w - q % w), w - abs(c % w - q % w)),
                       min(abs(c // w - q // w), h - abs(c // w - q // w))) >= 5
                   for q, _ in hubs):
                hubs.append((c, round(v / best, 3)))
        self.set_hubs(hubs)

    def update_goal(self, obs, did):
        """Keep or pick this dragon's exploration goal: the centre of a stale or
        unseen block, preferring nearby blocks, with a per-dragon offset so
        teammates spread over different blocks."""
        P = self.params
        sec = P.SECTOR
        if self.goal is not None:
            gs = (self.goal // self.width // sec) * self.sec_w + (self.goal % self.width) // sec
            fresh = obs.round - self.sector_seen[gs] <= 1
            if not fresh and obs.round - self.goal_round < P.GOAL_EVERY:
                return
        hx, hy = obs.head
        w, h = self.width, self.height
        best, best_score = None, None
        for sy in range(self.sec_h):
            for sx in range(self.sec_w):
                cx, cy = min(sx * sec + sec // 2, w - 1), min(sy * sec + sec // 2, h - 1)
                age = min(obs.round - self.sector_seen[sy * self.sec_w + sx], P.GOAL_STALE_CAP)
                if age <= 1:
                    continue
                dx, dy = abs(cx - hx), abs(cy - hy)
                dist = min(dx, w - dx) + min(dy, h - dy)
                noise = ((did * 2654435761 + (sy * self.sec_w + sx) * 40503) >> 7) % 1000 / 1000
                score = age - P.GOAL_DIST_W * dist + P.GOAL_NOISE * noise
                if best_score is None or score > best_score:
                    best, best_score = cy * w + cx, score
        self.goal, self.goal_round = best, obs.round

    def trail_body(self, length):
        """Return newest-first own body only when the trail is long enough.

        At spawn or after growth the trail may not yet cover the whole body;
        in that case search must use observed occupancy conservatively.
        """
        if length > len(self.trail) or length > 60:
            return None
        cells = [cell for cell, _ in self.trail[-length:]][::-1]
        return cells if len(set(cells)) == len(cells) else None
