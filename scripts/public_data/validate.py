"""Whole-snapshot validation gates."""

from typing import Optional

from .models import ParsedSnapshot, PreviousSnapshot
from .parse import CANONICAL_URL, PLATFORM, SOURCE


REQUIRED_POSITIONS = {"POR", "DEF", "MED", "DEL"}


class ValidationError(ValueError):
    """Raised when a candidate snapshot is unsafe to publish."""


def validate_snapshot(
    snapshot: ParsedSnapshot,
    previous: Optional[PreviousSnapshot] = None,
    minimum_players: int = 400,
    minimum_teams: int = 15,
    allow_large_change: bool = False,
) -> None:
    if snapshot.platform != PLATFORM:
        raise ValidationError("unexpected fantasy platform")
    if snapshot.source != SOURCE or snapshot.source_url != CANONICAL_URL:
        raise ValidationError("unexpected canonical source")
    if len(snapshot.players) < minimum_players:
        raise ValidationError("player count is below the minimum")
    player_ids = [player.id for player in snapshot.players]
    if len(player_ids) != len(set(player_ids)):
        raise ValidationError("duplicate player ID")
    source_ids = [player.source_id for player in snapshot.players]
    if len(source_ids) != len(set(source_ids)):
        raise ValidationError("duplicate player ID from source")
    if len({player.team_source_id for player in snapshot.players}) < minimum_teams:
        raise ValidationError("team count is below the minimum")
    if {player.position for player in snapshot.players} != REQUIRED_POSITIONS:
        raise ValidationError("snapshot does not contain all required positions")

    player_id_set = set(player_ids)
    value_ids = [value.player_id for value in snapshot.market_values]
    if len(value_ids) != len(set(value_ids)):
        raise ValidationError("duplicate market value")
    if set(value_ids) != player_id_set:
        raise ValidationError("market value references an unknown player")
    for value in snapshot.market_values:
        if isinstance(value.value, bool) or not isinstance(value.value, int) or value.value <= 0:
            raise ValidationError("market value must be a positive integer")
        if isinstance(value.daily_change, bool) or not isinstance(value.daily_change, int):
            raise ValidationError("daily change must be an integer")

    probability_ids = set()
    for probability in snapshot.starter_probabilities:
        if probability.player_id not in player_id_set:
            raise ValidationError("starter probability references an unknown player")
        if probability.player_id in probability_ids:
            raise ValidationError("duplicate starter probability")
        probability_ids.add(probability.player_id)
        if (
            isinstance(probability.value, bool)
            or not isinstance(probability.value, int)
            or not 0 <= probability.value <= 100
        ):
            raise ValidationError("starter probability must be between 0 and 100")
        if (
            isinstance(probability.target_matchday, bool)
            or not isinstance(probability.target_matchday, int)
            or probability.target_matchday <= 0
        ):
            raise ValidationError("target matchday must be a positive integer")

    if previous is None:
        return
    if previous.player_count and len(snapshot.players) < previous.player_count * 0.8:
        raise ValidationError("player count fell by more than 20%")
    if allow_large_change:
        return
    previous_by_id = {value.player_id: value.value for value in previous.market_values}
    for value in snapshot.market_values:
        prior = previous_by_id.get(value.player_id)
        if prior is None or prior <= 0:
            continue
        if abs(value.value - prior) / prior > 0.5:
            raise ValidationError(
                "market value changed by more than 50% for {}".format(value.player_id)
            )
