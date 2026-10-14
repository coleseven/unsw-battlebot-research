"""Reproduction-size ablation; frozen greedy movement and round-450 cutoff."""

import bc
import fission_config
import movement
import tactics


class Brain(movement.Brain):
    def turn(self, obs):
        if (obs.round < 450 and obs.length >= fission_config.THRESHOLD
                and obs.unit_count < self.init.unit_limit
                and bc.CENTER not in tactics.danger_cells(obs, self.team)):
            child = 2 if fission_config.SMALL_CHILD else obs.length // 2
            return f"SPLIT {child}"
        return super().turn(obs)
