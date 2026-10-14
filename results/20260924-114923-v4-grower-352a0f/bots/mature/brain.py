"""Frozen-v3 movement with a single local growth-role ablation."""

import bc
import v3_brain
import tactics
import adaptive_roles
import action_value
import action_model
import grower_config


class Brain(v3_brain.Brain):
    def __init__(self, init, seed=None):
        super().__init__(init, seed)
        self.v4_role = adaptive_roles.Role()

    def turn(self, obs):
        preserving = self.v4_role.update(obs, grower_config.MODE)
        if (not preserving and obs.round < 450 and obs.length >= 4 and
                obs.unit_count < self.init.unit_limit and
                bc.CENTER not in tactics.danger_cells(obs, self.team)):
            return f"SPLIT {obs.length // 2}"
        return action_value.choose(obs, self.team, action_model.MODEL)
