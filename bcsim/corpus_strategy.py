"""Descriptive strategy audit of high-rated battles already on disk.

Uses replay events, not hidden code. No network calls, training, or mutation of
the corpus. Ratings are the scraper's recorded snapshot, not current ratings.
"""

import json
import uuid
from collections import Counter, defaultdict
from datetime import datetime

from . import population, reconstruct, replay
from .paths import DATA, RESULTS, file_hash


def game_stats(path):
    r = replay.load(path)
    board = reconstruct.Board(r.map_text)
    teams = {i: team for i, (team, _) in enumerate(board.dragons)}
    living = Counter(teams.values())
    stats = {t: Counter() for t in "AB"}
    lengths = {t: Counter() for t in "AB"}
    sizes = {t: Counter() for t in "AB"}
    phases = {t: Counter() for t in "AB"}
    rnd = 0
    for ev in r.events:
        if ev[0] == replay.ROUND_START:
            rnd = ev[1]
            for team in "AB":
                stats[team]["max_population"] = max(stats[team]["max_population"], living[team])
        elif ev[0] == replay.DRAGON_ACTION:
            team = teams[ev[1]]
            stats[team]["actions"] += 1
            stats[team]["budget_exceeded"] += bool(ev[4])
            stats[team]["timed_out"] += bool(ev[5])
            if ev[2] and ev[2][0] == "move":
                n = len(ev[2][1])
                stats[team]["move_actions"] += 1
                stats[team]["sprint_actions"] += n > 1
                stats[team]["extra_steps"] += n - 1
                stats[team]["max_sprint_steps"] = max(stats[team]["max_sprint_steps"], n)
        elif ev[0] == replay.DRAGON_SPLIT:
            _, parent, child, team, _, pbody, cbody = ev
            teams[child] = team
            living[team] += 1
            stats[team]["max_population"] = max(stats[team]["max_population"], living[team])
            stats[team]["splits"] += 1
            stats[team]["late_splits"] += rnd >= 450
            lengths[team][len(pbody) + len(cbody)] += 1
            sizes[team][len(cbody)] += 1
            phases[team][f"{rnd // 50 * 50}-{rnd // 50 * 50 + 49}"] += 1
        elif ev[0] == replay.DRAGON_DEATH:
            team = teams[ev[1]]
            living[team] -= 1
            stats[team]["deaths_" + ev[2]] += 1
    return {team: {"counts": dict(stats[team]), "split_lengths": dict(lengths[team]),
                   "child_sizes": dict(sizes[team]), "split_phases": dict(phases[team]),
                   "won": r.result["winner"] == team} for team in "AB"}


def main():
    index = DATA / "index.jsonl"
    battles = [json.loads(l) for l in index.read_text(encoding="utf8").splitlines() if l.strip()]
    # Keep only complete, downloaded battles. Spread across submission pairs
    # so one repeatedly matched pair does not occupy the entire sample.
    battles.sort(key=lambda b: (-min(b["a"]["elo"], b["b"]["elo"]), -b["battle"]))
    seen, selected = set(), []
    for b in battles:
        pair = tuple(sorted((b.get("submission_a") or str(b["a"]["id"]),
                             b.get("submission_b") or str(b["b"]["id"])), key=str))
        if pair in seen or not all((DATA / "replays" / g["file"]).is_file() for g in b["games"]):
            continue
        seen.add(pair)
        selected.append(b)
        if len(selected) == 12:
            break
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-corpus-strategy-" + uuid.uuid4().hex[:6])
    out.mkdir()
    aggregate = defaultdict(lambda: {"counts": Counter(), "split_lengths": Counter(),
                                     "child_sizes": Counter(), "split_phases": Counter(), "games": 0})
    games = []
    for b in selected:
        for g in b["games"]:
            path = DATA / "replays" / g["file"]
            stats = game_stats(path)
            games.append({"battle": b["battle"], "game": g["game"], "map": g["map"],
                          "file_hash": file_hash(path), "stats": stats})
            for side in "AB":
                info = b[side.lower()]
                key = f"{info['id']}:{b.get('submission_' + side.lower())}"
                dest = aggregate[key]
                dest["name"], dest["team"] = info["name"], info["id"]
                dest["games"] += 1
                for field in ("counts", "split_lengths", "child_sizes", "split_phases"):
                    for key_, value in stats[side][field].items():
                        if field == "counts" and key_.startswith("max_"):
                            dest[field][key_] = max(dest[field][key_], value)
                        else:
                            dest[field][key_] += value
        print(f"corpus audit: {len(games)} games", flush=True)
    serial = {key: {k: dict(v) if isinstance(v, Counter) else v for k, v in value.items()}
              for key, value in aggregate.items()}
    result = {"index_hash": file_hash(index), "battles": selected, "games": games, "policies": serial,
              "limits": "Twelve highest-minimum-recorded-Elo complete battles with distinct submission pairs. "
                        "Observational, selection-biased, possibly repeated policies; not independent policy tests "
                        "or causal evidence that frequent actions are good. No private source code accessed."}
    population.write_json(out / "audit.json", result)
    lines = ["# Downloaded strong-player strategy audit", "", result["limits"], "",
             "| Team / submission | Games | Splits | Common split lengths | Common child sizes | Late splits | Sprint share |",
             "|---|---:|---:|---|---|---:|---:|"]
    for key, p in sorted(aggregate.items()):
        c = p["counts"]
        fraction = c["sprint_actions"] / max(1, c["move_actions"])
        lines.append(f"| {p['name']} ({key}) | {p['games']} | {c['splits']} | "
                     f"{p['split_lengths'].most_common(3)} | {p['child_sizes'].most_common(3)} | "
                     f"{c['late_splits']} | {fraction:.2%} |")
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf8")
    print(f"Saved {out}", flush=True)
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main()
