import unittest

from bcsim.split_mortality import count_births
from bcsim import replay as r


class SplitMortalityTest(unittest.TestCase):
    def test_births_deaths_and_censoring(self):
        def birth(parent, child, team="A"):
            return (r.DRAGON_SPLIT, parent, child, team, "N", [(0, 0)] * 2, [(1, 1)] * 2)
        events = [(r.ROUND_START, 0), (r.TURN_START, 0), birth(0, 2),
                  birth(0, 3), birth(0, 4), birth(0, 5), birth(1, 6, "B"),
                  (r.TURN_START, 1), (r.DRAGON_DEATH, 3, "H"),
                  (r.TURN_START, 2), (r.DRAGON_DEATH, 2, "W"),
                  (r.TURN_START, 4), (r.ROUND_START, 5),
                  (r.TURN_START, 4), (r.DRAGON_DEATH, 4, "O")]
        c = count_births(events, "A")
        self.assertEqual(c["births"], 4)
        self.assertEqual(c["child_length_2"], 4)
        self.assertEqual(c["newborn_first_turns"], 2)
        self.assertEqual(c["deaths_before_first_turn"], 1)
        self.assertEqual(c["first_own_turn_deaths"], 1)
        self.assertEqual(c["first_own_turn_death_W"], 1)
        self.assertEqual(c["birth_round_deaths"], 2)
        self.assertEqual(c["deaths_before_age5"], 2)
        self.assertEqual(c["children_alive_at_end"], 1)
        self.assertEqual(c["children_without_first_turn_at_end"], 1)


if __name__ == "__main__":
    unittest.main()
