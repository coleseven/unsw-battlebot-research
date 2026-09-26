import pathlib
import sys
import tempfile
import unittest

from bcsim import v6_initial
from bcsim.match import InProcessBot
from bcsim.paths import ROOT
from test_movement import board, edge

sys.path.insert(0, str(ROOT / "framework"))
import core_king
import core_memory
import core_params
import core_search
import core_split


class CoreSearchTest(unittest.TestCase):
    def test_current_tail_blocked_and_known_portal_gated(self):
        obs = board(length=3)
        obs.round = 1
        edge(obs, 24, "E", 7)
        mem = core_memory.WorldMemory(11, 11, core_params)
        mem.update(obs)
        legal = core_search.legal_moves(mem, obs, "A", 0)
        self.assertNotIn("S", legal)  # current own tail: collision before release
        self.assertNotIn("E", legal)  # exit not yet observed
        obs.round = 2
        obs.vedge[1][1] = 7
        mem.update(obs)
        self.assertIn("E", core_search.legal_moves(mem, obs, "A", 0))
        dest = mem.nav.destination(mem.cell(*obs.head), "E")
        mem.occupied[dest] = ("B", 9, False, "N", obs.round)
        self.assertNotIn("E", core_search.legal_moves(mem, obs, "A", 0))

    def test_combined_score_and_v6_snapshot(self):
        obs = board(length=3)
        obs.round = 10
        mem = core_memory.WorldMemory(30, 30, core_params)
        mem.update(obs)
        with tempfile.TemporaryDirectory() as temp:
            bot = v6_initial.variant(pathlib.Path(temp) / "v6")
            brain = InProcessBot(bot).new_brain(
                "ID 0\nTEAM A\nMAP 30 30\nUNIT_LIMIT 64\n", 0)
            model = brain.turn.__func__.__globals__["action_model"].MODEL
            scores = core_search.score_moves(mem, obs, "A", 0,
                                              core_params, model)
            self.assertTrue(scores)
            self.assertTrue(all(direction in "NEW" for direction in scores))
            self.assertTrue(brain.turn(obs).startswith("MOVE "))

    def test_split_and_feed_rules(self):
        obs = board(length=4)
        obs.round, obs.unit_count = 100, 10
        init = type("Init", (), {"width": 30, "height": 30,
                                  "unit_limit": 64})()
        self.assertEqual(core_split.should_split(init, obs, "A", core_params),
                         "SPLIT 2")
        obs.unit_count = 30
        self.assertIsNone(core_split.should_split(init, obs, "A", core_params,
                                                  protected=True))
        # After the cutoff a thin team no longer makes kings re-split, and the
        # low-population refill ends at FLOOR_UNTIL (late feeding thins it).
        obs.round, obs.unit_count = 460, 10
        self.assertIsNone(core_split.should_split(init, obs, "A", core_params,
                                                  protected=True))
        self.assertIsNone(core_split.should_split(init, obs, "A", core_params))
        large = type("Init", (), {"width": 48, "height": 24,
                                   "unit_limit": 64})()
        obs.round = 350  # past the large-map cutoff, before FLOOR_UNTIL
        self.assertEqual(core_split.should_split(large, obs, "A", core_params),
                         "SPLIT 2")
        self.assertIsNone(core_split.should_split(large, obs, "A", core_params,
                                                  protected=True))
        obs.unit_count = 30
        self.assertIsNone(core_split.should_split(large, obs, "A", core_params))
        obs.round = 460  # feeding window
        obs.length = 2
        for k in (10, 11, 12, 16, 17, 18):
            obs.occ[k] = ("A", 4, k == 10, "N")
        mem = core_memory.WorldMemory(30, 30, core_params)
        mem.update(obs)
        target = core_king.visible_target(mem, obs, "A", 0, core_params)
        self.assertIsNotNone(target)
        self.assertTrue(core_king.should_feed(mem, obs, "A", target,
                                              core_params))


    def test_short_dragon_attacks_adjacent_longer_enemy_head(self):
        obs = board(length=2)
        obs.round, obs.unit_count = 50, 10
        obs.occ[31] = ("A", 0, False, "N")            # our tail, length 2
        enemy = {17: True, 10: False, 3: False}       # head north of ours, length 3
        for k, is_head in enemy.items():
            obs.occ[k] = ("B", 7, is_head, "S")
        obs.bodies = [(p[0], p[1], k % 7, k // 7, p[3], p[2])
                      for k, p in enumerate(obs.occ) if p is not None]
        mem = core_memory.WorldMemory(30, 30, core_params)
        mem.update(obs)
        with tempfile.TemporaryDirectory() as temp:
            bot = v6_initial.variant(pathlib.Path(temp) / "v6")
            brain = InProcessBot(bot).new_brain(
                "ID 0\nTEAM A\nMAP 30 30\nUNIT_LIMIT 64\n", 0)
            model = brain.turn.__func__.__globals__["action_model"].MODEL
        scores = core_search.score_moves(mem, obs, "A", 0, core_params, model)
        expected = core_params.W_ATTACK + core_params.W_TRADE * (3 - 2)
        self.assertEqual(scores["N"], expected)
        self.assertEqual(max(scores, key=scores.get), "N")
        guarded = core_search.score_moves(mem, obs, "A", 0, core_params, model,
                                          protected=True)
        self.assertNotIn("N", guarded)                # kings never ram

if __name__ == "__main__":
    unittest.main()
