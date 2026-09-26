import pathlib
import tempfile
import unittest

from bcsim import v5_initial
from bcsim.match import InProcessBot
from test_movement import board, edge


class V5InitialTest(unittest.TestCase):
    def make(self, territory=False, king=False, feed=False, did=0,
             sonar=True, king_start=400):
        temp = tempfile.TemporaryDirectory()
        bot = v5_initial.variant(pathlib.Path(temp.name) / "v5", territory, king,
                                 feed, sonar, king_start)
        brain = InProcessBot(bot).new_brain(
            f"ID {did}\nTEAM A\nMAP 48 24\nUNIT_LIMIT 64\n", 0)
        return temp, brain

    def test_king_candidate_requires_size_room_and_distance(self):
        temp, brain = self.make(king=True)
        try:
            module = brain.turn.__func__.__globals__["v5_king"]
            obs = board(length=7)
            obs.round = 400
            self.assertTrue(module.candidate(obs, "A", 2, 0))
            obs.occ[17] = ("B", 1, True, "S")
            self.assertFalse(module.candidate(obs, "A", 2, 0))
            obs.occ[17] = None
            obs.length = 3
            self.assertFalse(module.candidate(obs, "A", 2, 400))
        finally:
            temp.cleanup()

    def test_protected_grower_stops_splitting(self):
        temp, brain = self.make(king=True, did=2)
        try:
            obs = board(length=3)
            obs.round = 399
            self.assertTrue(brain.turn(obs).startswith("MOVE "))
            obs.length = 4
            obs.round = 400
            self.assertTrue(brain.turn(obs).startswith("MOVE "))
            self.assertTrue(brain.protected)
            obs.round = 410
            self.assertTrue(brain.turn(obs).startswith("MOVE "))
        finally:
            temp.cleanup()

    def test_round_350_candidate_stops_splitting_then(self):
        temp, brain = self.make(king=True, did=2, king_start=350)
        try:
            obs = board(length=4)
            obs.round = 349
            self.assertEqual(brain.turn(obs), "SPLIT 2")
            obs.round = 350
            self.assertTrue(brain.turn(obs).startswith("MOVE "))
            self.assertTrue(brain.protected)
        finally:
            temp.cleanup()

    def test_territory_only_acts_on_known_map_shape(self):
        temp, brain = self.make(territory=True)
        try:
            module = brain.turn.__func__.__globals__["v5_hotspot"]
            obs = board(length=3)
            obs.round = 50
            self.assertTrue(module.eligible(brain.init, obs, "A", 2))
            brain.init.width = 32
            self.assertFalse(module.eligible(brain.init, obs, "A", 2))
        finally:
            temp.cleanup()

    def test_short_scout_takes_revealed_portal_but_long_dragon_does_not(self):
        temp, brain = self.make(territory=True)
        try:
            module = brain.turn.__func__.__globals__["v5_hotspot"]
            model = brain.turn.__func__.__globals__["action_model"].MODEL
            obs = board(length=3)
            obs.round = 50
            obs.x = [(10 + k % 7 - 3) % 48 for k in range(49)]
            obs.y = [(0 + k // 7 - 3) % 24 for k in range(49)]
            edge(obs, 24, "E", 0)
            self.assertEqual(module.choose(brain.init, obs, "A", 2, model, "MOVE N"),
                             "MOVE E")
            obs.length = 6
            self.assertEqual(module.choose(brain.init, obs, "A", 2, model, "MOVE N"),
                             "MOVE N")
        finally:
            temp.cleanup()

    def test_long_dragon_avoids_visible_enemy_head_reach(self):
        temp, brain = self.make(king=True)
        try:
            module = brain.turn.__func__.__globals__["v5_king"]
            model = brain.turn.__func__.__globals__["action_model"].MODEL
            obs = board(length=10)
            obs.round = 430
            obs.occ[18] = ("B", 1, True, "S")
            self.assertNotEqual(module.guarded_move(obs, "A", model,
                                                    "MOVE E", True), "MOVE E")
        finally:
            temp.cleanup()

    def test_scout_keeps_splitting_to_export_length_from_dead_end(self):
        temp, brain = self.make(territory=True, did=2)
        control_temp, control = self.make(territory=True, did=0)
        try:
            obs = board(length=4)
            obs.round = 50
            obs.x = [(16 + k % 7 - 3) % 48 for k in range(49)]
            obs.y = [(7 + k // 7 - 3) % 24 for k in range(49)]
            self.assertEqual(brain.turn(obs), "SPLIT 2")
            self.assertEqual(control.turn(obs), "SPLIT 2")
        finally:
            temp.cleanup()
            control_temp.cleanup()

    def test_trauma_gate_uses_visible_start_pattern(self):
        temp, brain = self.make(territory=True, did=2)
        try:
            module = brain.turn.__func__.__globals__["v5_hotspot"]
            obs = board(length=3)
            obs.x = [(4 + k % 7 - 3) % 48 for k in range(49)]
            obs.y = [(2 + k // 7 - 3) % 24 for k in range(49)]
            obs.pearl_in = [0 if (obs.x[k], obs.y[k]) in
                            {(x, y) for x in range(1, 5) for y in (23, 0)}
                            else -1 for k in range(49)]
            self.assertTrue(module.trauma_start(brain.init, obs, "A", 2))
            obs.pearl_in[7] = -1
            self.assertFalse(module.trauma_start(brain.init, obs, "A", 2))
        finally:
            temp.cleanup()

    def test_earlier_feeding_requires_collectible_drop(self):
        temp, brain = self.make(feed=True)
        try:
            module = brain.turn.__func__.__globals__["v5_feeding"]
            obs = board(length=3)
            obs.round, obs.unit_count = 440, 20
            for k in (17, 10, 3, 2, 1, 0):
                obs.occ[k] = ("A", 9, k == 17, "S")
            self.assertTrue(module.should_feed(obs, "A", 0))
            obs.occ[25] = ("B", 10, True, "W")
            self.assertFalse(module.should_feed(obs, "A", 0))
            obs.occ[25] = None
            obs.unit_count = 4
            self.assertFalse(module.should_feed(obs, "A", 0))
        finally:
            temp.cleanup()

    def test_no_sonar_mode_does_not_emit_public_beacon(self):
        temp, brain = self.make(sonar=False)
        try:
            obs = board(length=7)
            obs.round = 450
            self.assertTrue(brain.turn(obs).startswith("MOVE "))
            self.assertFalse(any(item.startswith("SONAR ") for item in brain.extra))
        finally:
            temp.cleanup()


if __name__ == "__main__":
    unittest.main()
