"""Phase-aware splitting ablations with unchanged frozen-v3 movement."""

import bc
import v3_brain
import tactics
import action_value
import action_model
import phase_config


class Brain(v3_brain.Brain):
    def turn(self, obs):
        mode = phase_config.MODE
        if mode == "global_300":
            cutoff = 300
        elif mode == "reserve_300":
            cutoff = 300 if self.init.id % 7 == 0 else 450
        else:
            raise ValueError(mode)
        if (obs.round < cutoff and obs.length >= 4 and
                obs.unit_count < self.init.unit_limit and
                bc.CENTER not in tactics.danger_cells(obs, self.team)):
            return f"SPLIT {obs.length // 2}"
        return action_value.choose(obs, self.team, action_model.MODEL)
