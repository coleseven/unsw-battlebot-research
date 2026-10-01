"""Counterfactual-move teacher for the new mover (R5, NEW_MOVER_PLAN.md).

A decision is (map, seed, sides, dragon id, round). The game is replayed from
the start with the same seed; at that decision the dragon's own reply is
produced as usual (its private state updates normally), then only its MOVE
line is rewritten to the forced direction. Every later decision of every bot
is recomputed from the changed observations.

    python -m bcsim.mover_teacher --identity      # M1 gate: no-op / same-move replay

The identity gate requires: no hook, a pass-through hook, and forcing the
move the bot chose anyway all reproduce the reference event stream (actions,
tile changes, moves, splits, deaths, sonar), ignoring CPU-point fields.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from . import guard, match, official_suite, replay as rp

STABLE = {rp.TILE_CHANGE, rp.DRAGON_ACTION, rp.DRAGON_UPDATE, rp.DRAGON_SPLIT,
          rp.DRAGON_DEATH, rp.SONAR_PING, rp.ROUND_START, rp.TURN_START}


def block_round(block: bytes) -> int:
    first = block.split(b"\n", 1)[0]
    return int(first.split()[1]) if first.startswith(b"ROUND") else -1


def move_of(reply: bytes) -> str | None:
    """The single-step direction of an ordinary MOVE reply, else None."""
    for line in reply.split(b"\n"):
        if line.startswith(b"MOVE "):
            d = line[5:].strip().decode()
            return d if len(d) == 1 else None
        if line.strip() and not line.startswith(b"SONAR") and not line.startswith(b"LOG"):
            return None
    return None


class Force:
    """Hook that forces `direction` for dragon `did` at `rnd` (a no-op when
    direction is None) and records what the bot originally chose."""

    def __init__(self, did: int | None = None, rnd: int | None = None, direction: str | None = None,
                 horizons=()):
        self.did, self.rnd, self.direction = did, rnd, direction
        self.original: str | None = None
        self.applied = False
        # short-horizon labels: each team's living dragons' lengths, from the
        # LENGTH line of every block at round rnd + h (every dragon gets a block)
        self.at = {rnd + h: h for h in horizons} if rnd is not None else {}
        self.snap = {h: {"A": [], "B": []} for h in horizons}

    def __call__(self, dragon_id, team, block, reply):
        r = block_round(block)
        if r in self.at and team in ("A", "B"):
            for line in block.split(b"\n", 4)[:4]:
                if line.startswith(b"LENGTH"):
                    self.snap[self.at[r]][team].append(int(line.split()[1]))
        if dragon_id != self.did or r != self.rnd:
            return reply
        self.original = move_of(reply)
        if self.direction is None or self.original is None:
            return reply
        lines = reply.split(b"\n")
        for i, line in enumerate(lines):
            if line.startswith(b"MOVE "):
                lines[i] = b"MOVE " + self.direction.encode()
                self.applied = True
                break
        return b"\n".join(lines)


def events(blob: bytes):
    out = []
    for ev in rp.decode(blob).events:
        if ev[0] not in STABLE:
            continue
        if ev[0] == rp.DRAGON_ACTION:
            ev = ev[:3]                      # drop CPU points / exceeded / tle
        out.append(ev)
    return out


def play_blob(map_path, a, b, seed, hook=None):
    tmp = Path(os.environ.get("TEMP", ".")) / f"mover-{os.getpid()}.replay"
    r = match.play(Path(map_path), Path(a), Path(b), seed=seed, replay_to=tmp, hook=hook)
    blob = tmp.read_bytes()
    tmp.unlink(missing_ok=True)
    return r, blob


def first_moves(blob: bytes, team: str, start_round: int, limit: int = 5):
    """A few (dragon id, round, direction) ordinary moves by `team` from start_round on."""
    r = rp.decode(blob)
    teams, rnd, out = {}, 0, []
    from . import reconstruct
    board = reconstruct.Board(r.map_text)
    for i, (t, _) in enumerate(board.dragons):
        teams[i] = t
    for ev in r.events:
        if ev[0] == rp.ROUND_START:
            rnd = ev[1]
        elif ev[0] == rp.DRAGON_SPLIT:
            teams[ev[2]] = ev[3]
        elif ev[0] == rp.DRAGON_ACTION and rnd >= start_round and teams.get(ev[1]) == team:
            act = ev[2]
            if act and act[0] == "move" and len(act[1]) == 1:
                out.append((ev[1], rnd, act[1]))
                if len(out) >= limit:
                    break
    return out


def identity(cases) -> dict:
    report = []
    for map_path, a, b, seed, team in cases:
        _, ref = play_blob(map_path, a, b, seed)
        ref_ev = events(ref)
        _, again = play_blob(map_path, a, b, seed, hook=Force())
        same_noop = events(again) == ref_ev
        rows = []
        for did, rnd, d in first_moves(ref, team, 40, 3) + first_moves(ref, team, 300, 2):
            f = Force(did, rnd, d)
            _, blob = play_blob(map_path, a, b, seed, hook=f)
            same = events(blob) == ref_ev
            others = [x for x in "NESW" if x != d]
            g = Force(did, rnd, others[0])
            _, blob2 = play_blob(map_path, a, b, seed, hook=g)
            rows.append({"dragon": did, "round": rnd, "move": d, "seen": f.original,
                         "same_move_identical": same, "other_move": others[0],
                         "other_applied": g.applied, "other_diverges": events(blob2) != ref_ev})
        report.append({"map": Path(map_path).stem, "a": Path(a).name, "b": Path(b).name, "seed": seed,
                       "team": team, "noop_identical": same_noop, "forced": rows})
        print(json.dumps(report[-1]), flush=True)
    return {"cases": report, "pass": all(c["noop_identical"] and all(r["same_move_identical"] for r in c["forced"])
                                         for c in report)}


def variant(base: str, name: str, over: dict) -> Path:
    """A copy of bot `base` with params.hpp constants overridden."""
    import re
    import shutil
    d = Path("results/mover-variants") / name
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(base, d, ignore=shutil.ignore_patterns(".unswbc-build", "FROZEN.txt"))
    p = d / "params.hpp"
    s = p.read_text(encoding="utf8")
    for k, v in over.items():
        s, n = re.subn(rf"(inline constexpr \w+ {k} = )[^;]+;", rf"\g<1>{v};", s)
        assert n == 1, k
    p.write_text(s, encoding="utf8")
    return d


def parse_mover_logs(blob: bytes):
    """Decisions logged with CPP_MOVER_LOG: [{round, id, chosen, cands: {dir: [64 floats]}}]."""
    out, cur = [], None
    for ev in rp.decode(blob).events:
        if ev[0] != rp.DRAGON_LOG:
            continue
        for line in str(ev[2]).splitlines():
            p = line.split()
            if p[:1] == ["MV"]:
                cur = {"round": int(p[1]), "id": int(p[2]), "chosen": p[3], "n": int(p[4]), "cands": {}}
                out.append(cur)
            elif p[:1] == ["MVC"] and cur is not None:
                cur["cands"][p[1]] = [float(v) for v in p[2:]]
    return out


def parity(reference: str, opponents, maps, seed: int) -> dict:
    """M1: the new build with the mover off, with zero weights on, and with
    feature logging must play exactly like the frozen incumbent."""
    import unswbc.engine as E
    off = variant(reference, "off", {})
    zero = variant(reference, "zero", {"CPP_MOVER": 1})
    log = variant(reference, "log8", {"CPP_MOVER_LOG": 8})
    rows = []
    for m in maps:
        for opp in opponents:
            for side in "AB":
                def pair(bot, debug=0):
                    a, b = (bot, opp) if side == "A" else (opp, bot)
                    tmp = Path(os.environ.get("TEMP", ".")) / f"parity-{os.getpid()}.replay"
                    match.play(Path(m), Path(a), Path(b), seed=seed, replay_to=tmp, debug=debug)
                    blob = tmp.read_bytes(); tmp.unlink(missing_ok=True)
                    return blob
                ref = events(pair(Path("versions/v10h")))
                logged = pair(log, E.DEBUG_ALL)
                decisions = parse_mover_logs(logged)
                widths = {len(v) for d in decisions for v in d["cands"].values()}
                rows.append({"map": Path(m).stem, "opp": Path(opp).name, "side": side,
                             "off": events(pair(off)) == ref, "zero": events(pair(zero)) == ref,
                             "log8": events(logged) == ref, "logged_decisions": len(decisions),
                             "feature_widths": sorted(widths)})
                print(json.dumps(rows[-1]), flush=True)
    return {"rows": rows, "pass": all(r["off"] and r["zero"] and r["log8"] and r["feature_widths"] == [64] for r in rows)}


FEATURES = (["v3_" + n for n in ("food_nearness", "soon_food", "food_count", "spawn_count", "space", "exits",
                                 "dead_end", "straight", "friendly_near", "enemy_near", "enemy_reach",
                                 "friendly_reach", "later_enemy_reach", "own_near", "boundary", "short_path",
                                 "length", "round", "population", "food_x_length", "space_x_length",
                                 "friendly_x_population", "exits_x_length", "boundary_x_no_food")]
            + ["round", "remaining", "log_length", "units_frac", "age", "founder", "protected", "cash_target",
               "known_hub", "map_known", "local_rate", "local_rate_valid"]
            + ["s0", "v3_part", "non_v3", "facing", "portal", "landing_in_view", "landing_age", "room_per_len",
               "exits", "landing_edges_known", "pearl_known", "pearl", "hub_dist", "hub_delta", "hub_rate_valid",
               "hub_rate", "cash_dist", "cash_delta", "target_age", "target_age_valid", "blocks_front",
               "recipient_visible", "friendly_heads", "enemy_heads", "threat_lower_id", "threat_higher_id",
               "own_visible", "big_enemy"])
OPP_PANEL = ["sparring/cpp_nicked_v92", "sparring/cpp_nicked_v75", "sparring/nicked_lab",
             "sparring/cpp_leviathan3", "results/v7-base-bot", "sparring/nicked_v44"]


def _source_job(args):
    map_path, bot, opp, seed, side, out = args
    import unswbc.engine as E
    a, b = (bot, opp) if side == "A" else (opp, bot)
    r = match.play(Path(map_path), Path(a), Path(b), seed=seed, replay_to=Path(out), debug=E.DEBUG_ALL)
    return {"map": map_path, "a": a, "b": b, "seed": seed, "side": side, "replay": out,
            "winner": r.winner, "error": r.error}


def pilot_sources(out: Path, logbot: Path, seed: int, workers: int) -> None:
    """One source game per (map, side) over the 15 ranked + 7 Sprint maps,
    opponents rotating through the panel; the incumbent logs every 8th
    eligible decision (its play is identical to the frozen incumbent)."""
    from concurrent.futures import ProcessPoolExecutor
    maps = official_suite.ranked_maps() + official_suite.sprint_maps()
    (out / "sources").mkdir(parents=True, exist_ok=True)
    jobs = []
    for i, m in enumerate(maps):
        for j, side in enumerate("AB"):
            opp = OPP_PANEL[(2 * i + j) % len(OPP_PANEL)]
            name = f"{m.stem}-{side}-{Path(opp).name}"
            jobs.append((str(m), str(logbot), opp, seed + i, side, str(out / "sources" / f"{name}.replay")))
    with guard.slot("mover-sources"), ProcessPoolExecutor(guard.cap_workers(workers), max_tasks_per_child=20) as pool:
        rows = list(pool.map(_source_job, jobs))
    (out / "sources.json").write_text(json.dumps(rows, indent=1), encoding="utf8")
    print(f"{len(rows)} source games, errors: {sum(1 for r in rows if r['error'])}", flush=True)


def pilot_sample(out: Path, per_game: int, seed: int) -> None:
    """Up to `per_game` logged decisions per source game, our team only:
    half at random, half among close calls (S0 gap between the best two
    candidates below the game's median), spread over phases."""
    import random
    rng = random.Random(seed)
    sources = json.loads((out / "sources.json").read_text())
    decisions = []
    for src in sources:
        if src["error"]:
            continue
        r = rp.load(src["replay"])
        logs = parse_mover_logs(Path(src["replay"]).read_bytes())
        if not logs:
            continue
        def gap(d):
            s = sorted((v[36] for v in d["cands"].values()), reverse=True)
            return s[0] - s[1]
        med = sorted(gap(d) for d in logs)[len(logs) // 2]
        close = [d for d in logs if gap(d) <= med]
        pick = rng.sample(logs, min(per_game // 2, len(logs)))
        rest = [d for d in close if d not in pick]
        pick += rng.sample(rest, min(per_game - len(pick), len(rest)))
        for d in pick:
            decisions.append({"source": src, "round": d["round"], "id": d["id"], "chosen": d["chosen"],
                              "cands": d["cands"], "gap": gap(d), "close": gap(d) <= med})
    (out / "decisions.json").write_text(json.dumps(decisions), encoding="utf8")
    print(f"{len(decisions)} decisions from {len(sources)} games", flush=True)


def _label_job(args):
    key, map_path, a, b, seed, side, did, rnd, direction = args
    f = Force(did, rnd, direction, horizons=(20, 40, 80))
    tmp = Path(os.environ.get("TEMP", ".")) / f"label-{os.getpid()}.replay"
    r = match.play(Path(map_path), Path(a), Path(b), seed=seed, replay_to=tmp, hook=f)
    tmp.unlink(missing_ok=True)
    us = side.lower(); them = "b" if us == "a" else "a"
    res = 1.0 if r.winner == side else 0.5 if r.winner is None and not r.error else 0.0
    them_t = "B" if side == "A" else "A"
    horizon = {str(h): {"our_n": len(v[side]), "our_total": sum(v[side]), "our_longest": max(v[side], default=0),
                        "their_n": len(v[them_t]), "their_total": sum(v[them_t]),
                        "their_longest": max(v[them_t], default=0), "reached": bool(v[side] or v[them_t])}
               for h, v in f.snap.items()}
    return {"key": key, "dir": direction, "applied": f.applied, "seen": f.original, "result": res,
            "horizon": horizon,
            "reason": r.reason, "rounds": r.rounds, "error": r.error,
            "our_longest": getattr(r, f"{us}_longest"), "their_longest": getattr(r, f"{them}_longest"),
            "our_total": getattr(r, f"{us}_length"), "their_total": getattr(r, f"{them}_length")}


def pilot_label(out: Path, playbot: Path, workers: int) -> None:
    """Force every candidate of every sampled decision (the chosen one too, as
    the reference) and play each game to the end with unchanged policies.
    Resumable: finished (decision, direction) pairs in labels.jsonl are skipped."""
    from concurrent.futures import ProcessPoolExecutor, as_completed
    decisions = json.loads((out / "decisions.json").read_text())
    done = set()
    lab = out / "labels.jsonl"
    if lab.exists():
        done = {(r["key"], r["dir"]) for r in map(json.loads, lab.read_text().splitlines())}
    jobs = []
    for i, d in enumerate(decisions):
        s = d["source"]
        a = str(playbot) if s["side"] == "A" else s["a"]
        b = str(playbot) if s["side"] == "B" else s["b"]
        for direction in d["cands"]:
            if (i, direction) not in done:
                jobs.append((i, s["map"], a, b, s["seed"], s["side"], d["id"], d["round"], direction))
    print(f"{len(jobs)} games to play", flush=True)
    with guard.slot("mover-label"), ProcessPoolExecutor(guard.cap_workers(workers), max_tasks_per_child=20) as pool, lab.open("a") as f:
        futs = [pool.submit(_label_job, j) for j in jobs]
        for n, fut in enumerate(as_completed(futs), 1):
            f.write(json.dumps(fut.result()) + "\n"); f.flush()
            if n % 50 == 0:
                print(f"labelled {n}/{len(jobs)}", flush=True)


def pilot_report(out: Path) -> dict:
    from collections import defaultdict
    decisions = json.loads((out / "decisions.json").read_text())
    labels = defaultdict(dict)
    for r in map(json.loads, (out / "labels.jsonl").read_text().splitlines()):
        labels[r["key"]][r["dir"]] = r
    rep = {"decisions": len(decisions), "labelled": 0, "errors": 0, "not_applied": 0,
           "chosen_reproduces_source": 0, "result_differs": 0, "margin_differs": 0,
           "oracle_gain": 0.0, "by_phase": defaultdict(lambda: [0, 0]), "by_map": defaultdict(lambda: [0, 0])}
    for i, d in enumerate(decisions):
        L = labels.get(i, {})
        if len(L) < len(d["cands"]):
            continue
        rep["labelled"] += 1
        rep["errors"] += sum(1 for r in L.values() if r["error"])
        rep["not_applied"] += sum(1 for r in L.values() if not r["applied"])
        ch = L[d["chosen"]]
        src_win = 1.0 if d["source"]["winner"] == d["source"]["side"] else 0.5 if d["source"]["winner"] is None else 0.0
        rep["chosen_reproduces_source"] += ch["result"] == src_win
        res = {k: r["result"] for k, r in L.items()}
        differs = len(set(res.values())) > 1
        rep["result_differs"] += differs
        marg = {k: r["our_longest"] - r["their_longest"] for k, r in L.items()}
        rep["margin_differs"] += len(set(marg.values())) > 1
        rep["oracle_gain"] += max(res.values()) - res[d["chosen"]]
        ph = "r<100" if d["round"] < 100 else "r<300" if d["round"] < 300 else "r>=300"
        rep["by_phase"][ph][0] += 1; rep["by_phase"][ph][1] += differs
        mp = Path(d["source"]["map"]).stem
        rep["by_map"][mp][0] += 1; rep["by_map"][mp][1] += differs
    rep["by_phase"] = dict(rep["by_phase"]); rep["by_map"] = dict(rep["by_map"])
    (out / "pilot_report.json").write_text(json.dumps(rep, indent=1), encoding="utf8")
    return rep


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--identity", action="store_true")
    ap.add_argument("--parity", help="new build to compare with versions/v10h (M1 off/zero/log gate)")
    ap.add_argument("--pilot", type=Path, help="M2 pilot directory")
    ap.add_argument("--step", choices=["sources", "sample", "label", "report"])
    ap.add_argument("--logbot", default="results/mover-variants/log8")
    ap.add_argument("--playbot", default="results/mover-variants/off")
    ap.add_argument("--per-game", type=int, default=7)
    ap.add_argument("--seed", type=int, default=381001)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--base", default="versions/v10h")
    ap.add_argument("--out", type=Path, default=Path("results/mover-m1-identity.json"))
    a = ap.parse_args()
    os.environ.setdefault("BCSIM_DETERMINISTIC_V6", "1")
    os.environ.setdefault("BCSIM_CPP_INPROC", "1")
    if a.identity:
        maps = {p.stem: p for p in official_suite.ranked_maps()}
        cases = [(maps["Portals"], a.base, "sparring/cpp_nicked_v92", 351001, "A"),
                 (maps["schooltime"], "sparring/nicked_lab", a.base, 351002, "B"),
                 (maps["trophy"], a.base, "results/v7-base-bot", 351003, "A")]
        with guard.slot("mover-identity"):
            rep = identity(cases)
        a.out.write_text(json.dumps(rep, indent=1), encoding="utf8")
        print("PASS" if rep["pass"] else "FAIL", a.out)
    if a.parity:
        maps = {p.stem: p for p in official_suite.ranked_maps() + official_suite.sprint_maps()}
        with guard.slot("mover-parity"):
            rep = parity(a.parity, ["sparring/cpp_nicked_v92", "results/v7-base-bot"],
                         [maps[m] for m in ("Portals", "trophy", "Prisoners_Dilemma", "Maze")], 371001)
        out = Path("results/mover-m1-parity.json")
        out.write_text(json.dumps(rep, indent=1), encoding="utf8")
        print("PASS" if rep["pass"] else "FAIL", out)
    if a.pilot:
        if a.step == "sources":
            pilot_sources(a.pilot, Path(a.logbot), a.seed, a.workers)
        elif a.step == "sample":
            pilot_sample(a.pilot, a.per_game, a.seed)
        elif a.step == "label":
            pilot_label(a.pilot, Path(a.playbot), a.workers)
        elif a.step == "report":
            print(json.dumps(pilot_report(a.pilot), indent=1))


if __name__ == "__main__":
    main()
