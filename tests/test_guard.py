import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from bcsim import guard


class GuardTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.lock = Path(self.tmp.name) / ".experiment.lock"
        self.patches = [mock.patch.object(guard, "LOCK", self.lock),
                        mock.patch.object(guard, "RESULTS", Path(self.tmp.name))]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.tmp.cleanup()

    def test_cap_workers(self):
        with mock.patch.object(guard, "MAX_WORKERS", 8):
            self.assertEqual(guard.cap_workers(12), 8)
            self.assertEqual(guard.cap_workers(4), 4)
            self.assertEqual(guard.cap_workers(0), 1)

    def test_lock_is_held_and_reentrant(self):
        with guard.slot("outer"):
            self.assertTrue(self.lock.exists())
            with guard.slot("inner"):          # same process: no deadlock
                self.assertTrue(self.lock.exists())
            self.assertTrue(self.lock.exists())
        self.assertFalse(self.lock.exists())

    def test_stale_lock_from_dead_process_is_taken_over(self):
        self.lock.write_text(json.dumps({"pid": 999999, "label": "crashed"}))
        with mock.patch.object(guard, "_alive", return_value=False):
            with guard.slot("next", poll=0.01):
                self.assertEqual(json.loads(self.lock.read_text())["label"], "next")

    def test_second_process_waits(self):
        code = ("import sys, time; from unittest import mock; from pathlib import Path; from bcsim import guard\n"
                f"p = Path(r'{self.lock}')\n"
                "with mock.patch.object(guard, 'LOCK', p), mock.patch.object(guard, 'RESULTS', p.parent):\n"
                "    with guard.slot('child', poll=0.05):\n"
                "        print('got', time.time(), flush=True)\n")
        with guard.slot("parent"):
            child = subprocess.Popen([sys.executable, "-c", code], stdout=subprocess.PIPE, text=True)
            time.sleep(1.0)
            self.assertIsNone(child.poll())    # still waiting for us
            released = time.time()
        out, _ = child.communicate(timeout=30)
        self.assertGreaterEqual(float(out.split()[-1]), released - 0.01)


if __name__ == "__main__":
    unittest.main()
