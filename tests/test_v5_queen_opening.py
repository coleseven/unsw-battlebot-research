import pathlib
import tempfile
import unittest

from bcsim import v5_initial
from bcsim.match import InProcessBot
from test_movement import board


class QueenOpeningTest(unittest.TestCase):
    def make(self, did=0):
        temp = tempfile.TemporaryDirectory()
        bot = v5_initial.variant(pathlib.Path(temp.name) / "queen", True, True,
                                 queen_opening=True)
        brain = InProcessBot(bot).new_brain(
            f"ID {did}\nTEAM A\nMAP 25 35\nUNIT_LIMIT 64\n", 0)
        return temp, brain

    def test_founder_opening_is_gated_by_observed_start(self):
        temp, brain = self.make()
        other_temp, other = self.make()
        try:
            module = brain.turn.__func__.__globals__["action_model"]
            obs = board(length=3)
            obs.round = 0
            obs.x = [x + 2 for x in obs.x]
            obs.y = [y + 8 for y in obs.y]
            self.assertNotEqual(brain.queen_policy.choose(obs, "A", module.MODEL,
                                                           "MOVE S"), "MOVE S")
            self.assertEqual(brain.queen_policy.target, (15, 2))
            obs.x = [x + 1 for x in obs.x]
            self.assertEqual(other.queen_policy.choose(obs, "A", module.MODEL,
                                                        "MOVE S"), "MOVE S")
        finally:
            temp.cleanup()
            other_temp.cleanup()


if __name__ == "__main__":
    unittest.main()
