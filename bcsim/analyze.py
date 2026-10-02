"""Summarise ranked-game replays into compact, token-cheap reports.

    python -m bcsim.analyze                          # everything under replays/
    python -m bcsim.analyze replays/mygames          # a folder, .zip, or .replay files
    python -m bcsim.analyze replays/mygames --maps   # add a per-map breakdown
    python -m bcsim.analyze --game M120320           # one game in detail
    python -m bcsim.analyze --json out.json          # every per-game stat, machine readable

Sides: `--us auto` (default) treats the side whose submission name or CPU points
the replay records as ours (the site only shows those for your own team). When
no side is ours, aggregates compare the winner with the loser instead.

Decoding a large replay takes seconds, so per-game stats are cached under
results/analyze_cache/ keyed by content hash; repeat runs are instant.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import statistics
import sys
import zipfile
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

from . import reconstruct, replay as rp
from .paths import RESULTS, ROOT

VERSION = 5                 # queen diagnostics; historical replays retain their recorded winner
CACHE = RESULTS / "analyze_cache"
BUDGET = 100_000_000        # judge CPU points per dragon-turn
SAMPLE = 10                 # timeline resolution in rounds
INFANT = 10                 # a death this many rounds after birth counts as infant
CONTACT = 3                 # heads within this Chebyshev distance = contact
CAUSE = {"W": "kelp", "S": "self", "O": "body", "H": "head-on", "A": "no-move"}


# -- sources -------------------------------------------------------------------------

def sources(paths):
    """Yield (name, battle, loader) for every replay in the given paths.
    loader is a picklable (kind, path, member) tuple."""
    for p in map(pathlib.Path, paths):
        files = sorted(p.rglob("*")) if p.is_dir() else [p]
        for f in files:
            if f.suffix == ".replay":
                yield f.stem, f.parent.name, ("file", str(f), None)
            elif f.suffix == ".zip":
                battle = f.stem.removeprefix("battle-").removesuffix("-replays")
                with zipfile.ZipFile(f) as z:
                    for m in sorted(z.namelist()):
                        if m.endswith(".replay"):
                            yield pathlib.PurePath(m).stem, battle, ("zip", str(f), m)


def read_blob(loader) -> bytes:
    kind, path, member = loader
    if kind == "zip":
        with zipfile.ZipFile(path) as z:
            return z.read(member)
    return pathlib.Path(path).read_bytes()


# -- per-game stats ------------------------------------------------------------------

def _team():
    return {"pearls": 0, "splits": 0, "split_parent_len": Counter(), "child_len": Counter(),
            "first_split": None, "deaths": Counter(), "kills": 0, "friendly": 0, "headon_trades": 0,
            "death_ages": [], "death_lens": [], "infant_deaths": 0, "len_lost": 0,
            "moves": 0, "sprints": 0, "extra_steps": 0, "sonar": 0, "idle": 0, "suicides": 0,
            "portal_steps": 0, "empty_turn_deaths": 0, "fed_deaths": 0, "last_split": None, "late_splits": 0,
            "points": [], "exceeded": 0, "tle": 0,
            "peak_alive": (0, 0), "peak_total": (0, 0), "peak_longest": (0, 0)}


def game_stats(blob: bytes) -> dict:
    r = rp.decode(blob)
    board = reconstruct.Board(r.map_text)
    w, h = board.w, board.h
    body, team, born = {}, {}, {}
    for i, (t, coords) in enumerate(board.dragons):
        body[i], team[i], born[i] = list(coords), t, 0
    T = {"A": _team(), "B": _team()}
    queens = {t: next((i for i in (0, 1) if team.get(i) == t), None) for t in "AB"}
    queen_deaths = {}
    timeline, deaths, contact = [], [], None
    rnd, actor, action, steps, headon = 0, None, None, 0, None

    def snapshot():
        row = {"round": rnd}
        row["queens"] = {t: len(body.get(d, [])) for t, d in queens.items()}
        for t in "AB":
            lens = [len(b) for d, b in body.items() if team[d] == t]
            row[t] = [len(lens), sum(lens), max(lens, default=0)]
        return row

    def occupant(cell):
        for d, b in body.items():
            if cell in b:
                return d, b.index(cell)
        return None, None

    for ev in r.events:
        k = ev[0]
        if k == rp.ROUND_START:
            rnd = ev[1]
            snap = snapshot()
            for t in "AB":
                s, (alive, total, longest) = T[t], snap[t]
                for key, v in (("peak_alive", alive), ("peak_total", total), ("peak_longest", longest)):
                    if v > s[key][0]:
                        s[key] = (v, rnd)
            if rnd % SAMPLE == 0:
                timeline.append(snap)
            if contact is None:
                heads = {t: [b[0] for d, b in body.items() if team[d] == t] for t in "AB"}
                for ax, ay in heads["A"]:
                    if any(min((ax - bx) % w, (bx - ax) % w) <= CONTACT and
                           min((ay - by) % h, (by - ay) % h) <= CONTACT for bx, by in heads["B"]):
                        contact = rnd
                        break
        elif k == rp.TURN_START:
            actor, action, steps, headon = ev[1], None, 0, None
        elif k == rp.DRAGON_ACTION:
            d, action, points, exceeded, tle = ev[1:6]
            s = T[team[d]]
            if points is not None:
                s["points"].append(points)
            s["exceeded"] += bool(exceeded)
            s["tle"] += bool(tle)
            if action is None:
                s["idle"] += 1
            elif action[0] == "move":
                s["moves"] += 1
                s["sprints"] += len(action[1]) > 1
                s["extra_steps"] += len(action[1]) - 1
            elif action[0] == "suicide":
                s["suicides"] += 1
        elif k == rp.TILE_CHANGE:
            if not ev[3] and actor in body and action and action[0] == "move":
                T[team[actor]]["pearls"] += 1
        elif k == rp.DRAGON_UPDATE:
            d, head, tail = ev[1], ev[3], ev[4]
            b = body.get(d)
            if b is None:
                continue
            if d == actor:
                steps += 1
            if b[0] != head:
                dx, dy = (head[0] - b[0][0]) % w, (head[1] - b[0][1]) % h
                if min(dx, w - dx) + min(dy, h - dy) != 1:
                    T[team[d]]["portal_steps"] += 1
                b.insert(0, head)
            if tail in b:
                del b[len(b) - b[::-1].index(tail):]
        elif k == rp.DRAGON_SPLIT:
            _, parent, child, t, _, pbody, cbody = ev
            s = T[t]
            s["splits"] += 1
            s["split_parent_len"][len(pbody) + len(cbody)] += 1
            s["child_len"][len(cbody)] += 1
            if s["first_split"] is None:
                s["first_split"] = rnd
            s["last_split"] = rnd
            s["late_splits"] += rnd >= 400
            body[parent], body[child] = list(pbody), list(cbody)
            team[child], born[child] = t, rnd
        elif k == rp.DRAGON_DEATH:
            d, why = ev[1], ev[2]
            b, t = body[d], team[d]
            if queens.get(t) == d:
                queen_deaths[t] = rnd
            # the other party: for "O" whoever's body is on the cell moved into;
            # a head-on kills both, the engine reporting the struck dragon first
            other = None
            if why == "H":
                other = actor if d != actor else headon
                headon = d
            elif why == "O" and d == actor and action and action[0] == "move" and steps < len(action[1]):
                cell = board.dest(*b[0], action[1][steps])
                other = occupant(cell)[0] if cell else None
            killer = team.get(other) if other != d else None
            s = T[t]
            age = rnd - born[d]
            s["deaths"][CAUSE[why]] += 1
            s["death_ages"].append(age)
            s["death_lens"].append(len(b))
            s["len_lost"] += len(b)
            s["infant_deaths"] += age <= INFANT
            # a turn with no action is the engine's default suicide: deliberate
            # or a crashed bot. "fed" = a much longer teammate's head is within
            # 2 tiles, where the ceil(L/2) dropped pearls could feed it
            if why == "A" and d == actor and (action is None or action[0] == "suicide"):
                s["empty_turn_deaths"] += 1
                hx, hy = b[0]
                s["fed_deaths"] += any(
                    team[o] == t and o != d and len(ob) >= len(b) + 5 and
                    min((ob[0][0] - hx) % w, (hx - ob[0][0]) % w) <= 2 and
                    min((ob[0][1] - hy) % h, (hy - ob[0][1]) % h) <= 2
                    for o, ob in body.items())
            if killer == t:
                s["friendly"] += 1
            elif killer is not None and why == "O":
                T[killer]["kills"] += 1
            elif killer is not None:
                s["headon_trades"] += 1
            deaths.append([rnd, t, why, killer, len(b), age, d, other])
            del body[d]
        elif k == rp.SONAR_PING:
            if ev[1] in team:
                T[team[ev[1]]]["sonar"] += 1
    last = snapshot()
    if not timeline or timeline[-1]["round"] != rnd:
        timeline.append(last)

    teams = {}
    for t, s in T.items():
        pts = sorted(s.pop("points"))
        ages, lens = s.pop("death_ages"), s.pop("death_lens")
        s["cpu"] = None if not pts else {
            "turns": len(pts), "mean": round(statistics.fmean(pts)),
            "p95": pts[int(0.95 * (len(pts) - 1))], "max": pts[-1],
            "over_half": sum(p > BUDGET // 2 for p in pts)}
        s["median_death_age"] = statistics.median(ages) if ages else None
        s["median_death_len"] = statistics.median(lens) if lens else None
        s["split_parent_len"] = dict(s["split_parent_len"])
        s["child_len"] = dict(s["child_len"])
        s["deaths"] = dict(s["deaths"])
        s["final"] = r.result.get(t.lower())
        s["queen"] = {"id": queens[t], "length": len(body.get(queens[t], [])),
                      "alive": queens[t] in body, "death_round": queen_deaths.get(t)}
        teams[t] = s
    names = {"A": r.bot_a, "B": r.bot_b}
    has_cpu = {t: teams[t]["cpu"] is not None for t in "AB"}
    return {"version": VERSION, "map": r.map_name, "size": [w, h], "rounds": rnd + 1,
            "end": r.result.get("end_reason"), "winner": r.result.get("winner"),
            "names": names, "has_cpu": has_cpu, "contact": contact,
            "teams": teams, "timeline": timeline, "deaths": deaths}


def load_stats(loader, use_cache=True) -> dict:
    blob = read_blob(loader)
    digest = hashlib.sha1(blob).hexdigest()[:20]
    path = CACHE / f"{digest}-v{VERSION}.json"
    if use_cache and path.is_file():
        return json.loads(path.read_text(encoding="utf8"))
    stats = game_stats(blob)
    CACHE.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(f".{os.getpid()}.tmp")
    tmp.write_text(json.dumps(stats), encoding="utf8")
    os.replace(tmp, path)
    return stats


def _job(args):
    name, battle, loader, use_cache = args
    g = load_stats(loader, use_cache)
    g["id"], g["battle"], g["source"] = name, battle, loader[1]
    return g


def _cached(loader):
    return CACHE / f"{hashlib.sha1(read_blob(loader)).hexdigest()[:20]}-v{VERSION}.json"


def collect(paths, use_cache=True, workers=None, game=None):
    jobs = [(n, b, l, use_cache) for n, b, l in sources(paths) if game is None or n == game]
    # cached games load in-process, so importers (even stdin scripts, which
    # cannot spawn workers on Windows) only pay for a pool when decoding
    todo = [j for j in jobs if not (use_cache and _cached(j[2]).is_file())]
    done = {}
    if len(todo) > 1 and workers != 1:
        with ProcessPoolExecutor(max_workers=workers or min(len(todo), os.cpu_count() or 1)) as ex:
            done = {j[2]: g for j, g in zip(todo, ex.map(_job, todo))}
    return [done.get(j[2]) or _job(j) for j in jobs]


# -- side assignment -----------------------------------------------------------------

def our_side(g, us):
    if us in ("A", "B"):
        return us
    if us == "none":
        return None
    named = [t for t in "AB" if g["names"][t]]
    if len(named) == 1:
        return named[0]
    cpu = [t for t in "AB" if g["has_cpu"][t]]
    return cpu[0] if len(cpu) == 1 else None


def roles(g, us):
    """(label_1, side_1, label_2, side_2): us/them if known, else winner/loser."""
    side = our_side(g, us)
    if side:
        return "us", side, "them", "B" if side == "A" else "A"
    if g["winner"]:
        return "winner", g["winner"], "loser", "B" if g["winner"] == "A" else "A"
    return "A", "A", "B", "B"


def outcome(g, side):
    if g["winner"] is None:
        return "D"
    return "W" if g["winner"] == side else "L"


# -- derived facts -------------------------------------------------------------------

def last_ahead(g, side):
    """Last timeline round where `side` led on the metric that decides the game
    (longest dragon at the round limit, alive count for eliminations)."""
    other = "B" if side == "A" else "A"
    i = 2 if g["end"] == "round_limit" else 0
    rounds = [row["round"] for row in g["timeline"] if row[side][i] > row[other][i]]
    return rounds[-1] if rounds else None


def lead_changes(g, i=2):
    changes, prev = 0, None
    for row in g["timeline"]:
        a, b = row["A"][i], row["B"][i]
        cur = "A" if a > b else "B" if b > a else prev
        if prev and cur != prev:
            changes += 1
        prev = cur
    return changes


def fmt_final(f):
    return "-" if not f else f"{f['dragons']}/{f['longest']}/{f['total']}"


def pct(a, b):
    return f"{100 * a / b:.0f}%" if b else "-"


def top(counter, n=3):
    c = Counter({int(k): v for k, v in counter.items()})
    return " ".join(f"{k}x{v}" for k, v in c.most_common(n)) or "-"


# -- reports -------------------------------------------------------------------------

def overview(games, us, show_maps):
    out = []
    games = sorted(games, key=lambda g: (g["battle"], g["id"]))
    l1, _, l2, _ = roles(games[0], us)
    out.append(f"# {len(games)} games · final = alive/longest/total · round-limit games go to the longest dragon")
    out.append("contact = first round heads of both teams were within 3 tiles · last ahead = last sampled "
               "round leading on the deciding metric (longest dragon at the limit, alive count if eliminated)")
    out.append("")
    out.append(f"game | battle | map | res({l1}) | end@round | {l1} final | {l2} final | contact | {l1} last ahead")
    out.append("---|---|---|---|---|---|---|---|---")
    for g in games:
        a, sa, b, sb = roles(g, us)
        end = "elim" if g["end"] == "eliminated" else "limit"
        out.append(f"{g['id']} | {g['battle']} | {g['map']} | {outcome(g, sa) if a == 'us' else sa + ' won' if a == 'winner' else '-'} | "
                   f"{end}@{g['rounds'] - 1} | {fmt_final(g['teams'][sa]['final'])} | {fmt_final(g['teams'][sb]['final'])} | "
                   f"{g['contact'] if g['contact'] is not None else '-'} | {last_ahead(g, sa) if last_ahead(g, sa) is not None else 'never'}")
    out.append("")
    out += aggregate(games, us)
    if show_maps:
        out.append("")
        out += per_map(games, us)
    out.append("")
    out += insights(games, us)
    return out


def _sum(games, us):
    """Aggregate team stats for the two roles across games."""
    agg = {}
    for g in games:
        for label, side in (roles(g, us)[0:2], roles(g, us)[2:4]):
            s, A = g["teams"][side], agg.setdefault(label, {
                "games": 0, "pearls": 0, "splits": 0, "kills": 0, "friendly": 0, "infant": 0,
                "len_lost": 0, "trades": 0, "moves": 0, "sprints": 0, "sonar": 0, "idle": 0, "exceeded": 0,
                "tle": 0, "deaths": Counter(), "parent": Counter(), "child": Counter(),
                "first_split": [], "peak_alive": [], "peak_longest": [], "death_age": [],
                "cpu_mean": [], "cpu_max": 0, "cpu_over_half": 0, "cpu_turns": 0})
            A["games"] += 1
            for key, src in (("pearls", "pearls"), ("splits", "splits"), ("kills", "kills"),
                             ("friendly", "friendly"), ("trades", "headon_trades"), ("infant", "infant_deaths"), ("len_lost", "len_lost"),
                             ("moves", "moves"), ("sprints", "sprints"), ("sonar", "sonar"),
                             ("idle", "idle"), ("exceeded", "exceeded"), ("tle", "tle")):
                A[key] += s[src]
            A["deaths"].update(s["deaths"])
            A["parent"].update({int(k): v for k, v in s["split_parent_len"].items()})
            A["child"].update({int(k): v for k, v in s["child_len"].items()})
            if s["first_split"] is not None:
                A["first_split"].append(s["first_split"])
            A["peak_alive"].append(s["peak_alive"][0])
            A["peak_longest"].append(s["peak_longest"][0])
            if s["median_death_age"] is not None:
                A["death_age"].append(s["median_death_age"])
            if s["cpu"]:
                A["cpu_mean"].append(s["cpu"]["mean"])
                A["cpu_max"] = max(A["cpu_max"], s["cpu"]["max"])
                A["cpu_over_half"] += s["cpu"]["over_half"]
                A["cpu_turns"] += s["cpu"]["turns"]
    return agg


def aggregate(games, us):
    agg = _sum(games, us)
    labels = list(agg)
    med = lambda xs: f"{statistics.median(xs):.0f}" if xs else "-"  # noqa: E731
    rec = Counter(outcome(g, roles(g, us)[1]) for g in games)
    elim = Counter(outcome(g, roles(g, us)[1]) for g in games if g["end"] == "eliminated")
    out = [f"## Aggregate ({labels[0]} vs {labels[1]})",
           f"record for {labels[0]}: {rec['W']}W {rec['L']}L {rec['D']}D · by elimination {elim['W']}W {elim['L']}L",
           "", "stat (per game unless noted) | " + " | ".join(labels), "---|" + "---|" * len(labels)]
    rows = [
        ("pearls eaten", lambda A: f"{A['pearls'] / A['games']:.1f}"),
        ("splits", lambda A: f"{A['splits'] / A['games']:.1f}"),
        ("median first split round", lambda A: med(A["first_split"])),
        ("split at length (top)", lambda A: top(A["parent"])),
        ("child length (top)", lambda A: top(A["child"])),
        ("median peak alive", lambda A: med(A["peak_alive"])),
        ("median peak longest", lambda A: med(A["peak_longest"])),
        ("deaths", lambda A: f"{sum(A['deaths'].values()) / A['games']:.1f}"),
        ("deaths by cause (share)", lambda A: " ".join(f"{c}:{pct(v, sum(A['deaths'].values()))}"
                                                       for c, v in A["deaths"].most_common())),
        ("kills (enemy ran into us)", lambda A: f"{A['kills'] / A['games']:.1f}"),
        ("head-on trades with enemy", lambda A: f"{A['trades'] / A['games']:.1f}"),
        ("friendly-fire deaths (own body/head)", lambda A: f"{A['friendly'] / A['games']:.1f}"),
        (f"infant deaths (<= {INFANT} rounds old)", lambda A: pct(A["infant"], sum(A["deaths"].values()))),
        ("median age at death (rounds)", lambda A: med(A["death_age"])),
        ("length lost to deaths", lambda A: f"{A['len_lost'] / A['games']:.0f}"),
        ("sprint share of moves", lambda A: pct(A["sprints"], A["moves"])),
        ("idle / exceeded / TLE turns (total)", lambda A: f"{A['idle']} / {A['exceeded']} / {A['tle']}"),
        ("CPU mean / max points", lambda A: "-" if not A["cpu_mean"] else
            f"{statistics.fmean(A['cpu_mean']) / 1e6:.1f}M / {A['cpu_max'] / 1e6:.1f}M "
            f"({pct(A['cpu_over_half'], A['cpu_turns'])} turns >50M)"),
    ]
    for name, f in rows:
        out.append(f"{name} | " + " | ".join(f(agg[l]) for l in labels))
    return out


def per_map(games, us):
    by = {}
    for g in games:
        by.setdefault(g["map"], []).append(g)
    l1 = roles(games[0], us)[0]
    out = ["## Per map", f"map | games | {l1} W-L-D | elim W-L | limit W-L | median {l1} longest vs other | median {l1} alive vs other",
           "---|---|---|---|---|---|---"]
    for m, gs in sorted(by.items()):
        rec, el, li = Counter(), Counter(), Counter()
        mine, theirs, ma, ta = [], [], [], []
        for g in gs:
            _, sa, _, sb = roles(g, us)
            o = outcome(g, sa)
            rec[o] += 1
            (el if g["end"] == "eliminated" else li)[o] += 1
            end = g["timeline"][-1]
            mine.append(end[sa][2]), theirs.append(end[sb][2]), ma.append(end[sa][0]), ta.append(end[sb][0])
        out.append(f"{m} | {len(gs)} | {rec['W']}-{rec['L']}-{rec['D']} | {el['W']}-{el['L']} | {li['W']}-{li['L']} | "
                   f"{statistics.median(mine):.0f} vs {statistics.median(theirs):.0f} | "
                   f"{statistics.median(ma):.0f} vs {statistics.median(ta):.0f}")
    return out


def insights(games, us):
    """Plain-language flags computed from the aggregate; heuristics, not verdicts."""
    agg = _sum(games, us)
    (l1, A), (l2, B) = list(agg.items())
    out = ["## Flags"]
    dA, dB = sum(A["deaths"].values()), sum(B["deaths"].values())
    if dA and dB:
        for cause in ("head-on", "body", "self", "kelp", "no-move"):
            a, b = A["deaths"][cause] / dA, B["deaths"][cause] / dB
            if a - b > 0.10 and A["deaths"][cause] >= 5:
                out.append(f"- {l1} die {cause} far more often: {a:.0%} of deaths vs {b:.0%} for {l2}.")
    if A["friendly"] > 1.5 * max(1, B["friendly"]) and A["friendly"] >= 5:
        out.append(f"- {l1} friendly-fire: {A['friendly']} deaths into own dragons vs {B['friendly']}.")
    if dA and dB and A["infant"] / dA - B["infant"] / dB > 0.10:
        out.append(f"- {l1} newborns die young: {A['infant'] / dA:.0%} of deaths within {INFANT} rounds "
                   f"of birth vs {B['infant'] / dB:.0%}.")
    for key, name in (("pearls", "pearls eaten"), ("splits", "splits"), ("kills", "kills")):
        a, b = A[key] / A["games"], B[key] / B["games"]
        if b > 1.3 * a and b - a >= 3:
            out.append(f"- {l2} have far more {name}: {b:.1f}/game vs {a:.1f}.")
        elif a > 1.3 * b and a - b >= 3:
            out.append(f"- {l1} have far more {name}: {a:.1f}/game vs {b:.1f}.")
    lost = [g for g in games if outcome(g, roles(g, us)[1]) == "L"]
    elim = [g for g in lost if g["end"] == "eliminated"]
    if elim:
        out.append(f"- {len(elim)}/{len(lost)} {l1} losses were eliminations, "
                   f"median end round {statistics.median(g['rounds'] - 1 for g in elim):.0f}.")
    limit = [g for g in lost if g["end"] == "round_limit"]
    if limit:
        gaps = [g["teams"][roles(g, us)[3]]["final"]["longest"] - g["teams"][roles(g, us)[1]]["final"]["longest"]
                for g in limit]
        out.append(f"- {len(limit)} {l1} round-limit losses; median longest-dragon gap {statistics.median(gaps):.0f}.")
    if A["cpu_max"] > 0.8 * BUDGET or A["exceeded"] or A["tle"]:
        out.append(f"- {l1} CPU: max {A['cpu_max'] / 1e6:.0f}M of {BUDGET // 1_000_000}M, "
                   f"{A['exceeded']} exceeded, {A['tle']} TLE.")
    if len(out) == 1:
        out.append("- nothing stands out.")
    return out


def detail(g, us, every):
    a, sa, b, sb = roles(g, us)
    out = [f"# {g['id']} (battle {g['battle']}) · {g['map']} {g['size'][0]}x{g['size'][1]}",
           f"{a}={sa} {b}={sb} · winner {g['winner']} · {g['end']} at round {g['rounds'] - 1} · "
           f"first contact round {g['contact']} · longest-dragon lead changes {lead_changes(g)} · "
           f"{a} last ahead: {last_ahead(g, sa) if last_ahead(g, sa) is not None else 'never'}",
           f"final (alive/longest/total): {a} {fmt_final(g['teams'][sa]['final'])} · {b} {fmt_final(g['teams'][sb]['final'])}",
           "", "## Timeline (alive/total/longest)",
           f"round | {a} | {b} | {a} deaths by cause (since last row) | {b} deaths by cause", "---|---|---|---|---"]
    rows = [r for r in g["timeline"] if r["round"] % every == 0 or r is g["timeline"][-1]]
    prev = -1
    for r in rows:
        window = [d for d in g["deaths"] if prev < d[0] <= r["round"]]
        cell = lambda side: " ".join(f"{CAUSE[c]}:{n}" for c, n in  # noqa: E731
                                     Counter(d[2] for d in window if d[1] == side).most_common()) or "-"
        out.append(f"{r['round']} | {'/'.join(map(str, r[sa]))} | {'/'.join(map(str, r[sb]))} | {cell(sa)} | {cell(sb)}")
        prev = r["round"]
    out += ["", "## Teams", f"stat | {a} | {b}", "---|---|---"]
    s1, s2 = g["teams"][sa], g["teams"][sb]
    fields = [
        ("pearls eaten", lambda s: s["pearls"]),
        ("splits (first at round)", lambda s: f"{s['splits']} ({s['first_split']})"),
        ("split at length (top)", lambda s: top(s["split_parent_len"])),
        ("child length (top)", lambda s: top(s["child_len"])),
        ("peak alive / total / longest (round)", lambda s: " / ".join(f"{v}@{r}" for v, r in
                                                                     (s["peak_alive"], s["peak_total"], s["peak_longest"]))),
        ("deaths by cause", lambda s: " ".join(f"{c}:{n}" for c, n in Counter(s["deaths"]).most_common()) or "-"),
        ("kills / head-on trades / friendly-fire deaths", lambda s: f"{s['kills']} / {s['headon_trades']} / {s['friendly']}"),
        (f"infant deaths / median age / median len at death", lambda s: f"{s['infant_deaths']} / "
         f"{s['median_death_age']} / {s['median_death_len']}"),
        ("length lost to deaths", lambda s: s["len_lost"]),
        ("moves / sprints / extra steps", lambda s: f"{s['moves']} / {s['sprints']} / {s['extra_steps']}"),
        ("idle / suicides / exceeded / TLE", lambda s: f"{s['idle']} / {s['suicides']} / {s['exceeded']} / {s['tle']}"),
        ("CPU mean / p95 / max", lambda s: "-" if not s["cpu"] else
            f"{s['cpu']['mean'] / 1e6:.1f}M / {s['cpu']['p95'] / 1e6:.1f}M / {s['cpu']['max'] / 1e6:.1f}M"),
    ]
    for name, f in fields:
        out.append(f"{name} | {f(s1)} | {f(s2)}")
    big = sorted((d for d in g["deaths"] if d[4] >= 8), key=lambda d: -d[4])[:10]
    if big:
        out += ["", "## Biggest deaths (length >= 8)", "round | team | cause | into team | length | age"]
        out += [f"{d[0]} | {a if d[1] == sa else b} | {CAUSE[d[2]]} | "
                f"{'-' if d[3] is None else a if d[3] == sa else b} | {d[4]} | {d[5]}" for d in big]
    return out


# -- CLI -----------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("paths", nargs="*", default=[str(ROOT / "replays")],
                    help="replay files, .zip bundles, or folders (default: replays/)")
    ap.add_argument("--us", default="auto", choices=["auto", "A", "B", "none"],
                    help="which side is ours (default: auto-detect, else winner vs loser)")
    ap.add_argument("--game", help="print one game in detail, e.g. M120320")
    ap.add_argument("--every", type=int, default=50, help="timeline step for --game (multiple of 10)")
    ap.add_argument("--maps", action="store_true", help="add a per-map breakdown")
    ap.add_argument("--json", metavar="FILE", help="also write all per-game stats to FILE")
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--workers", type=int)
    a = ap.parse_args(argv)
    if a.every % SAMPLE:
        ap.error(f"--every must be a multiple of {SAMPLE}")

    games = collect(a.paths, not a.no_cache, a.workers, a.game)
    if not games:
        sys.exit("no replays found" + (f" matching {a.game}" if a.game else ""))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(games, indent=1), encoding="utf8")
    lines = []
    for g in games if a.game else []:
        lines += detail(g, a.us, a.every) + [""]
    if not a.game:
        # us/them, winner/loser and A/B games get separate reports, since
        # their aggregates compare different things
        groups = {}
        for g in games:
            groups.setdefault(roles(g, a.us)[0], []).append(g)
        for label in ("us", "winner", "A"):
            if label in groups:
                lines += overview(groups[label], a.us, a.maps) + [""]
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
