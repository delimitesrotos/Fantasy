"""Freshness classification for dynamic observations."""

from datetime import datetime, timedelta
from typing import Optional


FUTURE_TOLERANCE = timedelta(minutes=5)


class FreshnessError(ValueError):
    """Raised when an observation cannot be classified safely."""


def _require_aware(value: datetime, label: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise FreshnessError("{} must include a timezone".format(label))


def classify_freshness(
    observed_at: Optional[datetime], now: datetime, max_age: timedelta
) -> str:
    """Return fresh, stale, or unknown for one dynamic observation."""
    _require_aware(now, "now")
    if observed_at is None:
        return "unknown"
    _require_aware(observed_at, "observed_at")
    if max_age.total_seconds() < 0:
        raise FreshnessError("max_age cannot be negative")
    age = now - observed_at
    if age < -FUTURE_TOLERANCE:
        raise FreshnessError("observation timestamp is in the future")
    return "fresh" if age <= max_age else "stale"
