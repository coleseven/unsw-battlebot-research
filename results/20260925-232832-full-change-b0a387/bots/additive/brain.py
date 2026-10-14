"""Frozen v3 policy plus local feeding and late-game sonar routing.

Unlike sonar_brain, this does not alter v3's population/split decision.
"""

import v3_brain
import action_model
import v4_feeding
import v4_sonar


class Brain(v3_brain.Brain):
    def __init__(self, init, seed=None):
        super().__init__(init, seed)
        self.target = None

    def turn(self, obs):
        for message in obs.msgs:
            packet = v4_sonar.decode(message, self.team, self.init.width, self.init.height)
            if packet and (self.target is None or packet[2] >= self.target[2]):
                self.target = (*packet, obs.round)
        if self.target and obs.round - self.target[3] > 8:
            self.target = None

        if v4_feeding.should_feed(obs, self.team, self.id):
            return ""

        # Let the frozen v3 policy decide splitting and its ordinary move.
        action = super().turn(obs)
        if (action.startswith("MOVE ") and self.target and obs.round >= 450 and
                obs.length <= 3 and obs.unit_count >= 12):
            action = v4_sonar.routed_move(obs, self.team, action_model.MODEL,
                                          self.target[:2], self.init.width, self.init.height)
        packet = v4_sonar.beacon(obs, self.team, action)
        if packet is not None:
            self.extra.append(f"SONAR {packet}")
        return action
