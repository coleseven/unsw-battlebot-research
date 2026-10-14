"""Endgame-only reproduction experiment on frozen v2 movement."""

import bc
import grower_config
import movement
import tactics


def is_grower(dragon_id, team):
    """Stable quarter-sampling of IDs; no shared state or movement RNG draw."""
    x = (dragon_id ^ (0xA341316C if team == "A" else 0xC8013EA4)) & 0xFFFFFFFF
    x = ((x ^ (x >> 16)) * 0x7FEB352D) & 0xFFFFFFFF
    x = ((x ^ (x >> 15)) * 0x846CA68B) & 0xFFFFFFFF
    x ^= x >> 16
    return x < 0x40000000


class Brain(movement.Brain):
    def __init__(self, init, seed=None):
        super().__init__(init, seed)
        self.grower = is_grower(self.id, self.team)

    def cutoff(self):
        return (grower_config.GROWER_CUTOFF if self.grower and grower_config.GROWER_CUTOFF is not None
                else grower_config.CUTOFF)

    def turn(self, obs):
        if (obs.round < self.cutoff() and obs.length >= 4
                and obs.unit_count < self.init.unit_limit
                and bc.CENTER not in tactics.danger_cells(obs, self.team)):
            return f"SPLIT {obs.length // 2}"
        return super().turn(obs)
