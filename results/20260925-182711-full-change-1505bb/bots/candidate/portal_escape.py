"""Portal last resort when no known-empty ordinary step exists.

An unseen portal exit is uncertain, not certified safe. Known occupied exits
are rejected, including our current tail. Preserve the baseline's immediate
enemy-head trade. No map memory, sprint, reproduction or RNG changes.
"""

import bc


def exit_score(obs, direction):
    """2 for a visible empty exit, 1 for unseen, -1 for visible occupied."""
    r = c = 3
    if direction in "NS":
        edges = obs.hedge
        origin = (r + (direction == "S"), c)
    else:
        edges = obs.vedge
        origin = (r, c + (direction == "E"))
    pid = edges[origin[0]][origin[1]]
    for row, entries in enumerate(edges):
        for col, value in enumerate(entries):
            if value != pid or (row, col) == origin:
                continue
            rr = row - (direction == "N")
            cc = col - (direction == "W")
            if not (0 <= rr < 7 and 0 <= cc < 7):
                return 1
            return 2 if obs.occ[rr * 7 + cc] is None else -1
    return 1


def choose(obs, team, original):
    if not original.startswith("MOVE ") or len(original.split()[1]) != 1:
        return original
    if any(obs.passable(bc.CENTER, d) for d in bc.DIRS):
        return original
    selected = original.split()[1]
    target = obs.step(bc.CENTER, selected)
    part = obs.occ[target]
    if obs.edge(bc.CENTER, selected) == bc.OPEN and part and part[2] and part[0] != team:
        return original  # leave the existing mutually lethal enemy-head trade intact
    choices = {d: exit_score(obs, d) for d in bc.DIRS if obs.edge(bc.CENTER, d) >= 0}
    choices = {d: score for d, score in choices.items() if score > 0}
    if not choices:
        return original
    best = max(choices, key=lambda d: (choices[d], d == selected))
    return "MOVE " + best
