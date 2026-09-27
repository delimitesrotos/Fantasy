"""Executable ordering contract for private-state turns."""

from typing import Any, Dict, Optional


def route_turn(
    *,
    sheet_ready: bool,
    has_private_update: bool,
    update_kind: Optional[str],
    asks_for_advice: bool,
) -> Dict[str, Any]:
    """Return the mandatory operation order for a conversational turn."""

    if not sheet_ready:
        return {
            "flow": "drive_setup",
            "steps": ["connect_drive", "create_or_find_sheet", "verify_write"],
        }

    if has_private_update:
        steps = ["read_control", "extract_draft"]
        if update_kind != "explicit_completed_event":
            steps.append("show_diff_and_confirm")
        steps.extend(["write_sheet", "readback_verify"])
        if asks_for_advice:
            steps.extend(["run_public_analysis", "present_decision_brief"])
        else:
            steps.append("report_state_update")
        return {"flow": "private_update_then_analysis", "steps": steps}

    if asks_for_advice:
        return {
            "flow": "personalized_analysis",
            "steps": [
                "read_control",
                "read_relevant_private_tabs",
                "run_public_analysis",
                "present_decision_brief",
            ],
        }

    return {
        "flow": "state_check",
        "steps": ["read_control", "ask_next_guided_question"],
    }

