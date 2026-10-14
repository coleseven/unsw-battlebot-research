import json, statistics as st
from collections import defaultdict
from pathlib import Path
from bcsim import analyze
if __name__ == "__main__":
    games = [json.loads(l) for l in open("results/v10-vs-v75/games.jsonl")]
    for mp in ("trophy", "schooltime", "Slithery_Fight", "Prisoners_Dilemma"):
        print("==", mp)
        for g in [g for g in games if g["map"] == mp]:
            s = "A" if g["bot_a"] == "v10" else "B"; o = "B" if s == "A" else "A"
            st_ = analyze.game_stats(Path(g["replay"]).read_bytes()); tl = {x["round"]: x for x in st_["timeline"]}
            T, O = st_["teams"][s], st_["teams"][o]
            curve = " ".join(f"r{r}:{tl[r][s][1]}/{tl[r][s][2]} v {tl[r][o][1]}/{tl[r][o][2]}" for r in (100, 200, 300, 400, 490) if r in tl)
            print(f"  seed {g['seed']} side {s} end {st_['end']}@{st_['rounds']}  pearls {T['pearls']} v {O['pearls']}  feed {T['deaths'].get('no-move',0)} v {O['deaths'].get('no-move',0)}  headon {T['deaths'].get('head-on',0)} v {O['deaths'].get('head-on',0)}  kelp {T['deaths'].get('kelp',0)} v {O['deaths'].get('kelp',0)} | total/longest {curve}")
