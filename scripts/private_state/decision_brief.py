"""Validation boundary for decisions and confirmed private-state events."""

from datetime import datetime, timezone
from typing import Any, Dict, Mapping
from uuid import uuid4


class DecisionBriefError(ValueError):
    """Raised when advice removes context or user agency."""


REQUIRED_BRIEF_FIELDS = (
    "decision",
    "context",
    "unknowns",
    "options",
    "preference",
    "switch_threshold",
    "choice_question",
)

REQUIRED_OPTION_FIELDS = (
    "name",
    "upside",
    "downside",
    "impact",
    "conditions",
    "reversibility",
    "confidence",
)


def _present(value: Any) -> bool:
    return value is not None and value != "" and value != []


def validate_decision_brief(brief: Mapping[str, Any]) -> Mapping[str, Any]:
    """Validate that a recommendation supports an informed human choice."""

    missing = [field for field in REQUIRED_BRIEF_FIELDS if not _present(brief.get(field))]
    if missing:
        raise DecisionBriefError(
            "Decision brief lacks context or required fields: " + ", ".join(missing)
        )

    options = brief["options"]
    if not isinstance(options, list) or len(options) < 2:
        raise DecisionBriefError("Decision brief must include at least two options")

    for index, option in enumerate(options, start=1):
        if not isinstance(option, Mapping):
            raise DecisionBriefError(f"Option {index} must be a mapping")
        absent = [field for field in REQUIRED_OPTION_FIELDS if not _present(option.get(field))]
        if absent:
            raise DecisionBriefError(
                f"Option {index} lacks implications: " + ", ".join(absent)
            )

    return brief


def event_from_confirmed_choice(
    *, event_type: str, player_id: str, amount: int, confirmed: bool
) -> Dict[str, Any]:
    """Create an append-only event only after explicit human confirmation."""

    if confirmed is not True:
        raise DecisionBriefError("Explicit confirmation is required before capsule update")
    if event_type not in {"BUY", "SELL", "CASH", "LINEUP"}:
        raise DecisionBriefError("Unsupported event type")
    if not player_id:
        raise DecisionBriefError("player_id is required")
    if not isinstance(amount, int) or amount < 0:
        raise DecisionBriefError("amount must be a non-negative integer")

    return {
        "event_id": str(uuid4()),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "player_id": player_id,
        "amount": amount,
        "confirmed": True,
    }
