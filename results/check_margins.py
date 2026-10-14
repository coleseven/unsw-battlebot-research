import json, time
from bcsim import tune
if __name__ == "__main__":
    D = "results/20260926-182526-tune-4fcea2/gen000"
    games = [json.loads(l) for l in open(D + "/games.jsonl")][:80]
    t = time.time(); serial = {g["replay"]: tune._side_margins(g["replay"]) for g in games}; t1 = time.time() - t
    t = time.time(); par = tune.replay_margins(games, 8); t2 = time.time() - t
    print(len(games), "games; identical:", serial == par, f"serial {t1:.1f}s parallel {t2:.1f}s")
