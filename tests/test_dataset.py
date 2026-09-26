"""Dataset contract tests; synthetic files are confined to temporary directories."""
import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "framework"))
import bc
import features
from bcsim import dataset_v2 as ds
from bcsim import replay as rp


def observation():
    lines = ["ROUND 12", "DIR N", "LENGTH 4", "UNIT_COUNT 2", "NUM_MSGS 3",
             "0", "4294967295", "42"]
    lines += [f"{k % 7} {k // 7} {int(k == 1)} {300 if k == 2 else -1}" for k in range(49)]
    lines += ["DRAGON_BODIES 4", "A 10 3 3 N 1", "B 9 2 3 E 1",
              "B 50000 4 3 W 1", "A 10 3 4 N 0"]
    h = [["."] * 7 for _ in range(8)]
    h[2][2] = "7"
    h[4][4] = "11"
    lines += [" ".join(row) for row in h]
    lines += [" ".join(["."] * 8) for _ in range(7)]
    return bc.Obs("\n".join(lines) + "\n")


def synthetic_replay():
    actions = [("move", "NNE"), ("move", "NEN"), ("split", 2),
               ("move", "N"), ("suicide",), None]
    events = []
    for r, action in enumerate(actions):
        events.extend([(rp.ROUND_START, r), (rp.TURN_START, 0),
                       (rp.DRAGON_ACTION, 0, action, None, r == 3, False)])
    return rp.Replay(1, "MAP 10 10\nDRAGON 0 3 5 5 4 5 3 5\nDRAGON 1 3 8 8 7 8 6 8\n",
                     "a", "b", events, {"terminated": True, "winner": "A"})


class FeaturesTest(unittest.TestCase):
    def test_complete_action_roundtrip(self):
        actions = [("move", "NNE"), ("move", "NEN"), ("move", "NNN"),
                   ("move", "NESW" * 100), ("move", ""), ("split", 40000),
                   ("suicide",), None]
        tokens = [features.action_tokens(a) for a in actions]
        self.assertEqual(len({tuple(t) for t in tokens[:3]}), 3)
        for action, t in zip(actions, tokens):
            kind, _, _, split = features.action_label(action)
            self.assertEqual(features.decode_action(kind, t, split), action)
        with self.assertRaises(ValueError):
            features.decode_action(0, [-1])

    def test_inputs_preserve_information_without_changing_legacy_grid(self):
        obs = observation()
        out = features.encode_observation(obs, "A", 10, (10, 11))
        grid, scalar = features.encode(obs, "A", 10)
        np.testing.assert_array_equal(grid, out["grid"])
        np.testing.assert_array_equal(scalar, out["scalar"])
        self.assertEqual(out["dragon_ids"][3, 4], 50000)
        np.testing.assert_array_equal(out["turn_order"][3, 2:5], [1, 2, 3])
        np.testing.assert_array_equal(out["sonar"], [0, 2**32 - 1, 42])
        self.assertEqual(out["sonar"].dtype, np.uint32)
        self.assertEqual(out["portal_ids"][0, 2, 2], 7)
        self.assertEqual(out["portal_ids"][0, 4, 4], 11)
        self.assertEqual(out["pearl_countdown"][0, 2], 300)
        np.testing.assert_array_equal(out["map_size"], [10, 11])


class DatasetTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="bc-dataset-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.raw = self.root / "raw"
        self.out = self.root / "out"
        self.raw.mkdir()
        (self.raw / "1.replay").write_bytes(b"synthetic")
        self.meta = {"battle": 20, "winner": "a", "elo_a": 1900, "elo_b": 1800,
                     "submission_a": 100, "submission_b": 200}

    def build(self, **kwargs):
        with patch.object(rp, "decode", return_value=synthetic_replay()):
            return ds.build_game(1, self.meta, replay_dir=self.raw, output_dir=self.out, **kwargs)

    def test_build_cache_invalidation_and_non_destructive_rebuild(self):
        self.assertEqual(self.build(), 6)
        self.assertEqual(self.build(), -1)
        with self.assertRaisesRegex(ds.DatasetError, "stale"):
            self.build(min_elo=2000)
        self.assertEqual(self.build(min_elo=2000, rebuild=True), 0)
        with np.load(self.out / "1.npz") as z:
            self.assertEqual(z["grid"].shape, (0, 17, 7, 7))
            self.assertEqual(z["action_offsets"].tolist(), [0])
        self.assertEqual(self.build(min_elo=2000), -1)
        self.assertTrue((self.raw / "1.replay").exists())
        self.assertEqual(self.build(rebuild=True), 6)
        self.meta["submission_a"] = 999
        with self.assertRaisesRegex(ds.DatasetError, "stale"):
            self.build()

    def test_pipeline_and_raw_content_invalidate_cache(self):
        self.build(fingerprint="old")
        with self.assertRaisesRegex(ds.DatasetError, "stale"):
            self.build(fingerprint="new")
        self.build(fingerprint="new", rebuild=True)
        (self.raw / "1.replay").write_bytes(b"changed")
        with self.assertRaisesRegex(ds.DatasetError, "stale"):
            self.build(fingerprint="new")

    def test_stream_padding_and_action_roundtrip(self):
        self.build()
        batches = list(ds.iter_batches(2, dataset_dir=self.out, shuffle=False))
        self.assertEqual([len(b["kind"]) for b in batches], [2, 2, 2])
        actions = []
        for b in batches:
            self.assertEqual(b["sonar"].shape, (len(b["kind"]), 0))
            for i in range(len(b["kind"])):
                actions.append(features.decode_action(int(b["kind"][i]),
                    b["action_tokens"][i][b["action_tokens_mask"][i]], int(b["split"][i])))
        self.assertEqual(actions[:2], [("move", "NNE"), ("move", "NEN")])
        self.assertEqual(actions[-2:], [("suicide",), None])
        self.assertFalse(batches[1]["policy_eligible"][1])  # budget failure

    def test_sonar_zero_and_maximum_are_not_padding(self):
        self.build()
        path = self.out / "1.npz"
        with np.load(path) as z:
            arrays = dict(z)
        arrays["sonar_values"] = np.asarray([0, 2**32 - 1, 42], dtype=np.uint32)
        arrays["sonar_offsets"] = np.asarray([0, 2, 3, 3, 3, 3, 3], dtype=np.int64)
        ds._atomic_npz(path, arrays)
        b = next(ds.iter_batches(2, dataset_dir=self.out, columns=["sonar"], shuffle=False))
        np.testing.assert_array_equal(b["sonar"], [[0, 2**32 - 1], [42, 0]])
        np.testing.assert_array_equal(b["sonar_mask"], [[True, True], [True, False]])

    def test_sampling_and_memory_guard(self):
        self.build()
        a = list(ds.iter_batches(dataset_dir=self.out, seed=19, columns=["round"], fraction=.5))
        b = list(ds.iter_batches(dataset_dir=self.out, seed=19, columns=["round"], fraction=.5))
        np.testing.assert_array_equal(a[0]["round"], b[0]["round"])
        rare = list(ds.iter_batches(dataset_dir=self.out, shuffle=False, columns=["steps", "kind"],
                                    category_keep={"step": 0, "other": 0}))
        np.testing.assert_array_equal(rare[0]["kind"], [0, 0, 1])
        with self.assertRaises(MemoryError):
            ds.load_all(dataset_dir=self.out, max_bytes=1)
        self.assertEqual(len(ds.load_all(dataset_dir=self.out, columns=["kind"])["kind"]), 6)

    def test_legacy_and_mixed_caches_rejected_before_yield(self):
        self.out.mkdir()
        ds._atomic_npz(self.out / "legacy.npz", {"kind": np.array([0])})
        with self.assertRaisesRegex(ds.DatasetError, "legacy"):
            next(ds.iter_batches(dataset_dir=self.out))
        (self.out / "legacy.npz").unlink()
        self.build()
        with np.load(self.out / "1.npz") as z:
            arrays = dict(z)
        m = json.loads(str(arrays["_meta"].item()))
        m["pipeline"] = "different"
        arrays["_meta"] = np.asarray(json.dumps(m))
        ds._atomic_npz(self.out / "2.npz", arrays)
        with self.assertRaisesRegex(ds.DatasetError, "mixed"):
            next(ds.iter_batches(dataset_dir=self.out))

    def test_incomplete_replay_is_not_a_draw(self):
        rep = synthetic_replay()
        rep.result["terminated"] = False
        with patch.object(rp, "decode", return_value=rep), self.assertRaisesRegex(ds.DatasetError, "incomplete"):
            ds.build_game(1, self.meta, replay_dir=self.raw, output_dir=self.out)

    def test_draw_and_index_disagreement(self):
        rep = synthetic_replay()
        rep.result["winner"] = None
        with patch.object(rp, "decode", return_value=rep):
            ds.build_game(1, {**self.meta, "winner": "draw"}, replay_dir=self.raw, output_dir=self.out)
        with np.load(self.out / "1.npz") as z:
            self.assertTrue(np.all(z["won"] == .5))
        rep.result["winner"] = "B"
        with patch.object(rp, "decode", return_value=rep), self.assertRaisesRegex(ds.DatasetError, "disagree"):
            ds.build_game(1, self.meta, replay_dir=self.raw, output_dir=self.out, rebuild=True)

    def populate_partition_corpus(self):
        self.build()
        with np.load(self.out / "1.npz") as z:
            base = dict(z)
        for i in range(1, 101):
            m = json.loads(str(base["_meta"].item()))
            group = (i - 1) // 2
            m.update(game=i, map_sha256=f"map-{group}")
            m["source"].update(battle=group, submission_a=group * 3, submission_b=group * 3 + 1)
            arrays = {**base, "_meta": np.asarray(json.dumps(m))}
            ds._atomic_npz(self.out / f"{i}.npz", arrays)

    def test_grouped_partitions_stable_and_frozen(self):
        self.populate_partition_corpus()
        for mode in ("battle", "map", "submission"):
            manifest = ds.make_partitions(dataset_dir=self.out, group_by=mode)
            groups = {}
            for entry in manifest["shards"]:
                groups.setdefault(entry["group"], set()).add(entry["split"])
            self.assertTrue(all(len(s) == 1 for s in groups.values()))
            self.assertEqual(manifest, ds.make_partitions(dataset_dir=self.out, group_by=mode))
        path = self.root / "partitions.json"
        ds.save_partitions(path, manifest)
        with self.assertRaises(FileExistsError):
            ds.save_partitions(path, manifest)
        count = sum(len(b["kind"]) for b in ds.iter_batches(dataset_dir=self.out, columns=["kind"],
                    partition_manifest=path, split="test"))
        self.assertEqual(count, manifest["rows"]["test"])
        entry = next(e for e in manifest["shards"] if e["split"] == "test")
        shard = self.out / entry["file"]
        with np.load(shard) as z:
            arrays = dict(z)
        m = json.loads(str(arrays["_meta"].item()))
        m["replay_sha256"] = "changed"
        arrays["_meta"] = np.asarray(json.dumps(m))
        ds._atomic_npz(shard, arrays)
        with self.assertRaisesRegex(ds.DatasetError, "changed"):
            next(ds.iter_batches(dataset_dir=self.out, partition_manifest=path, split="test"))

    def test_submission_components_cannot_leak_transitively(self):
        self.build()
        with np.load(self.out / "1.npz") as z:
            base = dict(z)
        for i, pair in enumerate(((1, 2), (2, 3), (3, 4)), 1):
            m = json.loads(str(base["_meta"].item()))
            m["source"].update(submission_a=pair[0], submission_b=pair[1])
            ds._atomic_npz(self.out / f"{i}.npz", {**base, "_meta": np.asarray(json.dumps(m))})
        with self.assertRaisesRegex(ds.DatasetError, "empty"):
            ds.make_partitions(dataset_dir=self.out, group_by="submission")


if __name__ == "__main__":
    unittest.main()
