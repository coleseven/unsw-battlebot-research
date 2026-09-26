import pathlib
import tempfile
import unittest

from bcsim import v4_additive_portal
from bcsim.match import InProcessBot
from bcsim.paths import ROOT, bot_hash
from test_movement import board, edge


class V4AdditivePortalTest(unittest.TestCase):
    def make_brain(self, path):
        return InProcessBot(path).new_brain(
            "ID 0\nTEAM A\nMAP 7 7\nUNIT_LIMIT 64\n", 0)

    def test_no_portal_decision_matches_additive(self):
        with tempfile.TemporaryDirectory() as tmp:
            bot = v4_additive_portal.make_candidate(pathlib.Path(tmp) / "portal")
            baseline = self.make_brain(v4_additive_portal.BASE)
            candidate = self.make_brain(bot)
            self.assertNotEqual(bot_hash(bot), bot_hash(v4_additive_portal.BASE))
            for rnd, length in ((399, 4), (449, 4), (450, 6), (460, 3)):
                obs = board(length=length)
                obs.round = rnd
                self.assertEqual(candidate.turn(obs), baseline.turn(obs))

    def test_portal_only_when_no_ordinary_step_and_never_replaces_split(self):
        with tempfile.TemporaryDirectory() as tmp:
            bot = v4_additive_portal.make_candidate(pathlib.Path(tmp) / "portal")
            brain = self.make_brain(bot)
            obs = board(length=3, open_=False)
            edge(obs, 24, "E", 0)
            self.assertEqual(brain.turn(obs), "MOVE E")
            edge(obs, 24, "N", -1)
            self.assertEqual(brain.turn(obs), "MOVE N")
            obs.round, obs.length = 400, 4
            self.assertEqual(brain.turn(obs), "SPLIT 2")


if __name__ == "__main__":
    unittest.main()
