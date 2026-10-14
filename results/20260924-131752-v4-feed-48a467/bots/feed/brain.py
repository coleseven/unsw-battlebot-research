"""Frozen v3 movement with protected growers and optional local feeding."""

import bc
import v3_brain
import tactics
import action_value
import action_model
import feed_config
import v4_feeding


class Brain(v3_brain.Brain):
    def __init__(self, init, seed=None):
        super().__init__(init, seed)
        self.grower = v4_feeding.is_grower(self.id, self.team)

    def turn(self, obs):
        if feed_config.FEED and v4_feeding.should_feed(obs, self.team, self.id):
            # An empty action followed by ENDTURN is the engine's no-action
            # death. The body's dropped pearls are available to nearby allies.
            return ""
        cutoff = 400 if self.grower else 450
        if (obs.round < cutoff and obs.length >= 4 and
                obs.unit_count < self.init.unit_limit and
                bc.CENTER not in tactics.danger_cells(obs, self.team)):
            return f"SPLIT {obs.length // 2}"
        return action_value.choose(obs, self.team, action_model.MODEL)
