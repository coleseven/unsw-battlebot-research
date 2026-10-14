"""Ablations of trap avoidance: hard head-risk guard, then own-tail lookahead.

No map-name special cases, no extra information, no new split/sprint actions.
Other bodies are static. Unknown vision boundaries remain optimistic. This is
a short-horizon heuristic, not a safety proof against moving opponents.
"""

import bc
import local_safety


def own_body(obs):
    """Order a FULLY visible body using segment-facing links, or return None.

    A segment faces the next segment toward the head. Portal links and partly
    visible bodies are deliberately not reconstructed by guessing.
    """
    head = obs.occ[bc.CENTER]
    if head is None:
        return None
    own = {k for k, part in enumerate(obs.occ) if part and part[:2] == head[:2]}
    if len(own) != obs.length:
        return None
    behind = {}
    for k in own - {bc.CENTER}:
        direction = obs.occ[k][3]
        if obs.edge(k, direction) != bc.OPEN:
            return None
        front = obs.step(k, direction)
        if front not in own or front in behind:
            return None
        behind[front] = k
    body = [bc.CENTER]
    while body[-1] in behind:
        k = behind[body[-1]]
        if k in body:
            return None
        body.append(k)
    return tuple(body) if len(body) == obs.length else None


def continuation(obs, direction, body):
    """Longest continuation up to three turns with exact own-tail release.

    Collision is tested BEFORE removing the old tail. Visible pearls and any
    pearl countdown that might mature before arrival conservatively cause
    growth. Revisited pearl cells are also assumed to regrow (safer occupancy).
    """
    fixed = {k for k, part in enumerate(obs.occ) if part is not None and k not in body}
    first = obs.step(bc.CENTER, direction)
    if obs.edge(bc.CENTER, direction) != bc.OPEN or first < 0 or first in fixed or first in body:
        return None

    def grow(k, elapsed):
        return obs.pearl[k] or 0 <= obs.pearl_in[k] <= elapsed

    body = (first,) + (body if grow(first, 0) else body[:-1])

    def search(current_body, remaining, elapsed):
        if remaining == 0:
            return 0
        best = 0
        for d in bc.DIRS:
            if obs.edge(current_body[0], d) != bc.OPEN:
                continue
            n = obs.step(current_body[0], d)
            if n < 0:
                return remaining  # matches the original unknown-boundary assumption
            if n in fixed or n in current_body:
                continue
            updated = (n,) + (current_body if grow(n, elapsed) else current_body[:-1])
            best = max(best, 1 + search(updated, remaining - 1, elapsed + 1))
            if best == remaining:
                break
        return best

    return search(body, 3, 1)


def choose(obs, team, original, mode):
    if mode not in ("head_guard", "tail_guard", "food_guard"):
        raise ValueError("unknown guarded movement mode")
    if not original.startswith("MOVE ") or len(original.split()[1]) != 1:
        return original
    selected = original.split()[1]
    view = local_safety.View(obs, team)
    profiles = {d: p for d in bc.DIRS if (p := view.profile(d)) is not None}
    if selected not in profiles:
        return original
    if mode == "tail_guard" and (body := own_body(obs)) is not None:
        for d, p in profiles.items():
            depth = continuation(obs, d, body)
            assert depth is not None
            p["score"] += 30 * (depth - p["depth"])
            p["depth"] = depth
    old = profiles[selected]
    old_danger = obs.step(bc.CENTER, selected) in view.danger
    choices = {d: p for d, p in profiles.items()
               if old_danger or obs.step(bc.CENTER, d) not in view.danger}
    if mode == "food_guard" and old["pearls"] and old["depth"] > 0:
        choices = {d: p for d, p in choices.items() if p["pearls"]}
    best = max(choices, key=lambda d: (choices[d]["score"], d == selected))
    if choices[best]["score"] >= old["score"] + 15:
        return "MOVE " + best
    return original
