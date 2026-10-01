"""M5 parity: in a game with the mover on (and feature logging), recompute each
logged decision's choice in Python from the logged features and the exported
artifact; it must equal the C++ choice (chosen) except numerical ties."""
import json
import os
from pathlib import Path

import numpy as np
import unswbc.engine as E

from bcsim import guard, match, official_suite, mover_teacher as mt

TAU = 0.5
art = json.loads(Path("framework/mover_r5.json").read_text())
mean, std, scale = np.array(art["mean"]), np.array(art["std"]), art["score_scale"]
w1 = np.array(art["w1"]).reshape(24, 64); b1 = np.array(art["b1"]); w2 = np.array(art["w2"]); b2 = art["b2"]

bot = mt.variant("results/v10q-bot", "mv05log", {"CPP_MOVER": 1, "CPP_MOVER_TAU": TAU, "CPP_MOVER_LOG": 1})
maps = {p.stem: p for p in official_suite.ranked_maps() + official_suite.sprint_maps()}
agree = disagree = overrides = 0
worst = 0.0
with guard.slot("mover-m5"):
    for m in ("Portals", "Australia"):
        tmp = Path(os.environ["TEMP"]) / "m5.replay"
        match.play(maps[m], bot, Path("sparring/cpp_nicked_v92"), seed=401001, replay_to=tmp, debug=E.DEBUG_ALL)
        for d in mt.parse_mover_logs(tmp.read_bytes()):
            dirs = list(d["cands"])
            F = np.array([d["cands"][k] for k in dirs])
            s0 = F[:, 36].copy(); v3c = F[:, 37].copy(); mu = s0.mean()
            X = F.copy(); X[:, 36] = (s0 - mu) / scale; X[:, 37] = v3c / scale; X[:, 38] = (s0 - v3c - mu) / scale
            Z = (X - mean) / std
            f = np.maximum(Z @ w1.T + b1, 0) @ w2 + b2
            q = X[:, 36] + 2 * np.tanh(f)
            # incumbent: max S0, ties prefer the current facing (logged slot 39), first in order otherwise
            facing = F[:, 39]
            i0 = max(range(len(dirs)), key=lambda i: (s0[i], facing[i], -i))
            best = int(np.argmax(q))
            pick = dirs[best] if q[best] - q[i0] > TAU else dirs[i0]
            overrides += pick != dirs[i0]
            if pick == d["chosen"]:
                agree += 1
            else:
                disagree += 1
                worst = max(worst, abs((q[best] - q[i0]) - TAU))
print(json.dumps({"agree": agree, "disagree": disagree, "overrides": overrides, "closest_margin_on_disagreement": worst}))
