"""Deterministic 24-case selection for DIAGNOSTIC_FINDINGS.md (made before viewing
any replay). Rules from NEXT_STEPS_2026-10-04 section 3:
- 12 elimination losses: 4 each from stripes, trophy, dilemma; cycle opponent
  families (nicked, ours, other) and alternate sides, distinct opponents first.
- 6 both-dead losses: 3 with ours_total > theirs_total and 3 without, cycling
  portals, islands, weakhold, tower_defense.
- 6 controls: C10 base wins on the same map and opponent as the first two
  elimination cases of each target map (else same map, same family).
Order within a pool: (opponent, seed, side) sorted; no outcome detail is used
beyond the class and the total-length comparison."""
import json
from pathlib import Path
from bcsim.ablate import _family

RUN = Path("results/20261003-224713-ablate-d440c5")
idx = json.load(open("results/next-steps-20261004/diagnostic-case-index.json"))
key = lambda c: (c["opponent"], c["seed"], c["side"])

def pick(pool, n):
    pool = sorted(pool, key=key); out = []; fams = ["nicked", "ours", "other"]
    famof = lambda c: _family(c["opponent"]) if _family(c["opponent"]) in ("nicked", "ours") else "other"
    i = 0
    while len(out) < n and len(out) < len(pool):
        want_f = fams[i % 3]; want_s = "AB"[len(out) % 2]; i += 1
        used = {c["opponent"] for c in out}
        for strict in (3, 2, 1, 0):
            cand = [c for c in pool if c not in out and (strict < 1 or famof(c) == want_f)
                    and (strict < 2 or c["side"] == want_s) and (strict < 3 or c["opponent"] not in used)]
            if cand: out.append(cand[0]); break
        if i > 30: break
    return out

cases = []
for m in ("stripes", "trophy", "dilemma"):
    for c in pick([c for c in idx if c["class"] == "elimination" and c["map"] == m], 4):
        cases.append({**c, "group": "elimination"})
for adv in (True, False):
    chosen = []
    maps = ["portals", "islands", "weakhold", "tower_defense"]
    for m in maps:
        if len(chosen) == 3: break
        pool = sorted([c for c in idx if c["class"] == "both_dead" and c["map"] == m and (c["ours_total"] > c["theirs_total"]) == adv], key=key)
        if pool: chosen.append(pool[0])
    cases += [{**c, "group": "both_dead_" + ("more_total" if adv else "no_total_adv")} for c in chosen]
games = [json.loads(l) for l in open(RUN / "runs/base/games.jsonl")]
wins = sorted([g for g in games if g["winner"] == ("A" if g["bot_a"] == "base" else "B")],
              key=lambda g: (g["map"], g["block"][0], g["seed"], g["bot_a"] != "base"))
for m in ("stripes", "trophy", "dilemma"):
    for c in [c for c in cases if c["group"] == "elimination" and c["map"] == m][:2]:
        cand = [g for g in wins if g["map"] == m and g["block"][0] == c["opponent"]] or \
               [g for g in wins if g["map"] == m and _family(g["block"][0]) == _family(c["opponent"])]
        taken = {(x["map"], x["opponent"], x["seed"], x["side"]) for x in cases}
        cand = [g for g in cand if (g["map"], g["block"][0], g["seed"], "A" if g["bot_a"] == "base" else "B") not in taken]
        if cand:
            g = cand[0]
            cases.append({"map": m, "opponent": g["block"][0], "seed": g["seed"], "side": "A" if g["bot_a"] == "base" else "B",
                          "class": "win", "group": "control", "control_for": f"{c['opponent']} s{c['seed']} {c['side']}"})
Path("results/next-steps-20261004/selected_cases.json").write_text(json.dumps(cases, indent=1))
for c in cases: print(c["group"], c["map"], c["opponent"], c["seed"], c["side"])
print(len(cases), "cases")
