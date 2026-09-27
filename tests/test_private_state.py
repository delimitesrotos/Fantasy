import unittest

from scripts.private_state.onboarding import next_onboarding_step


class OnboardingStateMachineTests(unittest.TestCase):
    def test_first_stage_requires_friends_drive_document(self):
        result = next_onboarding_step({}, "¿Qué hago hoy?")

        self.assertEqual(result["stage"], "drive_setup")
        self.assertEqual(result["flow"], "onboarding")
        self.assertEqual(len(result["questions"]), 1)
        self.assertIn("tu google drive", result["questions"][0].lower())

    def test_drive_stage_is_not_complete_without_canonical_sheet_url(self):
        state = {"drive_setup": {"complete": True}}

        result = next_onboarding_step(state, "Empezar Fantasy")

        self.assertEqual(result["stage"], "drive_setup")
        self.assertEqual(result["action"], "connect_or_create_private_sheet")

    def test_partial_state_resumes_at_first_missing_stage(self):
        state = {
            "drive_setup": {
                "complete": True,
                "spreadsheet_url": "https://docs.google.com/spreadsheets/d/example",
            },
            "league_rules": {"complete": True},
            "own_team": {"complete": True},
            "standings": {"complete": False},
            "rival_rosters": {"complete": False},
        }

        result = next_onboarding_step(state, "Empezar Fantasy")

        self.assertEqual(result["stage"], "standings")
        self.assertEqual(len(result["questions"]), 1)
        self.assertIn("clasificación", result["questions"][0].lower())

    def test_rival_rosters_are_progressive_and_do_not_block_ready_state(self):
        state = {
            "drive_setup": {
                "complete": True,
                "spreadsheet_url": "https://docs.google.com/spreadsheets/d/example",
            },
            "league_rules": {"complete": True},
            "own_team": {"complete": True},
            "standings": {"complete": True},
            "rival_rosters": {"complete": False, "known_rivals": 0},
        }

        result = next_onboarding_step(state, "¿Qué hago hoy?")

        self.assertEqual(result["stage"], "ready")
        self.assertEqual(result["flow"], "daily")
        self.assertEqual(result["questions"], [])
        self.assertIn("rivales", result["warnings"][0].lower())

    def test_ready_state_routes_matchday_trigger(self):
        state = {
            "drive_setup": {
                "complete": True,
                "spreadsheet_url": "https://docs.google.com/spreadsheets/d/example",
            },
            "league_rules": {"complete": True},
            "own_team": {"complete": True},
            "standings": {"complete": True},
        }

        result = next_onboarding_step(state, "Prepara mi jornada")

        self.assertEqual(result["stage"], "ready")
        self.assertEqual(result["flow"], "matchday")


if __name__ == "__main__":
    unittest.main()
