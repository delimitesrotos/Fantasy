from datetime import datetime, timedelta
import unittest

from scripts.public_data.freshness import FreshnessError, classify_freshness


class FreshnessTests(unittest.TestCase):
    def test_classifies_observation_within_max_age_as_fresh(self):
        observed = datetime.fromisoformat("2026-09-27T03:00:00+02:00")
        now = datetime.fromisoformat("2026-09-28T08:59:59+02:00")
        self.assertEqual(
            classify_freshness(observed, now, timedelta(hours=30)), "fresh"
        )

    def test_classifies_observation_beyond_max_age_as_stale(self):
        observed = datetime.fromisoformat("2026-09-27T03:00:00+02:00")
        now = datetime.fromisoformat("2026-09-28T09:00:01+02:00")
        self.assertEqual(
            classify_freshness(observed, now, timedelta(hours=30)), "stale"
        )

    def test_classifies_missing_observation_as_unknown(self):
        now = datetime.fromisoformat("2026-09-27T12:00:00+02:00")
        self.assertEqual(
            classify_freshness(None, now, timedelta(hours=30)), "unknown"
        )

    def test_rejects_naive_datetimes(self):
        observed = datetime.fromisoformat("2026-09-27T03:00:00")
        now = datetime.fromisoformat("2026-09-27T12:00:00+02:00")
        with self.assertRaises(FreshnessError):
            classify_freshness(observed, now, timedelta(hours=30))

    def test_rejects_observation_more_than_five_minutes_in_future(self):
        now = datetime.fromisoformat("2026-09-27T12:00:00+02:00")
        observed = now + timedelta(minutes=6)
        with self.assertRaisesRegex(FreshnessError, "future"):
            classify_freshness(observed, now, timedelta(hours=30))


if __name__ == "__main__":
    unittest.main()
