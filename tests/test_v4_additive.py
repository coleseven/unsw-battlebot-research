import pathlib
import tempfile
import unittest

from bcsim import v4_additive
from bcsim.match import InProcessBot
from bcsim.paths import ROOT, bot_hash
from test_movement import board


class V4AdditiveTest(unittest.TestCase):
    def make_brain(self, bot, did=0):
        return InProcessBot(bot).new_brain(
            f"ID {did}\nTEAM A\nMAP 7 7\nUNIT_LIMIT 64\n", 0)

    def test_v3_split_schedule_and_unmodified_early_moves(self):
        with tempfile.TemporaryDirectory() as tmp:
            bot = v4_additive.make_candidate(pathlib.Path(tmp) / "additive")
            self.assertNotEqual(bot_hash(bot), bot_hash(ROOT / "versions/v3"))
            candidate = self.make_brain(bot)
            reference = self.make_brain(ROOT / "versions/v3")
            for rnd, length in ((399, 4), (400, 4), (449, 4),
                                (449, 3), (450, 4), (460, 3)):
                obs = board(length=length)
                obs.round = rnd
                self.assertEqual(candidate.turn(obs), reference.turn(obs))
            obs = board(length=4)
            obs.round = 449
            self.assertEqual(candidate.turn(obs), "SPLIT 2")

    def test_feeding_and_sonar_still_activate(self):
        with tempfile.TemporaryDirectory() as tmp:
            bot = v4_additive.make_candidate(pathlib.Path(tmp) / "additive")
            brain = self.make_brain(bot)
            codec = brain.turn.__func__.__globals__["v4_sonar"]
            obs = board(length=6)
            obs.round = 450
            action = brain.turn(obs)
            self.assertTrue(action.startswith("MOVE "))
            self.assertTrue(any(line.startswith("SONAR ") for line in brain.extra))
            obs = board(length=2)
            obs.round, obs.unit_count = 465, 20
            for k in (17, 10, 3, 2, 1, 0):
                obs.occ[k] = ("A", 9, k == 17, "S")
            brain.extra = []
            self.assertEqual(brain.turn(obs), "")
            self.assertFalse(brain.extra)
            obs.occ = board(length=2).occ
            obs.msgs = [codec.encode("A", 5, 3, 12)]
            self.assertTrue(brain.turn(obs).startswith("MOVE "))
            self.assertEqual(brain.target[:3], (5, 3, 12))


if __name__ == "__main__":
    unittest.main()
