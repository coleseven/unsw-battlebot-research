import unittest

from bcsim.map_matrix import render


class MapMatrixTest(unittest.TestCase):
    def test_both_sides_required_and_reported(self):
        games = [
            {"map": "arena", "bot_a": "candidate", "bot_b": "v3", "winner": "A"},
            {"map": "arena", "bot_a": "v3", "bot_b": "candidate", "winner": "A"},
        ]
        self.assertIn("| arena | 1-0-1 |", render(games, "candidate", ["v3"], ["arena"]))
        with self.assertRaises(ValueError):
            render(games[:1], "candidate", ["v3"], ["arena"])


if __name__ == "__main__":
    unittest.main()
