"""Harvest public battles from game.battlecode.au.

Every battle on the site is public. This pages through the battle list,
keeps the ones worth learning from (by default: ranked, both teams rated
>= --min-elo), downloads every game's replay (gzip'd, as served) and records
metadata in data/index.jsonl. Maps embedded in the replays are extracted to
maps/server/.

    python -m bcsim.scrape --pages 40 --min-elo 1700
    python -m bcsim.scrape --maps-only        # just refresh maps/server from data/

Re-running is incremental: known battles and downloaded replays are skipped.
Requests are rate limited; please keep it that way.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from . import replay as rp
from .paths import DATA, MAPS

SITE = "https://game.battlecode.au"
REPLAYS = DATA / "replays"
INDEX = DATA / "index.jsonl"
UA = "unswbc-local-trainer (team 777)"


class RateLimiter:
    def __init__(self, per_second: float) -> None:
        self.gap = 1.0 / per_second
        self.next = 0.0
        self.lock = threading.Lock()

    def wait(self) -> None:
        with self.lock:
            now = time.monotonic()
            if now < self.next:
                time.sleep(self.next - now)
                now = self.next
            self.next = now + self.gap


LIMIT = RateLimiter(4.0)


def fetch(url: str, tries: int = 4) -> bytes:
    for attempt in range(tries):
        LIMIT.wait()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (404, 403):
                raise
            time.sleep(2 ** attempt)
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            time.sleep(2 ** attempt)
    raise RuntimeError(f"giving up on {url}")


def devalue(payload: dict, node: int = 1):
    """Decode a SvelteKit __data.json node (flat, index-referenced)."""
    data = payload["nodes"][node]["data"]

    def r(i):
        if not isinstance(i, int) or i < 0:
            return None
        v = data[i]
        if isinstance(v, dict):
            return {k: r(j) for k, j in v.items()}
        if isinstance(v, list):
            if len(v) == 2 and v[0] == "Date":
                return v[1]
            return [r(j) for j in v]
        return v

    return r(0)


def battle_page(page: int, team: int | None = None, ranked_only: bool = True) -> dict:
    query = f"page={page}" + (f"&teams={team}" if team is not None else "")
    if team is not None and ranked_only:
        query += "&kind=ranked"
    return devalue(json.loads(fetch(f"{SITE}/battles/__data.json?{query}")))


def battle_games(match_id: int) -> dict:
    return devalue(json.loads(fetch(f"{SITE}/visualiser/__data.json?match={match_id}")))


def known_battles() -> set[int]:
    if not INDEX.is_file():
        return set()
    return {json.loads(l)["battle"] for l in INDEX.read_text(encoding="utf8").splitlines() if l.strip()}


def download_replay(game_id: int) -> pathlib.Path | None:
    out = REPLAYS / f"{game_id}.replay"
    if out.is_file() and out.stat().st_size > 0:
        return out
    try:
        blob = fetch(f"{SITE}/api/matches/{game_id}/replay")
    except urllib.error.HTTPError:
        return None
    out.write_bytes(blob)
    return out


def _safe(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name).strip("_") or "map"


def _norm(text: str) -> str:
    """Map content without its name, for spotting duplicates."""
    return "\n".join(l.strip() for l in text.splitlines()
                     if l.strip() and not l.startswith("MAP_NAME"))


_BUNDLED: dict[str, str] | None = None


def bundled_maps() -> dict[str, str]:
    global _BUNDLED
    if _BUNDLED is None:
        _BUNDLED = {_norm(p.read_text(encoding="utf8")): p.stem for p in MAPS.glob("*.map")}
    return _BUNDLED


def extract_map(path: pathlib.Path, seen: dict[str, str]) -> str | None:
    """Save the replay's map under maps/server/ unless we already have it.
    Returns the local map name (bundled or server)."""
    try:
        r = rp.load(path)
    except Exception:
        return None
    text = r.map_text.replace("\r\n", "\n").strip() + "\n"
    if _norm(text) in bundled_maps():
        return bundled_maps()[_norm(text)]
    digest = hashlib.sha1(text.encode()).hexdigest()[:8]
    if digest in seen:
        return seen[digest]
    name = _safe(r.map_name or f"unnamed_{digest}")
    dest = MAPS / "server" / f"{name}.map"
    if dest.is_file() and dest.read_text(encoding="utf8") != text:
        dest = MAPS / "server" / f"{name}_{digest}.map"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf8", newline="\n")
    seen[digest] = dest.stem
    return dest.stem


def refresh_maps() -> None:
    seen: dict[str, str] = {}
    for p in (MAPS / "server").glob("*.map") if (MAPS / "server").is_dir() else []:
        seen[hashlib.sha1(p.read_text(encoding="utf8").encode()).hexdigest()[:8]] = p.stem
    for f in sorted(REPLAYS.glob("*.replay")):
        extract_map(f, seen)
    print(f"{len(list((MAPS / 'server').glob('*.map')))} server maps in {MAPS / 'server'}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pages", type=int, default=20, help="battle-list pages to scan (25 battles each)")
    ap.add_argument("--start-page", type=int, default=1)
    ap.add_argument("--min-elo", type=int, default=1650, help="both teams at least this rated")
    ap.add_argument("--unranked", action="store_true", help="also keep unranked battles")
    ap.add_argument("--max-battles", type=int, default=400)
    ap.add_argument("--workers", type=int, default=3, help="parallel downloads (still rate limited)")
    ap.add_argument("--maps-only", action="store_true")
    ap.add_argument("--team", type=int, action="append",
                    help="team id (repeatable): take its most recent ranked battles, "
                         "ignoring --min-elo; --max-battles applies per team")
    ap.add_argument("--submission", type=int, action="append",
                    help="submission id (repeatable): download only battles where either side "
                         "played one of these (checked before any replay is fetched)")
    args = ap.parse_args()

    REPLAYS.mkdir(parents=True, exist_ok=True)
    if args.maps_only:
        refresh_maps()
        return

    have = known_battles()
    picked = []
    for team in args.team or [None]:
        mine = []
        for page in range(args.start_page, args.start_page + args.pages):
            try:
                listing = battle_page(page, team, not args.unranked)
            except Exception as e:
                print(f"page {page}: {e}")
                break
            rows = listing.get("battles") or []
            if not rows:
                break
            for b in rows:
                if b.get("wait") is not None or (team is None and b["id"] in have):
                    continue
                if b.get("outcome") not in ("a", "b", "draw") or not b.get("resultsA"):
                    continue
                if not b["ranked"] and not args.unranked:
                    continue
                if team is None and min(b["a"]["elo"], b["b"]["elo"]) < args.min_elo:
                    continue
                # known battles still count toward a team's quota, so reruns
                # top up to --max-battles instead of reaching further back
                mine.append(b)
            label = f"team {team} " if team is not None else ""
            print(f"{label}page {page}: {len(mine)} battles selected so far")
            if len(mine) >= args.max_battles:
                break
        picked += [b for b in mine[:args.max_battles] if b["id"] not in have]
        have |= {b["id"] for b in picked}

    seen: dict[str, str] = {}
    done = 0

    def handle(b: dict) -> dict | None:
        try:
            info = battle_games(b["replayId"])
        except Exception as e:
            print(f"battle {b['id']}: {e}")
            return None
        match = (info.get("battle") or {}).get("match", {})
        if args.submission and not {match.get("submissionAId"), match.get("submissionBId")} & set(args.submission):
            return None
        games = [g for g in (info.get("games") or []) if g.get("hasReplay")]
        rows = []
        for g in games:
            path = download_replay(g["id"])
            mp = extract_map(path, seen) if path else None
            rows.append({"game": g["id"], "winner": g.get("winner"), "map": mp,
                         "file": path.name if path else None})
        return {
            "battle": b["id"], "at": b["at"], "ranked": b["ranked"],
            "a": b["a"], "b": b["b"], "outcome": b["outcome"],
            "submission_a": (info.get("battle") or {}).get("match", {}).get("submissionAId"),
            "submission_b": (info.get("battle") or {}).get("match", {}).get("submissionBId"),
            "games": rows,
        }

    with ThreadPoolExecutor(args.workers) as pool, INDEX.open("a", encoding="utf8") as idx:
        for rec in pool.map(handle, picked):
            if rec is None:
                continue
            idx.write(json.dumps(rec) + "\n")
            idx.flush()
            done += 1
            if done % 10 == 0 or done == len(picked):
                print(f"{done}/{len(picked)} battles downloaded")
    refresh_maps()


if __name__ == "__main__":
    main()
