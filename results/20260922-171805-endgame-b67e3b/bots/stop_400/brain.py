"""Change only reproduction timing; use the frozen movement after cutoff."""

import endgame_config
import movement
import reproduction


class Brain(reproduction.Brain):
    def turn(self, obs):
        cutoff = endgame_config.STOP_ROUND
        if cutoff is not None and obs.round >= cutoff:
            return movement.Brain.turn(self, obs)
        return super().turn(obs)
