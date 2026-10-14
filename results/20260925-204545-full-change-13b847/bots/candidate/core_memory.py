"""Per-dragon, observation-only world memory for the v6 search core."""

import bc
import navigation
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

    def trail_body(self, length):
        """Return newest-first own body only when the trail is long enough.

        At spawn or after growth the trail may not yet cover the whole body;
        in that case search must use observed occupancy conservatively.
        """
        if length > len(self.trail) or length > 60:
            return None
        cells = [cell for cell, _ in self.trail[-length:]][::-1]
        return cells if len(set(cells)) == len(cells) else None
