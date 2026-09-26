import unittest

from bcsim import feed_trace, replay


class FeedTraceTest(unittest.TestCase):
    def test_own_corpse_pearl_reaches_final_king(self):
        map_text = "MAP 5 5\nMAP_NAME test\nDRAGON 0 2 1 1 1 2\nDRAGON 0 2 2 1 2 2\n"
        events = [
            (replay.ROUND_START, 400),
            (replay.TURN_START, 0),
            (replay.DRAGON_ACTION, 0, ("suicide",), None, False, False),
            (replay.DRAGON_DEATH, 0, "A"),
            (replay.TILE_CHANGE, 1, 1, True),
            (replay.TURN_START, 1),
            (replay.DRAGON_ACTION, 1, ("move", "W"), None, False, False),
            (replay.TILE_CHANGE, 1, 1, False),
            (replay.DRAGON_UPDATE, 1, "W", (1, 1), (2, 2)),
        ]
        r = replay.Replay(0, map_text, "ours", "theirs", events,
                          {"winner": "A", "end_reason": "round_limit"})
        result = feed_trace.trace(r)
        self.assertEqual(result["teams"]["A"]["king_late_pearls"], {"own_corpse": 1})
        self.assertEqual(result["teams"]["A"]["king_late_own_corpse_fraction"], 1)
        self.assertEqual(result["teams"]["A"]["king_late_own_no_action_corpse"], 1)
        self.assertEqual(result["checks"]["corpse_pearls_created"], 1)

    def test_natural_spawn_is_not_a_corpse(self):
        map_text = "MAP 5 5\nMAP_NAME test\nDRAGON 0 2 2 1 2 2\n"
        events = [(replay.ROUND_START, 400), (replay.TILE_CHANGE, 1, 1, True),
                  (replay.TURN_START, 0),
                  (replay.DRAGON_ACTION, 0, ("move", "W"), None, False, False),
                  (replay.TILE_CHANGE, 1, 1, False),
                  (replay.DRAGON_UPDATE, 0, "W", (1, 1), (2, 2))]
        r = replay.Replay(0, map_text, "ours", "theirs", events,
                          {"winner": "A", "end_reason": "round_limit"})
        result = feed_trace.trace(r)
        self.assertEqual(result["teams"]["A"]["king_late_pearls"], {"spawn": 1})


if __name__ == "__main__":
    unittest.main()
