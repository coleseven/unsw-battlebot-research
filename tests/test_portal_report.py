import contextlib
import io
import json
import pathlib
import tempfile
import unittest

from bcsim.portal_report import report


class PortalReportTest(unittest.TestCase):
    def test_aggregation_and_final_audit_requirement(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = pathlib.Path(tmp)
            maps = []
            audits = []
            for stage in ("validation", "transfer"):
                (out / stage).mkdir()
                path = out / (stage + ".map")
                path.write_text("MAP 11 11\nTILE_COUNT 1\nTILE 1 1 2 5\nEDGE_COUNT 0\nDRAGON_COUNT 0\n")
                maps.append(str(path))
                replay_path = str((out / stage / "g.replay").resolve())
                game = {"bot_a": "portal_escape", "bot_b": "reference_v2", "map": stage,
                        "winner": "A", "reason": "length", "a_longest": 7, "replay": replay_path}
                (out / stage / "games.jsonl").write_text(json.dumps(game) + "\n")
                audits.append({"key": replay_path, "counts": {"games": 1, "verified_candidate_turns": 100,
                               "portal_overrides": 5, "override_survived_own_turn": 4}})
            plan = {"official_maps": maps[:1], "transfer_maps": maps[1:],
                    "expected_games": {"validation": 1, "transfer": 1}}
            (out / "plan.json").write_text(json.dumps(plan))
            (out / "audit-progress.jsonl").write_text("\n".join(map(json.dumps, audits)))
            with self.assertRaises(FileNotFoundError):
                report(out)
            self.assertFalse((out / "mechanism-report.json").exists())
            (out / "replay-audit.json").write_text(json.dumps({"counts": {"games": 2}}))
            with contextlib.redirect_stdout(io.StringIO()):
                report(out)
            result = json.loads((out / "mechanism-report.json").read_text())
            self.assertEqual(len(result["maps"]), 2)
            for row in result["maps"]:
                self.assertEqual(row["overrides_per_1000_turns"], 50)
                self.assertEqual(row["immediate_override_survival"], .8)
                self.assertEqual(row["portal_pairs"], 0)
                self.assertAlmostEqual(row["spawn_tile_fraction"], 1/121)
            self.assertEqual(result["phase_diagnostics"]["transfer"]["portal_escape"]["wins"], 1)


if __name__ == "__main__":
    unittest.main()
