"""Movement-only wrapper around the frozen round-450 baseline."""

import baseline_brain
import local_safety
import movement_config


class Brain(baseline_brain.Brain):
    def turn(self, obs):
        original = super().turn(obs)
        return local_safety.choose(obs, self.team, original, movement_config.MODE)
