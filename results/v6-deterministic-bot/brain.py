"""V6: one bounded search-based move decision per dragon-turn."""

import time

import action_model
import action_value
import bc
import core_king
import core_memory
import core_params as P
import core_search
import core_split
import v4_sonar


class Brain(bc.Brain):
    def __init__(self, init, seed=None):
        super().__init__(init, seed)
        self.memory = core_memory.WorldMemory(init.width, init.height, P)
        self.born_round = None
        self.hard_fallbacks = 0

    def turn(self, obs):
        started = time.perf_counter()
        self.memory.update(obs)
        if self.born_round is None:
            self.born_round = obs.round
        if P.SONAR:
            for message in obs.msgs:
                v4_sonar.decode(message, self.team, self.init.width,
                                self.init.height)
        protected = core_king.protected(obs, self.born_round, P)
        founder = 2 if self.team == "A" else 3
        portal_scout = (not protected and obs.round < P.SCOUT_ROUNDS and
                        obs.length <= P.PORTAL_SCOUT_MAXLEN and
                        self.id >= founder and
                        (self.id - founder) % P.PORTAL_SCOUT_MOD == 0)
        target = core_king.visible_target(self.memory, obs, self.team, self.id, P)
        if core_king.should_feed(self.memory, obs, self.team, target, P):
            return ""
        split = core_split.should_split(self.init, obs, self.team, P, protected)
        if split:
            return split
        if time.perf_counter() - started > P.HARD_S:
            self.hard_fallbacks += 1
            self.extra.append("LOG V6_HARD_FALLBACK")
            return action_value.choose(obs, self.team, action_model.MODEL)
        scores = core_search.score_moves(self.memory, obs, self.team, self.id,
                                         P, action_model.MODEL, protected,
                                         target, portal_scout)
        if not scores:
            if obs.length >= 4 and obs.unit_count < self.init.unit_limit:
                return f"SPLIT {obs.length - 2}"
            return self.fallback(obs)
        direction = max(scores, key=lambda d: (scores[d], d == obs.facing))
        action = "MOVE " + direction
        if P.SONAR:
            packet = v4_sonar.beacon(obs, self.team, action)
            if packet is not None:
                self.extra.append(f"SONAR {packet}")
        return action
