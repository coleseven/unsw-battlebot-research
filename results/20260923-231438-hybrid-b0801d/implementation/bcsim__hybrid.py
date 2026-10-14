"""Frozen hybrid experiment: adaptive roles and matched linear/MLP imitation.

Artifacts are isolated under results. This never activates or uploads a bot.
"""

import argparse
import hashlib
import json
import os
import random
import shutil
import sys
import uuid
import zipfile
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

from . import arena, guarded, population, reconstruct, replay
from .paths import ROOT, RESULTS, bot_hash, file_hash, map_signature, resolve_maps

BASE = ROOT / "versions/v2"
CORPUS = RESULTS / "20260922-234132-corpus-strategy-de8cf0/audit.json"
MODES = ("mature", "opportunity")


def write_source(path, text):
    with path.open("x", encoding="utf8") as f:
        f.write(text)


def make_bot(source, dest, mode, model=None):
    population.snapshot(source, dest)
    (dest / "brain.py").rename(dest / "baseline_brain.py")
    shutil.copy2(ROOT / "experiments/hybrid/brain.py", dest / "brain.py")
    for name in ("adaptive_roles.py", "action_value.py"):
        shutil.copy2(ROOT / "framework" / name, dest / name)
    write_source(dest / "hybrid_config.py", f"MODE = {mode!r}\n")
    write_source(dest / "action_model.py", f"MODEL = {model!r}\n")
    return dest


def prepare():
    out = RESULTS / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-hybrid-" + uuid.uuid4().hex[:6])
    out.mkdir()
    for name in ("control_450", "reference_v2"):
        population.snapshot(BASE, out / "bots" / name)
    for name in ("splitter", "hunter"):
        population.snapshot(guarded.MOVEMENT / "bots" / name, out / "bots" / name)
    for mode in MODES:
        make_bot(BASE, out / "bots" / mode, mode)
    (out / "maps").mkdir()
    map_texts = [(p.stem, p.read_text()) for p in resolve_maps("all")]
    with zipfile.ZipFile(ROOT / "replays/mygames/battle-M120436-replays.zip") as z:
        for name in z.namelist():
            r = replay.decode(z.read(name))
            map_texts.append((r.map_name.replace(" ", "_"), r.map_text))
    maps, seen = [], set()
    for name, text in map_texts:
        sig = map_signature(SimpleNamespace(read_text=lambda **kw: text))
        if sig in seen:
            continue
        seen.add(sig)
        path = out / "maps" / f"{name}_{sig}.map"
        write_source(path, text)
        maps.append(str(path))
    corpus = json.loads(CORPUS.read_text())
    battles = sorted(corpus["battles"], key=lambda b: b["battle"])
    random.Random(28000).shuffle(battles)
    rows = []
    for i, battle in enumerate(battles):
        split = "train" if i < 8 else "dev" if i < 10 else "test"
        for game in battle["games"]:
            path = ROOT / "data/replays" / game["file"]
            rows.append({"game": game["game"], "battle": battle["battle"], "partition": split,
                         "path": str(path), "hash": file_hash(path)})
    implementation = out / "implementation"
    implementation.mkdir()
    sources = [ROOT / "bcsim" / n for n in ("hybrid.py", "reconstruct.py", "replay.py", "match.py",
                "arena.py", "bounded.py", "population.py", "guarded.py", "paths.py")]
    sources += [ROOT / "framework" / n for n in ("action_value.py", "adaptive_roles.py")]
    sources += [ROOT / "experiments/hybrid/brain.py"]
    hashes = {}
    for src in sources:
        name = str(src.relative_to(ROOT)).replace("\\", "__").replace("/", "__")
        shutil.copy2(src, implementation / name)
        hashes[str(src.relative_to(ROOT))] = file_hash(src)
    plan = {
        "question": "Do adaptive roles or a small learned movement ranker improve frozen v2?",
        "baseline_hash": bot_hash(BASE), "live_hash": bot_hash(ROOT / "mybot"),
        "maps": maps, "roles": list(MODES), "corpus": rows, "implementation": hashes,
        "sampling": {"stride_probability": .125, "max_rows_per_game": 4000, "seed": 28000},
        "training": {"hidden": 16, "epochs": 20, "batch": 512, "lr": .003,
                     "linear_seeds": [0], "mlp_seeds": [0, 1, 2]},
        "screen_seeds": list(range(28000, 28004)),
        "validation_seeds": list(range(29000, 29008)),
        "selection": "Best role and best evaluator separately, direct screen score must exceed .5. "
                     "MLP initialization chosen by dev imitation loss before matches. No retuning on test or matches.",
        "gate": "Each finalist direct v2 map-cluster 95% lower bound > .5 and paired "
                "pool improvement map-cluster 95% lower bound > 0. Then exact replay and judge budget checks. "
                "No automatic promotion; multiple finalists and familiar opponents limit generality.",
        "limits": "No hidden state or winner labels used for learning. Battles disjoint across training/dev/test, "
                  "NOT necessarily teams, submissions, maps. Current top-team archives are not training data. "
                  "Only ordinary visible-empty moves modeled; splitting remains v2. "
                  "Role experiments do not use learned movement. RNG changes bots, not engine map randomness."
    }
    population.write_json(out / "plan.json", plan)
    print(out, flush=True)
    return out


def extraction_job(args):
    spec, destination, feature_path = args
    import numpy as np
    sys.path.insert(0, str(feature_path))
    import bc
    import action_value
    import psutil
    psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if os.name == "nt" else 5)
    if psutil.virtual_memory().available < 4 * 2**30:
        raise RuntimeError("memory guard")
    assert file_hash(Path(spec["path"])) == spec["hash"]
    r = replay.load(spec["path"])
    rng = random.Random(28000 + int(spec["game"]))
    rows, masks, targets, rounds = [], [], [], []
    counts = Counter()
    eligible = 0
    for turn in reconstruct.turns(r):
        counts["turns"] += 1
        if rng.random() >= .125:
            continue
        counts["sampled"] += 1
        if not turn.action or turn.action[0] != "move" or len(turn.action[1]) != 1:
            counts["non_single_move"] += 1
            continue
        obs = bc.Obs(turn.block)
        directions = action_value.candidates(obs, turn.team)
        if turn.action[1] not in directions:
            counts["teacher_outside_candidate_set"] += 1
            continue
        if len(directions) < 2:
            counts["forced_single_choice"] += 1
            continue
        eligible += 1
        slot = len(rows) if len(rows) < 4000 else rng.randrange(eligible)
        if slot >= 4000:
            continue
        _, values = action_value.features(obs, turn.team, directions)
        x = np.zeros((4, len(action_value.FEATURES)), dtype=np.float32)
        mask = np.zeros(4, dtype=bool)
        for d, value in zip(directions, values):
            x[bc.DIRS.index(d)] = value
            mask[bc.DIRS.index(d)] = True
        row = (x, mask, bc.DIRS.index(turn.action[1]), turn.round)
        if slot == len(rows):
            rows.append(row[0]); masks.append(row[1]); targets.append(row[2]); rounds.append(row[3])
        else:
            rows[slot], masks[slot], targets[slot], rounds[slot] = row
    path = Path(destination) / f"{spec['game']}.npz"
    with path.open("xb") as f:
        np.savez_compressed(f, x=np.asarray(rows, dtype=np.float32).reshape(-1, 4, len(action_value.FEATURES)),
                            mask=np.asarray(masks, dtype=bool).reshape(-1, 4),
                            y=np.asarray(targets, dtype=np.int64), rounds=np.asarray(rounds, dtype=np.int16))
    return {**spec, "rows": len(rows), "eligible": eligible, "counts": dict(counts), "shard_hash": file_hash(path)}


def extract(out, workers):
    plan = json.loads((out / "plan.json").read_text())
    dest = out / "training_data"
    dest.mkdir()
    specs = plan["corpus"]
    rows = []
    with (dest / "progress.jsonl").open("x") as log:
        # Recycle after 12 games to bound decoder/reconstruction worker memory.
        for start in range(0, len(specs), 12):
            with ProcessPoolExecutor(workers) as pool:
                futures = [pool.submit(extraction_job, (s, str(dest), str(out / "bots/mature")))
                           for s in specs[start:start + 12]]
                for future in as_completed(futures):
                    row = future.result()
                    rows.append(row)
                    log.write(json.dumps(row) + "\n"); log.flush()
                    print(f"extracted {len(rows)}/{len(specs)} games; {row['game']}: {row['rows']} rows", flush=True)
    population.write_json(dest / "manifest.json", rows)


def train(out):
    import copy
    import numpy as np
    import torch
    import psutil
    torch.set_num_threads(2)
    psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if os.name == "nt" else 5)
    plan = json.loads((out / "plan.json").read_text())
    manifest = json.loads((out / "training_data/manifest.json").read_text())
    parts = {}
    for part in ("train", "dev", "test"):
        arrays = []
        for row in manifest:
            if row["partition"] != part or not row["rows"]:
                continue
            path = out / "training_data" / f"{row['game']}.npz"
            assert file_hash(path) == row["shard_hash"]
            with np.load(path) as z:
                arrays.append({k: z[k].copy() for k in ("x", "mask", "y")})
        parts[part] = {k: torch.from_numpy(np.concatenate([a[k] for a in arrays])) for k in ("x", "mask", "y")}
    def evaluate(net, part):
        data = parts[part]
        with torch.no_grad():
            logits = net(data["x"]).squeeze(-1).masked_fill(~data["mask"], -1e9)
            return {"loss": torch.nn.functional.cross_entropy(logits, data["y"]).item(),
                    "accuracy": (logits.argmax(-1) == data["y"]).float().mean().item(),
                    "rows": len(data["y"])}
    models = out / "models"
    models.mkdir()
    results, exports = {}, {}
    for kind, seed in [("linear", 0), ("mlp", 0), ("mlp", 1), ("mlp", 2)]:
        torch.manual_seed(seed)
        features = parts["train"]["x"].shape[-1]
        net = torch.nn.Linear(features, 1) if kind == "linear" else torch.nn.Sequential(
            torch.nn.Linear(features, 16), torch.nn.Tanh(), torch.nn.Linear(16, 1))
        optimizer = torch.optim.Adam(net.parameters(), lr=.003, weight_decay=1e-4)
        best_loss, best_state, history, best_epoch = float("inf"), None, [], 0
        for epoch in range(20):
            order = torch.randperm(len(parts["train"]["y"]))
            for ids in order.split(512):
                x, mask, y = (parts["train"][k][ids] for k in ("x", "mask", "y"))
                logits = net(x).squeeze(-1).masked_fill(~mask, -1e9)
                loss = torch.nn.functional.cross_entropy(logits, y)
                optimizer.zero_grad(); loss.backward(); optimizer.step()
            dev = evaluate(net, "dev")
            history.append(dev)
            if dev["loss"] < best_loss:
                best_loss, best_state, best_epoch = dev["loss"], copy.deepcopy(net.state_dict()), epoch + 1
        net.load_state_dict(best_state)
        if kind == "linear":
            model = {"kind": kind, "weight": net.weight.detach()[0].tolist(), "bias": net.bias.item()}
        else:
            model = {"kind": kind, "w1": net[0].weight.detach().tolist(), "b1": net[0].bias.detach().tolist(),
                     "w2": net[2].weight.detach()[0].tolist(), "b2": net[2].bias.item()}
        name = f"{kind}_{seed}"
        exports[name] = model
        # Test is not inspected until the dev-only model selection is frozen.
        results[name] = {"dev": evaluate(net, "dev"), "best_epoch": best_epoch, "history": history}
        print(name, json.dumps(results[name]["dev"]), flush=True)
    chosen = min((f"mlp_{i}" for i in range(3)), key=lambda k: results[k]["dev"]["loss"])
    population.write_json(models / "selection.json", {"linear": "linear_0", "mlp": chosen,
                                                      "criterion": "dev cross-entropy only"})
    # Verify portable inference against Torch with raw, unstandardized features.
    sys.path.insert(0, str(out / "bots/mature"))
    import action_value
    for name, model in exports.items():
        population.write_json(models / f"{name}.json", model)
        if model["kind"] == "linear":
            net = torch.nn.Linear(features, 1)
            with torch.no_grad():
                net.weight.copy_(torch.tensor([model["weight"]])); net.bias.fill_(model["bias"])
        else:
            net = torch.nn.Sequential(torch.nn.Linear(features, 16), torch.nn.Tanh(), torch.nn.Linear(16, 1))
            with torch.no_grad():
                net[0].weight.copy_(torch.tensor(model["w1"])); net[0].bias.copy_(torch.tensor(model["b1"]))
                net[2].weight.copy_(torch.tensor([model["w2"]])); net[2].bias.fill_(model["b2"])
        results[name]["test"] = evaluate(net, "test")
        probes = parts["test"]["x"][:128].reshape(-1, features)
        with torch.no_grad():
            predicted = net(probes).squeeze(-1).numpy()
        diff = max(abs(action_value.score(row.tolist(), model) - float(value)) for row, value in zip(probes, predicted))
        assert diff < 1e-4, diff
        results[name]["portable_max_abs_error"] = diff
    population.write_json(models / "metrics.json", results)
    for name, model in (("linear", exports["linear_0"]), ("neural", exports[chosen])):
        make_bot(BASE, out / "bots" / name, "evaluator", model)
    # Explicit heuristic control: same features, action candidates and compute path.
    weights = [0.] * len(action_value.FEATURES)
    for feature, value in {"food_nearness": 4, "soon_food": 1, "space": .5, "exits": .5,
                           "dead_end": -4, "straight": .1, "friendly_near": -1,
                           "enemy_reach": -3, "friendly_reach": -.5, "short_path": 1}.items():
        weights[action_value.FEATURES.index(feature)] = value
    make_bot(BASE, out / "bots/heuristic", "evaluator", {"kind": "linear", "weight": weights, "bias": 0})
    print(json.dumps({k: {s: v[s] for s in ("dev", "test", "best_epoch")} for k, v in results.items()}, indent=2), flush=True)


def screen(out, family, workers):
    plan = json.loads((out / "plan.json").read_text())
    names = list(MODES) if family == "roles" else ["heuristic", "linear", "neural"]
    candidates = [out / "bots" / n for n in ["control_450"] + names]
    hashes = {p.name: bot_hash(p) for p in candidates}
    population.write_json(out / f"{family}-inputs.json", hashes)
    games = guarded.stage(out, family + "-screen", candidates, [out / "bots/reference_v2"],
                          [Path(p) for p in plan["maps"]], plan["screen_seeds"], workers, True)
    scores = {n: population.tally(games, n).score for n in names}
    selected = max(names, key=scores.get)
    selection = {"scores": scores, "selected": selected if scores[selected] > .5 else None,
                 "hash": hashes[selected], "names": names}
    population.write_json(out / f"{family}-selection.json", selection)
    print(json.dumps(selection, indent=2), flush=True)


def validate(out, workers):
    plan = json.loads((out / "plan.json").read_text())
    selected = []
    for family in ("roles", "evaluators"):
        s = json.loads((out / f"{family}-selection.json").read_text())
        if s["selected"]:
            assert bot_hash(out / "bots" / s["selected"]) == s["hash"]
            selected.append(s["selected"])
    if not selected:
        population.write_json(out / "comparison.json", {"selected": [], "performance_gate": False})
        return
    games = guarded.stage(out, "validation", [out / "bots" / n for n in ["control_450"] + selected],
                          [out / "bots" / n for n in ("reference_v2", "splitter", "hunter")],
                          [Path(p) for p in plan["maps"]], plan["validation_seeds"], workers, True)
    results = {}
    for name in selected:
        direct = [g for g in games if name in (g["bot_a"], g["bot_b"]) and
                  "reference_v2" in (g["bot_a"], g["bot_b"])]
        grouped = defaultdict(list)
        for g in direct:
            grouped[g["map"]].append(arena.score_for(g, name))
        ci = arena.block_bootstrap(list(grouped.values()), iters=8000)
        delta = population.paired_delta(games, name, "control_450")
        tally = population.tally(direct, name)
        results[name] = {"direct": {"wins": tally.w, "draws": tally.d, "losses": tally.l,
                                    "score": tally.score, "map_ci95": ci}, "paired_pool": delta,
                         "performance_gate": ci[0] > .5 and delta["map_cluster_ci95"][0] > 0}
    assert bot_hash(BASE) == plan["baseline_hash"]
    assert bot_hash(ROOT / "mybot") == plan["live_hash"]
    population.write_json(out / "comparison.json", results)
    print(json.dumps(results, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--extract", type=Path)
    parser.add_argument("--train", type=Path)
    parser.add_argument("--screen", type=Path)
    parser.add_argument("--family", choices=["roles", "evaluators"])
    parser.add_argument("--validate", type=Path)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    if args.prepare:
        prepare()
    elif args.extract:
        extract(args.extract, args.workers)
    elif args.train:
        train(args.train)
    elif args.screen:
        if not args.family:
            parser.error("--screen requires --family")
        screen(args.screen, args.family, args.workers)
    elif args.validate:
        validate(args.validate, args.workers)
