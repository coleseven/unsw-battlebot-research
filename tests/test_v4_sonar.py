import pathlib
import tempfile
import unittest

from bcsim import v4_sonar
from bcsim.match import InProcessBot
from bcsim.paths import ROOT
from test_movement import board


class V4SonarTest(unittest.TestCase):
    def test_packet_roundtrip_rejects_noise_and_wrong_team(self):
        with tempfile.TemporaryDirectory() as tmp:
            bot = v4_sonar.make_candidate(pathlib.Path(tmp) / "beacon", "beacon")
            brain = InProcessBot(bot).new_brain("ID 5\nTEAM A\nMAP 64 64\nUNIT_LIMIT 64\n", 0)
            codec = brain.turn.__func__.__globals__["v4_sonar"]
            p = codec.encode("A", 17, 38, 12)
            self.assertEqual(codec.decode(p, "A", 64, 64), (17, 38, 12))
            self.assertIsNone(codec.decode(p, "B", 64, 64))
            self.assertIsNone(codec.decode(p ^ 1, "A", 64, 64))
            self.assertIsNone(codec.decode(0, "A", 64, 64))

    def test_beacon_position_and_route_bias(self):
        with tempfile.TemporaryDirectory() as tmp:
            bot = v4_sonar.make_candidate(pathlib.Path(tmp) / "route", "route")
            brain = InProcessBot(bot).new_brain("ID 5\nTEAM A\nMAP 7 7\nUNIT_LIMIT 64\n", 0)
            codec = brain.turn.__func__.__globals__["v4_sonar"]
            obs = board(length=6)
            obs.round = 450
            action = brain.turn(obs)
            self.assertTrue(action.startswith("MOVE "))
            self.assertTrue(any(x.startswith("SONAR ") for x in brain.extra))
            packet = int(brain.extra[-1].split()[1])
            k = obs.step(24, action[-1])
            self.assertEqual(codec.decode(packet, "A", 7, 7)[:2], (obs.x[k], obs.y[k]))
            obs.length, obs.unit_count = 2, 20
            obs.msgs = [codec.encode("A", 5, 3, 12)]
            obs.round = 460
            brain.extra = []
            brain.turn(obs)
            self.assertEqual(brain.target[:3], (5, 3, 12))
            self.assertEqual(codec.routed_move(obs, "A", brain.turn.__func__.__globals__["action_model"].MODEL,
                                               (5, 3), 7, 7), "MOVE E")


if __name__ == "__main__":
    unittest.main()
