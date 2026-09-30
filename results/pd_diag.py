import os, json
os.environ["BCSIM_DETERMINISTIC_V6"] = "1"; os.environ["BCSIM_CPP_INPROC"] = "1"
from pathlib import Path
from collections import Counter
from bcsim import guard, match, official_suite, analyze
maps = {p.stem: p for p in official_suite.ranked_maps()}
m = maps["Prisoners_Dilemma"]
with guard.slot("pd-diag"):
    for seed in (281001, 281002):
        for us in "AB":
            a, b = (Path("versions/v10h"), Path("sparring/cpp_nicked_v92")) if us == "A" else (Path("sparring/cpp_nicked_v92"), Path("versions/v10h"))
            out = Path(f"results/pd-diag/pd-{seed}-{us}.replay")
            r = match.play(m, a, b, seed=seed, replay_to=out)
            g = analyze.game_stats(out.read_bytes() if not str(out).endswith("gz") else out.read_bytes())
            th = "B" if us == "A" else "A"
            print(f"\nseed {seed} we={us} winner={r.winner} {r.reason} r{r.rounds}")
            print(" round: ours [alive,total,longest] | theirs")
            for row in g["timeline"]:
                if row["round"] <= 260 and row["round"] % 20 == 0:
                    print(f"  {row['round']:3}: {row[us]} | {row[th]}")
            dc = Counter(); kc = Counter()
            for rnd, t, why, killer, ln, age, d, other in g["deaths"]:
                if t == us and rnd <= 250: dc[(rnd // 50 * 50, why)] += 1
                if t == us and killer == th: kc[why] += 1
            print(" our deaths by (bucket, cause):", dict(sorted(dc.items())))
            print(" our deaths caused by them:", dict(kc), " pearls ours/theirs:", g["teams"][us]["pearls"], g["teams"][th]["pearls"], " splits", g["teams"][us]["splits"], g["teams"][th]["splits"], flush=True)
