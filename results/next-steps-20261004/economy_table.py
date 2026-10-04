import json, sys
cs = json.load(open("results/next-steps-20261004/economy_cases.json"))
WS = ("0", "20", "40", "60", "80", "100")
def early(s, k, ws=WS): return sum(s.get(w, {}).get(k, 0) for w in ws)
def row(c, ws, label):
    us, th = c["us"], "B" if c["us"] == "A" else "A"
    S, T = c["stats"][us], c["stats"][th]
    cov = lambda s: early(s, "cov_sum", ws) / max(1, early(s, "rounds", ws))
    d = lambda s: "/".join(str(early(s, "death_" + x, ws)) for x in "WHOS")
    return (f"{c['group'][:12]:12} {c['map'][:9]:9} {c['opponent'][:12]:12} {c['side']} | {str(c['deficit_len']):>4} {str(c['deficit_pop']):>4} | "
            f"{early(S,'nat',ws):3}/{early(S,'drop',ws):<3} {early(S,'wturns',ws):5} {early(S,'passed',ws):3} {early(S,'dry20',ws):5} {cov(S):4.1f} {early(S,'splits',ws):3} {d(S):9} | "
            f"{early(T,'nat',ws):3}/{early(T,'drop',ws):<3} {early(T,'wturns',ws):5} {early(T,'passed',ws):3} {early(T,'dry20',ws):5} {cov(T):4.1f} {early(T,'splits',ws):3} {d(T):9}")
ws = tuple(sys.argv[1].split(",")) if len(sys.argv) > 1 else WS
print("group        map       opp          s | dLen dPop | US nat/drop wturn pass  dry20 cov spl W/H/O/S   | THEM nat/drop wturn pass dry20 cov spl W/H/O/S")
for c in cs: print(row(c, ws, ""))
