import pathlib
import sys
import tempfile
import unittest

from bcsim import navigation_experiment, reconstruct, portal_followup
from bcsim.match import InProcessBot, play
from bcsim.paths import ROOT, bot_hash
from test_movement import board, edge

sys.path.insert(0, str(ROOT / "framework"))
import bc
import navigation


class NavigationTest(unittest.TestCase):
    def test_all_global_destinations_match_reference(self):
        b = reconstruct.Board(portal_followup.generate(portal_followup.SPECS[0]))
        m = navigation.Memory(b.w, b.h, True)
        for y in range(b.h):
            for x in range(b.w):
                cell = y*b.w+x
                for d in "NESW":
                    m.remember(m.edge_key(cell, d), b.edge(x, y, d))
        for y in range(b.h):
            for x in range(b.w):
                for d in "NESW":
                    expected = b.dest(x, y, d)
                    self.assertEqual(m.destination(y*b.w+x, d),
                                     None if expected is None else expected[1]*b.w+expected[0])

    def test_update_wrap_and_pair_coordinates(self):
        o = board()
        o.x = [(x-3) % 11 for x in o.x]
        o.y = [(y-3) % 11 for y in o.y]
        edge(o, 24, "E", 7)
        o.vedge[1][1] = 7
        m = navigation.Memory(11, 11, True)
        m.update(o)
        self.assertEqual(m.destination(0, "E"), 9*11+9)
        self.assertEqual(m.edges[m.edge_key(0, "N")], bc.OPEN)
        self.assertEqual(len(m.visible), 49)

    def test_deliberate_portal_route_and_blocked_exit(self):
        o = board(length=2, open_=False)
        edge(o, 24, "E", 0)
        o.vedge[1][1] = 0
        o.pearl[8] = True
        for portals in (False, True):
            m = navigation.Memory(11, 11, portals)
            m.update(o)
            self.assertEqual(m.choose(o, "A", "MOVE N"), "MOVE E" if portals else "MOVE N")
        o.occ[8] = ("A", 0, False, "N")
        m.update(o)
        self.assertEqual(m.choose(o, "A", "MOVE N"), "MOVE N")
        self.assertEqual(m.choose(o, "A", "SPLIT 2"), "SPLIT 2")

    def test_unknown_pair_is_not_traversed(self):
        o = board(open_=False)
        edge(o, 24, "E", 0)
        m = navigation.Memory(11, 11, True)
        m.update(o)
        self.assertIsNone(m.destination(3*11+3, "E"))

    def test_pair_discovered_across_separate_observations(self):
        o = board()
        edge(o, 24, "E", 2)
        m = navigation.Memory(30, 30, True)
        m.update(o)
        self.assertIsNone(m.destination(3*30+3, "E"))
        first_round = o.round
        o.x = [x+10 for x in o.x]
        o.y = [y+10 for y in o.y]
        o.round += 1
        m.update(o)
        self.assertEqual(m.destination(13*30+13, "E"), 3*30+4)
        self.assertNotIn(3*30+4, m.visible)
        self.assertEqual(m.seen[3*30+4], first_round)
        self.assertEqual(len(m.ends[2]), 2)

    def test_off_window_threat_is_not_last_visible_cell(self):
        o = board(length=2, open_=False)
        o.occ[0] = ("B", 1, True, "S")
        edge(o, 0, "N", bc.OPEN)  # local step is -1, not cell 48
        edge(o, 24, "E", 0)
        o.vedge[6][6] = 0
        o.pearl[48] = True
        m = navigation.Memory(11, 11, True)
        m.update(o)
        self.assertEqual(m.choose(o, "A", "MOVE N"), "MOVE E")

    def test_memory_persists_food_expires_and_search_is_bounded(self):
        o = board()
        o.pearl[8] = True
        m = navigation.Memory(30, 30)
        m.update(o)
        key = 31
        self.assertIn(key, m.food)
        old = m.edges[0]
        o.x = [x+10 for x in o.x]
        o.y = [y+10 for y in o.y]
        o.round += 9
        m.update(o)
        self.assertNotIn(key, m.food)
        self.assertEqual(m.edges[0], old)
        m.choose(o, "A", "MOVE N")
        self.assertLessEqual(m.expanded, 96)

    def test_reproduction_and_newborn_memory_isolation(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = ROOT / "versions/v2"
            initial = bot_hash(source)
            path = navigation_experiment.make_variant(source, pathlib.Path(tmp)/"nav", True)
            loader = InProcessBot(path)
            a = loader.new_brain("ID 0\nTEAM A\nMAP 11 11\nUNIT_LIMIT 64\n", 1)
            b = loader.new_brain("ID 2\nTEAM A\nMAP 11 11\nUNIT_LIMIT 64\n", 1)
            o = board(length=4)
            o.round = 100
            self.assertEqual(a.turn(o), "SPLIT 2")
            self.assertTrue(a.memory.visible)
            self.assertFalse(b.memory.visible)
            self.assertEqual(bot_hash(source), initial)

    def test_no_portal_ablation_real_game_equivalence(self):
        from bcsim import navigation_audit, navigation_diagnostics
        with tempfile.TemporaryDirectory() as tmp:
            paths = [navigation_experiment.make_variant(ROOT/"versions/v2", pathlib.Path(tmp)/str(mode), mode)
                     for mode in (False, True)]
            games = []
            for p in paths:
                replay_path = pathlib.Path(tmp) / (p.name + ".replay")
                game = play(ROOT/"maps/default_small.map", p, ROOT/"opponents/splitter", 20999,
                            replay_to=replay_path).to_dict()
                game["replay"] = str(replay_path)
                counts, samples = navigation_audit.one_game((game, str(p), str(ROOT/"maps/default_small.map")))
                self.assertGreater(counts["verified_candidate_turns"], 0)
                self.assertIn(p.name + "__mapped_cells", samples)
                if p.name == "True":
                    detail, _ = navigation_diagnostics.one_game((game, str(p), str(ROOT/"maps/default_small.map")))
                    self.assertEqual(detail["verified_candidate_turns"], counts["verified_candidate_turns"])
                games.append(game)
            for field in ("winner", "reason", "rounds", "a_length", "b_length", "a_longest", "b_longest", "deaths", "error"):
                self.assertEqual(games[0][field], games[1][field], field)


if __name__ == "__main__":
    unittest.main()
