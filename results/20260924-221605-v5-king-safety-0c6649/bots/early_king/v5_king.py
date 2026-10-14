"""Observation-only protected-grower experiment; not a global king election."""

import bc
import action_value
import tactics


def selected_id(did, team):
    """Sparse, stable election without public sonar or shared global memory."""
    x = (did ^ (0xA341316C if team == "A" else 0xC8013EA4)) & 0xFFFFFFFF
    x = ((x ^ (x >> 16)) * 0x7FEB352D) & 0xFFFFFFFF
    x = ((x ^ (x >> 15)) * 0x846CA68B) & 0xFFFFFFFF
    x ^= x >> 16
    return x < 0x20000000  # one eighth, versus the failed one-quarter trial


def candidate(obs, team, did, born_round):
    """Protect a pre-existing, safely located dragon before it grows long.

    Larger late survivors are a fallback if all early electees perish. This
    only establishes local candidates; actual one-king coordination remains
    a separate experiment.
    """
    early = 400 <= obs.round <= 420 and born_round < 400 and selected_id(did, team)
    backup = obs.round >= 450 and obs.length >= 6
    if not (early or backup):
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
