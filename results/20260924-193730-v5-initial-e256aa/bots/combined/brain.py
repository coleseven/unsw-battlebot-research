"""Isolated v5 territory/protected-grower experiment on frozen v3."""

import action_model
import action_value
import v3_brain
import v4_feeding
import v4_sonar
import v5_hotspot
import v5_king
import v5_config


class Brain(v3_brain.Brain):
    def __init__(self, init, seed=None):
        super().__init__(init, seed)
        self.target = None
        self.protected = False
        self.collector = False

    def turn(self, obs):
        for message in obs.msgs:
            packet = v4_sonar.decode(message, self.team, self.init.width,
                                     self.init.height)
            if packet and (self.target is None or packet[2] >= self.target[2]):
                self.target = (*packet, obs.round)
        if self.target and obs.round - self.target[3] > 8:
            self.target = None

        if (v5_config.TERRITORY and
                v5_hotspot.scout(self.init, self.team, self.id) and
                not ((self.team == "A" and obs.head[0] <= 10) or
                     (self.team == "B" and obs.head[0] >= 37))):
            self.collector = True

        if not self.collector and v4_feeding.should_feed(obs, self.team, self.id):
            return ""

        if v5_config.KING and v5_king.candidate(obs, self.team):
            self.protected = True
        if self.collector or (self.protected and obs.round >= 400):
            action = action_value.choose(obs, self.team, action_model.MODEL)
        else:
            action = super().turn(obs)
        if action.startswith("MOVE "):
            if v5_config.TERRITORY:
                action = v5_hotspot.choose(self.init, obs, self.team, self.id,
                                           action_model.MODEL, action)
            if (not self.collector and self.target and obs.round >= 450 and obs.length <= 3 and
                    obs.unit_count >= 12):
                action = v4_sonar.routed_move(obs, self.team, action_model.MODEL,
                                              self.target[:2], self.init.width,
                                              self.init.height)
            if v5_config.KING or self.collector:
                action = v5_king.guarded_move(obs, self.team,
                                               action_model.MODEL, action,
                                               self.protected or self.collector)
        packet = v4_sonar.beacon(obs, self.team, action)
        if packet is not None:
            self.extra.append(f"SONAR {packet}")
        return action
