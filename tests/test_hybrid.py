import math
import pathlib
import sys
import tempfile
import unittest

from bcsim import hybrid
from bcsim.match import InProcessBot, play
from bcsim.paths import ROOT, bot_hash, foreign_imports
from test_movement import board, edge

sys.path.insert(0, str(ROOT / "framework"))
import action_value
import adaptive_roles
import bc


class HybridTest(unittest.TestCase):
    def test_candidates_exclude_occupied_portal_reverse(self):
        obs = board(length=2)
        edge(obs, 24, "E", 0)
        obs.occ[23] = ("A", 8, True, "E")
        self.assertEqual(action_value.candidates(obs, "A"), ["N"])
        obs.occ[17] = ("B", 9, False, "S")
        self.assertEqual(action_value.candidates(obs, "A"), [])

    def test_feature_dimensions_values_and_food(self):
        obs = board(length=2)
        obs.pearl[17] = True
        dirs, rows = action_value.features(obs, "A")
        self.assertEqual(rows[dirs.index("N")][0], 1)
        for row in rows:
            self.assertEqual(len(row), len(action_value.FEATURES))
            self.assertTrue(all(math.isfinite(v) and 0 <= v <= 1 for v in row))
        # Uniform context cannot favor a direction in the linear control.
        model = {"kind": "linear", "weight": [0.] * len(action_value.FEATURES), "bias": 0.}
        model["weight"][0] = 1
        self.assertEqual(action_value.choose(obs, "A", model), "MOVE N")

    def test_reach_and_boundary_dont_wrap_minus_one(self):
        obs = board(length=2)
        obs.occ[0] = ("B", 10, True, "N")
        dirs, rows = action_value.features(obs, "A")
        self.assertTrue(all(row[10] == 0 for row in rows))
        obs.occ[18] = ("B", 10, True, "W")
        _, rows = action_value.features(obs, "A", ["N"])
        self.assertEqual(rows[0][10], 1)
        self.assertEqual(rows[0][12], 1)

    def test_dead_end_and_short_path(self):
        obs = board(length=2, open_=False)
        edge(obs, 24, "N", bc.OPEN)
        _, rows = action_value.features(obs, "A", ["N"])
        self.assertEqual(rows[0][6], 1)
        self.assertEqual(rows[0][15], 0)
        self.assertEqual(rows[0][4], 1 / 49)

    def test_features_rotate_with_observation(self):
        obs = board(length=2)
        obs.pearl[16] = True
        obs.pearl_in[10] = 2
        obs.occ[11] = ("B", 7, True, "E")
        edge(obs, 17, "E", bc.KELP)
        rotated = board(length=2, open_=False)
        rotate = lambda k: (k % 7) * 7 + 6 - k // 7
        clockwise = dict(zip("NESW", "ESWN"))
        rotated.facing = clockwise[obs.facing]
        rotated.occ = [None] * 49
        for k in range(49):
            dest = rotate(k)
            rotated.pearl[dest] = obs.pearl[k]
            rotated.pearl_in[dest] = obs.pearl_in[k]
            if obs.occ[k]:
                t, did, head, facing = obs.occ[k]
                rotated.occ[dest] = (t, did, head, clockwise[facing])
            for d in bc.DIRS:
                edge(rotated, dest, clockwise[d], obs.edge(k, d))
        directions, rows = action_value.features(obs, "A")
        turned, values = action_value.features(rotated, "A")
        self.assertEqual(set(turned), {clockwise[d] for d in directions})
        for d, row in zip(directions, rows):
            self.assertEqual(row, values[turned.index(clockwise[d])])

    def test_mlp_portable_calculation(self):
        row = [0.2] * len(action_value.FEATURES)
        model = {"kind": "mlp", "w1": [[1.] * len(row)], "b1": [.1], "w2": [.5], "b2": .3}
        self.assertAlmostEqual(action_value.score(row, model), .5 * math.tanh(sum(row) + .1) + .3)

    def test_role_adoption_hysteresis_and_isolation(self):
        obs = board(length=8)
        obs.round, obs.unit_count = 200, 16
        first, second = adaptive_roles.Role(), adaptive_roles.Role()
        self.assertTrue(first.update(obs, "mature"))
        self.assertFalse(second.preserving)
        obs.length, obs.unit_count = 5, 9
        self.assertTrue(first.update(obs, "mature"))
        obs.unit_count = 7
        self.assertFalse(first.update(obs, "mature"))
        self.assertEqual((first.adoptions, first.releases), (1, 1))
        obs.round, obs.unit_count, obs.length = 250, 16, 4
        obs.pearl[17] = obs.pearl[18] = obs.pearl[19] = True
        self.assertTrue(second.update(obs, "opportunity"))

    def test_wrapper_and_split_policy(self):
        original_hash = bot_hash(hybrid.BASE)
        with tempfile.TemporaryDirectory() as tmp:
            model = {"kind": "linear", "weight": [0.] * len(action_value.FEATURES), "bias": 0}
            path = hybrid.make_bot(hybrid.BASE, pathlib.Path(tmp) / "probe", "evaluator", model)
            self.assertFalse(foreign_imports(path))
            bot = InProcessBot(path).new_brain("ID 0\nTEAM A\nMAP 11 11\nUNIT_LIMIT 64\n", 42)
            rng_before = bot.rng.getstate()
            obs = board(length=4)
            obs.round, obs.unit_count = 449, 63
            self.assertEqual(bot.turn(obs), "SPLIT 2")
            obs.round = 450
            self.assertTrue(bot.turn(obs).startswith("MOVE "))
            self.assertEqual(bot.rng.getstate(), rng_before)
            control = hybrid.make_bot(hybrid.BASE, pathlib.Path(tmp) / "control", "control")
            a = play(ROOT / "maps/default_small.map", hybrid.BASE, ROOT / "opponents/splitter", 28000).to_dict()
            b = play(ROOT / "maps/default_small.map", control, ROOT / "opponents/splitter", 28000).to_dict()
            for key in ("winner", "reason", "rounds", "a_length", "b_length", "deaths", "error"):
                self.assertEqual(a[key], b[key])
        self.assertEqual(bot_hash(hybrid.BASE), original_hash)


if __name__ == "__main__":
    unittest.main()
