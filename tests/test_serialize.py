from datetime import datetime
import json
from pathlib import Path
import tempfile
import unittest

from scripts.public_data.serialize import build_documents, publish_documents
from tests.test_validation import make_snapshot


NOW = datetime.fromisoformat("2026-09-27T12:00:00+02:00")


class SerializationTests(unittest.TestCase):
    def test_builds_sorted_documents_with_provenance_and_freshness(self):
        snapshot = make_snapshot()
        documents = build_documents(snapshot, NOW)

        self.assertEqual(
            list(documents),
            [
                "players.json",
                "market-values.json",
                "starter-probabilities.json",
                "metadata.json",
            ],
        )
        first = documents["market-values.json"]["market_values"][0]
        self.assertEqual(first["player_id"], "futbolfantasy:1")
        self.assertEqual(first["market_value"]["platform"], "laliga_fantasy_oficial")
        self.assertEqual(first["market_value"]["source"], "futbolfantasy")
        self.assertEqual(first["market_value"]["freshness"], "fresh")
        self.assertEqual(
            documents["metadata.json"]["sources"]["starter_probabilities"]["freshness_max_age_hours"],
            8,
        )

    def test_publishes_all_documents_as_valid_json(self):
        documents = build_documents(make_snapshot(), NOW)
        with tempfile.TemporaryDirectory() as raw_dir:
            output_dir = Path(raw_dir) / "latest"
            publish_documents(documents, output_dir)
            for name, expected in documents.items():
                self.assertEqual(
                    json.loads((output_dir / name).read_text()), expected
                )
                self.assertTrue((output_dir / name).read_text().endswith("\n"))

    def test_invalid_staged_document_preserves_existing_files(self):
        documents = build_documents(make_snapshot(), NOW)
        documents["metadata.json"]["not_json"] = {object()}
        with tempfile.TemporaryDirectory() as raw_dir:
            output_dir = Path(raw_dir) / "latest"
            output_dir.mkdir()
            original = '{"status":"previous"}\n'
            (output_dir / "metadata.json").write_text(original)
            with self.assertRaises(TypeError):
                publish_documents(documents, output_dir)
            self.assertEqual((output_dir / "metadata.json").read_text(), original)
            self.assertFalse((output_dir / "players.json").exists())


if __name__ == "__main__":
    unittest.main()
