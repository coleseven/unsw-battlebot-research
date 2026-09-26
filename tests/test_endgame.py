import pathlib
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from bcsim import endgame
from bcsim.match import InProcessBot, play
from bcsim.paths import ROOT, bot_hash


class EndgameTest(unittest.TestCase):
    def test_cutoff_boundaries_and_frozen_movement(self):
        before = bot_hash(ROOT / "mybot")
        with tempfile.TemporaryDirectory() as tmp:
            for cutoff in endgame.CUTOFFS:
                path = endgame.make_variant(ROOT / "versions/v1", pathlib.Path(tmp) / str(cutoff), cutoff)
                self.assertEqual((path / "movement.py").read_bytes(), (ROOT / "versions/v1/brain.py").read_bytes())
                b = InProcessBot(path).new_brain("ID 0\nTEAM A\nMAP 16 16\nUNIT_LIMIT 64\n", 1)
                glob = b.turn.__func__.__globals__
                with patch.object(glob["reproduction"].Brain, "turn", return_value="SPLIT 4"), \
                     patch.object(glob["movement"].Brain, "turn", return_value="MOVE N"):
                    for round_ in (0, 199, 200, 299, 300, 399, 400, 449, 450, 499, 500):
                        expected = "MOVE N" if cutoff is not None and round_ >= cutoff else "SPLIT 4"
                        self.assertEqual(b.turn(SimpleNamespace(round=round_)), expected)
        self.assertEqual(bot_hash(ROOT / "mybot"), before)

    def test_invalid_cutoffs(self):
        for cutoff in (-1, 501, 1.5, True, "200"):
            with self.assertRaises(ValueError):
                endgame.make_variant(ROOT / "mybot", ROOT / "unused-invalid-destination", cutoff)

    def test_reference_equivalence_in_real_engine(self):
        with tempfile.TemporaryDirectory() as tmp:
            for cutoff, reference in ((None, ROOT / "opponents/splitter"), (0, ROOT / "versions/v1")):
                path = endgame.make_variant(ROOT / "versions/v1", pathlib.Path(tmp) / str(cutoff), cutoff)
                for m in ("arena", "Colosseum"):
                    expected = play(ROOT / "maps" / f"{m}.map", reference, ROOT / "opponents/hunter", 222).to_dict()
                    actual = play(ROOT / "maps" / f"{m}.map", path, ROOT / "opponents/hunter", 222).to_dict()
                    for key in ("bot_a", "hash_a", "seconds"):
                        expected.pop(key)
                        actual.pop(key)
                    self.assertEqual(actual, expected)

    def test_selection_tie_prefers_later_cutoff(self):
        candidates = [pathlib.Path(n) for n in ("perpetual", "stop_200", "stop_450")]
        games = [{"bot_a": p.name, "bot_b": "o", "winner": "A", "block": ["o", "m", 1]}
                 for p in candidates]
        self.assertEqual(endgame.select_candidate(games, candidates).name, "stop_450")

    def test_diagnostics_separate_endgame_and_elimination(self):
        games = [
            {"bot_a": "c", "bot_b": "o", "winner": "B", "reason": "length", "a_longest": 9},
            {"bot_a": "o", "bot_b": "c", "winner": "B", "reason": "length", "b_longest": 21},
            {"bot_a": "c", "bot_b": "o", "winner": "B", "reason": "elimination"},
            {"bot_a": "c", "bot_b": "o", "winner": None, "reason": "error", "error": "failed"},
        ]
        d = endgame.diagnostics(games, "c")
        self.assertEqual(d["games"], 3)
        self.assertEqual(d["errors"], 1)
        self.assertEqual(d["losses"], 2)
        self.assertEqual(d["length_losses"], 1)
        self.assertEqual(d["elimination_losses"], 1)
        self.assertEqual(d["mean_longest_in_length_decisions"], 15)


if __name__ == "__main__":
    unittest.main()
