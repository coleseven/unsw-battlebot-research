import glob
from collections import Counter, defaultdict
from pathlib import Path
from bcsim import analyze
if __name__ == "__main__":
    for bot in ("v9n-base-bot",):
        files = sorted(glob.glob(f"results/v9n-check/{bot}_*cpp_nicked_v75_*.replay"))
        tot = defaultdict(Counter); ho_len = Counter(); ho_rounds = []; n = 0
        for f in files:
            side = Path(f).stem[-1]; o = "B" if side == "A" else "A"; n += 1
            g = analyze.game_stats(Path(f).read_bytes())
            lens = {}
            for rnd, t, why, killer, L, age, did, other in g["deaths"]:
                who = "us" if t == side else "them"
                tot[who][why] += 1
                if why == "O": tot[who]["O_by_" + ("them" if killer == (o if who == "us" else side) else "own")] += 1
                if why == "H": lens[did] = (rnd, t, L, other)
            seen = set()
            for did, (rnd, t, L, other) in lens.items():
                if other in lens and (other, did) not in seen and did not in seen:
                    seen.update({(did, other), did, other})
                    r2, t2, L2, _ = lens[other]
                    if t == t2: ho_len["own-team head-on"] += 1; continue
                    ours, theirs = (L, L2) if t == side else (L2, L)
                    ho_len["we lost longer" if ours > theirs else "we lost shorter" if ours < theirs else "equal"] += 1
                    ho_len["our length lost"] += ours; ho_len["their length lost"] += theirs
                    ho_rounds.append(rnd)
        print(bot, n, "games vs nicked v75")
        for who in ("us", "them"): print("  deaths", who, {k: round(v / n, 1) for k, v in tot[who].most_common()})
        print("  head-on pairs (all games):", dict(ho_len))
        print("  head-on trades by round:", sorted(Counter(r // 100 * 100 for r in ho_rounds).items()))
