import baseline_brain
import guarded_safety
import guarded_config


class Brain(baseline_brain.Brain):
    def turn(self, obs):
        original = super().turn(obs)
        return guarded_safety.choose(obs, self.team, original, guarded_config.MODE)
