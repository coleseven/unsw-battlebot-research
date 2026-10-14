"""Bounded, conservative local geometry for movement experiments.

This is not a full simulator: visible bodies stay blocked, portals/unknown
destinations are refused, and an open vision boundary is only potential room.
Enemy danger uses the original one-step heuristic (not enemy sprint search).
"""

import bc
import tactics


class View:
    def __init__(self, obs, team):
        self.obs = obs
        self.danger = tactics.danger_cells(obs, team)
        self.next = [{} for _ in range(49)]
        self.boundary = set()
        for k in range(49):
            for d in bc.DIRS:
                if obs.edge(k, d) != bc.OPEN:
                    continue
                n = obs.step(k, d)
                if n < 0:
                    self.boundary.add(k)
                elif obs.occ[n] is None:
                    self.next[k][d] = n

    def profile(self, path):
        """Check EVERY step; score the endpoint and three-step continuation.

        Conservatively reserve sprint cost without relying on future pearls.
        Never traverse old bodies or revisit a new path cell, even if a more
        complete tail simulation could permit it. Other dragons cannot move
        between sprint steps, but may threaten the final endpoint afterward.
        """
        if not path or any(d not in bc.DIRS for d in path):
            return None
        if len(path) > 1 and self.obs.length < len(path) + 1:
            return None
        current, cells = bc.CENTER, []
        for d in path:
            n = self.next[current].get(d)
            if n is None or n == bc.CENTER or n in cells:
                return None
            cells.append(n)
            current = n
        blocked = set(cells[:-1])
        pearls = sum(self.obs.pearl[k] for k in cells)
        length = self.obs.length + pearls - (len(path) - 1)
        need = min(length, 24)
        seen, stack = {current}, [current]
        opens = current in self.boundary
        while stack and len(seen) < need and not opens:
            k = stack.pop()
            for n in self.next[k].values():
                if n not in seen and n not in blocked:
                    seen.add(n)
                    stack.append(n)
                    opens |= n in self.boundary
        exits = sum(n not in blocked for n in self.next[current].values())

        def depth(k, trail, remaining):
            if remaining == 0 or k in self.boundary:
                return remaining
            best = 0
            for n in self.next[k].values():
                if n not in trail and n not in blocked:
                    value = 1 + depth(n, trail | {n}, remaining - 1)
                    best = max(best, value)
                    if best == remaining:
                        break
            return best

        reach = depth(current, {current}, 3)
        deficit = 0 if opens else max(0, need - len(seen)) / max(1, need)
        score = -30 * (3 - reach) - 30 * deficit - (60 if current in self.danger else 0)
        return {"score": score, "exits": exits, "pearls": pearls,
                "room": len(seen), "open_boundary": opens, "depth": reach}


def choose(obs, team, original, mode):
    """Independent ablations: neither changes split actions or the other mode."""
    if mode not in ("trap", "sprint"):
        raise ValueError("unknown movement experiment")
    if not original.startswith("MOVE ") or len(original.split()[1]) != 1:
        return original
    if mode == "sprint" and obs.length < 3:
        return original
    view = View(obs, team)
    singles = {d: p for d in bc.DIRS if (p := view.profile(d)) is not None}
    if not singles:
        return original  # no sprint can bypass a blocked first step
    if mode == "trap":
        selected = original.split()[1]
        best = max(singles, key=lambda d: (singles[d]["score"], d == selected))
        old_score = singles.get(selected, {}).get("score", -1000)
        if singles[best]["score"] >= old_score + 15:
            return "MOVE " + best
        return original
    # Emergency sprint ONLY: do not substitute a different normal move.
    if max(p["score"] for p in singles.values()) > -15:
        return original
    choices = []
    for d1 in singles:
        for d2 in bc.DIRS:
            p = view.profile(d1 + d2)
            if p is not None and p["score"] >= 0:
                choices.append(((p["exits"], p["pearls"], d1 == obs.facing), d1 + d2))
    if choices:
        # Stable iteration order resolves exact ties; never consumes bot RNG.
        return "MOVE " + max(choices, key=lambda item: item[0])[1]
    return original
