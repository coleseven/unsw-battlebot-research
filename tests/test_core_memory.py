import sys
import unittest

from bcsim import reconstruct, replay
from bcsim.paths import ROOT
from test_movement import board, edge

sys.path.insert(0, str(ROOT / "framework"))
import bc
import core_memory
import core_params


class CoreMemoryTest(unittest.TestCase):
    def test_portal_spawn_pearl_and_occupancy_expiry(self):
        obs = board(length=3)
        obs.round = 10
        obs.pearl[25] = True
        obs.pearl_in[25] = 5
        obs.bodies = [("A", 0, 3, 3, "N", True),
                      ("B", 1, 4, 4, "W", True)]
        edge(obs, 24, "E", 7)
        obs.vedge[1][1] = 7
        mem = core_memory.WorldMemory(11, 11, core_params)
        mem.update(obs)
        self.assertEqual(mem.nav.destination(3 * 11 + 3, "E"), 1 * 11 + 1)
        self.assertEqual(mem.spawn[3 * 11 + 4], (15, 10))
        self.assertEqual(mem.pearl[3 * 11 + 4], 10)
        self.assertEqual(mem.occupied[4 * 11 + 4][:2], ("B", 1))
        obs.x = [(x + 5) % 11 for x in obs.x]
        obs.y = [(y + 5) % 11 for y in obs.y]
        obs.round = 13
        obs.pearl[25] = False
        obs.pearl_in[25] = -1
        obs.bodies = []
        mem.update(obs)
        self.assertNotIn(4 * 11 + 4, mem.occupied)
        self.assertIn(3 * 11 + 4, mem.pearl)
        obs.round = 19
        mem.update(obs)
        self.assertNotIn(3 * 11 + 4, mem.pearl)

    def test_trail_body_only_when_complete_and_distinct(self):
        obs = board(length=3)
        obs.round = 1
        mem = core_memory.WorldMemory(30, 30, core_params)
        mem.update(obs)
        self.assertIsNone(mem.trail_body(3))
        obs.x = [x + 1 for x in obs.x]
        obs.round = 2
        mem.update(obs)
        obs.x = [x + 1 for x in obs.x]
        obs.round = 3
        mem.update(obs)
        self.assertEqual(mem.trail_body(3), [3 * 30 + 5,
                                             3 * 30 + 4,
                                             3 * 30 + 3])
        with self.assertRaises(ValueError):
            mem.update(obs)

    def test_recorded_observation_block(self):
        path = (ROOT / "results/20260924-233609-full-change-bb86e5/full/replays/"
                "candidate-vs-nicked-default_small-s53001.replay")
        turns = reconstruct.turns(replay.load(path))
        first = next(turn for turn in turns if turn.team == "A")
        obs = bc.Obs(first.block)
        mem = core_memory.WorldMemory(16, 16, core_params)
        mem.update(obs)
        self.assertEqual(mem.trail[-1][0], obs.y[bc.CENTER] * 16 + obs.x[bc.CENTER])
        self.assertEqual(len(mem.nav.visible), 49)
        self.assertTrue(all(entry[4] == obs.round for entry in mem.occupied.values()))


if __name__ == "__main__":
    unittest.main()
