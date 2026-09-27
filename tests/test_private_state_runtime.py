import unittest

from scripts.private_state.runtime import route_turn


class PrivateStateRuntimeTests(unittest.TestCase):
    def test_storage_is_precondition_before_private_collection(self):
        result = route_turn(
            sheet_ready=False,
            has_private_update=True,
            update_kind="attachment",
            asks_for_advice=False,
        )

        self.assertEqual(result["flow"], "drive_setup")
        self.assertEqual(result["steps"], ["connect_drive", "create_or_find_sheet", "verify_write"])

    def test_attachment_is_confirmed_and_persisted_before_analysis(self):
        result = route_turn(
            sheet_ready=True,
            has_private_update=True,
            update_kind="attachment",
            asks_for_advice=True,
        )

        self.assertEqual(result["flow"], "private_update_then_analysis")
        self.assertEqual(
            result["steps"],
            [
                "read_control",
                "extract_draft",
                "show_diff_and_confirm",
                "write_sheet",
                "readback_verify",
                "run_public_analysis",
                "present_decision_brief",
            ],
        )

    def test_explicit_completed_event_is_self_confirming_but_still_verified(self):
        result = route_turn(
            sheet_ready=True,
            has_private_update=True,
            update_kind="explicit_completed_event",
            asks_for_advice=False,
        )

        self.assertNotIn("show_diff_and_confirm", result["steps"])
        self.assertEqual(result["steps"][-2:], ["readback_verify", "report_state_update"])

    def test_personalized_advice_reads_sheet_before_public_sources(self):
        result = route_turn(
            sheet_ready=True,
            has_private_update=False,
            update_kind=None,
            asks_for_advice=True,
        )

        self.assertEqual(
            result["steps"],
            ["read_control", "read_relevant_private_tabs", "run_public_analysis", "present_decision_brief"],
        )


if __name__ == "__main__":
    unittest.main()
