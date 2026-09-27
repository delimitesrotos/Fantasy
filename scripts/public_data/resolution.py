"""Executable form of the exact market-value resolution policy."""

from dataclasses import dataclass
from typing import Mapping, Optional

from .parse import PLATFORM


@dataclass(frozen=True)
class ResolvedValue:
    value: Optional[int]
    origin: str


def _positive_integer(value, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError("{} must be a positive integer".format(label))
    return value


def resolve_market_value(
    user_value: Optional[int] = None,
    snapshot: Optional[Mapping[str, object]] = None,
    canonical: Optional[Mapping[str, object]] = None,
    search_snippet_value: Optional[int] = None,
) -> ResolvedValue:
    """Resolve an exact value without ever trusting a search snippet."""
    if user_value is not None:
        return ResolvedValue(
            _positive_integer(user_value, "user_value"), "user_official_app"
        )
    if (
        snapshot is not None
        and snapshot.get("freshness") == "fresh"
        and snapshot.get("platform") == PLATFORM
    ):
        return ResolvedValue(
            _positive_integer(snapshot.get("value"), "snapshot value"),
            "repository_snapshot",
        )
    if (
        canonical is not None
        and canonical.get("verified") is True
        and canonical.get("platform") == PLATFORM
    ):
        return ResolvedValue(
            _positive_integer(canonical.get("value"), "canonical value"),
            "canonical_source",
        )
    _ = search_snippet_value
    return ResolvedValue(None, "unknown")
