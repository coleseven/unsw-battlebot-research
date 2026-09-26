import pathlib
import tempfile
import unittest

from bcsim.match import InProcessBot
from bcsim.paths import ROOT, bot_hash
from test_movement import board

from bcsim import v4_feed


class V4FeedingTest(unittest.TestCase):
    def make_brain(self, feed, did=0):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        name = "feed" if feed else "grower"
        bot = v4_feed.make_candidate(pathlib.Path(tmp.name) / name, feed)
        self.assertNotEqual(bot_hash(bot), bot_hash(ROOT / "versions/v3"))
        return InProcessBot(bot).new_brain(
            f"ID {did}\nTEAM A\nMAP 11 11\nUNIT_LIMIT 64\n", 0)

    def test_growth_role_is_per_id_and_split_cutoff(self):
        b = self.make_brain(False, 0)
        is_grower = b.turn.__func__.__globals__["v4_feeding"].is_grower
        self.assertEqual(b.grower, is_grower(0, "A"))
        obs = board(length=4)
        obs.round = 399
        self.assertEqual(b.turn(obs), "SPLIT 2")
        obs.round = 400
        expected = "MOVE " if b.grower else "SPLIT 2"
        self.assertTrue(b.turn(obs).startswith(expected))

    def test_feed_only_when_long_ally_can_take_drop(self):
        b = self.make_brain(True)
        obs = board(length=2)
        obs.unit_count, obs.round = 20, 465
        for k in (17, 10, 3, 2, 1, 0):
            obs.occ[k] = ("A", 9, k == 17, "S")
        self.assertEqual(b.turn(obs), "")
        obs.round = 464
        self.assertTrue(b.turn(obs).startswith("MOVE "))
        obs.round = 465
        obs.occ[25] = ("B", 10, True, "N")
        self.assertTrue(b.turn(obs).startswith("MOVE "))

    def test_control_never_feeds(self):
        b = self.make_brain(False)
        obs = board(length=2)
        obs.unit_count, obs.round = 20, 465
        for k in (17, 10, 3, 2, 1, 0):
            obs.occ[k] = ("A", 9, k == 17, "S")
        self.assertTrue(b.turn(obs).startswith("MOVE "))


if __name__ == "__main__":
    unittest.main()
