"""Clean additive v3+feeding+sonar, with last-resort portal escape."""

import additive_brain
import portal_escape


class Brain(additive_brain.Brain):
    def turn(self, obs):
        original = super().turn(obs)
        return portal_escape.choose(obs, self.team, original)
