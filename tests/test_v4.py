import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

from bcsim import v4
from bcsim.match import load_bot
from bcsim.paths import ROOT, bot_hash
from test_movement import board

sys.path.insert(0, str(ROOT / "framework"))
import action_value
import bc
import v4_safety


class V4SafetyTest(unittest.TestCase):
    def setUp(self):
        self.model = {"kind": "linear", "weight": [1.] + [0.] * (len(action_value.FEATURES) - 1),
                      "bias": 0.}

    def test_friendly_reach_blocks_food_when_alternative_exists(self):
        obs = board(length=2)
        obs.occ[24] = ("A", 10, True, "N")
        obs.occ[10] = ("A", 20, True, "S")
        obs.pearl[17] = True
        self.assertEqual(action_value.choose(obs, "A", self.model), "MOVE N")
        self.assertIn(17, v4_safety.threatened_by_friendly(obs, "A", 10))
        self.assertNotEqual(v4_safety.choose(obs, "A", self.model), "MOVE N")
        self.assertNotEqual(v4_safety.choose(obs, "A", self.model, later_only=True), "MOVE N")

    def test_id_order_and_all_threatened_fallback(self):
        obs = board(length=2)
        obs.occ[24] = ("A", 10, True, "N")
        obs.occ[10] = ("A", 5, True, "S")
        obs.pearl[17] = True
        self.assertEqual(v4_safety.choose(obs, "A", self.model, later_only=True), "MOVE N")
        self.assertNotEqual(v4_safety.choose(obs, "A", self.model), "MOVE N")
        obs.occ[26] = ("A", 6, True, "W")
        obs.occ[22] = ("A", 7, True, "E")
        self.assertEqual(v4_safety.choose(obs, "A", self.model), "MOVE N")

    def test_candidate_snapshot_and_split_rule(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = v4.make_candidate(pathlib.Path(tmp) / "guard", False)
            self.assertNotEqual(bot_hash(target), bot_hash(v4.BASE))
            from bcsim.match import InProcessBot
            bot = InProcessBot(target).new_brain("ID 10\nTEAM A\nMAP 11 11\nUNIT_LIMIT 64\n", 0)
            obs = board(length=4)
            obs.round = 449
            self.assertEqual(bot.turn(obs), "SPLIT 2")
            obs.round = 450
            self.assertTrue(bot.turn(obs).startswith("MOVE "))

    def test_ctmes_uses_process_adapter(self):
        with patch("bcsim.match.ProcessBot", return_value="process") as process:
            self.assertEqual(load_bot(ROOT / "sparring/ctmes", "A"), "process")
            process.assert_called_once()


if __name__ == "__main__":
    unittest.main()
