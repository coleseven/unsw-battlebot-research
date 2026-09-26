import sys
import pathlib
import tempfile
import unittest

from bcsim.paths import ROOT
sys.path.insert(0, str(ROOT / "framework"))
import bc
import portal_escape
from test_movement import board, edge


class PortalEscapeTest(unittest.TestCase):
    def test_no_portal_real_games_unchanged(self):
        from bcsim import portal_experiment
        from bcsim.match import play
        with tempfile.TemporaryDirectory() as tmp:
            source = ROOT / "versions/v2"
            candidate = portal_experiment.make_variant(source, pathlib.Path(tmp) / "portal")
            for mapname in ("arena", "default_small"):
                path = ROOT / "maps" / (mapname + ".map")
                a = play(path, source, ROOT / "opponents/splitter", 17499).to_dict()
                b = play(path, candidate, ROOT / "opponents/splitter", 17499).to_dict()
                for field in ("winner", "reason", "rounds", "a_length", "b_length", "a_longest", "b_longest", "deaths", "error"):
                    self.assertEqual(a[field], b[field], field)

    def test_only_last_resort_and_preserve_splits_and_head_trade(self):
        o = board(open_=False)
        edge(o, 24, "E", 0)
        self.assertEqual(portal_escape.choose(o, "A", "MOVE N"), "MOVE E")
        self.assertEqual(portal_escape.choose(o, "A", "SPLIT 2"), "SPLIT 2")
        edge(o, 24, "N", bc.OPEN)
        self.assertEqual(portal_escape.choose(o, "A", "MOVE N"), "MOVE N")
        o.occ[17] = ("B", 1, True, "S")
        self.assertEqual(portal_escape.choose(o, "A", "MOVE N"), "MOVE N")
        o.occ[17] = ("A", 1, True, "S")
        self.assertEqual(portal_escape.choose(o, "A", "MOVE N"), "MOVE E")

    def test_visible_exit_and_tail_blocked(self):
        o = board(open_=False)
        edge(o, 24, "E", 0)
        o.vedge[1][1] = 0
        self.assertEqual(portal_escape.exit_score(o, "E"), 2)
        o.occ[8] = ("A", 0, False, "E")
        self.assertEqual(portal_escape.exit_score(o, "E"), -1)
        self.assertEqual(portal_escape.choose(o, "A", "MOVE N"), "MOVE N")

    def test_all_four_exit_orientations(self):
        for d, target in (("N", 1), ("S", 8), ("W", 7), ("E", 8)):
            o = board(open_=False)
            edge(o, 24, d, 0)
            matrix = o.hedge if d in "NS" else o.vedge
            matrix[1][1] = 0
            self.assertEqual(portal_escape.exit_score(o, d), 2)
            o.occ[target] = ("B", 1, False, "N")
            self.assertEqual(portal_escape.exit_score(o, d), -1)

    def test_real_engine_escape(self):
        from bcsim.match import engine
        # A at (4,4): wall north/west, own neck south, portal east.
        text = ("MAP 11 11\nMAP_NAME Portal_Test\nTILE_COUNT 0\nEDGE_COUNT 4\n"
                "EDGE 100 1 -1\nEDGE 112 1 -1\nEDGE 113 2 0\nEDGE 38 2 0\n"
                "DRAGON_COUNT 2\nDRAGON 0 3 4 4 4 5 4 6\nDRAGON 1 3 8 8 8 9 8 10\n")
        teams, actions, notices = {}, [], []
        def spawn(did, init):
            teams[did] = bc.Init(init.decode()).team
        def reply(did, block):
            if teams[did] == "B":
                return b"SUICIDE\nENDTURN\n"
            action = portal_escape.choose(bc.Obs(block.decode()), "A", "MOVE N")
            actions.append(action)
            return (action + "\nENDTURN\n").encode()
        result = engine().run(text.encode(), reply, lambda *args: None, spawn, notices.append, 0)
        self.assertFalse(notices)
        self.assertEqual(actions, ["MOVE E"])
        self.assertEqual(result.a_dragons, 1)
        self.assertEqual(result.winner, "A")


if __name__ == "__main__":
    unittest.main()
