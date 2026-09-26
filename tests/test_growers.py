import pathlib
import tempfile
import unittest

from bcsim import growers
from bcsim.match import InProcessBot, play
from bcsim.paths import ROOT, bot_hash
from test_movement import board


class GrowerTest(unittest.TestCase):
    def test_early_equivalence_round_count_boundary(self):
        from bcsim.grower_report import early_equivalence
        game = {"bot_a": "control_450", "bot_b": "reference_v2", "block": ["reference_v2", "m", 1],
                "rounds": 350, "winner": "A", "map": "m", "seed": 1}
        candidate = {**game, "bot_a": "stop350"}
        self.assertEqual(early_equivalence([game, candidate], "stop350", 350), 1)
        candidate["winner"] = "B"
        with self.assertRaises(ValueError):
            early_equivalence([game, candidate], "stop350", 350)
        game["rounds"] = 351
        self.assertEqual(early_equivalence([game, candidate], "stop350", 350), 0)

    def test_role_distribution_rng_and_cutoffs(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = ROOT / "versions/v2"
            base_hash = bot_hash(source)
            for mode, config in growers.MODES.items():
                path = growers.make_variant(source, pathlib.Path(tmp) / mode, *config)
                loader = InProcessBot(path)
                probe = loader.new_brain("ID 0\nTEAM A\nMAP 11 11\nUNIT_LIMIT 64\n", 42)
                classify = probe.turn.__func__.__globals__["is_grower"]
                for team in "AB":
                    fraction = sum(classify(i, team) for i in range(1024)) / 1024
                    self.assertTrue(.20 <= fraction <= .30)
                    for parity in (0, 1):
                        f = sum(classify(i, team) for i in range(parity, 1024, 2)) / 512
                        self.assertTrue(.18 <= f <= .32)
                for role in (False, True):
                    did = next(i for i in range(64) if classify(i, "A") == role)
                    init = f"ID {did}\nTEAM A\nMAP 11 11\nUNIT_LIMIT 64\n"
                    brain = loader.new_brain(init, 42)
                    original = InProcessBot(source).new_brain(init, 42)
                    self.assertEqual(brain.rng.getstate(), original.rng.getstate())
                    cutoff = config[1] if role and config[1] is not None else config[0]
                    self.assertEqual(brain.cutoff(), cutoff)
                    obs = board(length=4)
                    obs.round = cutoff - 1
                    self.assertEqual(brain.turn(obs), "SPLIT 2")
                    obs.round = cutoff
                    self.assertTrue(brain.turn(obs).startswith("MOVE "))
                    obs.round, obs.unit_count = 100, 64
                    self.assertTrue(brain.turn(obs).startswith("MOVE "))
            self.assertEqual(bot_hash(source), base_hash)

    def test_cutoff450_is_equivalent_to_v2(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = ROOT / "versions/v2"
            path = growers.make_variant(source, pathlib.Path(tmp) / "equivalent", 450)
            for seed in (321, 322):
                a = play(ROOT / "maps/default_small.map", source, ROOT / "opponents/splitter", seed).to_dict()
                b = play(ROOT / "maps/default_small.map", path, ROOT / "opponents/splitter", seed).to_dict()
                for key in ("winner", "reason", "rounds", "a_length", "b_length", "a_longest", "b_longest", "deaths", "error"):
                    self.assertEqual(a[key], b[key], key)


if __name__ == "__main__":
    unittest.main()
