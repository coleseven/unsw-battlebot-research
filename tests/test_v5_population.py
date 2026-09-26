import pathlib
import tempfile
import unittest

from bcsim import v5_initial
from bcsim.match import InProcessBot
from test_movement import board


class PopulationTest(unittest.TestCase):
    def test_big_board_cap_cutoff_and_floor(self):
        with tempfile.TemporaryDirectory() as temp:
            bot = v5_initial.variant(pathlib.Path(temp) / "population", True,
                                     True, population_control=True)
            brain = InProcessBot(bot).new_brain(
                "ID 0\nTEAM A\nMAP 64 64\nUNIT_LIMIT 64\n", 0)
            module = brain.turn.__func__.__globals__["v5_population"]
            model = brain.turn.__func__.__globals__["action_model"].MODEL
            obs = board(length=4)
            obs.round, obs.unit_count = 100, 48
            self.assertTrue(module.choose(brain.init, obs, "A", model,
                                          "SPLIT 2").startswith("MOVE "))
            obs.round, obs.unit_count = 320, 24
            self.assertTrue(module.choose(brain.init, obs, "A", model,
                                          "SPLIT 2").startswith("MOVE "))
            obs.unit_count = 23
            self.assertEqual(module.choose(brain.init, obs, "A", model,
                                            "SPLIT 2"), "SPLIT 2")
            brain.init.width, brain.init.height = 32, 32
            self.assertEqual(module.choose(brain.init, obs, "A", model,
                                            "SPLIT 2"), "SPLIT 2")


if __name__ == "__main__":
    unittest.main()
