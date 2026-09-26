import pathlib
import tempfile
import unittest

from bcsim import endgame, fission
from bcsim.match import InProcessBot, play
from bcsim.paths import ROOT, bot_hash
from test_movement import board


class FissionTest(unittest.TestCase):
    def test_split_size_legality_cutoff_and_movement_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            control = endgame.make_variant(ROOT / "versions/v1", root / "control", 450)
            original_hash = bot_hash(control)
            for name, config in fission.MODES.items():
                bot = fission.make_variant(control, root / name, *config)
                self.assertEqual((bot / "movement.py").read_bytes(), (control / "movement.py").read_bytes())
                brain = InProcessBot(bot).new_brain("ID 0\nTEAM A\nMAP 11 11\nUNIT_LIMIT 64\n", 123)
                for length in range(2, 17):
                    o = board(length=length)
                    o.round = 449
                    action = brain.turn(o)
                    if length >= config[0]:
                        self.assertTrue(action.startswith("SPLIT "))
                        child = int(action.split()[1])
                        self.assertGreaterEqual(child, 2)
                        self.assertGreaterEqual(length - child, 2)
                    else:
                        self.assertTrue(action.startswith("MOVE "))
                    o.round = 450
                    self.assertTrue(brain.turn(o).startswith("MOVE "))
                    o.round, o.unit_count = 100, 64
                    self.assertTrue(brain.turn(o).startswith("MOVE "))
            self.assertEqual(bot_hash(control), original_hash)

    def test_threshold_eight_is_behaviorally_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            control = endgame.make_variant(ROOT / "versions/v1", root / "control", 450)
            equivalent = fission.make_variant(control, root / "equivalent", 8)
            a = play(ROOT / "maps/arena.map", control, ROOT / "opponents/splitter", 42).to_dict()
            b = play(ROOT / "maps/arena.map", equivalent, ROOT / "opponents/splitter", 42).to_dict()
            for key in ("winner", "rounds", "a_length", "b_length", "a_longest", "b_longest", "deaths", "error"):
                self.assertEqual(a[key], b[key], key)

    def test_replay_action_audit(self):
        from bcsim import fission_audit
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            control = endgame.make_variant(ROOT / "versions/v1", root / "control", 450)
            bot = fission.make_variant(control, root / "split4", 4)
            rp = root / "game.replay"
            mapfile = ROOT / "maps/arena.map"
            game = play(mapfile, bot, ROOT / "opponents/greedy", 123, replay_to=rp).to_dict()
            game["replay"] = str(rp)
            counts, samples = fission_audit.one_game((game, str(bot), str(mapfile)))
            self.assertGreater(counts["verified_candidate_turns"], 0)
            self.assertGreater(counts["splits"], 0)
            self.assertEqual(counts["late_splits"], 0)
            self.assertIn("dense", samples)

    def test_audit_checkpoint_resume_and_input_change_detection(self):
        from bcsim import audit_jobs, fission_audit
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            control = endgame.make_variant(ROOT / "versions/v1", root / "control", 450)
            bot = fission.make_variant(control, root / "split4", 4)
            rp = root / "game.replay"
            mapfile = ROOT / "maps/arena.map"
            game = play(mapfile, bot, ROOT / "opponents/greedy", 123, replay_to=rp).to_dict()
            game["replay"] = str(rp)
            tasks = [(game, str(bot), str(mapfile))]
            first = audit_jobs.run(tasks, 1, root, fission_audit.one_game, "test audit")
            saved = (root / "audit-progress.jsonl").read_bytes()
            second = audit_jobs.run(tasks, 1, root, fission_audit.one_game, "test audit")
            self.assertEqual(first, second)
            self.assertEqual(saved, (root / "audit-progress.jsonl").read_bytes())
            game["seed"] += 1
            with self.assertRaises(ValueError):
                audit_jobs.run(tasks, 1, root, fission_audit.one_game, "test audit")


if __name__ == "__main__":
    unittest.main()
