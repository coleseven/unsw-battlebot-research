"""Hybrid ablations: role-only OR action evaluator, never an implicit blend."""

import bc
import baseline_brain
import movement
import hybrid_config
import tactics
import adaptive_roles
import action_value
import action_model


class Brain(baseline_brain.Brain):
    def __init__(self, init, seed=None):
        super().__init__(init, seed)
        self.role = adaptive_roles.Role()

    def turn(self, obs):
        mode = hybrid_config.MODE
        if mode in ("mature", "opportunity"):
            if self.role.update(obs, mode):
                return movement.Brain.turn(self, obs)
            return super().turn(obs)
        if mode == "control":
            return super().turn(obs)
        if mode != "evaluator":
            raise ValueError(mode)
        # Exactly v2's population policy. Learning only ranks MOVE candidates.
        if (obs.round < 450 and obs.length >= 4 and
                obs.unit_count < self.init.unit_limit and
                bc.CENTER not in tactics.danger_cells(obs, self.team)):
            return f"SPLIT {obs.length // 2}"
        return action_value.choose(obs, self.team, action_model.MODEL)
