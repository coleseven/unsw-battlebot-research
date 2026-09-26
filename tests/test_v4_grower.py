import pathlib
import tempfile
import unittest

from bcsim import v4_grower
from bcsim.match import InProcessBot
from bcsim.paths import bot_hash
from test_movement import board


class V4GrowerTest(unittest.TestCase):
    def make_brain(self, mode):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        bot = v4_grower.make_candidate(pathlib.Path(tmp.name) / mode, mode)
        self.assertNotEqual(bot_hash(bot), bot_hash(v4_grower.BASE))
        return InProcessBot(bot).new_brain("ID 10\nTEAM A\nMAP 11 11\nUNIT_LIMIT 64\n", 0)

    def test_mature_preserves_only_after_threshold(self):
        brain = self.make_brain("mature")
        obs = board(length=8)
        obs.round, obs.unit_count = 199, 16
        self.assertEqual(brain.turn(obs), "SPLIT 4")
        obs.round = 200
        self.assertTrue(brain.turn(obs).startswith("MOVE "))
        obs.length, obs.unit_count = 5, 9
        self.assertTrue(brain.turn(obs).startswith("MOVE "))
        obs.unit_count = 7
        self.assertEqual(brain.turn(obs), "SPLIT 2")

    def test_opportunity_uses_local_food_and_v3_split_cutoff(self):
        brain = self.make_brain("opportunity")
        obs = board(length=4)
        obs.round, obs.unit_count = 250, 16
        self.assertEqual(brain.turn(obs), "SPLIT 2")
        for k in (3, 4, 5):
            obs.pearl[k] = True
        self.assertTrue(brain.turn(obs).startswith("MOVE "))
        obs.round, obs.unit_count = 450, 7
        self.assertTrue(brain.turn(obs).startswith("MOVE "))


if __name__ == "__main__":
    unittest.main()
