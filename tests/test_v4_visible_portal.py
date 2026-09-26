import pathlib
import sys
import tempfile
import unittest

from bcsim import v4_visible_portal
from bcsim.match import InProcessBot
from bcsim.paths import ROOT
from test_movement import board, edge

sys.path.insert(0, str(ROOT / "framework"))
import portal_visible


class V4VisiblePortalTest(unittest.TestCase):
    def test_only_visible_empty_exit_is_added(self):
        obs = board(open_=False)
        edge(obs, 24, "E", 0)
        self.assertEqual(portal_visible.choose(obs, "A", "MOVE N"), "MOVE N")
        obs.vedge[1][1] = 0
        self.assertEqual(portal_visible.choose(obs, "A", "MOVE N"), "MOVE E")
        obs.occ[8] = ("B", 4, False, "N")
        self.assertEqual(portal_visible.choose(obs, "A", "MOVE N"), "MOVE N")
        self.assertEqual(portal_visible.choose(obs, "A", "SPLIT 2"), "SPLIT 2")

    def test_candidate_preserves_v3_split_and_additive_on_no_portal_view(self):
        with tempfile.TemporaryDirectory() as tmp:
            bot = v4_visible_portal.make_candidate(pathlib.Path(tmp) / "visible_portal")
            init = "ID 0\nTEAM A\nMAP 7 7\nUNIT_LIMIT 64\n"
            candidate = InProcessBot(bot).new_brain(init, 0)
            additive = InProcessBot(v4_visible_portal.BASE).new_brain(init, 0)
            for rnd, length in ((399, 4), (449, 4), (450, 6), (470, 3)):
                obs = board(length=length)
                obs.round = rnd
                self.assertEqual(candidate.turn(obs), additive.turn(obs))


if __name__ == "__main__":
    unittest.main()
