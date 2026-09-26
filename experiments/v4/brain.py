"""Frozen v3 split rule and weights, experimental teammate-head move guard."""

import bc
import v3_brain
import tactics
import action_model
import v4_config
import v4_safety


class Brain(v3_brain.Brain):
    def turn(self, obs):
        if (obs.round < 450 and obs.length >= 4 and
                obs.unit_count < self.init.unit_limit and
                bc.CENTER not in tactics.danger_cells(obs, self.team)):
            return f"SPLIT {obs.length // 2}"
        return v4_safety.choose(obs, self.team, action_model.MODEL,
                                later_only=v4_config.LATER_ONLY)
