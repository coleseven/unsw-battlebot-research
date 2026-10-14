import os, sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
os.environ["BCSIM_DETERMINISTIC_V6"] = "1"; os.environ["BCSIM_CPP_INPROC"] = "1"
def one(args):
    from bcsim import match
    m, a, b, seed = args
    r = match.play(Path(m), Path(a), Path(b), seed=seed)
    return (r.winner, r.rounds, r.a_length, r.b_length, r.a_longest, r.b_longest, tuple(sorted(r.deaths.items())), r.error)
if __name__ == "__main__":
    from bcsim import official_suite, match
    dev, base = sys.argv[1], sys.argv[2]
    maps = [str(m) for m in official_suite.official_maps()] if len(sys.argv) < 4 else [str(m) for m in official_suite.ranked_maps() if m.stem in sys.argv[3].split(",")]
    match.prebuild([dev, base])
    pairs = []
    for m in maps:
        for opp in ("opponents/splitter", "versions/v6"):
            for seed in (1, 2):
                pairs.append(((m, dev, opp, seed), (m, base, opp, seed)))
                pairs.append(((m, opp, dev, seed), (m, opp, base, seed)))
    with ProcessPoolExecutor(12) as ex:
        a = list(ex.map(one, [p[0] for p in pairs])); b = list(ex.map(one, [p[1] for p in pairs]))
    same = sum(x == y for x, y in zip(a, b))
    print("identical", same, "of", len(pairs))
    for p, x, y in zip(pairs, a, b):
        if x != y: print("DIFF", Path(p[0][0]).stem, p[0][1:], x[:6], y[:6])
