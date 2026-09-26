"""Versioned replay datasets, grouped partitions, and streaming batches.

V2 goes to data/dataset_v2; the legacy corpus remains untouched.
See DATASET_V2.md for fields, training examples, and migration instructions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from .paths import DATA, FRAMEWORK

SCHEMA_VERSION = 2
OUT = DATA / "dataset_v2"
REPLAYS = DATA / "replays"
RAGGED = {"action_tokens": ("action_values", "action_offsets", -1),
          "sonar": ("sonar_values", "sonar_offsets", 0)}
FIXED_COLUMNS = (
    "grid", "scalar", "dragon_ids", "turn_order", "portal_ids", "coordinates",
    "pearl_countdown", "map_size", "unit_limit", "kind", "dir", "steps", "split",
    "round", "dragon", "team", "won", "elo", "points", "policy_eligible",
    "game", "battle", "submission", "budget_exceeded", "timed_out",
)


class DatasetError(ValueError):
    pass


def _json(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _digest(value) -> str:
    return hashlib.sha256(_json(value).encode()).hexdigest()


def pipeline_hash() -> str:
    """Invalidate caches when observation, replay, or feature logic changes."""
    h = hashlib.sha256()
    for p in (pathlib.Path(__file__), FRAMEWORK / "features.py", FRAMEWORK / "bc.py",
              pathlib.Path(__file__).with_name("replay.py"),
              pathlib.Path(__file__).with_name("reconstruct.py")):
        h.update(p.name.encode())
        h.update(p.read_bytes())
    return h.hexdigest()


def _index(path=None) -> dict[int, dict]:
    path = pathlib.Path(path) if path is not None else DATA / "index.jsonl"
    out = {}
    if not path.is_file():
        return out
    lines = path.read_text(encoding="utf8").splitlines()
    for n, line in enumerate(lines):
        if not line.strip():
            continue
        try:
            b = json.loads(line)
        except json.JSONDecodeError:
            if n == len(lines) - 1:
                print("warning: ignoring incomplete final index record", file=sys.stderr)
                break
            raise
        for g in b["games"]:
            out[int(g["game"])] = {
                "battle": b["battle"], "at": b.get("at"), "winner": g.get("winner"),
                "elo_a": b["a"]["elo"], "elo_b": b["b"]["elo"],
                "team_a": b["a"]["id"], "team_b": b["b"]["id"],
                "submission_a": b.get("submission_a"), "submission_b": b.get("submission_b"),
            }
    return out


def read_metadata(path) -> dict:
    with np.load(path, allow_pickle=False) as z:
        if "_meta" not in z.files:
            raise DatasetError(f"{path}: legacy/unversioned shard; rebuild from the raw replay into dataset_v2")
        meta = json.loads(str(z["_meta"].item()))
    if meta.get("schema") != SCHEMA_VERSION:
        raise DatasetError(f"{path}: unsupported schema {meta.get('schema')}")
    return meta


def _atomic_npz(path, arrays) -> None:
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=path.stem + "-", suffix=".tmp.npz", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            np.savez_compressed(f, **arrays)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def _pack_sequences(sequences, dtype):
    offsets = np.zeros(len(sequences) + 1, dtype=np.int64)
    offsets[1:] = np.cumsum([len(s) for s in sequences], dtype=np.int64)
    values = np.concatenate(sequences).astype(dtype, copy=False) if sequences else np.empty(0, dtype=dtype)
    return values, offsets


def build_game(game: int, meta: dict, *, replay_dir=REPLAYS, output_dir=OUT,
               winners_only=False, min_elo=0, rebuild=False, fingerprint=None) -> int:
    """Build one game atomically. -1 = matching cache; >=0 = written rows.

    A stale cache is an error unless rebuild=True. No corpus-wide deletion.
    """
    if str(FRAMEWORK) not in sys.path:
        sys.path.insert(0, str(FRAMEWORK))
    import bc
    import features
    from . import replay as rp
    from .reconstruct import Board, turns

    source = pathlib.Path(replay_dir) / f"{game}.replay"
    blob = source.read_bytes()
    expected = {
        "schema": SCHEMA_VERSION, "feature_version": features.FEATURE_VERSION,
        "pipeline": fingerprint or pipeline_hash(), "game": int(game),
        "replay_sha256": hashlib.sha256(blob).hexdigest(), "source": meta,
        "filters": {"winners_only": bool(winners_only), "min_elo": int(min_elo)},
    }
    path = pathlib.Path(output_dir) / f"{game}.npz"
    if path.is_file() and not rebuild:
        cached = read_metadata(path)
        if all(cached.get(k) == v for k, v in expected.items()):
            return -1
        raise DatasetError(f"{path}: stale source, pipeline, or filters; use --rebuild or another --output")
    rep = rp.decode(blob)
    board = Board(rep.map_text)
    winner = meta.get("winner")
    if winner is None:
        winner = rep.result.get("winner")
    winner = str(winner).upper() if winner is not None else None
    if winner == "DRAW":
        winner = None
    if winner not in (None, "A", "B"):
        raise DatasetError(f"game {game}: unknown winner {winner!r}")
    if not rep.result or not rep.result.get("terminated"):
        raise DatasetError(f"game {game}: incomplete replay; outcome cannot be used as a training target")
    if rep.result.get("winner") != winner:
        raise DatasetError(f"game {game}: index and replay winners disagree")

    failures, event_round = {}, 0
    for event in rep.events:
        if event[0] == rp.ROUND_START:
            event_round = event[1]
        elif event[0] == rp.DRAGON_ACTION:
            failures[event_round, event[1]] = (event[4], event[5])

    cols = {k: [] for k in FIXED_COLUMNS}
    actions, messages = [], []
    for t in turns(rep, str(game)):
        won = 0.5 if winner is None else float(winner == t.team)
        elo = int(meta.get("elo_a" if t.team == "A" else "elo_b", 0))
        if (winners_only and won != 1) or elo < min_elo:
            continue
        obs = bc.Obs(t.block)
        encoded = features.encode_observation(obs, t.team, t.id, (board.w, board.h))
        messages.append(encoded.pop("sonar"))
        kind, direction, steps, split = features.action_label(t.action)
        actions.append(features.action_tokens(t.action))
        exceeded, timed_out = failures.get((t.round, t.id), (False, False))
        encoded.update(kind=kind, dir=direction, steps=steps, split=split,
                       round=t.round, dragon=t.id, team=int(t.team == "B"),
                       won=won, elo=elo, points=-1 if t.points is None else t.points,
                       game=game, battle=meta.get("battle", -1),
                       submission=meta.get("submission_a" if t.team == "A" else "submission_b") or -1,
                       budget_exceeded=exceeded, timed_out=timed_out,
                       policy_eligible=kind in (0, 1) and (kind != 0 or steps > 0)
                                       and not exceeded and not timed_out)
        for k in FIXED_COLUMNS:
            cols[k].append(encoded[k])
    shapes = {"grid": (17, 7, 7), "scalar": (5,), "dragon_ids": (7, 7),
              "turn_order": (7, 7), "portal_ids": (4, 7, 7), "coordinates": (2, 7, 7),
              "pearl_countdown": (7, 7), "map_size": (2,)}
    types = {"grid": np.uint8, "turn_order": np.uint8, "scalar": np.float32,
             "won": np.float32, "points": np.int64, "policy_eligible": np.bool_,
             "game": np.int64, "battle": np.int64, "submission": np.int64,
             "budget_exceeded": np.bool_, "timed_out": np.bool_}
    arrays = {k: np.asarray(v, dtype=types.get(k, np.int32)).reshape((len(actions),) + shapes.get(k, ()))
              for k, v in cols.items()}
    arrays["action_values"], arrays["action_offsets"] = _pack_sequences(actions, np.int8)
    arrays["sonar_values"], arrays["sonar_offsets"] = _pack_sequences(messages, np.uint32)
    map_text = "\n".join(line.strip() for line in rep.map_text.splitlines()
                         if line.strip() and not line.strip().startswith("MAP_NAME"))
    expected.update(map_sha256=hashlib.sha256(map_text.encode()).hexdigest(), rows=len(actions))
    arrays["_meta"] = np.asarray(_json(expected))
    _atomic_npz(path, arrays)
    return len(actions)


def shards(pattern="*.npz", *, dataset_dir=OUT) -> list[pathlib.Path]:
    return sorted(p for p in pathlib.Path(dataset_dir).glob(pattern)
                  if not p.name.endswith(".tmp.npz"))


def _compatible(metas):
    signatures = {_json({k: m.get(k) for k in ("schema", "feature_version", "pipeline", "filters")})
                  for m in metas}
    if len(signatures) > 1:
        raise DatasetError("mixed pipelines/filter settings; use a single consistent dataset")


def make_partitions(*, dataset_dir=OUT, group_by="battle", seed=0,
                    fractions=(0.8, 0.1, 0.1)) -> dict:
    """Freeze assignments by battle, map, or connected submission components.

    Submission grouping joins games sharing EITHER submission, transitively.
    A highly connected league may be impossible to split this way.
    """
    if group_by not in ("battle", "map", "submission"):
        raise ValueError("group_by must be battle, map, or submission")
    if len(fractions) != 3 or any(x < 0 for x in fractions) or not np.isclose(sum(fractions), 1):
        raise ValueError("fractions must be three nonnegative values summing to 1")
    paths = shards(dataset_dir=dataset_dir)
    metas = [read_metadata(p) for p in paths]
    _compatible(metas)
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    if group_by == "submission":
        for m in metas:
            a, b = (m["source"].get("submission_" + s) for s in "ab")
            if a is None or b is None:
                raise DatasetError("submission grouping requires both submission IDs for every game")
            ra, rb = find(str(a)), find(str(b))
            parent[max(ra, rb)] = min(ra, rb)
    entries = []
    counts = {s: 0 for s in ("train", "validation", "test")}
    for p, m in zip(paths, metas):
        if group_by == "battle":
            group = m["source"].get("battle")
            if group is None:
                raise DatasetError("battle grouping requires battle IDs; refresh the source index")
        elif group_by == "map":
            group = m["map_sha256"]
        else:
            group = find(str(m["source"]["submission_a"]))
        u = int(_digest([seed, group_by, str(group)])[:16], 16) / 2**64
        split = "train" if u < fractions[0] else "validation" if u < sum(fractions[:2]) else "test"
        counts[split] += m["rows"]
        entries.append({"file": p.name, "group": str(group), "split": split,
                        "metadata_sha256": _digest(m), "rows": m["rows"]})
    for split, fraction in zip(counts, fractions):
        if fraction and not counts[split]:
            raise DatasetError(f"{split} is empty: need more independent groups, another seed, or another grouping; "
                               "submission-connected games must not cross partitions")
    return {"version": 1, "schema": SCHEMA_VERSION, "group_by": group_by,
            "seed": seed, "fractions": list(fractions), "rows": counts, "shards": entries}


def save_partitions(path, manifest) -> None:
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")


def _selection(dataset_dir, pattern, partition_manifest, split):
    if partition_manifest is None:
        if split is not None:
            raise ValueError("split requires partition_manifest")
        return [(p, None) for p in shards(pattern, dataset_dir=dataset_dir)]
    if split not in ("train", "validation", "test"):
        raise ValueError("choose train, validation, or test with a partition manifest")
    manifest = json.loads(pathlib.Path(partition_manifest).read_text(encoding="utf8"))
    if manifest.get("version") != 1 or manifest.get("schema") != SCHEMA_VERSION:
        raise DatasetError("unsupported partition manifest")
    result = []
    for e in manifest["shards"]:
        if pathlib.Path(e["file"]).name != e["file"]:
            raise DatasetError("partition entries must be shard filenames")
        if e["split"] == split:
            result.append((pathlib.Path(dataset_dir) / e["file"], e["metadata_sha256"]))
    return result


def iter_batches(batch_size=1024, *, dataset_dir=OUT, pattern="*.npz", columns=None,
                 fraction=1.0, seed=0, shuffle=True, where=None, category_keep=None,
                 partition_manifest=None, split=None):
    """Keep one game's selected arrays, plus one padded batch, in memory.

    Shard tails yield smaller batches. category_keep thins step/sprint/split/other
    without replacement. Sequence outputs have explicit boolean *_mask fields.
    where receives selected fixed columns; include fields needed by the predicate.
    """
    if batch_size <= 0 or not 0 <= fraction <= 1:
        raise ValueError("batch_size must be positive and fraction in [0,1]")
    rates = dict(category_keep or {})
    if set(rates) - {"step", "sprint", "split", "other"} or any(not 0 <= p <= 1 for p in rates.values()):
        raise ValueError("category_keep uses step/sprint/split/other probabilities in [0,1]")
    columns = tuple(columns) if columns is not None else FIXED_COLUMNS + tuple(RAGGED)
    if not columns or set(columns) - set(FIXED_COLUMNS) - set(RAGGED):
        raise ValueError("unknown or empty columns")
    selected = _selection(dataset_dir, pattern, partition_manifest, split)
    metas = []
    for path, expected in selected:
        m = read_metadata(path)
        if expected is not None and _digest(m) != expected:
            raise DatasetError(f"{path}: changed since partition creation; create a new manifest")
        metas.append(m)
    _compatible(metas)
    rng = np.random.default_rng(seed)
    if shuffle:
        rng.shuffle(selected)
    for path, _ in selected:
        with np.load(path, allow_pickle=False) as z:
            fixed = {k: z[k] for k in set(columns) & set(FIXED_COLUMNS)}
            kind, steps = z["kind"], z["steps"]
            n = len(kind)
            keep = np.ones(n, dtype=bool) if where is None else np.asarray(where(fixed), dtype=bool).copy()
            if keep.shape != (n,):
                raise ValueError("where must return one boolean per row")
            probabilities = np.full(n, fraction, dtype=np.float64)
            for category, prob in rates.items():
                mask = ((kind == 0) & (steps == 1)) if category == "step" else \
                       ((kind == 0) & (steps > 1)) if category == "sprint" else \
                       (kind == 1) if category == "split" else \
                       ((kind >= 2) | ((kind == 0) & (steps == 0)))
                probabilities[mask] *= prob
            keep &= rng.random(n) < probabilities
            indices = np.flatnonzero(keep)
            if shuffle:
                rng.shuffle(indices)
            sequences = {k: (z[RAGGED[k][0]], z[RAGGED[k][1]]) for k in columns if k in RAGGED}
            for k, (values, offsets) in sequences.items():
                if (len(offsets) != n + 1 or offsets[0] != 0 or offsets[-1] != len(values)
                        or np.any(np.diff(offsets) < 0)):
                    raise DatasetError(f"{path}: invalid {k} offsets")
            for start in range(0, len(indices), batch_size):
                ids = indices[start:start + batch_size]
                batch = {k: v[ids] for k, v in fixed.items()}
                for k, (values, offsets) in sequences.items():
                    lengths = offsets[ids + 1] - offsets[ids]
                    width = int(lengths.max(initial=0))
                    padded = np.full((len(ids), width), RAGGED[k][2], dtype=values.dtype)
                    mask = np.zeros(padded.shape, dtype=bool)
                    for row, idx in enumerate(ids):
                        length = int(lengths[row])
                        padded[row, :length] = values[offsets[idx]:offsets[idx + 1]]
                        mask[row, :length] = True
                    batch[k] = padded
                    batch[k + "_mask"] = mask
                yield batch


def load_all(pattern="*.npz", fraction=1.0, seed=0, where=None, *, dataset_dir=OUT,
             columns=None, max_bytes=512 * 1024**2):
    """Small fixed-column samples only; prefer iter_batches for training.

    Limit includes final concatenation, but not the currently decompressed shard.
    """
    columns = tuple(columns) if columns is not None else FIXED_COLUMNS
    if set(columns) & set(RAGGED):
        raise ValueError("use iter_batches for padded sequence columns")
    parts = {k: [] for k in columns}
    size = 0
    for batch in iter_batches(dataset_dir=dataset_dir, pattern=pattern, columns=columns,
                              fraction=fraction, seed=seed, shuffle=False, where=where):
        size += sum(v.nbytes for v in batch.values())
        if 2 * size > max_bytes:
            raise MemoryError("load_all exceeds memory allowance; use iter_batches or a smaller fraction")
        for k in columns:
            parts[k].append(batch[k])
    return {k: np.concatenate(v) for k, v in parts.items() if v}


def _job(args):
    game, meta, options = args
    return game, build_game(game, meta, **options)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=pathlib.Path, default=OUT)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--winners-only", action="store_true")
    ap.add_argument("--min-elo", type=int, default=0)
    ap.add_argument("--rebuild", action="store_true", help="atomically replace selected shards; never delete the corpus")
    ap.add_argument("--games", help="comma-separated game IDs")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--partition", type=pathlib.Path, help="write a new frozen partition manifest instead of building")
    ap.add_argument("--group-by", choices=["battle", "map", "submission"], default="battle")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    if args.partition:
        manifest = make_partitions(dataset_dir=args.output, group_by=args.group_by, seed=args.seed)
        save_partitions(args.partition, manifest)
        print(_json(manifest["rows"]))
        return
    if args.workers < 1 or (args.limit is not None and args.limit < 1):
        ap.error("workers and limit must be positive")
    if args.output.resolve() == (DATA / "dataset").resolve():
        ap.error("use a separate V2 directory; data/dataset is the legacy corpus")
    games = sorted(int(p.stem) for p in REPLAYS.glob("*.replay"))
    if args.games:
        games = [int(g) for g in args.games.split(",")]
    if args.limit:
        games = games[:args.limit]
    index = _index()
    options = dict(output_dir=args.output, winners_only=args.winners_only, min_elo=args.min_elo,
                   rebuild=args.rebuild, fingerprint=pipeline_hash())
    jobs = [(g, index.get(g, {}), options) for g in games]
    total = 0

    def report(results):
        nonlocal total
        for done, (game, n) in enumerate(results, 1):
            total += max(0, n)
            print(f"{done}/{len(games)} game={game} rows={'cached' if n < 0 else n} new_total={total}", flush=True)

    if args.workers == 1:
        report(map(_job, jobs))
    else:
        with ProcessPoolExecutor(args.workers) as pool:
            report(pool.map(_job, jobs, chunksize=1))


if __name__ == "__main__":
    main()
