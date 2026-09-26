"""Clean additive bot plus only confirmed-visible portal escapes."""

import additive_brain
import portal_visible


class Brain(additive_brain.Brain):
    def turn(self, obs):
        original = super().turn(obs)
        return portal_visible.choose(obs, self.team, original)
