"""V4 feeding baseline with beacon-only or beacon-plus-routing sonar."""

import bc
import v3_brain
import tactics
import action_value
import action_model
import sonar_config
import v4_feeding
import v4_sonar


class Brain(v3_brain.Brain):
    def __init__(self, init, seed=None):
        super().__init__(init, seed)
        self.grower = v4_feeding.is_grower(self.id, self.team)
        self.target = None

    def turn(self, obs):
        mode = sonar_config.MODE
        if mode not in ("beacon", "route"):
            raise ValueError(mode)
        for message in obs.msgs:
            packet = v4_sonar.decode(message, self.team, self.init.width, self.init.height)
            if packet and (self.target is None or packet[2] >= self.target[2]):
                self.target = (*packet, obs.round)
        if self.target and obs.round - self.target[3] > 8:
            self.target = None
        if v4_feeding.should_feed(obs, self.team, self.id):
            return ""
        cutoff = 400 if self.grower else 450
        if (obs.round < cutoff and obs.length >= 4 and
                obs.unit_count < self.init.unit_limit and
                bc.CENTER not in tactics.danger_cells(obs, self.team)):
            return f"SPLIT {obs.length // 2}"
        if (mode == "route" and self.target and obs.round >= 450 and
                obs.length <= 3 and obs.unit_count >= 12):
            action = v4_sonar.routed_move(obs, self.team, action_model.MODEL,
                                          self.target[:2], self.init.width, self.init.height)
        else:
            action = action_value.choose(obs, self.team, action_model.MODEL)
        packet = v4_sonar.beacon(obs, self.team, action)
        if packet is not None:
            self.extra.append(f"SONAR {packet}")
        return action
