"""The in-process C++ loader (BCSIM_CPP_INPROC) must match the process build
byte-for-byte and keep dragons isolated from one another."""

import hashlib
import os
import pathlib
import shutil
import tempfile
import unittest

from bcsim import match, reconstruct
from bcsim import replay as rp
from bcsim.paths import ROOT

HAVE_CXX = shutil.which("clang++") or shutil.which("g++")
V7 = ROOT / "versions/v7-base"
SPLITTER = ROOT / "opponents/splitter"
SMALL = ROOT / "maps/default_small.map"


@unittest.skipUnless(HAVE_CXX and V7.is_dir(), "needs a C++ compiler and versions/v7-base")
class InProcTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Deterministic Python opponents: their wall-clock search budget would
        # otherwise make the reference (process) and in-process games differ
        # under CPU load -- that is the opponent's nondeterminism, not ours.
        os.environ["BCSIM_DETERMINISTIC_V6"] = "1"
        match.build_cpp_lib(V7)  # build the shared library once
        cls.tmp = pathlib.Path(tempfile.mkdtemp())

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def _play(self, inproc, seed=1):
        os.environ["BCSIM_CPP_INPROC"] = "1" if inproc else "0"
        out = self.tmp / f"{'in' if inproc else 'pr'}.replay"
        r = match.play(SMALL, V7, SPLITTER, seed=seed, replay_to=out)
        return r, hashlib.sha256(out.read_bytes()).hexdigest()

    def test_game_matches_process_build(self):
        rp_, hp = self._play(False)
        ri, hi = self._play(True)
        self.assertEqual(rp_.winner, ri.winner)
        self.assertEqual(rp_.rounds, ri.rounds)
        self.assertEqual((rp_.a_length, rp_.b_length), (ri.a_length, ri.b_length))
        self.assertEqual(rp_.deaths, ri.deaths)
        self.assertEqual(hp, hi, "replay bytes differ between in-process and process build")
        self.assertEqual(rp_.hash_a, ri.hash_a, "bot identity hash must not change")

    def test_dragon_isolation(self):
        # Drive two handles interleaved and confirm each dragon's replies match
        # running it alone: proves no state leaks between handles.
        os.environ["BCSIM_CPP_INPROC"] = "1"
        out = self.tmp / "iso.replay"
        match.play(SMALL, V7, SPLITTER, seed=2, replay_to=out)
        turns = list(reconstruct.turns(rp.load(out)))
        board = reconstruct.Board(rp.load(out).map_text)
        by_id: dict[int, list] = {}
        for t in turns:
            by_id.setdefault(t.id, []).append(t)
        ids = [i for i in by_id if len(by_id[i]) >= 3][:2]
        self.assertEqual(len(ids), 2, "need two dragons with enough turns")
        lib = match._load_cpp_lib(V7)

        def init_of(t):
            return f"ID {t.id}\nTEAM {t.team}\nMAP {board.w} {board.h}\nUNIT_LIMIT 64\n".encode()

        def run_alone(did):
            d = match._CppDragon(lib, init_of(by_id[did][0]))
            acts = [d.ask(t.block.encode()) for t in by_id[did]]
            d.stop()
            return acts

        alone = {i: run_alone(i) for i in ids}
        # interleave the two dragons round by round on fresh handles
        d0 = match._CppDragon(lib, init_of(by_id[ids[0]][0]))
        d1 = match._CppDragon(lib, init_of(by_id[ids[1]][0]))
        inter = {ids[0]: [], ids[1]: []}
        for a, b in zip(by_id[ids[0]], by_id[ids[1]]):
            inter[ids[0]].append(d0.ask(a.block.encode()))
            inter[ids[1]].append(d1.ask(b.block.encode()))
        d0.stop(); d1.stop()
        for i in ids:
            n = len(inter[i])
            self.assertEqual(alone[i][:n], inter[i], f"dragon {i} diverged when interleaved")


if __name__ == "__main__":
    unittest.main()
