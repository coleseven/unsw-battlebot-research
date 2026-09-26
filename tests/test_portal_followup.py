import pathlib
import tempfile
import unittest

from bcsim import portal_followup as f, reconstruct, trap_followup
from bcsim.paths import map_signature


class PortalFollowupTest(unittest.TestCase):
    def test_generated_maps(self):
        signatures = set()
        with tempfile.TemporaryDirectory() as tmp:
            for spec in f.SPECS:
                text = f.generate(spec)
                self.assertEqual(text, f.generate(spec))
                board = reconstruct.Board(text)
                self.assertTrue(f.connected(board))
                self.assertEqual(len(board.portals), spec[-1])
                self.assertTrue(all(len(p) == 2 and p[0][0] == p[1][0] for p in board.portals.values()))
                # Reflection maps portal destinations as well as ordinary edges.
                for x in range(board.w):
                    for y in range(board.h):
                        for d in "NESW":
                            dest = board.dest(x, y, d)
                            for axis in "xy":
                                def mirror(p):
                                    if p is None:
                                        return None
                                    a, b = p
                                    return (board.w-1-a, b) if axis == "x" else (a, board.h-1-b)
                                reflected_d = ({"E": "W", "W": "E"} if axis == "x" else {"N": "S", "S": "N"}).get(d, d)
                                self.assertEqual(mirror(dest), board.dest(*mirror((x, y)), reflected_d))
                path = pathlib.Path(tmp) / (spec[0] + ".map")
                path.write_text(text)
                trap_followup.validate_map(path)
                signatures.add(map_signature(path))
        self.assertEqual(len(signatures), 8)

    def test_no_portal_equivalence_guard(self):
        a = {"map": "m", "bot_a": "control_450", "bot_b": "reference_v2", "block": ["reference_v2", "m", 1], "winner": "A"}
        b = {**a, "bot_a": "portal_escape"}
        self.assertEqual(f.unchanged_no_portal([a, b], ["m"]), 1)
        b["winner"] = "B"
        with self.assertRaises(AssertionError):
            f.unchanged_no_portal([a, b], ["m"])


if __name__ == "__main__":
    unittest.main()
