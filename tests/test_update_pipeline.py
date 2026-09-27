import json
from pathlib import Path
import tempfile
import unittest

from scripts.update_public_data import run


FIXTURES = Path(__file__).parent / "fixtures"


def valid_args(output_dir):
    return [
        "--input",
        str(FIXTURES / "valid_market.html"),
        "--output",
        str(output_dir),
        "--now",
        "2026-09-27T12:00:00+02:00",
        "--minimum-players",
        "4",
        "--minimum-teams",
        "4",
    ]


class UpdatePipelineTests(unittest.TestCase):
    def test_check_mode_validates_without_publishing(self):
        with tempfile.TemporaryDirectory() as raw_dir:
            output_dir = Path(raw_dir) / "latest"
            self.assertEqual(run(valid_args(output_dir) + ["--check"]), 0)
            self.assertFalse(output_dir.exists())

    def test_rejects_ambiguous_platform(self):
        with tempfile.TemporaryDirectory() as raw_dir:
            output_dir = Path(raw_dir) / "latest"
            args = valid_args(output_dir)
            args[1] = str(FIXTURES / "ambiguous_platform.html")
            self.assertEqual(run(args + ["--check"]), 1)
            self.assertFalse(output_dir.exists())

    def test_publishes_valid_fixture(self):
        with tempfile.TemporaryDirectory() as raw_dir:
            output_dir = Path(raw_dir) / "latest"
            self.assertEqual(run(valid_args(output_dir)), 0)
            metadata = json.loads((output_dir / "metadata.json").read_text())
            self.assertEqual(metadata["pipeline_status"], "valid")
            self.assertEqual(metadata["counts"]["players"], 4)

    def test_failure_preserves_snapshot_and_marks_metadata_stale(self):
        with tempfile.TemporaryDirectory() as raw_dir:
            output_dir = Path(raw_dir) / "latest"
            self.assertEqual(run(valid_args(output_dir)), 0)
            original_players = (output_dir / "players.json").read_text()
            args = valid_args(output_dir)
            args[1] = str(FIXTURES / "ambiguous_platform.html")
            now_index = args.index("--now") + 1
            args[now_index] = "2026-09-29T12:00:00+02:00"
            self.assertEqual(run(args), 1)
            self.assertEqual((output_dir / "players.json").read_text(), original_players)
            metadata = json.loads((output_dir / "metadata.json").read_text())
            self.assertEqual(metadata["pipeline_status"], "failed")
            self.assertEqual(metadata["sources"]["market_values"]["status"], "stale")
            self.assertEqual(metadata["sources"]["starter_probabilities"]["status"], "stale")
            self.assertIn("canonical platform", metadata["last_error"])


if __name__ == "__main__":
    unittest.main()
