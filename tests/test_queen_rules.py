"""Behavioral contract against the isolated official queen engine, not a mock."""
import unittest
import unswbc
from unswbc.engine import EngineModule
from bcsim import analyze, replay
from bcsim.margin import game_margin


def fixture(length=5, tiles=(), edges=(), bodies=None):
    if bodies is None:
        bodies = [(0, [(15-i, 2) for i in range(length)]),
                  (1, [(24+i, 7) for i in range(length)])]
    lines = ["MAP 40 10", "SYMMETRY xy", "MAP_NAME Queen fixture",
             f"TILE_COUNT {len(tiles)}"]
    lines += [f"TILE {x} {y} {lo} {hi}" for x, y, lo, hi in tiles]
    lines += [f"EDGE_COUNT {len(edges)}"] + list(edges)
    lines += [f"DRAGON_COUNT {len(bodies)}"]
    lines += [f"DRAGON {t} {len(b)} " + " ".join(f"{x} {y}" for x, y in b) for t, b in bodies]
    return ("\n".join(lines) + "\n").encode()


@unittest.skipUnless(unswbc.__version__ in ("1.2.3", "1.2.9"), "run via bcsim.queen_runtime")
class QueenEngineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = EngineModule()

    def run_game(self, m, policy):
        result = self.engine.run(m, lambda d, b: (policy(d, b.decode()) + "\nENDTURN\n").encode(),
                                 on_notice=lambda _: None)
        blob = self.engine.replay("a", "b")
        self.assertEqual(replay.read_result(blob)["winner"], result.winner)
        return result, replay.decode(blob), analyze.game_stats(blob)

    def first_action(self, length, path, **kwargs):
        return self.run_game(fixture(length, **kwargs), lambda d, _: "MOVE " + path if d == 0 else "")

    def test_free_step_boundaries_and_paid_step(self):
        for length in (4, 5, 8, 9, 12, 13):
            with self.subTest(length=length):
                free = (length + 3) // 4
                r, _, s = self.first_action(length, "E" * free)
                self.assertEqual(r.a_queen, length)
                self.assertEqual(s["teams"]["A"]["queen"]["length"], length)
                r, _, _ = self.first_action(length, "E" * (free + 1))
                self.assertEqual(r.a_queen, length - 1)

    def test_eating_does_not_increase_this_turn_allowance(self):
        r, _, s = self.first_action(4, "EE", tiles=[(16, 2, 1, 1), (23, 7, 1, 1)])
        self.assertEqual(r.a_queen, 4)  # +1 eaten, -1 second-step cost
        self.assertEqual(s["teams"]["A"]["pearls"], 1)

    def test_tail_collision_before_tail_moves(self):
        bodies = [(0, [(10, 2), (10, 3), (9, 3), (9, 2)]),
                  (1, [(29, 7), (29, 6), (30, 6), (30, 7)])]
        r, _, s = self.first_action(4, "W", bodies=bodies)
        self.assertEqual(r.a_queen, 0)
        self.assertEqual(s["teams"]["A"]["deaths"]["self"], 1)
        self.assertEqual(s["teams"]["A"]["queen"]["death_round"], 0)

    def test_split_retains_queen_and_child_acts_same_round(self):
        r, rep, s = self.run_game(fixture(8), lambda d, _: "SPLIT 6" if d == 0 else "MOVE W" if d == 2 else "")
        turns = [e[1] for e in rep.events if e[0] == replay.TURN_START]
        self.assertEqual(turns, [0, 1, 2])
        self.assertEqual((r.a_queen, r.a_longest), (2, 6))
        self.assertEqual(s["teams"]["A"]["queen"]["length"], 2)

    def test_queen_beats_large_surviving_child(self):
        bodies = [(0, [(15, 2), (14, 2)]),
                  (1, [(24+i, 7) for i in range(12)])]
        def policy(d, block):
            if d == 1:
                return "SPLIT 10" if block.startswith("ROUND 0\n") else ""
            return "MOVE S" if d == 2 and block.startswith("ROUND 0\n") else "MOVE E"
        r, _, s = self.run_game(fixture(bodies=bodies), policy)
        self.assertEqual((r.rounds, r.winner, r.a_queen, r.b_queen), (499, "A", 2, 0))
        self.assertEqual(r.b_longest, 10)
        self.assertEqual(s["teams"]["B"]["queen"]["death_round"], 1)
        self.assertEqual(game_margin(s, "A")["wins"], 1)
        self.assertEqual(game_margin(s, "B")["wins"], -1)

    def test_equal_queens_fall_through_to_longest(self):
        bodies = [(0, [(15-i, 2) for i in range(4)]),
                  (1, [(24+i, 7) for i in range(8)])]
        def policy(d, block):
            if d == 1 and block.startswith("ROUND 0\n"):
                return "SPLIT 6"
            if d == 2:
                return "MOVE S" if block.startswith("ROUND 0\n") else "MOVE E"
            return "MOVE E" if d == 0 else "MOVE W"
        # A sheds two segments in a paid move, B splits down to two.
        def wrapped(d, b):
            return "MOVE EEE" if d == 0 and b.startswith("ROUND 0\n") else policy(d, b)
        r, _, _ = self.run_game(fixture(bodies=bodies), wrapped)
        self.assertEqual((r.a_queen, r.b_queen, r.winner), (2, 2, "B"))


if __name__ == "__main__":
    unittest.main()
