"""The C++ port's data headers must stay generated from the Python source."""

import unittest

from bcsim import gen_cpp
from bcsim.paths import ROOT


class GenCppTest(unittest.TestCase):
    def test_headers_match_committed(self):
        # Python is the single source: the committed cppbot/*.hpp must equal a
        # fresh `python -m bcsim.gen_cpp`. If this fails, re-run gen_cpp.
        for name, text in (("params.hpp", gen_cpp.gen_params()),
                           ("model.hpp", gen_cpp.gen_model()),
                           ("portal_book.hpp", gen_cpp.gen_portal_book()),
                           ("hub_book.hpp", gen_cpp.gen_hub_book())):
            committed = (ROOT / "cppbot" / name).read_text(encoding="utf8")
            self.assertEqual(committed, text, f"cppbot/{name} is stale; run python -m bcsim.gen_cpp")

    def test_parity_param_present(self):
        import sys
        sys.path.insert(0, str(ROOT / "framework"))
        sys.modules.pop("core_params", None)
        import core_params
        self.assertFalse(core_params.PARITY, "PARITY must default to False for release play")


if __name__ == "__main__":
    unittest.main()
