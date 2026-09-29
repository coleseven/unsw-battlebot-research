import json
import tempfile
import unittest
from pathlib import Path

from bcsim import tune


class TuneTest(unittest.TestCase):
    def test_rewrites_python_and_cpp_settings(self):
        with tempfile.TemporaryDirectory() as t:
            py = Path(t) / "core_params.py"
            py.write_text("W_HUB = 60.0\nN_SEARCH = 200\nW_HUB_X = 1.0\n", encoding="utf8")
            tune.write_params(py, {"W_HUB": 12.5, "N_SEARCH": 150})
            self.assertEqual(py.read_text(encoding="utf8"), "W_HUB = 12.5\nN_SEARCH = 150\nW_HUB_X = 1.0\n")
            cpp = Path(t) / "params.hpp"
            cpp.write_text("constexpr double W_HUB = 60.0;\nstatic constexpr int N_SEARCH = 200;\n"
                           "#define DEPTH_MAX 16\n", encoding="utf8")
            tune.write_params(cpp, {"W_HUB": 7.25, "N_SEARCH": 999, "DEPTH_MAX": 20})
            self.assertEqual(cpp.read_text(encoding="utf8"),
                             "constexpr double W_HUB = 7.25;\nstatic constexpr int N_SEARCH = 999;\n"
                             "#define DEPTH_MAX 20\n")
            with self.assertRaises(ValueError):
                tune.write_params(py, {"MISSING": 1})

    def test_decode_encode_round_trip(self):
        space = {"A": [0, 100], "B": [2, 6, "int"]}
        vals = tune.decode([0.5, 0.49], space)
        self.assertEqual(vals, {"A": 50.0, "B": 4})
        self.assertEqual(tune.encode({"A": 25, "B": 6}, space), [0.25, 1.0])


    def test_rewrites_the_cpp_port_params_format(self):
        with tempfile.TemporaryDirectory() as t:
            hpp = Path(t) / "params.hpp"
            hpp.write_text("\n".join(["namespace params {", "",
                                      "inline constexpr double W_HUB = 60.0;",
                                      "inline constexpr int N_SEARCH = 200;",
                                      "}  // namespace params", ""]), encoding="utf8")
            tune.write_params(hpp, {"W_HUB": 12.5, "N_SEARCH": 400})
            text = hpp.read_text(encoding="utf8")
            self.assertIn("inline constexpr double W_HUB = 12.5;", text)
            self.assertIn("inline constexpr int N_SEARCH = 400;", text)

    def test_booleans_and_group_multipliers(self):
        with tempfile.TemporaryDirectory() as t:
            py = Path(t) / "core_params.py"
            py.write_text("GOAL = True\nW_A = 10.0\nW_B = 4.0\n", encoding="utf8")
            hpp = Path(t) / "params.hpp"
            hpp.write_text("inline constexpr bool GOAL = true;\ninline constexpr double W_A = 10.0;\n"
                           "inline constexpr double W_B = 4.0;\n", encoding="utf8")
            space = {"G": {"low": 0, "high": 3, "scale": ["W_A", "W_B"]}, "W_C": [0, 1]}
            self.assertEqual(tune.read_current(hpp, {"G": space["G"]}), {"G": 1.0})
            base = tune.read_members(hpp, space)
            self.assertEqual(base, {"W_A": 10.0, "W_B": 4.0})
            settings = tune.expand({"G": 0.5, "W_C": 0.2}, space, base)
            self.assertEqual(settings, {"W_A": 5.0, "W_B": 2.0, "W_C": 0.2})
            self.assertEqual(tune.decode(tune.encode({"G": 1.5, "W_C": 0.5}, space), space),
                             {"G": 1.5, "W_C": 0.5})
            for f in (py, hpp):
                tune.write_params(f, {"GOAL": False, "W_A": 5.0})
            self.assertEqual(py.read_text(encoding="utf8"), "GOAL = False\nW_A = 5.0\nW_B = 4.0\n")
            self.assertIn("inline constexpr bool GOAL = false;", hpp.read_text(encoding="utf8"))
            self.assertIn("inline constexpr double W_A = 5.0;", hpp.read_text(encoding="utf8"))

    def test_aligned_objective_follows_the_longest_dragon(self):
        from bcsim import margin
        # we have more total length but a shorter longest dragon, and lose
        timeline = [{"round": r, "A": [10, 200, 20], "B": [3, 60, 25]} for r in range(10, 500, 10)]
        timeline.append({"round": 499, "A": [10, 200, 20], "B": [3, 60, 25]})
        stats = {"timeline": timeline, "end": "round_limit", "winner": "B"}
        m = margin.game_margin(stats, "A")
        self.assertGreater(m["margin"], 0)          # length share says we were ahead
        self.assertLess(m["aligned"], 0)            # the result and the longest dragon say otherwise
        self.assertAlmostEqual(m["aligned"], 0.5 * -1 + 0.25 * (20 - 25) / 45 + 0.25 * m["margin"])
        elim = {"timeline": timeline[:5], "end": "eliminated", "winner": "A"}
        self.assertGreater(margin.game_margin(elim, "A")["aligned"], 0.9)

    def test_pair_map_sampling(self):
        maps = [Path(f"{m}.map") for m in ("a", "a_p1", "b", "b_p1", "c")]
        plan = {"map_sample": "pair", "seed": 3}
        picked = tune.gen_maps(plan, maps, 0)
        self.assertEqual(sorted(p.stem.split("_")[0] for p in picked), ["a", "b", "c"])
        self.assertEqual(picked, tune.gen_maps(plan, maps, 0))          # same for all candidates
        self.assertEqual(tune.gen_maps({"seed": 3}, maps, 0), maps)     # default: every map
        seen = {p.stem for g in range(20) for p in tune.gen_maps(plan, maps, g)}
        self.assertTrue({"a", "a_p1", "b", "b_p1"} <= seen)

    def test_cmaes_backend_and_warm_start(self):
        import pickle
        import cma
        es = tune._CMAesLRA([0.5, 0.5], 0.2, 6)
        xs = es.ask()
        self.assertEqual(len(xs), 6)
        es.tell(xs, [sum(x) for x in xs])
        self.assertEqual(es.gen, 1)
        self.assertEqual(len(es.mean), 2)
        with tempfile.TemporaryDirectory() as t:
            src = Path(t)
            old_space = {"A": [0, 10], "B": [0, 1]}
            (src / "plan.json").write_text(json.dumps({"space": old_space}), encoding="utf8")
            old = cma.CMAEvolutionStrategy([0.3, 0.8], 0.2, {"bounds": [0, 1], "verbose": -9, "seed": 1})
            (src / "cma.pkl").write_bytes(pickle.dumps(old))
            space = {"A": [0, 20], "C": [0, 1]}              # A's range doubled; C is new
            x0, cov = tune.warm_start({"warm_from": str(src), "start": {"A": 0, "C": 0.25}}, space)
            self.assertAlmostEqual(x0[0], 0.15)              # A = 3.0 -> 3/20
            self.assertAlmostEqual(x0[1], 0.25)              # new parameter starts at plan start
            self.assertAlmostEqual(cov[0][0], old.sm.C[0][0] * 0.25)   # (10/20)^2
            self.assertAlmostEqual(cov[1][1], 1.0)
            # warm_mean "base": the base bot's values, the old run's covariance
            x0b, covb = tune.warm_start({"warm_from": str(src), "warm_mean": "base",
                                         "start": {"A": 5, "C": 0.25}}, space)
            self.assertAlmostEqual(x0b[0], 0.25)             # A = 5 (base) -> 5/20
            self.assertAlmostEqual(covb[0][0], cov[0][0])    # shape kept

    def test_generation_seeds(self):
        self.assertEqual(tune.gen_seeds({"seed": 7}, 3), [7])
        self.assertEqual(tune.gen_seeds({"seed": 7, "seeds_per_gen": 2}, 0), [7, 8])
        self.assertEqual(tune.gen_seeds({"seed": 7, "seeds_per_gen": 2}, 3), [13, 14])


if __name__ == "__main__":
    unittest.main()
