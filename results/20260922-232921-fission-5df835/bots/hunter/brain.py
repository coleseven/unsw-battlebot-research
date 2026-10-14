"""Hunter: aggressive. When an enemy head is close, sprint across the tile
directly in front of it so our body (not our head) ends up there, and the
enemy dies if it keeps going straight. Eats the dropped pearls. Otherwise
farms like greedy."""

import bc
import tactics


class Brain(bc.Brain):
    def cut_off(self, obs: bc.Obs) -> str | None:
        if obs.length < 4:
            return None
        danger = tactics.danger_cells(obs, self.team)
        for h in obs.enemy_heads(self.team):
            facing = obs.occ[h][3]
            if obs.edge(h, facing) != bc.OPEN:
                continue
            t = obs.step(h, facing)
            if t < 0 or obs.occ[t] is not None:
                continue
            # one step onto t, then one step out that is not next to their head
            for d1 in bc.DIRS:
                if bc.Obs.step(bc.CENTER, d1) != t or not obs.passable(bc.CENTER, d1):
                    continue
                for d2 in bc.DIRS:
                    if d2 == bc.OPPOSITE[d1] or not obs.passable(t, d2):
                        continue
                    out = obs.step(t, d2)
                    if out in danger or out == h:
                        continue
                    return "MOVE " + d1 + d2
        return None

    def turn(self, obs: bc.Obs) -> str:
        attack = self.cut_off(obs)
        if attack:
            self.extra.append("INDICATOR cut-off")
            return attack
        safe = tactics.safe_moves(obs, self.team)
        if not safe:
            return "MOVE " + obs.facing
        good = {d: s for d, s in safe.items() if s > -10}
        paths = obs.bfs()
        for _, k in tactics.pearl_targets(obs, paths):
            first = paths[k][1]
            if first in good:
                return "MOVE " + first
        # drift toward the nearest enemy to find prey
        heads = obs.enemy_heads(self.team)
        if heads and good:
            target = min(heads, key=lambda h: paths.get(h, (99,))[0])
            tr, tc = divmod(target, 7)

            def closer(d: str) -> float:
                r, c = divmod(obs.step(bc.CENTER, d), 7)
                return -(abs(r - tr) + abs(c - tc)) + good[d]

            return "MOVE " + max(good, key=closer)
        return "MOVE " + tactics.explore_dir(obs, self.rng, good or safe)
