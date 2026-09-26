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


if __name__ == "__main__":
    unittest.main()
