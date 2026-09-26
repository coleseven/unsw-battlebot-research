import pathlib
import contextlib
import io
import json
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from bcsim import population
from bcsim.match import InProcessBot
from bcsim.paths import ROOT, bot_hash, map_signature, resolve_maps


class PopulationTest(unittest.TestCase):
    def test_variants_keep_movement_and_source_unchanged(self):
        source = ROOT / "versions/v1"
        before = bot_hash(source)
        with tempfile.TemporaryDirectory() as tmp:
            for cap in population.CAPS:
                p = population.make_variant(source, pathlib.Path(tmp) / f"pop_{cap}", cap)
                self.assertEqual((source / "brain.py").read_bytes(), (p / "movement.py").read_bytes())
                for name in ("bc.py", "tactics.py"):
                    self.assertEqual((source / name).read_bytes(), (p / name).read_bytes())
                brain = InProcessBot(p).new_brain("ID 0\nTEAM A\nMAP 16 16\nUNIT_LIMIT 64\n", 1)
                globals_ = brain.turn.__func__.__globals__
                obs = SimpleNamespace(length=8, unit_count=1)
                with patch.object(globals_["tactics"], "danger_cells", return_value=set()), \
                     patch.object(globals_["movement"].Brain, "turn", return_value="MOVE N"):
                    self.assertEqual(brain.turn(obs), "SPLIT 4" if cap else "MOVE N")
                    obs.unit_count = max(cap, 1)
                    self.assertEqual(brain.turn(obs), "MOVE N")
                    obs.unit_count, obs.length = 1, 7
                    self.assertEqual(brain.turn(obs), "MOVE N")
                    obs.length, brain.init.unit_limit = 8, 1
                    self.assertEqual(brain.turn(obs), "MOVE N")
                with patch.object(globals_["tactics"], "danger_cells", return_value={24}), \
                     patch.object(globals_["movement"].Brain, "turn", return_value="MOVE E"):
                    brain.init.unit_limit = 64
                    self.assertEqual(brain.turn(obs), "MOVE E")
        self.assertEqual(bot_hash(source), before)

    def test_map_partition_is_disjoint_and_order_independent(self):
        maps = resolve_maps("all")
        a, b = population.reserve_maps(maps)
        self.assertEqual((a, b), population.reserve_maps(list(reversed(maps))))
        self.assertFalse(set(map(map_signature, a)) & set(map(map_signature, b)))
        self.assertEqual(len(a), 4)

    def test_explicit_open_edges_do_not_change_map_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = (pathlib.Path(tmp) / n for n in ("a.map", "b.map"))
            a.write_text("MAP 16 16\nSYMMETRY xy\nEDGE_COUNT 0\n")
            b.write_text("MAP 16 16\nSYMMETRY xy\nEDGE_COUNT 1\nEDGE 17 0 -1\n")
            self.assertEqual(map_signature(a), map_signature(b))

    def test_extreme_caps_reproduce_reference_matches(self):
        from bcsim.match import play
        with tempfile.TemporaryDirectory() as tmp:
            for cap, reference in ((0, ROOT / "versions/v1"), (64, ROOT / "opponents" / "splitter")):
                candidate = population.make_variant(ROOT / "versions/v1", pathlib.Path(tmp) / f"pop_{cap}", cap)
                for map_name in ("arena", "Colosseum"):
                    m = ROOT / "maps" / f"{map_name}.map"
                    opponent = ROOT / "opponents" / "hunter"
                    actual = play(m, candidate, opponent, seed=42).to_dict()
                    expected = play(m, reference, opponent, seed=42).to_dict()
                    for key in ("bot_a", "hash_a", "seconds"):
                        actual.pop(key)
                        expected.pop(key)
                    self.assertEqual(actual, expected, (cap, map_name))

    def test_jobs_are_side_paired(self):
        jobs = population.jobs_for([pathlib.Path("c")], [pathlib.Path("o")],
                                  [pathlib.Path("m.map")], [1000])
        self.assertEqual(len(jobs), 2)
        self.assertEqual(jobs[0][-1], jobs[1][-1])
        self.assertEqual(jobs[0][1:3], tuple(reversed(jobs[1][1:3])))

    def test_audit_excludes_leaks_and_duplicates_without_reselection(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = pathlib.Path(tmp)
            maps = []
            for name, width in (("screen", 16), ("leak", 16), ("held", 17), ("copy", 17), ("other", 18)):
                m = out / f"{name}.map"
                m.write_text(f"MAP {width} 16\nSYMMETRY xy\n")
                maps.append(m)
            population.write_json(out / "plan.json", {"screen_maps": [str(maps[0])],
                "holdout_maps": list(map(str, maps[1:])), "control": "control"})
            population.write_json(out / "selection.json", {"selected": "candidate"})
            (out / "holdout").mkdir()
            games = [{"bot_a": bot, "bot_b": "opponent", "winner": "A", "map": m.stem,
                      "seed": 1, "deaths": {}, "block": ["opponent", m.stem, 1]}
                     for bot in ("control", "candidate") for m in maps[1:]]
            raw = "\n".join(map(json.dumps, games))
            (out / "holdout" / "games.jsonl").write_text(raw)
            with contextlib.redirect_stdout(io.StringIO()):
                population.audit_saved_run(out)
            audit = json.loads((out / "map-audit" / "comparison.json").read_text())
            self.assertEqual(audit["kept_maps"], ["held", "other"])
            self.assertEqual(audit["excluded_games"], 4)
            self.assertFalse(audit["selection_changed"])
            self.assertEqual((out / "holdout" / "games.jsonl").read_text(), raw)

    def test_paired_delta_and_missing_pair_rejection(self):
        games = []
        for bot in ("candidate", "control"):
            for m in ("m1", "m2"):
                for side in ("A", "B"):
                    games.append({"bot_a": bot if side == "A" else "o",
                                  "bot_b": bot if side == "B" else "o",
                                  "winner": side if bot == "candidate" else None,
                                  "block": ["o", m, 1]})
        delta = population.paired_delta(games, "candidate", "control")
        self.assertEqual(delta["difference"], 0.5)
        self.assertEqual(delta["map_cluster_ci95"], (0.5, 0.5))
        with self.assertRaises(ValueError):
            population.paired_delta(games[:-1], "candidate", "control")
        with self.assertRaises(ValueError):
            population.paired_delta(games + [games[0]], "candidate", "control")


if __name__ == "__main__":
    unittest.main()
