"""Arena scoring, uncertainty, provenance and match statistics.

    .venv\\Scripts\\python -m unittest discover -s tests -v

The match tests play a handful of short real games (seconds); nothing here
runs a tournament or submits anything.
"""

import pathlib
import shutil
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from bcsim import arena, paths  # noqa: E402
from bcsim import replay as rp  # noqa: E402


def game(a, b, winner, map_="m", seed=0, error=None, block=None, **kw):
    g = {"map": map_, "bot_a": a, "bot_b": b, "seed": seed, "winner": winner,
         "reason": "error" if error else "length", "deaths": {}, "error": error}
    if block is not None:
        g["block"] = block
    g.update(kw)
    return g


class ScoreTest(unittest.TestCase):
    def test_score_for(self):
        self.assertEqual(arena.score_for(game("x", "y", "A"), "x"), 1.0)
        self.assertEqual(arena.score_for(game("x", "y", "A"), "y"), 0.0)
        self.assertEqual(arena.score_for(game("x", "y", None), "y"), 0.5)
        self.assertIsNone(arena.score_for(game("x", "y", None, error="boom"), "x"))
        self.assertIsNone(arena.score_for(game("x", "y", "A"), "z"))

    def test_errors_excluded_not_counted_as_draws(self):
        games = [game("me", "o", "A", seed=s, block=["o", "m", s]) for s in range(3)]
        games += [game("o", "me", None, seed=s, error="crash", block=["o", "m", s]) for s in range(3)]
        text = arena.summarize_eval(games, "me")
        row = next(l for l in text.splitlines() if l.startswith("| o |"))
        # 3 real games, all wins: 3-0-0, 100% win rate and score; 3 errors listed
        self.assertIn("| 3-0-0 | 100% | 100% |", row)
        self.assertTrue(row.rstrip().endswith("| 3 | 3 |"), row)
        self.assertIn("3 games errored and are excluded", text)
        self.assertIn("Fewer than 20 blocks for o", text)

    def test_score_vs_win_rate(self):
        t = arena.Tally()
        for i, s in enumerate([1.0, 0.5, 0.5, 0.0]):
            t.add(s, i)
        self.assertEqual((t.w, t.d, t.l), (1, 2, 1))
        self.assertAlmostEqual(t.win_rate, 0.25)
        self.assertAlmostEqual(t.score, 0.5)
        row = t.row("x")
        self.assertIn("| 1-2-1 | 25% | 50% |", row)

    def test_tournament_excludes_errors(self):
        games = [game("a", "b", "A", block=["a", "b", "m", 0]),
                 game("b", "a", "B", block=["a", "b", "m", 0]),
                 game("a", "b", None, seed=1, error="x", block=["a", "b", "m", 1])]
        text = arena.summarize_tournament(games, ["a", "b"])
        self.assertIn("1 games errored and are excluded", text)
        rows = {l.split("|")[2].strip(): l for l in text.splitlines() if l.startswith("| 1 ") or l.startswith("| 2 ")}
        self.assertIn("100%", rows["a"])
        self.assertIn("0%", rows["b"])
        ratings = arena.fit_elo([g for g in games if not arena.is_error(g)], ["a", "b"])
        self.assertGreater(ratings["a"], ratings["b"])


class BootstrapTest(unittest.TestCase):
    def test_deterministic_and_bounded(self):
        blocks = [[1.0, 0.0], [1.0, 1.0], [0.5, 0.0], [1.0, 0.5], [0.0, 0.0]] * 4
        lo, hi = arena.block_bootstrap(blocks)
        self.assertEqual((lo, hi), arena.block_bootstrap(blocks))
        mean = sum(map(sum, blocks)) / sum(map(len, blocks))
        self.assertLess(lo, mean)
        self.assertGreater(hi, mean)
        self.assertGreaterEqual(lo, 0.0)
        self.assertLessEqual(hi, 1.0)

    def test_pairing_matters(self):
        """Side-dependent outcomes (every map won as A, lost as B) are one
        coin flip per block, so blocks carry no side variance: the paired
        interval collapses onto 0.5, while treating the same games as
        independent would give a wide one."""
        paired = [[1.0, 0.0] for _ in range(20)]
        lo, hi = arena.block_bootstrap(paired)
        self.assertEqual((lo, hi), (0.5, 0.5))
        unpaired_lo, unpaired_hi = arena.block_bootstrap([[s] for b in paired for s in b])
        self.assertLess(unpaired_lo, 0.4)
        self.assertGreater(unpaired_hi, 0.6)

    def test_too_few_blocks(self):
        self.assertEqual(arena.block_bootstrap([[1.0, 1.0]]), (0.0, 1.0))
        self.assertEqual(arena.block_bootstrap([]), (0.0, 1.0))

    def test_eval_groups_both_sides_into_one_block(self):
        games = []
        for s in range(10):
            b = ["o", "m", s]
            games += [game("me", "o", "A", seed=s, block=b), game("o", "me", "A", seed=s, block=b)]
        t = arena.Tally()
        for g in games:
            t.add(arena.score_for(g, "me"), tuple(g["block"]))
        self.assertEqual(len(t.blocks), 10)
        self.assertEqual(t.ci(), (0.5, 0.5))


class ProvenanceTest(unittest.TestCase):
    def test_hash_mismatch_detected(self):
        prov = {"bots": {"me": {"hash": "aaa"}, "o": {"hash": "bbb"}}}
        ok = [game("me", "o", "A", hash_a="aaa", hash_b="bbb")]
        self.assertEqual(arena.check_hashes(ok, prov), [])
        bad = ok + [game("o", "me", "A", hash_a="bbb", hash_b="ccc")]
        warn = arena.check_hashes(bad, prov)
        self.assertEqual(len(warn), 1)
        self.assertIn("me", warn[0])

    def test_provenance_contents(self):
        bot = ROOT / "opponents" / "greedy"
        m = ROOT / "maps" / "arena.map"
        prov = arena.provenance([bot], [m], {"seeds": 2, "func": object()})
        self.assertEqual(prov["bots"]["greedy"]["hash"], paths.bot_hash(bot))
        self.assertIn("arena", prov["maps"])
        self.assertIn("engine", prov)
        self.assertNotIn("func", prov["settings"])


class MapTest(unittest.TestCase):
    def test_border_edge_twins_share_signature(self):
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            base = (ROOT / "maps" / "arena.map").read_text()
            lines = base.splitlines()
            w = int(next(l for l in lines if l.startswith("MAP ")).split()[1])
            # re-state a west-border kelp edge on its east-border twin
            west = next(l for l in lines if l.startswith("EDGE ") and l.split()[2] == "1"
                        and (int(l.split()[1]) // (w + 1)) % 2 == 1 and int(l.split()[1]) % (w + 1) == 0)
            idx = int(west.split()[1]) + w
            twin = base + f"\nEDGE {idx} 1 -1\n"
            (tmp / "a.map").write_text(base)
            (tmp / "b.map").write_text(twin.replace("MAP_NAME", "MAP_NAME Other #"))
            (tmp / "c.map").write_text(base.replace("TILE 1 1", "TILE 1 1 9 9 #", 1))
            self.assertEqual(paths.map_signature(tmp / "a.map"), paths.map_signature(tmp / "b.map"))
            self.assertNotEqual(paths.map_signature(tmp / "a.map"), paths.map_signature(tmp / "c.map"))
        finally:
            shutil.rmtree(tmp)

    def test_explicit_open_edges_ignored(self):
        """Server exports spell out open edges (`EDGE i 0 -1`) that bundled
        maps omit; they mean nothing to the engine."""
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            base = (ROOT / "maps" / "arena.map").read_text()
            (tmp / "a.map").write_text(base)
            (tmp / "b.map").write_text(base + "\nEDGE 129 0 -1\nEDGE 5 0 -1\n")
            self.assertEqual(paths.map_signature(tmp / "a.map"), paths.map_signature(tmp / "b.map"))
        finally:
            shutil.rmtree(tmp)

    def test_server_copies_of_bundled_maps_dropped(self):
        bundled = {paths.map_signature(b) for b in (ROOT / "maps").glob("*.map")}
        for s in (ROOT / "maps" / "server").glob("*.map"):
            if s.stem.lower() in {b.stem.lower() for b in (ROOT / "maps").glob("*.map")}:
                self.assertIn(paths.map_signature(s), bundled, s.name)
        names = [m.stem.lower() for m in paths.resolve_maps("all")]
        self.assertEqual(len(names), len(set(names)))

    def test_all_maps_deduplicated(self):
        maps = paths.resolve_maps("all")
        sigs = [paths.map_signature(m) for m in maps]
        self.assertEqual(len(sigs), len(set(sigs)))
        # bundled copies win over identical server copies
        for m in maps:
            if m.parent.name == "server":
                self.assertFalse(any(paths.map_signature(b) == paths.map_signature(m)
                                     for b in (ROOT / "maps").glob("*.map")))


class MatchStatsTest(unittest.TestCase):
    """Real (short) games: final stats must equal the engine's standings."""

    def test_longest_matches_engine_standings(self):
        from bcsim.match import engine, play
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            cases = [("arena", "splitter", "greedy"), ("Colosseum", "splitter", "turtle"),
                     ("default_small", "hunter", "splitter")]
            for m, a, b in cases:
                path = tmp / f"{m}.replay"
                r = play(ROOT / "maps" / f"{m}.map", ROOT / "opponents" / a, ROOT / "opponents" / b,
                         seed=1, replay_to=path)
                res = rp.decode(path.read_bytes()).result
                self.assertEqual((r.a_longest, r.b_longest),
                                 (res["a"]["longest"], res["b"]["longest"]), m)
                self.assertEqual((r.a_length, r.b_length), (res["a"]["total"], res["b"]["total"]), m)
                self.assertEqual((r.a_dragons, r.b_dragons), (res["a"]["dragons"], res["b"]["dragons"]), m)
                self.assertEqual(r.winner, res["winner"], m)
                self.assertEqual(r.hash_a, paths.bot_hash(ROOT / "opponents" / a))
                self.assertEqual(r.hash_b, paths.bot_hash(ROOT / "opponents" / b))
                if a != b:
                    self.assertNotEqual(r.hash_a, r.hash_b)
        finally:
            shutil.rmtree(tmp)

    def _scripted(self, root: pathlib.Path, name: str, turn_body: str) -> pathlib.Path:
        d = root / name
        d.mkdir()
        (d / "bot.toml").write_text('[project]\nlanguage = "py"\ninclude = [ "*.py" ]\n')
        shutil.copy2(ROOT / "framework" / "bc.py", d / "bc.py")
        (d / "brain.py").write_text("import bc\n\nclass Brain(bc.Brain):\n"
                                    "    def turn(self, obs):\n" + turn_body)
        return d

    def test_last_turn_length_change(self):
        """The final action changes a dragon's length, then the game ends
        (the opponent forfeits in the same round). Lengths seen before that
        action would be stale; the reported ones must be the final ones."""
        from bcsim.match import play
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            forfeit = self._scripted(tmp, "forfeit", "        return 'NOT_A_COMMAND'\n")
            sprint = self._scripted(tmp, "sprint", "        return 'MOVE ' + obs.facing * 2\n")
            split = self._scripted(tmp, "split", "        if obs.length >= 4:\n"
                                   "            return 'SPLIT 2'\n"
                                   "        return self.fallback(obs)\n")
            # arena.map: one length-3 dragon per side; team A (id 0) acts first
            r = play(ROOT / "maps" / "arena.map", sprint, forfeit)
            self.assertEqual((r.winner, r.rounds), ("A", 1))
            # a 2-step sprint costs a segment: seen 3 before the move, final 2
            self.assertEqual((r.a_longest, r.a_length, r.a_dragons), (2, 2, 1))

            # the same map with team A's dragon lengthened to 4, then it splits
            text = (ROOT / "maps" / "arena.map").read_text()
            text = text.replace("DRAGON 0 3 3 5 2 5 1 5", "DRAGON 0 4 3 5 2 5 1 5 0 5")
            m = tmp / "arena4.map"
            m.write_text(text)
            r = play(m, split, forfeit)
            self.assertEqual((r.winner, r.rounds), ("A", 1))
            # seen 4 before the split; final: parent 2 + child 2
            self.assertEqual((r.a_longest, r.a_length, r.a_dragons), (2, 4, 2))
        finally:
            shutil.rmtree(tmp)

    def test_errored_game_is_marked(self):
        from bcsim.match import play
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            bad = tmp / "bad.map"
            bad.write_text("MAP 3 3\nNONSENSE\n")
            r = play(bad, ROOT / "opponents" / "greedy", ROOT / "opponents" / "greedy")
            self.assertEqual(r.reason, "error")
            self.assertTrue(r.error)
            self.assertIsNone(arena.score_for(r.to_dict(), "greedy"))
        finally:
            shutil.rmtree(tmp)

    def test_job_reports_block_and_load_errors(self):
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            broken = tmp / "broken"
            broken.mkdir()
            (broken / "bot.toml").write_text('[project]\nlanguage = "py"\ninclude = [ "*.py" ]\n')
            (broken / "brain.py").write_text("this is not python(\n")
            d = arena._job((str(ROOT / "maps" / "arena.map"), str(broken),
                            str(ROOT / "opponents" / "greedy"), 0, None, ["greedy", "arena", 0]))
            self.assertTrue(arena.is_error(d))
            self.assertEqual(d["block"], ["greedy", "arena", 0])
        finally:
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
