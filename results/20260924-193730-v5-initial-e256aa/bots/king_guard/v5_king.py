"""Observation-only protected-grower experiment; not a global king election."""

import bc
import action_value
import tactics


def candidate(obs, team):
    """A plausible king must be sizeable and have room to survive now."""
    if obs.round < 400 or obs.length < 6:
        return False
    if any(abs(k // 7 - 3) + abs(k % 7 - 3) <= 4
           for k in obs.enemy_heads(team)):
        return False
    safe = tactics.safe_moves(obs, team)
    return sum(value > -10 for value in safe.values()) >= 2 and \
        len(obs.bfs()) >= min(18, obs.length + 5)


def guarded_move(obs, team, model, original, protected=False):
    """Protect long dragons from visible head reach and shallow pockets.

    Only changes a one-step move if another known-empty ordinary step exists.
    This deliberately does not assume unseen portal exits are safe.
    """
    if not original.startswith("MOVE ") or len(original) != 6:
        return original
    if obs.length < 6 and not protected:
        return original
    options = action_value.candidates(obs, team)
    if not options:
        return original
    if len(options) == 1:
        return "MOVE " + options[0]
    danger = tactics.danger_cells(obs, team)
    safer = [d for d in options if obs.step(bc.CENTER, d) not in danger]
    if safer:
        options = safer
    if len(options) == 1:
        return "MOVE " + options[0]
    _, rows = action_value.features(obs, team, options)

    def value(i):
        d = options[i]
        dest = obs.step(bc.CENTER, d)
        continuations = sum(obs.passable(dest, nd) for nd in bc.DIRS)
        pocket = 2.0 if protected and continuations <= 1 else 0.0
        return (action_value.score(rows[i], model) - pocket,
                d == original[-1], d == obs.facing)

    return "MOVE " + options[max(range(len(options)), key=value)]
