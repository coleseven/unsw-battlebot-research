import sys
import types
import unittest

from bcsim import official_suite, reconstruct
from bcsim.paths import ROOT

sys.path.insert(0, str(ROOT / "framework"))
import core_memory
import core_params
import v6_portal_book


class PortalBookTest(unittest.TestCase):
    def test_book_crossings_match_engine_geometry(self):
        checked = 0
        for path in official_suite.official_maps():
            board = reconstruct.Board(path.read_text(encoding="utf8"))
            w, h, n = board.w, board.h, board.w * board.h
            for pid, ends in board.portals.items():
                for kind, (x, y) in ends:
                    key = y * w + x + (n if kind == "v" else 0)
                    mem = core_memory.WorldMemory(w, h, core_params)
                    mem.nav.remember(key, pid)   # this dragon saw one end only
                    mem.apply_book()
                    # step across the seen end from both of its sides
                    if kind == "h":
                        moves = [((x, y), "N"), ((x, (y - 1) % h), "S")]
                    else:
                        moves = [((x, y), "W"), (((x - 1) % w, y), "E")]
                    for (cx, cy), d in moves:
                        got = mem.nav.destination(cy * w + cx, d)
                        want = board.dest(cx, cy, d)
                        self.assertEqual(got, want[1] * w + want[0], (path.stem, pid, d))
                        checked += 1
        self.assertGreater(checked, 0)

    def test_mismatched_id_is_ignored(self):
        w, h = 48, 24
        mem = core_memory.WorldMemory(w, h, core_params)
        key = v6_portal_book.BOOK[(w, h)][0][0][0]
        mem.nav.remember(key, 99)            # a portal id no book map has here
        mem.apply_book()
        self.assertEqual(len(mem.nav.ends[99]), 1)

    def test_book_off_by_parameter(self):
        params = types.SimpleNamespace(**{k: getattr(core_params, k) for k in dir(core_params)
                                          if k.isupper()})
        params.PORTAL_BOOK = False
        mem = core_memory.WorldMemory(48, 24, params)
        self.assertEqual(mem.book, ())


if __name__ == "__main__":
    unittest.main()
