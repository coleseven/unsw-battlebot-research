"""One v6 split schedule with v3's visible head-danger legality guard."""

import bc
import tactics


def should_split(init, obs, team, P, protected=False):
    if obs.length < P.SPLIT_AT or obs.length < P.CHILD + 2:
        return None
    if obs.unit_count >= min(P.CAP, init.unit_limit):
        return None
    if bc.CENTER in tactics.danger_cells(obs, team):
        return None
    cutoff = (P.SPLIT_UNTIL_SMALL if init.width * init.height < P.AREA_SPLIT
              else P.SPLIT_UNTIL_LARGE)
    late = obs.round > cutoff
    # Protected growers only refill a thin team before the cutoff; afterwards
    # they must keep their length (they are the longest-dragon tiebreak).
    if protected and (late or obs.unit_count >= P.FLOOR):
        return None
    # The low-population refill stops at FLOOR_UNTIL, so late feeding, which
    # deliberately thins the team, cannot trigger a wave of re-splitting.
    if late and (obs.unit_count >= P.FLOOR or obs.round >= P.FLOOR_UNTIL):
        return None
    return f"SPLIT {P.CHILD}"
