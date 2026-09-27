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

    def test_generation_seeds(self):
        self.assertEqual(tune.gen_seeds({"seed": 7}, 3), [7])
        self.assertEqual(tune.gen_seeds({"seed": 7, "seeds_per_gen": 2}, 0), [7, 8])
        self.assertEqual(tune.gen_seeds({"seed": 7, "seeds_per_gen": 2}, 3), [13, 14])


if __name__ == "__main__":
    unittest.main()
