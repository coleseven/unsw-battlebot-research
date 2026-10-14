import baseline_brain
import bc
import portal_escape


class Brain(baseline_brain.Brain):
    def turn(self, obs):
        original = super().turn(obs)
        return portal_escape.choose(obs, self.team, original)
