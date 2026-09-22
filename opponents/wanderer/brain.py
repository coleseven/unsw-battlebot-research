"""Wanderer: the baseline. Random safe steps, slight preference for going
straight, eats a pearl only if it is adjacent. Anything worth submitting
should beat this nearly every game."""

import bc
import tactics


class Brain(bc.Brain):
    def turn(self, obs: bc.Obs) -> str:
        safe = tactics.safe_moves(obs, self.team, avoid_heads=False)
        if not safe:
            return "MOVE " + obs.facing
        for d in safe:
            if obs.pearl[obs.step(bc.CENTER, d)]:
                return "MOVE " + d
        best = max(safe, key=lambda d: safe[d] + (1.0 if d == obs.facing else 0) + self.rng.random() * 2)
        return "MOVE " + best
