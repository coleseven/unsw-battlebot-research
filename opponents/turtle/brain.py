"""Turtle: survival first. Keeps well away from every other dragon, only
takes pearls that no enemy head is near, never sprints or splits. Aims to
win the round-500 tiebreak by simply never dying."""

import bc
import tactics


def _dist(a: int, b: int) -> int:
    ar, ac = divmod(a, 7)
    br, bc_ = divmod(b, 7)
    return abs(ar - br) + abs(ac - bc_)


class Brain(bc.Brain):
    def turn(self, obs: bc.Obs) -> str:
        safe = tactics.safe_moves(obs, self.team)
        if not safe:
            return "MOVE " + obs.facing
        enemies = [k for k in range(49)
                   if obs.occ[k] is not None and obs.occ[k][0] != self.team]
        heads = obs.enemy_heads(self.team)
        paths = obs.bfs()
        for dist, k in tactics.pearl_targets(obs, paths):
            if any(_dist(k, h) <= dist + 1 for h in heads):
                continue
            first = paths[k][1]
            if first in safe and safe[first] > -10:
                return "MOVE " + first

        def score(d: str) -> float:
            n = obs.step(bc.CENTER, d)
            near = min((_dist(n, e) for e in enemies), default=7)
            return safe[d] + 2.0 * near + tactics.room(obs, n) * 0.2 + self.rng.random() * 0.3

        return "MOVE " + max(safe, key=score)
