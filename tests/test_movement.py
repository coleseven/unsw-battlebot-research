import pathlib
import sys
import tempfile
import unittest

from bcsim import movement, endgame, replay
from bcsim.match import InProcessBot, play, engine
from bcsim.paths import ROOT, bot_hash

sys.path.insert(0, str(ROOT / "framework"))
import bc
import local_safety


def board(length=5, open_=True):
    o = bc.Obs.__new__(bc.Obs)
    o.round, o.facing, o.length, o.unit_count = 460, "N", length, 1
    o.msgs, o.bodies = [], []
    o.x, o.y = [k % 7 for k in range(49)], [k // 7 for k in range(49)]
    o.pearl, o.pearl_in = [False] * 49, [-1] * 49
    o.occ = [None] * 49
    o.occ[24] = ("A", 0, True, "N")
    o.occ[31] = ("A", 0, False, "N")
    edge = bc.OPEN if open_ else bc.KELP
    o.hedge = [[edge] * 7 for _ in range(8)]
    o.vedge = [[edge] * 8 for _ in range(7)]
    return o


def edge(o, k, direction, value):
    r, c = divmod(k, 7)
    if direction == "N":
        o.hedge[r][c] = value
    elif direction == "S":
        o.hedge[r + 1][c] = value
    elif direction == "W":
        o.vedge[r][c] = value
    else:
        o.vedge[r][c + 1] = value


class GeometryTest(unittest.TestCase):
    def test_each_sprint_step_checked(self):
        o = board()
        self.assertIsNotNone(local_safety.View(o, "A").profile("NE"))
        edge(o, 17, "E", bc.KELP)
        self.assertIsNone(local_safety.View(o, "A").profile("NE"))
        edge(o, 17, "E", 3)  # portal destination is not assumed safe
        self.assertIsNone(local_safety.View(o, "A").profile("NE"))
        edge(o, 17, "E", bc.OPEN)
        o.occ[18] = ("B", 1, False, "S")
        self.assertIsNone(local_safety.View(o, "A").profile("NE"))

    def test_body_tail_revisit_and_cost(self):
        o = board(length=2)
        v = local_safety.View(o, "A")
        self.assertIsNone(v.profile("NN"))
        self.assertIsNone(v.profile("S"))
        self.assertIsNone(v.profile("NS"))
        o.length = 3
        self.assertIsNotNone(local_safety.View(o, "A").profile("NN"))
        self.assertIsNone(local_safety.View(o, "A").profile("NNN"))
        o.length = 10
        self.assertIsNone(local_safety.View(o, "A").profile("NESW"))

    def test_trap_override_and_keep_safe_original(self):
        o = board(open_=False)
        edge(o, 24, "N", bc.OPEN)  # north dead end
        for k in (24, 25, 26, 27):
            edge(o, k, "E", bc.OPEN)  # east corridor to unknown boundary
        self.assertLess(local_safety.View(o, "A").profile("N")["score"], -15)
        self.assertEqual(local_safety.choose(o, "A", "MOVE N", "trap"), "MOVE E")
        self.assertEqual(local_safety.choose(o, "A", "MOVE E", "trap"), "MOVE E")
        self.assertEqual(local_safety.choose(board(), "A", "MOVE N", "trap"), "MOVE N")

    def test_sprint_only_in_emergency(self):
        o = board()
        self.assertEqual(local_safety.choose(o, "A", "MOVE N", "sprint"), "MOVE N")
        # Only east is open, threatened by a head south of that cell. EE ends
        # beyond the threat and has open room; the enemy cannot interrupt it.
        edge(o, 24, "N", bc.KELP)
        edge(o, 24, "W", bc.KELP)
        o.occ[32] = ("B", 1, True, "N")
        result = local_safety.choose(o, "A", "MOVE E", "sprint")
        self.assertEqual(len(result.split()[1]), 2)
        self.assertEqual(result.split()[1][0], "E")
        self.assertGreaterEqual(local_safety.View(o, "A").profile(result.split()[1])["score"], 0)
        o.length = 2
        self.assertEqual(local_safety.choose(o, "A", "MOVE E", "sprint"), "MOVE E")

    def test_split_and_boxed_in_unchanged(self):
        for mode in ("trap", "sprint"):
            self.assertEqual(local_safety.choose(board(), "A", "SPLIT 4", mode), "SPLIT 4")
            self.assertEqual(local_safety.choose(board(open_=False), "A", "MOVE N", mode), "MOVE N")


class WrapperTest(unittest.TestCase):
    def test_accepted_two_step_paths_survive_real_engine(self):
        accepted = []
        for d1 in bc.DIRS:
            for d2 in bc.DIRS:
                path = d1 + d2
                teams, checked = {}, []

                def spawn(did, init):
                    teams[did] = bc.Init(init.decode()).team

                def reply(did, block):
                    if teams[did] == "B":
                        return b"NOT_A_COMMAND\nENDTURN\n"  # end after A's first action
                    obs = bc.Obs(block.decode())
                    legal = local_safety.View(obs, "A").profile(path) is not None
                    checked.append(legal)
                    return ("MOVE " + (path if legal else obs.facing) + "\nENDTURN\n").encode()

                result = engine().run((ROOT / "maps/arena.map").read_bytes(), reply,
                                      lambda *a: None, spawn, lambda *a: None, 0)
                if checked and checked[0]:
                    accepted.append(path)
                    self.assertGreater(result.a_dragons, 0, path)
                    self.assertGreaterEqual(result.a_length, 2, path)
        self.assertGreaterEqual(len(accepted), 3)

    def test_frozen_baseline_and_real_matches(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            source = endgame.make_variant(ROOT / "versions/v1", root / "control", 450)
            before = bot_hash(source)
            for mode in ("trap", "sprint"):
                candidate = movement.make_variant(source, root / mode, mode)
                for name in ("movement.py", "reproduction.py", "endgame_config.py", "tactics.py"):
                    self.assertEqual((candidate / name).read_bytes(), (source / name).read_bytes())
                brain = InProcessBot(candidate).new_brain("ID 0\nTEAM A\nMAP 16 16\nUNIT_LIMIT 64\n", 0)
                o = board(length=8)
                o.round = 100
                self.assertEqual(brain.turn(o), "SPLIT 4")
                o.round = 450
                self.assertTrue(brain.turn(o).startswith("MOVE "))
                result = play(ROOT / "maps/arena.map", candidate, ROOT / "opponents/splitter", 987,
                              replay_to=root / f"{mode}.replay")
                self.assertIsNone(result.error)
                self.assertNotIn("A:A", result.deaths)
                r = replay.load(root / f"{mode}.replay")
                self.assertFalse(any(e[0] == replay.DRAGON_ACTION and (e[4] or e[5]) for e in r.events))
            self.assertEqual(bot_hash(source), before)


if __name__ == "__main__":
    unittest.main()
