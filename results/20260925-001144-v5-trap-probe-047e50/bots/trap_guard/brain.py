"""Isolated v5 territory/protected-grower experiment on frozen v3."""

import action_model
import action_value
import v3_brain
import v4_feeding
import v4_sonar
import v5_hotspot
import v5_king
import v5_feeding
import v5_portal_push
import local_safety
import v5_config


class Brain(v3_brain.Brain):
    def __init__(self, init, seed=None):
        super().__init__(init, seed)
        self.target = None
        self.protected = False
        self.born_round = None
        self.trauma_scout = False
        self.portal_policy = v5_portal_push.Policy(init) if v5_config.PORTAL_PUSH else None

    def turn(self, obs):
        if self.born_round is None:
            self.born_round = obs.round
            if v5_config.TERRITORY:
                self.trauma_scout = v5_hotspot.trauma_start(
                    self.init, obs, self.team, self.id)
        for message in obs.msgs:
            packet = v4_sonar.decode(message, self.team, self.init.width,
                                     self.init.height)
            if packet and (self.target is None or packet[2] >= self.target[2]):
                self.target = (*packet, obs.round)
        if self.target and obs.round - self.target[3] > 8:
            self.target = None

        if ((v5_config.FEED and v5_feeding.should_feed(obs, self.team, self.id)) or
                v4_feeding.should_feed(obs, self.team, self.id)):
            return ""

        if v5_config.KING and v5_king.candidate(obs, self.team, self.id,
                                                self.born_round,
                                                v5_config.KING_START):
            self.protected = True
        if self.protected and obs.round >= v5_config.KING_START:
            action = action_value.choose(obs, self.team, action_model.MODEL)
        else:
            action = super().turn(obs)
        if v5_config.TRAP_GUARD:
            action = local_safety.choose(obs, self.team, action, "trap")
        if action.startswith("MOVE "):
            if self.trauma_scout:
                action = v5_hotspot.choose(self.init, obs, self.team, self.id,
                                           action_model.MODEL, action)
            if (self.target and obs.round >= 450 and obs.length <= 3 and
                    obs.unit_count >= 12):
                action = v4_sonar.routed_move(obs, self.team, action_model.MODEL,
                                              self.target[:2], self.init.width,
                                              self.init.height)
            if v5_config.FEED:
                action = v5_feeding.route(obs, self.team, self.id,
                                          action_model.MODEL, action)
            if self.portal_policy is not None:
                action = self.portal_policy.choose(self.init, obs, self.team,
                                                   self.id, action_model.MODEL, action)
            if v5_config.KING:
                action = v5_king.guarded_move(obs, self.team,
                                               action_model.MODEL, action,
                                               self.protected)
        elif self.portal_policy is not None:
            self.portal_policy.memory.update(obs)
        if v5_config.SONAR:
            packet = v4_sonar.beacon(obs, self.team, action)
            if packet is not None:
                self.extra.append(f"SONAR {packet}")
        return action
