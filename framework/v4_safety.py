"""Experimental teammate-head guard around the frozen v3 movement ranker."""

import bc
import action_value


def threatened_by_friendly(obs, team, own_id, later_only=False):
    """Visible empty cells another friendly head could enter by an ordinary step."""
    cells = set()
    for k, part in enumerate(obs.occ):
        if not part or not part[2] or part[0] != team or part[1] == own_id:
            continue
        if later_only and part[1] < own_id:
            continue
        for d in bc.DIRS:
            if d == bc.OPPOSITE[part[3]] or obs.edge(k, d) != bc.OPEN:
                continue
            dest = obs.step(k, d)
            if dest >= 0 and obs.occ[dest] is None:
                cells.add(dest)
    return cells


def choose(obs, team, model, later_only=False):
    original = action_value.candidates(obs, team)
    if not original:
        return "MOVE " + obs.facing
    if len(original) == 1:
        return "MOVE " + original[0]
    myself = obs.occ[bc.CENTER]
    own_id = myself[1] if myself else -1
    threatened = threatened_by_friendly(obs, team, own_id, later_only)
    alternatives = [d for d in original if obs.step(bc.CENTER, d) not in threatened]
    directions = alternatives or original
    if len(directions) == 1:
        return "MOVE " + directions[0]
    _, rows = action_value.features(obs, team, directions)
    best = max(range(len(rows)), key=lambda i:
               (action_value.score(rows[i], model), directions[i] == obs.facing))
    return "MOVE " + directions[best]
