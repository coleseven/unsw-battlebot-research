"""E1 population ablation: movement is an unchanged snapshot of mybot.

CAP limits living teammates, not lifetime births. Deaths allow replenishment.
The danger check is the existing splitter's heuristic, not a safety guarantee.
"""

import bc
import movement
import population_config
import tactics


class Brain(movement.Brain):
    def turn(self, obs):
        cap = population_config.CAP
        if (cap > 0 and obs.length >= 8
                and obs.unit_count < min(cap, self.init.unit_limit)
                and bc.CENTER not in tactics.danger_cells(obs, self.team)):
            return f"SPLIT {obs.length // 2}"
        return super().turn(obs)
