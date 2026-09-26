import glob
import sys
import unittest

from bcsim import reconstruct, replay
from bcsim.paths import ROOT

sys.path.insert(0, str(ROOT / "framework"))
import bc
import core_memory
import core_params
import v6_hub_book

REPLAYS = ROOT / "results" / "20260925-191302-full-change-a71535" / "full" / "replays"


class HubBookTest(unittest.TestCase):
    def test_real_observations_identify_their_map(self):
        paths = sorted(glob.glob(str(REPLAYS / "candidate-vs-v3-*.replay")))
        if not paths:
            self.skipTest("frozen replays not present")
        seen_maps = set()
        for path in paths:
            r = replay.load(path)
            board = reconstruct.Board(r.map_text)
            expected = [h for bits, h in v6_hub_book.BOOK.get((board.w, board.h), ())
                        if _matches(bits, board)]
            mem = did = None
            for turn in reconstruct.turns(r):
                if turn.team != "A" or (did is not None and turn.id != did):
                    continue
                did = turn.id
                obs = bc.Obs(turn.block)
                if mem is None:
                    mem = core_memory.WorldMemory(board.w, board.h, core_params)
                mem.update(obs)
                if turn.round >= 5:
                    break
            want = expected[0] if expected else []
            self.assertEqual(mem.hubs, list(want), r.map_name)
            seen_maps.add(r.map_name)
        self.assertEqual(len(seen_maps), 11)


    def test_learned_hubs_on_an_unknown_map(self):
        from test_movement import board
        mem = core_memory.WorldMemory(40, 40, core_params)   # no book map is 40x40
        self.assertEqual(mem.hub_maps, [])
        obs = board(length=3)
        obs.pearl_in = [500] * 49               # slow tiles everywhere in view ...
        obs.pearl_in[8] = 1                     # ... except (1, 1), a fast one
        obs.round = core_params.LEARN_EVERY
        mem.update(obs)
        self.assertTrue(mem.hubs)
        hub, value = mem.hubs[0]
        self.assertEqual(value, 1.0)
        self.assertLessEqual(max(abs(hub % 40 - 1), abs(hub // 40 - 1)), 2)
        self.assertLess(mem.local_rate, 0.1)

    def test_exploration_goal_points_away_from_seen_ground(self):
        from test_movement import board
        import core_search
        mem = core_memory.WorldMemory(40, 40, core_params)
        obs = board(length=3)
        obs.round, obs.unit_count = 20, 5
        mem.update(obs)
        mem.update_goal(obs, 0)
        self.assertIsNotNone(mem.goal)
        gx, gy = mem.goal % 40, mem.goal // 40
        self.assertGreater(max(min(gx, 40 - gx), min(gy, 40 - gy)), 3)   # not the block we stand in
        terms = {}
        for d in "NEW":
            dest = mem.nav.destination(mem.cell(*obs.head), d)
            terms[d] = core_search.search_one(mem, obs, "A", 0, dest, d, core_params,
                                              {}, 0.0, 1e9)["progress"]
        head = mem.cell(*obs.head)
        toward = min("NEW", key=lambda d: core_search.torus_distance(
            mem.nav.destination(head, d), mem.goal, 40, 40))
        self.assertEqual(max(terms, key=terms.get), toward)

def _matches(bits, board):
    """True when the book entry is this map's static layout."""
    n = board.w * board.h
    layout = 0
    for (x, y) in board.hedge:
        layout |= 1 << (y * board.w + x)
    for (x, y) in board.vedge:
        layout |= 1 << (n + y * board.w + x)
    return int(bits, 16) == layout

if __name__ == "__main__":
    unittest.main()
