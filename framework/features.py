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
FEATURE_VERSION = 2


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
    """Summary only; use action_tokens for the complete sprint path.

    (kind, first_dir, steps, split_size); kind 0 move, 1 split, 2 suicide, 3 none.
    """
    if action is None:
        return 3, -1, 0, 0
    if action[0] == "move":
        steps = action[1]
        return 0, DIR_INDEX[steps[0]] if steps else -1, len(steps), 0
    if action[0] == "split":
        return 1, -1, 0, action[1]
    if action[0] == "suicide":
        return 2, -1, 0, 0
    raise ValueError(f"unknown action: {action!r}")


def action_tokens(action) -> np.ndarray:
    """Lossless variable-length MOVE path: N/E/S/W = 0/1/2/3, without a cap."""
    return np.asarray([DIR_INDEX[d] for d in action[1]]
                      if action is not None and action[0] == "move" else [], dtype=np.int8)


def decode_action(kind: int, tokens, split_size: int = 0):
    """Reconstruct a replay action. Remove batch padding using its mask first."""
    if kind == 0:
        if any(int(t) not in range(4) for t in tokens):
            raise ValueError("move tokens must be in 0..3; remove padding first")
        return "move", "".join("NESW"[int(t)] for t in tokens)
    if kind == 1:
        return "split", int(split_size)
    if kind == 2:
        return ("suicide",)
    if kind == 3:
        return None
    raise ValueError(f"unknown action kind: {kind}")


def encode_observation(obs: bc.Obs, team: str, my_id: int,
                       map_size: tuple[int, int], unit_limit: int = 64) -> dict:
    """V2 inputs derived exclusively from this dragon's observation/init.

    Preserve encode()'s compact grid and add exact fields for richer models.
    turn_order: 0 empty, 1 earlier ID, 2 self, 3 later ID.
    portal_ids: -1 no portal. sonar: ordered uint32 values. IDs are categorical.
    """
    grid, scalar = encode(obs, team, my_id)
    ids = np.full((7, 7), -1, dtype=np.int32)
    order = np.zeros((7, 7), dtype=np.uint8)
    portals = np.full((4, 7, 7), -1, dtype=np.int32)
    for k, part in enumerate(obs.occ):
        r, c = divmod(k, 7)
        if part is not None:
            pid = part[1]
            ids[r, c] = pid
            order[r, c] = 1 if pid < my_id else 2 if pid == my_id else 3
        for d, name in enumerate("NESW"):
            edge = obs.edge(k, name)
            if edge >= 0:
                portals[d, r, c] = edge
    return {
        "grid": grid, "scalar": scalar,
        "dragon_ids": ids, "turn_order": order, "portal_ids": portals,
        "coordinates": np.asarray([obs.x, obs.y], dtype=np.int32).reshape(2, 7, 7),
        "pearl_countdown": np.asarray(obs.pearl_in, dtype=np.int32).reshape(7, 7),
        "map_size": np.asarray(map_size, dtype=np.int32),
        "unit_limit": np.int32(unit_limit), "sonar": np.asarray(obs.msgs, dtype=np.uint32),
    }
