"""Conservative local feeding predicate for an isolated v4 ablation."""

import bc


def is_grower(dragon_id, team):
    """Stable quarter-sampling; same role assignment as the earlier v2 trial."""
    x = (dragon_id ^ (0xA341316C if team == "A" else 0xC8013EA4)) & 0xFFFFFFFF
    x = ((x ^ (x >> 16)) * 0x7FEB352D) & 0xFFFFFFFF
    x = ((x ^ (x >> 15)) * 0x846CA68B) & 0xFFFFFFFF
    x ^= x >> 16
    return x < 0x40000000


def distance(a, b):
    ar, ac = divmod(a, 7)
    br, bc_ = divmod(b, 7)
    return abs(ar - br) + abs(ac - bc_)


def should_feed(obs, team, own_id):
    """Die only if a visibly long ally can step onto our head's drop cell.

    Requires a nonreverse open one-step path for that ally, a healthy team,
    and no visible enemy head within three cells of either head. This is not
    a globally elected king, and the predicate deliberately favors precision
    over firing often.
    """
    if obs.round < 465 or obs.length not in (2, 3) or obs.unit_count < 12:
        return False
    for k, part in enumerate(obs.occ):
        if part and part[2] and part[0] != team and (
                distance(k, bc.CENTER) <= 3):
            return False
    segments = {}
    heads = []
    for k, part in enumerate(obs.occ):
        if not part or part[0] != team or part[1] == own_id:
            continue
        segments[part[1]] = segments.get(part[1], 0) + 1
        if part[2]:
            heads.append((k, part[1], part[3]))
    for head, did, facing in heads:
        if segments[did] < 6:
            continue
        if any(part and part[2] and part[0] != team and distance(k, head) <= 3
               for k, part in enumerate(obs.occ)):
            continue
        for direction in bc.DIRS:
            if (direction != bc.OPPOSITE[facing] and
                    obs.edge(head, direction) == bc.OPEN and
                    obs.step(head, direction) == bc.CENTER):
                return True
    return False
