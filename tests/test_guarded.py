import pathlib
import sys
import tempfile
import unittest

from bcsim.paths import ROOT
sys.path.insert(0, str(ROOT / "framework"))
import bc
import guarded_safety
import local_safety
from test_movement import board, edge


class GuardedTest(unittest.TestCase):
    def test_complete_body_order_and_fallback(self):
        o = board(length=3)
        o.occ[32] = ("A", 0, False, "W")
        self.assertEqual(guarded_safety.own_body(o), (24, 31, 32))
        o.length = 4
        self.assertIsNone(guarded_safety.own_body(o))
        o.length = 3
        edge(o, 32, "W", 4)
        self.assertIsNone(guarded_safety.own_body(o))

    def test_future_vacated_tail_is_traversable_not_current_tail(self):
        o = board(length=3, open_=False)
        o.occ[32] = ("A", 0, False, "W")
        for k, d in ((24, "E"), (25, "S"), (32, "W"), (31, "N")):
            edge(o, k, d, bc.OPEN)
        body = guarded_safety.own_body(o)
        self.assertEqual(body, (24, 31, 32))
        self.assertEqual(local_safety.View(o, "A").profile("E")["depth"], 0)
        self.assertEqual(guarded_safety.continuation(o, "E", body), 3)
        o.pearl[25] = True  # first move grows; tail is STILL occupied next turn
        self.assertEqual(guarded_safety.continuation(o, "E", body), 0)
        o.pearl[25] = False
        o.occ[32] = ("B", 1, False, "W")
        self.assertIsNone(guarded_safety.own_body(o))

    def test_head_guard_does_not_trade_safe_head_for_deeper_path(self):
        o = board(open_=False)
        edge(o, 24, "N", bc.OPEN)  # north is a cul-de-sac
        for k in (24, 25, 26, 27):
            edge(o, k, "E", bc.OPEN)
        o.occ[32] = ("B", 1, True, "N")
        edge(o, 32, "N", bc.OPEN)
        self.assertEqual(local_safety.choose(o, "A", "MOVE N", "trap"), "MOVE E")
        for mode in ("head_guard", "tail_guard", "food_guard"):
            self.assertEqual(guarded_safety.choose(o, "A", "MOVE N", mode), "MOVE N")
            self.assertEqual(guarded_safety.choose(o, "A", "SPLIT 4", mode), "SPLIT 4")

    def test_food_guard_preserves_pearl_unless_immediate_dead_end(self):
        o = board(open_=False)
        for k in (24, 17):
            edge(o, k, "N", bc.OPEN)
        for k in (24, 25, 26, 27):
            edge(o, k, "E", bc.OPEN)
        o.pearl[17] = True
        self.assertEqual(guarded_safety.choose(o, "A", "MOVE N", "head_guard"), "MOVE E")
        self.assertEqual(guarded_safety.choose(o, "A", "MOVE N", "food_guard"), "MOVE N")

    def test_tail_release_matches_four_real_engine_steps(self):
        from bcsim.match import engine
        # Two disjoint small body loops, no food or walls. A's first east step
        # vacates (4,4); the next south step can legally enter that old tail.
        text = ("MAP 11 11\nSYMMETRY xy\nMAP_NAME Tail_Test\nTILE_COUNT 0\n"
                "EDGE_COUNT 0\nDRAGON_COUNT 2\nDRAGON 0 3 3 3 3 4 4 4\n"
                "DRAGON 1 3 7 7 7 6 6 6\n")
        teams, seen, deaths = {}, [], []

        def spawn(did, data):
            teams[did] = bc.Init(data.decode()).team

        def reply(did, data):
            o = bc.Obs(data.decode())
            if teams[did] == "A":
                if o.round == 0:
                    self.assertEqual(guarded_safety.own_body(o), (24, 31, 32))
                    self.assertEqual(guarded_safety.continuation(o, "E", (24, 31, 32)), 3)
                seen.append(o.head)
                action = "MOVE " + "ESWN"[o.round % 4]
            else:
                action = "SUICIDE" if o.round >= 3 else "MOVE " + "WNES"[o.round % 4]
            return (action + "\nENDTURN\n").encode()

        result = engine().run(text.encode(), reply, lambda did, *args: deaths.append(did), spawn, lambda _: None, 0)
        self.assertEqual(seen[:4], [(3, 3), (4, 3), (4, 4), (3, 4)])
        self.assertEqual(result.winner, "A")
        self.assertTrue(all(teams[did] == "B" for did in deaths))


class BoundedRunnerTest(unittest.TestCase):
    def test_semantic_replay_map_verification(self):
        from bcsim.audit_jobs import verify_map
        mapfile = ROOT / "maps/arena.map"
        lines = mapfile.read_text().splitlines()
        # Keep MAP first: the normalizer uses dimensions while parsing edges.
        reordered = "\n".join([lines[0], *reversed(lines[1:])])
        # Dragon record order is meaningful, so preserve that order explicitly.
        dragons = [l for l in lines if l.startswith("DRAGON ")]
        reordered = "\n".join(l for l in reordered.splitlines() if not l.startswith("DRAGON "))
        reordered += "\n" + "\n".join(dragons)
        verify_map(mapfile, reordered)
        with self.assertRaises(AssertionError):
            verify_map(mapfile, reordered.replace("TILE 1 1 8 20", "TILE 1 1 9 20"))

    def test_worker_recycling_preserves_identical_results(self):
        from bcsim import bounded
        with tempfile.TemporaryDirectory() as tmp:
            job = (str(ROOT / "maps/arena.map"), str(ROOT / "mybot"),
                   str(ROOT / "opponents/greedy"), 123, None, ["greedy", "arena", 123])
            games = bounded.run([job, job], 1, pathlib.Path(tmp), batch_per_worker=1)
            self.assertNotEqual(games[0]["worker"]["pid"], games[1]["worker"]["pid"])
            for key in ("winner", "reason", "rounds", "a_length", "b_length", "hash_a", "hash_b", "deaths"):
                self.assertEqual(games[0][key], games[1][key], key)


if __name__ == "__main__":
    unittest.main()
