"""Allow a portal override only when its actual exit is visible and empty."""

import portal_escape


def choose(obs, team, original):
    candidate = portal_escape.choose(obs, team, original)
    if candidate != original and portal_escape.exit_score(obs, candidate[-1]) == 2:
        return candidate
    return original
