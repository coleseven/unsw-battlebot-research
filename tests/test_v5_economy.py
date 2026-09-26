import pathlib
import sys
import tempfile
import unittest

from bcsim import v5_initial
from bcsim.match import InProcessBot
from bcsim.paths import ROOT
from test_movement import board

sys.path.insert(0, str(ROOT / "framework"))
import v5_economy


class EconomyTest(unittest.TestCase):
    def test_recent_offscreen_pearl_and_bounded_search(self):
        obs = board(length=3)
        obs.pearl[25] = True
        policy = v5_economy.Policy(type("Init", (), {"width": 30, "height": 30})())
        self.assertEqual(policy.choose(obs, "A", "MOVE N"), "MOVE N")
        obs.pearl[25] = False
        obs.x = [x + 5 for x in obs.x]
        obs.round += 1
        self.assertEqual(policy.choose(obs, "A", "MOVE N"), "MOVE W")
        self.assertLessEqual(policy.last_expanded, 96)

    def test_visible_food_keeps_local_evaluator(self):
        obs = board(length=3)
        obs.pearl[17] = True
        policy = v5_economy.Policy(type("Init", (), {"width": 30, "height": 30})())
        self.assertEqual(policy.choose(obs, "A", "MOVE N"), "MOVE N")

    def test_variant_is_opt_in_and_isolated(self):
        with tempfile.TemporaryDirectory() as temp:
            path = v5_initial.variant(pathlib.Path(temp) / "economy", True, True,
                                      economy=True)
            brain = InProcessBot(path).new_brain(
                "ID 2\nTEAM A\nMAP 30 30\nUNIT_LIMIT 64\n", 0)
            self.assertIsNotNone(brain.economy_policy)


if __name__ == "__main__":
    unittest.main()
