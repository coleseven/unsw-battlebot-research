"""Last-step guard against visible friendly and enemy head-on threats."""

import bc
import action_value
import tactics
import v4_safety


def choose(obs, team, own_id, model, original):
    if not original.startswith("MOVE ") or len(original) != 6:
        return original
    options = action_value.candidates(obs, team)
    if len(options) < 2:
        return original
    threatened = v4_safety.threatened_by_friendly(obs, team, own_id)
    threatened.update(tactics.danger_cells(obs, team))
    safe = [d for d in options if obs.step(bc.CENTER, d) not in threatened]
    if not safe or original[-1] in safe:
        return original
    if len(safe) == 1:
        return "MOVE " + safe[0]
    _, rows = action_value.features(obs, team, safe)
    best = max(range(len(safe)), key=lambda i: (
        action_value.score(rows[i], model), safe[i] == obs.facing))
    return "MOVE " + safe[best]
