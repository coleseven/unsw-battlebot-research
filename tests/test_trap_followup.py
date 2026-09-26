import pathlib
import tempfile
import unittest

from bcsim.paths import ROOT, map_signature
from bcsim.reconstruct import Board
from bcsim.trap_followup import arena_variant, validate_map


class ArenaVariantsTest(unittest.TestCase):
    def test_original_partitioned_map_is_not_rejected_as_a_generated_map(self):
        validate_map(ROOT / "maps/schooltime.map", require_connected=False)
        with self.assertRaises(ValueError):
            validate_map(ROOT / "maps/schooltime.map", require_connected=True)

    def test_maps_are_distinct_connected_and_engine_valid(self):
        source = (ROOT / "maps/arena.map").read_text()
        original = Board(source)
        with tempfile.TemporaryDirectory() as tmp:
            signatures = {map_signature(ROOT / "maps/arena.map")}
            for kind in ("baffles", "pockets", "slow_food"):
                p = pathlib.Path(tmp) / f"{kind}.map"
                p.write_text(arena_variant(source, kind))
                validate_map(p)
                signatures.add(map_signature(p))
                b = Board(p.read_text())
                self.assertEqual(b.dragons, original.dragons)
                self.assertEqual(b.spawns, original.spawns)
                if kind == "slow_food":
                    self.assertEqual((b.hedge, b.vedge), (original.hedge, original.vedge))
                else:
                    self.assertGreater(len(b.hedge) + len(b.vedge), len(original.hedge) + len(original.vedge))
            self.assertEqual(len(signatures), 4)


if __name__ == "__main__":
    unittest.main()
