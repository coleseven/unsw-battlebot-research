import unittest

from bcsim import official_suite


class OfficialSuiteTest(unittest.TestCase):
    def test_exact_eleven_distinct_maps_and_dimensions(self):
        paths = official_suite.official_maps()
        self.assertEqual(len(paths), 11)
        self.assertEqual(
            [(p.stem, official_suite.dimensions(p)) for p in paths],
            [(name, (width, height)) for name, _, width, height
             in official_suite.SPECS],
        )
        official_suite.require_coverage(paths)

    def test_missing_or_duplicate_map_is_rejected(self):
        paths = official_suite.official_maps()
        with self.assertRaises(ValueError):
            official_suite.require_coverage(paths[:-1])
        with self.assertRaises(ValueError):
            official_suite.require_coverage(paths[:-1] + [paths[0]])


if __name__ == "__main__":
    unittest.main()
