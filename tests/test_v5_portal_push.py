import pathlib
import tempfile
import unittest

from bcsim import v5_initial
from bcsim.match import InProcessBot
from test_movement import board, edge


class V5PortalPushTest(unittest.TestCase):
    def make(self):
        temp = tempfile.TemporaryDirectory()
        bot = v5_initial.variant(pathlib.Path(temp.name) / "bot", True, True,
                                 portal_push=True)
        brain = InProcessBot(bot).new_brain(
            "ID 2\nTEAM A\nMAP 48 24\nUNIT_LIMIT 64\n", 0)
        return temp, brain

    def test_sparse_explorer_and_visible_portal_entry(self):
        temp, brain = self.make()
        try:
            module = brain.turn.__func__.__globals__["v5_portal_push"]
            model = brain.turn.__func__.__globals__["action_model"].MODEL
            obs = board(length=3)
            obs.round = 30
            obs.x = [(10 + k % 7 - 3) % 48 for k in range(49)]
            obs.y = [(0 + k // 7 - 3) % 24 for k in range(49)]
            edge(obs, 24, "E", 0)
            self.assertTrue(module.explorer("A", 2))
            self.assertFalse(module.explorer("A", 3))
            self.assertEqual(module.pocket_route(brain.init, obs, "A", 2,
                                                 model, "MOVE N"), "MOVE E")
            obs.occ[26] = ("A", 9, False, "N")
            edge(obs, 25, "E", 0)
            self.assertNotEqual(module.pocket_route(brain.init, obs, "A", 2,
                                                    model, "MOVE N"), "MOVE E")
        finally:
            temp.cleanup()


if __name__ == "__main__":
    unittest.main()
