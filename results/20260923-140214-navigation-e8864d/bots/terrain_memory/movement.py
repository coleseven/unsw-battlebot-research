"""mybot: our bot. Starts as a copy of the greedy sparring bot (BFS to the
nearest pearl, avoid enemy heads and traps); improve from here."""

import bc
import tactics


class Brain(bc.Brain):
    def turn(self, obs: bc.Obs) -> str:
        safe = tactics.safe_moves(obs, self.team)
        if not safe:
            return "MOVE " + obs.facing
        good = {d: s for d, s in safe.items() if s > -10}
        paths = obs.bfs()
        for _, k in tactics.pearl_targets(obs, paths):
            first = paths[k][1]
            if first in good:
                return "MOVE " + first
        return "MOVE " + tactics.explore_dir(obs, self.rng, good or safe)
