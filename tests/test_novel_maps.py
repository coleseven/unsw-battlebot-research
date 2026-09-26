import pathlib
import tempfile
import unittest

from bcsim import novel_maps, reconstruct, trap_followup
from bcsim.paths import map_signature


class NovelMapsTest(unittest.TestCase):
    def test_reproducible_connected_symmetric_engine_accepted(self):
        signatures = set()
        with tempfile.TemporaryDirectory() as tmp:
            for spec in novel_maps.SPECS:
                text = novel_maps.generate(spec)
                self.assertEqual(text, novel_maps.generate(spec))
                path = pathlib.Path(tmp) / (spec[0] + ".map")
                path.write_text(text)
                trap_followup.validate_map(path)
                signatures.add(map_signature(path))
                board = reconstruct.Board(text)
                self.assertGreater(len(board.spawns), 0)
                for x, y in board.spawns:
                    self.assertIn((board.w - 1 - x, y), board.spawns)
                    self.assertIn((x, board.h - 1 - y), board.spawns)
                for (x, y), value in board.hedge.items():
                    self.assertEqual(board.hedge.get((board.w - 1 - x, y)), value)
                    self.assertEqual(board.hedge.get((x, (-y) % board.h)), value)
                for (x, y), value in board.vedge.items():
                    self.assertEqual(board.vedge.get(((-x) % board.w, y)), value)
                    self.assertEqual(board.vedge.get((x, board.h - 1 - y)), value)
            self.assertEqual(len(signatures), len(novel_maps.SPECS))


if __name__ == "__main__":
    unittest.main()
