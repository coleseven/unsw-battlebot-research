"""bcsim.sync and freeze: frozen versions stay frozen; snapshots are complete.

    .venv\\Scripts\\python -m unittest discover -s tests -v
"""

import pathlib
import shutil
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from bcsim import arena, paths, sync  # noqa: E402

TOML = '[project]\nlanguage = "py"\ninclude = [ "*.py" ]\n'


def make_bot(d: pathlib.Path, brain: str, **extra: str) -> pathlib.Path:
    d.mkdir(parents=True)
    (d / "bot.toml").write_text(TOML)
    (d / "main.py").write_text("import bc\nimport brain\nbc.run(brain.Brain)\n")
    (d / "brain.py").write_text(brain)
    for name, text in extra.items():
        (d / name).write_text(text)
    return d


SIMPLE_BRAIN = "import bc\n\nclass Brain(bc.Brain):\n    def turn(self, obs):\n        return 'MOVE N'\n"


class SyncTest(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.fw = self.tmp / "framework"
        self.fw.mkdir()
        shutil.copy2(ROOT / "framework" / "bc.py", self.fw / "bc.py")
        (self.fw / "tactics.py").write_text("NEW_TACTICS = 1\n")
        (self.fw / "features.py").write_text("NEW_FEATURES = 1\n")
        self.root = self.tmp / "proj"
        make_bot(self.root / "mybot", SIMPLE_BRAIN, **{"bc.py": "OLD\n", "features.py": "OLD\n"})
        make_bot(self.root / "opponents" / "foo", SIMPLE_BRAIN, **{"bc.py": "OLD\n"})
        make_bot(self.root / "versions" / "v1", SIMPLE_BRAIN, **{"bc.py": "FROZEN\n", "tactics.py": "FROZEN\n"})
        # a non-framework bot (no brain.py) is left alone too
        (self.root / "opponents" / "cpp").mkdir()
        (self.root / "opponents" / "cpp" / "bot.toml").write_text(TOML)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_versions_untouched(self):
        done = sync.sync(self.root, self.fw)
        self.assertEqual(sorted(p.name for p in done), ["foo", "mybot"])
        v1 = self.root / "versions" / "v1"
        self.assertEqual((v1 / "bc.py").read_text(), "FROZEN\n")
        self.assertEqual((v1 / "tactics.py").read_text(), "FROZEN\n")
        self.assertFalse((self.root / "opponents" / "cpp" / "bc.py").exists())

    def test_live_bots_updated(self):
        sync.sync(self.root, self.fw)
        mybot = self.root / "mybot"
        self.assertEqual((mybot / "bc.py").read_bytes(), (self.fw / "bc.py").read_bytes())
        self.assertEqual((mybot / "tactics.py").read_text(), "NEW_TACTICS = 1\n")
        # optional modules refresh only where a bot already uses them
        self.assertEqual((mybot / "features.py").read_text(), "NEW_FEATURES = 1\n")
        self.assertFalse((self.root / "opponents" / "foo" / "features.py").exists())

    def test_keep_tactics(self):
        (self.root / "opponents" / "foo" / "tactics.py").write_text("MINE\n")
        sync.sync(self.root, self.fw, keep_tactics={"foo"})
        self.assertEqual((self.root / "opponents" / "foo" / "tactics.py").read_text(), "MINE\n")

    def test_sync_targets_exclude_versions(self):
        names = [p.parent.name + "/" + p.name for p in paths.sync_targets(self.root)]
        self.assertNotIn("versions/v1", names)
        self.assertIn("versions/v1", [p.parent.name + "/" + p.name for p in paths.bot_dirs(self.root)])


class FreezeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.fw = self.tmp / "framework"
        self.fw.mkdir()
        shutil.copy2(ROOT / "framework" / "bc.py", self.fw / "bc.py")
        (self.fw / "helpers2.py").write_text("import bc\nVALUE = 7\n")
        (self.fw / "tactics.py").write_text("import helpers2\n")
        self.versions = self.tmp / "versions"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_pulls_in_missing_dependencies_transitively(self):
        brain = "import bc\nimport tactics\n\nclass Brain(bc.Brain):\n    def turn(self, obs):\n        return 'MOVE N'\n"
        src = make_bot(self.tmp / "mybot", brain, **{"bc.py": (self.fw / "bc.py").read_text()})
        (src / ".unswbc-build").mkdir()
        (src / ".unswbc-build" / "junk.py").write_text("x")
        (src / "__pycache__").mkdir()
        (src / "__pycache__" / "brain.cpython-314.pyc").write_bytes(b"x")
        dst = arena.freeze(src, self.versions, framework=self.fw)
        self.assertEqual(dst.name, "v1")
        for name in ("bc.py", "brain.py", "main.py", "bot.toml", "tactics.py", "helpers2.py"):
            self.assertTrue((dst / name).is_file(), name)
        self.assertFalse((dst / ".unswbc-build").exists())
        self.assertFalse((dst / "__pycache__").exists())
        note = (dst / "FROZEN.txt").read_text()
        self.assertIn("tactics.py", note)
        self.assertIn(paths.bot_hash(dst), note)
        # FROZEN.txt is not part of the bot's identity
        self.assertEqual(paths.bot_hash(dst), paths.bot_hash(dst))
        # the snapshot runs on its own
        from bcsim.match import InProcessBot
        InProcessBot(dst).new_brain("ID 0\nTEAM A\nMAP 16 16\nUNIT_LIMIT 64\n", seed=0)
        self.assertEqual(arena.freeze(src, self.versions, framework=self.fw).name, "v2")

    def test_unknown_import_refused(self):
        brain = "import bc\nimport nosuchmodule\n\nclass Brain(bc.Brain):\n    pass\n"
        src = make_bot(self.tmp / "mybot", brain, **{"bc.py": (self.fw / "bc.py").read_text()})
        with self.assertRaises(SystemExit):
            arena.freeze(src, self.versions, framework=self.fw)
        self.assertEqual([p for p in self.versions.iterdir()], [])

    def test_broken_bot_refused(self):
        brain = "import bc\n\nclass Brain(bc.Brain):\n    def __init__(self, *a, **k):\n        raise RuntimeError('boom')\n"
        src = make_bot(self.tmp / "mybot", brain, **{"bc.py": (self.fw / "bc.py").read_text()})
        with self.assertRaises(SystemExit):
            arena.freeze(src, self.versions, framework=self.fw)
        self.assertEqual([p for p in self.versions.iterdir()], [])

    def test_stale_framework_copy_noted(self):
        src = make_bot(self.tmp / "mybot", SIMPLE_BRAIN,
                       **{"bc.py": (self.fw / "bc.py").read_text() + "\n# local tweak\n"})
        dst = arena.freeze(src, self.versions, framework=self.fw)
        self.assertIn("differs from framework", (dst / "FROZEN.txt").read_text())
        self.assertIn("# local tweak", (dst / "bc.py").read_text())


class HashTest(unittest.TestCase):
    def test_hash_tracks_content_and_ignores_caches(self):
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            bot = make_bot(tmp / "b", SIMPLE_BRAIN)
            h1 = paths.bot_hash(bot)
            (bot / "__pycache__").mkdir()
            (bot / "__pycache__" / "x.pyc").write_bytes(b"1")
            (bot / "FROZEN.txt").write_text("note")
            self.assertEqual(paths.bot_hash(bot), h1)
            (bot / "brain.py").write_text(SIMPLE_BRAIN + "# change\n")
            self.assertNotEqual(paths.bot_hash(bot), h1)
        finally:
            shutil.rmtree(tmp)

    def test_inprocess_hash_matches_dir_hash(self):
        from bcsim.match import InProcessBot
        for name in ("greedy", "splitter"):
            bot = ROOT / "opponents" / name
            self.assertEqual(InProcessBot(bot).hash, paths.bot_hash(bot))


if __name__ == "__main__":
    unittest.main()
