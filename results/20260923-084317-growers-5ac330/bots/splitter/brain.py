"""Splitter: greedy farming plus reproduction. Splits in half whenever it
reaches SPLIT_AT, so the team spreads out and farms the whole map with many
small dragons, then wins on total length or by attrition."""

import bc
import tactics

SPLIT_AT = 8


class Brain(bc.Brain):
    def turn(self, obs: bc.Obs) -> str:
        if (obs.length >= SPLIT_AT and obs.unit_count < self.init.unit_limit
                and not tactics.danger_cells(obs, self.team) & {bc.CENTER}):
            return f"SPLIT {obs.length // 2}"
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
