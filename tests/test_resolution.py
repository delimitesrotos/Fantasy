import json
from pathlib import Path
import unittest

from scripts.public_data.resolution import resolve_market_value


CASES = json.loads(
    (Path(__file__).parent / "fixtures" / "data_resolution_cases.json").read_text()
)


class ResolutionPolicyTests(unittest.TestCase):
    def test_acceptance_cases_a_through_f(self):
        for case in CASES:
            with self.subTest(case=case["name"]):
                result = resolve_market_value(
                    user_value=case["user_value"],
                    snapshot=case["snapshot"],
                    canonical=case["canonical"],
                    search_snippet_value=case["search_snippet_value"],
                )
                self.assertEqual(
                    {"value": result.value, "origin": result.origin}, case["expected"]
                )

    def test_rejects_non_positive_explicit_app_value(self):
        with self.assertRaises(ValueError):
            resolve_market_value(user_value=0)


if __name__ == "__main__":
    unittest.main()
