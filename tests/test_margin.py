import unittest

from bcsim.margin import game_margin


class MarginTest(unittest.TestCase):
    def test_elimination_fills_to_500(self):
        stats = {"end": "eliminated", "winner": "B", "timeline": [
            {"round": 0, "A": [1, 3, 3], "B": [1, 3, 3]},
            {"round": 10, "A": [1, 4, 4], "B": [1, 4, 4]},
            {"round": 20, "A": [0, 0, 0], "B": [1, 5, 5]},
        ]}
        report = game_margin(stats, "A")
        self.assertEqual(report["samples"], 50)
        self.assertAlmostEqual(report["margin"], -49 / 50)
        self.assertEqual(report["elimination_round"], 20)
        self.assertEqual(report["outcome"], "loss")

    def test_round_limit_uses_last_state_for_500(self):
        timeline = [{"round": 0, "A": [1, 2, 2], "B": [1, 2, 2]}]
        timeline.extend({"round": r, "A": [1, 4, 4], "B": [1, 2, 2]}
                        for r in range(10, 500, 10))
        timeline.append({"round": 499, "A": [1, 6, 6], "B": [1, 2, 2]})
        report = game_margin({"end": "round_limit", "winner": "A",
                              "timeline": timeline}, "A")
        self.assertAlmostEqual(report["margin"], (49 / 3 + 0.5) / 50)
        self.assertAlmostEqual(report["final_share"], 0.5)
        self.assertIsNone(report["elimination_round"])


if __name__ == "__main__":
    unittest.main()
