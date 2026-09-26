"""Scouting reports on specific ladder teams from downloaded ranked games.

    python -m bcsim.scrape --team 470 --max-battles 12 --pages 3   # download first
    python -m bcsim.scout --team 470 --team 545                   # compare + per-team detail
    python -m bcsim.scout --leaderboard 10                        # top 10 by current rating

Games come from data/index.jsonl (written by bcsim.scrape); the team's side in
each replay comes from the index, and is cross-checked against every game's
recorded winner. Per-game stats reuse bcsim.analyze and its cache.
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

from . import analyze as an
from .paths import DATA

INDEX = DATA / "index.jsonl"
MARKS = (50, 100, 200, 300, 400, 450, 499)


def team_games(team: int, battles: int, submissions=None, unranked=False) -> list[dict]:
    rows = [json.loads(l) for l in INDEX.read_text(encoding="utf8").splitlines() if l.strip()]
    rows = [r for r in rows if (r.get("ranked") or unranked) and team in (r["a"]["id"], r["b"]["id"])]
    if submissions:
        rows = [r for r in rows
                if r.get("submission_" + ("a" if r["a"]["id"] == team else "b")) in submissions]
    rows.sort(key=lambda r: r["at"], reverse=True)
    out = []
    for r in rows[:battles]:
        side = "a" if r["a"]["id"] == team else "b"
        other = r["b" if side == "a" else "a"]
        for g in r["games"]:
            if g.get("file"):
                out.append({"battle": r["battle"], "at": r["at"], "side": side.upper(),
                            "name": r[side]["name"], "elo": r[side]["elo"],
                            "opp": other["name"], "opp_elo": other["elo"],
                            "submission": r.get(f"submission_{side}"), "index_winner": g.get("winner"),
                            "loader": ("file", str(DATA / "replays" / g["file"]), None)})
    return out


def _load(loader):
    return an.load_stats(loader)


def load(entries, workers=None):
    todo = [e for e in entries if not an._cached(e["loader"]).is_file()]
    done = {}
    if len(todo) > 1:
        with ProcessPoolExecutor(max_workers=workers or os.cpu_count()) as ex:
            done = dict(zip((e["loader"] for e in todo), ex.map(_load, (e["loader"] for e in todo))))
    for e in entries:
        e["g"] = done.get(e["loader"]) or an.load_stats(e["loader"])
    # rematches between the same two submissions replay identically; count once
    seen, unique = set(), []
    for e in entries:
        g = e["g"]
        key = (e["side"], g["map"], g["rounds"], g["winner"], json.dumps(g["timeline"]), len(g["deaths"]))
        if key not in seen:
            seen.add(key)
            unique.append(e)
    return unique


def at(g, side, r, i):
    rows = [x for x in g["timeline"] if x["round"] <= r]
    return rows[-1][side][i] if rows else 0


def med(xs, fmt="{:.0f}"):
    xs = [x for x in xs if x is not None]
    return fmt.format(statistics.median(xs)) if xs else "-"


def trade_up(g, side):
    """Head-on trades where our dead dragon was shorter than theirs, as (up, even, down)."""
    info = {d[6]: d for d in g["deaths"] if len(d) > 7}
    up = even = down = 0
    for d in g["deaths"]:
        if len(d) < 8 or d[1] != side or d[2] != "H" or d[3] in (None, side):
            continue
        o = info.get(d[7])
        if o is None:
            continue
        up += d[4] < o[4]
        even += d[4] == o[4]
        down += d[4] > o[4]
    return up, even, down


def summarize(team, entries):
    games = [e for e in entries]
    res = Counter()
    mismatches = 0
    for e in games:
        g, s = e["g"], e["side"]
        o = "B" if s == "A" else "A"
        e["o"] = o
        e["res"] = "D" if g["winner"] is None else "W" if g["winner"] == s else "L"
        iw = e["index_winner"]
        if iw is not None and (iw.upper() if isinstance(iw, str) else iw) != g["winner"]:
            mismatches += 1
        res[e["res"]] += 1
    return res, mismatches


def per_game_rates(entries, key):
    return sum(e["g"]["teams"][e["side"]][key] for e in entries) / max(1, len(entries))


def compare_table(teams):
    out = ["## Comparison (their side, per game)",
           "team | elo | games | W-L-D | elim wins / losses | pearls | splits | last split (median rd) | "
           "peak alive | longest @499 in wins | deaths | own-team deaths | kills | head-on up/even/down | "
           "empty-turn deaths (fed) | sprint % | portal steps | sonar",
           "---|" * 18]
    for t in teams:
        es, res = t["entries"], t["res"]
        elim = Counter(e["res"] for e in es if e["g"]["end"] == "eliminated")
        T = lambda e: e["g"]["teams"][e["side"]]  # noqa: E731
        ups = [trade_up(e["g"], e["side"]) for e in es]
        up, ev, dn = (sum(x[i] for x in ups) for i in range(3))
        tot = max(1, up + ev + dn)
        moves = sum(T(e)["moves"] for e in es)
        wins = [e for e in es if e["res"] == "W" and e["g"]["end"] == "round_limit"]
        out.append(
            f"{t['name']} | {t['elo']} | {len(es)} | {res['W']}-{res['L']}-{res['D']} | {elim['W']} / {elim['L']} | "
            f"{per_game_rates(es, 'pearls'):.0f} | {per_game_rates(es, 'splits'):.0f} | "
            f"{med(T(e)['last_split'] for e in es)} | {med(T(e)['peak_alive'][0] for e in es)} | "
            f"{med(at(e['g'], e['side'], 499, 2) for e in wins)} | "
            f"{sum(sum(T(e)['deaths'].values()) for e in es) / len(es):.0f} | "
            f"{per_game_rates(es, 'friendly'):.0f} | {per_game_rates(es, 'kills'):.1f} | "
            f"{up / tot:.0%}/{ev / tot:.0%}/{dn / tot:.0%} | "
            f"{per_game_rates(es, 'empty_turn_deaths'):.1f} ({per_game_rates(es, 'fed_deaths'):.1f}) | "
            f"{an.pct(sum(T(e)['sprints'] for e in es), moves)} | "
            f"{per_game_rates(es, 'portal_steps'):.1f} | {per_game_rates(es, 'sonar'):.0f}")
    return out


def team_detail(t):
    es = t["entries"]
    subs = Counter(e["submission"] for e in es)
    out = [f"## {t['name']} (id {t['id']}, elo {t['elo']})",
           f"{len(es)} distinct games ({t.get('dupes', 0)} identical rematches dropped) from "
           f"{len({e['battle'] for e in es})} battles, "
           f"{es[-1]['at'][:16]} to {es[0]['at'][:16]} · submissions {dict(subs.most_common())} · "
           f"median opponent elo {med(e['opp_elo'] for e in es)}"]
    # per map
    out += ["", "map | W-L-D | elim W-L | limit W-L | median longest us/them @499 | median alive us/them @499",
            "---|---|---|---|---|---"]
    by = {}
    for e in es:
        by.setdefault(e["g"]["map"], []).append(e)
    for m, gs in sorted(by.items(), key=lambda kv: -len(kv[1])):
        r = Counter(e["res"] for e in gs)
        el = Counter(e["res"] for e in gs if e["g"]["end"] == "eliminated")
        li = Counter(e["res"] for e in gs if e["g"]["end"] == "round_limit")
        out.append(f"{m} | {r['W']}-{r['L']}-{r['D']} | {el['W']}-{el['L']} | {li['W']}-{li['L']} | "
                   f"{med(at(e['g'], e['side'], 499, 2) for e in gs)}/{med(at(e['g'], e['o'], 499, 2) for e in gs)} | "
                   f"{med(at(e['g'], e['side'], 499, 0) for e in gs)}/{med(at(e['g'], e['o'], 499, 0) for e in gs)}")
    # curves
    out += ["", "median curve (alive / total / longest), theirs vs opponent",
            "games | " + " | ".join(f"r{r}" for r in MARKS), "---|" * (len(MARKS) + 1)]
    for label, sel in (("wins", [e for e in es if e["res"] == "W"]), ("losses", [e for e in es if e["res"] == "L"])):
        if not sel:
            continue
        cells = []
        for r in MARKS:
            mine = "/".join(med(at(e["g"], e["side"], r, i) for e in sel) for i in range(3))
            them = "/".join(med(at(e["g"], e["o"], r, i) for e in sel) for i in range(3))
            cells.append(f"{mine} v {them}")
        out.append(f"{label} ({len(sel)}) | " + " | ".join(cells))
    # style
    T = lambda e: e["g"]["teams"][e["side"]]  # noqa: E731
    parent, child, deaths = Counter(), Counter(), Counter()
    for e in es:
        parent.update({int(k): v for k, v in T(e)["split_parent_len"].items()})
        child.update({int(k): v for k, v in T(e)["child_len"].items()})
        deaths.update(T(e)["deaths"])
    nd = sum(deaths.values())
    out += ["", f"splits at length {an.top(parent, 4)} · child length {an.top(child, 3)} · "
                f"median first/last split round {med(T(e)['first_split'] for e in es)}/{med(T(e)['last_split'] for e in es)} · "
                f"late splits (r>=400) {per_game_rates(es, 'late_splits'):.1f}/game",
            "deaths: " + " ".join(f"{c} {v / nd:.0%}" for c, v in deaths.most_common()) +
            f" · infant (<= {an.INFANT} rounds) {an.pct(sum(T(e)['infant_deaths'] for e in es), nd)}"
            f" · median age {med(T(e)['median_death_age'] for e in es)}"]
    # losses
    losses = [e for e in es if e["res"] != "W"]
    if losses:
        out += ["", "losses/draws: opponent (elo) · map · end · final alive/longest/total them v opponent"]
        for e in losses:
            g = e["g"]
            out.append(f"- {e['opp']} ({e['opp_elo']}) · {g['map']} · {g['end']}@{g['rounds'] - 1} · "
                       f"{an.fmt_final(g['teams'][e['side']]['final'])} v {an.fmt_final(g['teams'][e['o']]['final'])}")
    return out


def leaderboard(n):
    from . import scrape
    d = scrape.devalue(json.loads(scrape.fetch(scrape.SITE + "/leaderboard/__data.json")))
    return [t["id"] for t in d["teams"][:n]]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--team", type=int, action="append", default=[])
    ap.add_argument("--leaderboard", type=int, help="add the current top N teams")
    ap.add_argument("--battles", type=int, default=12, help="most recent ranked battles per team")
    ap.add_argument("--submission", type=int, action="append",
                    help="only battles where the team played this submission (repeatable)")
    ap.add_argument("--unranked", action="store_true", help="include unranked battles")
    ap.add_argument("--json", metavar="FILE")
    ap.add_argument("--workers", type=int)
    a = ap.parse_args(argv)
    ids = list(dict.fromkeys(a.team + (leaderboard(a.leaderboard) if a.leaderboard else [])))
    if not ids:
        ap.error("give --team and/or --leaderboard")
    teams = []
    for tid in ids:
        es = team_games(tid, a.battles, a.submission, a.unranked)
        if not es:
            print(f"team {tid}: no downloaded ranked games (run bcsim.scrape --team {tid})", file=sys.stderr)
            continue
        teams.append({"id": tid, "name": es[0]["name"], "elo": es[0]["elo"], "entries": es})
    for t in teams:
        before = len(t["entries"])
        t["entries"] = load(t["entries"], a.workers)
        t["dupes"] = before - len(t["entries"])
        t["res"], t["mismatch"] = summarize(t["id"], t["entries"])
        if t["mismatch"]:
            print(f"WARNING {t['name']}: {t['mismatch']} games whose index winner disagrees with the replay",
                  file=sys.stderr)
    lines = [f"# Scouting report: {len(teams)} teams", "",
             "Their side unless noted. Elo is the rating recorded with their most recent downloaded battle.",
             "Games are distinct: rematches of the same two submissions on a map replay identically.", ""]
    lines += compare_table(teams)
    for t in teams:
        lines += [""] + team_detail(t)
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(lines))
    if a.json:
        slim = [{"id": t["id"], "name": t["name"], "elo": t["elo"],
                 "games": [{k: v for k, v in e.items() if k != "loader"} for e in t["entries"]]} for t in teams]
        with open(a.json, "w", encoding="utf8") as f:
            json.dump(slim, f)


if __name__ == "__main__":
    main()
