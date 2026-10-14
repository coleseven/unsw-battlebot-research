import baseline_brain
import bc
import navigation
import navigation_config


class Brain(baseline_brain.Brain):
    def __init__(self, init, seed=None):
        super().__init__(init, seed)
        self.memory = navigation.Memory(init.width, init.height, navigation_config.PORTALS)

    def turn(self, obs):
        self.memory.update(obs)
        original = super().turn(obs)
        return self.memory.choose(obs, self.team, original)
