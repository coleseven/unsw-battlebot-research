"""Turn a bc.Obs into fixed-size numpy features: the shared input format for
models trained on the GPU and for the bot that runs them.

grid: uint8 [C, 7, 7], channels:
   0 own body (not head)       1 ally body          2 ally head
   3 enemy body                4 enemy head         5 pearl
   6 pearl countdown, clipped to 0..254 (255 = tile never spawns)
   7-10 kelp on the N/E/S/W edge of the cell
  11-14 portal on the N/E/S/W edge of the cell
  15 head facing, 1..4 = N/E/S/W (0 = no head)
  16 body-segment facing (toward its head), 1..4 (0 = no segment)
scalars: float32 [5] = length, unit_count, round, facing (0..3), messages
"""

from __future__ import annotations

import numpy as np

import bc

C = 17
N_SCALARS = 5
DIR_INDEX = {"N": 0, "E": 1, "S": 2, "W": 3}


def encode(obs: bc.Obs, team: str, my_id: int) -> tuple[np.ndarray, np.ndarray]:
    g = np.zeros((C, 7, 7), dtype=np.uint8)
    for k in range(49):
        r, c = divmod(k, 7)
        part = obs.occ[k]
        if part is not None:
            pteam, pid, is_head, f = part
            if is_head:
                g[15, r, c] = DIR_INDEX[f] + 1
                if pid != my_id:
                    g[2 if pteam == team else 4, r, c] = 1
            else:
                g[16, r, c] = DIR_INDEX[f] + 1
                g[0 if pid == my_id else 1 if pteam == team else 3, r, c] = 1
        if obs.pearl[k]:
            g[5, r, c] = 1
        pin = obs.pearl_in[k]
        g[6, r, c] = 255 if pin < 0 else min(pin, 254)
    h = np.array(obs.hedge, dtype=np.int32)   # 8 x 7
    v = np.array(obs.vedge, dtype=np.int32)   # 7 x 8
    for ch, e in ((0, h[:7, :]), (1, v[:, 1:]), (2, h[1:, :]), (3, v[:, :7])):   # N E S W
        g[7 + ch] = e == bc.KELP
        g[11 + ch] = e >= 0
    s = np.array([obs.length, obs.unit_count, obs.round, DIR_INDEX[obs.facing], len(obs.msgs)],
                 dtype=np.float32)
    return g, s


def action_label(action) -> tuple[int, int, int, int]:
    """(kind, first_dir, steps, split_size); kind 0 move, 1 split, 2 suicide, 3 none."""
    if action is None:
        return 3, -1, 0, 0
    if action[0] == "move":
        steps = action[1]
        return 0, DIR_INDEX[steps[0]] if steps else -1, len(steps), 0
    if action[0] == "split":
        return 1, -1, 0, action[1]
    return 2, -1, 0, 0
