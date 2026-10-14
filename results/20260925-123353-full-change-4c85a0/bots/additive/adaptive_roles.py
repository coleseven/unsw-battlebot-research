"""Local, hysteretic growth roles; no globally elected champion is implied."""


class Role:
    def __init__(self):
        self.preserving = False
        self.adoptions = 0
        self.releases = 0

    def update(self, obs, mode):
        if mode not in ("mature", "opportunity"):
            raise ValueError(mode)
        if self.preserving and (obs.unit_count < 8 or obs.length < 4):
            self.preserving = False
            self.releases += 1
        if not self.preserving:
            eligible = obs.round >= 200 and obs.unit_count >= 16 and obs.length >= 8
            if mode == "opportunity":
                # Local food opportunity, not an ID lottery. Retain the role
                # after leaving this food patch unless the population collapses.
                local_food = sum(obs.pearl[k] and obs.occ[k] is None for k in range(49))
                eligible = (obs.round >= 250 and obs.unit_count >= 16 and
                            obs.length >= 4 and local_food >= 3)
            if eligible:
                self.preserving = True
                self.adoptions += 1
        return self.preserving
