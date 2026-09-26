import pathlib
import sys
import tempfile
import unittest

from bcsim import v5_initial
from bcsim.match import InProcessBot
from bcsim.paths import ROOT
from test_movement import board

sys.path.insert(0, str(ROOT / "framework"))
import v5_exploration


class ExplorationTest(unittest.TestCase):
    def test_memory_and_search_bound(self):
        obs = board(length=3)
        obs.round = 0
        init = type("Init", (), {"width": 30, "height": 30})()
        policy = v5_exploration.Policy(init)
        policy.update(obs)
        self.assertEqual(len(policy.memory.visible), 49)
        with tempfile.TemporaryDirectory() as temp:
            bot = v5_initial.variant(pathlib.Path(temp) / "explorer", True,
                                     True, exploration=True)
            brain = InProcessBot(bot).new_brain(
                "ID 0\nTEAM A\nMAP 30 30\nUNIT_LIMIT 64\n", 0)
            model = brain.turn.__func__.__globals__["action_model"].MODEL
            self.assertTrue(policy.choose(obs, "A", model).startswith("MOVE "))
            self.assertLessEqual(policy.expanded, 4 * 48)
            self.assertIsNotNone(brain.explore_policy)


if __name__ == "__main__":
    unittest.main()
