import pathlib
import tempfile
import unittest

from bcsim import v4_phase
from bcsim.match import InProcessBot
from bcsim.paths import bot_hash
from test_movement import board


class V4PhaseTest(unittest.TestCase):
    def make_brain(self, mode, did):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        bot = v4_phase.make_candidate(pathlib.Path(tmp.name) / mode, mode)
        self.assertNotEqual(bot_hash(bot), bot_hash(v4_phase.BASE))
        return InProcessBot(bot).new_brain(
            f"ID {did}\nTEAM A\nMAP 11 11\nUNIT_LIMIT 64\n", 0)

    def test_global_cutoff_boundary(self):
        brain = self.make_brain("global_300", 1)
        obs = board(length=4)
        obs.round = 299
        self.assertEqual(brain.turn(obs), "SPLIT 2")
        obs.round = 300
        self.assertTrue(brain.turn(obs).startswith("MOVE "))

    def test_reserve_is_per_dragon_and_otherwise_v3(self):
        king = self.make_brain("reserve_300", 7)
        worker = self.make_brain("reserve_300", 8)
        obs = board(length=4)
        obs.round = 299
        self.assertEqual(king.turn(obs), "SPLIT 2")
        self.assertEqual(worker.turn(obs), "SPLIT 2")
        obs.round = 300
        self.assertTrue(king.turn(obs).startswith("MOVE "))
        self.assertEqual(worker.turn(obs), "SPLIT 2")
        obs.round = 450
        self.assertTrue(worker.turn(obs).startswith("MOVE "))


if __name__ == "__main__":
    unittest.main()
