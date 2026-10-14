"""Shared tactical helpers for the sparring bots (and a starting point for
ours). Everything works on the 7x7 window of a bc.Obs."""

from __future__ import annotations

from bc import CENTER, DIRS, OPPOSITE, Obs


def danger_cells(obs: Obs, team: str) -> set[int]:
    """Cells an enemy head could step into this round (head-on risk)."""
    out = set()
    for k in obs.enemy_heads(team):
        for d in DIRS:
            if obs.edge(k, d) == -1:
                n = obs.step(k, d)
                if n >= 0:
                    out.add(n)
    return out


def room(obs: Obs, start: int, cap: int = 49) -> int:
    """Flood-fill size reachable from `start` (a crude trap detector)."""
    seen = {start}
    stack = [start]
    while stack and len(seen) < cap:
        k = stack.pop()
        for d in DIRS:
            if obs.passable(k, d):
                n = obs.step(k, d)
                if n not in seen:
                    seen.add(n)
                    stack.append(n)
    return len(seen)


def edge_of_window(k: int) -> bool:
    r, c = divmod(k, 7)
    return r in (0, 6) or c in (0, 6)


def safe_moves(obs: Obs, team: str, avoid_heads: bool = True) -> dict[str, float]:
    """Score every legal single step: -inf-free dict of direction -> score.
    Higher is safer. Empty when every move is fatal."""
    danger = danger_cells(obs, team) if avoid_heads else set()
    need = min(obs.length, 12)
    out = {}
    for d in DIRS:
        if d == OPPOSITE.get(obs.facing) and obs.length > 1:
            continue
        if not obs.passable(CENTER, d):
            continue
        n = obs.step(CENTER, d)
        score = 0.0
        if n in danger:
            score -= 50.0
        space = room(obs, n, cap=need + 4)
        if space < need and not edge_of_window(n):
            score -= 20.0 * (need - space) / need
        out[d] = score
    return out


def pearl_targets(obs: Obs, paths: dict) -> list[tuple[float, int]]:
    """(cost, cell) for visible pearls and soon-to-spawn empty tiles."""
    out = []
    for k, (dist, _) in paths.items():
        if k == CENTER:
            continue
        if obs.pearl[k]:
            out.append((dist, k))
        elif 0 <= obs.pearl_in[k] <= dist + 1 and obs.occ[k] is None:
            out.append((dist + 2, k))
    out.sort()
    return out


def explore_dir(obs: Obs, rng, safe: dict[str, float]) -> str:
    """Head toward the open window border with the most spawnable tiles."""
    best, best_score = None, None
    for d, s in safe.items():
        n = obs.step(CENTER, d)
        spawn = 0
        r, c = divmod(n, 7)
        for k in range(49):
            kr, kc = divmod(k, 7)
            if abs(kr - r) + abs(kc - c) <= 3 and obs.pearl_in[k] >= 0:
                spawn += 1
        score = s + 0.3 * spawn + (0.5 if d == obs.facing else 0) + rng.random() * 0.5
        if best_score is None or score > best_score:
            best, best_score = d, score
    return best
