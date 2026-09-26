import pathlib
import tempfile
import unittest

from bcsim import v5_initial
from bcsim.match import InProcessBot
from test_movement import board


class HeadGuardTest(unittest.TestCase):
    def test_avoid_friendly_head_reach_when_alternative_exists(self):
        with tempfile.TemporaryDirectory() as temp:
            bot = v5_initial.variant(pathlib.Path(temp) / "guard", True, True,
                                     head_guard=True)
            brain = InProcessBot(bot).new_brain(
                "ID 0\nTEAM A\nMAP 30 30\nUNIT_LIMIT 64\n", 0)
            module = brain.turn.__func__.__globals__["v5_head_guard"]
            model = brain.turn.__func__.__globals__["action_model"].MODEL
            obs = board(length=3)
            obs.occ[26] = ("A", 2, True, "W")
            self.assertNotEqual(module.choose(obs, "A", 0, model, "MOVE E"),
                                "MOVE E")
            self.assertEqual(module.choose(obs, "A", 0, model, "MOVE N"),
                             "MOVE N")


if __name__ == "__main__":
    unittest.main()
