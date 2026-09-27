from dataclasses import replace
from datetime import datetime
import unittest

from scripts.public_data.models import (
    MarketValue,
    ParsedSnapshot,
    Player,
    PreviousSnapshot,
    StarterProbability,
)
from scripts.public_data.parse import CANONICAL_URL
from scripts.public_data.validate import ValidationError, validate_snapshot


NOW = datetime.fromisoformat("2026-09-27T12:00:00+02:00")


def make_snapshot(count=16):
    positions = ("POR", "DEF", "MED", "DEL")
    players = tuple(
        Player(
            id="futbolfantasy:{}".format(index),
            source_id=str(index),
            name="Player {}".format(index),
            normalized_name="player_{}".format(index),
            team="Team {}".format(index % 15),
            team_source_id=str(index % 15),
            position=positions[index % len(positions)],
        )
        for index in range(1, count + 1)
    )
    values = tuple(MarketValue(player.id, 1_000_000 + index, index) for index, player in enumerate(players))
    probabilities = tuple(
        StarterProbability(player.id, index % 101, 8)
        for index, player in enumerate(players)
    )
    return ParsedSnapshot(
        platform="laliga_fantasy_oficial",
        source="futbolfantasy",
        source_url=CANONICAL_URL,
        retrieved_at=NOW,
        source_updated_at=datetime.fromisoformat("2026-09-27T03:00:00+02:00"),
        players=players,
        market_values=values,
        starter_probabilities=probabilities,
    )


class ValidateSnapshotTests(unittest.TestCase):
    def test_accepts_complete_consistent_snapshot(self):
        validate_snapshot(make_snapshot(), minimum_players=4, minimum_teams=1)

    def test_rejects_duplicate_source_ids(self):
        snapshot = make_snapshot()
        duplicate = replace(snapshot.players[1], id=snapshot.players[0].id, source_id=snapshot.players[0].source_id)
        with self.assertRaisesRegex(ValidationError, "duplicate player ID"):
            validate_snapshot(
                replace(snapshot, players=(snapshot.players[0], duplicate) + snapshot.players[2:]),
                minimum_players=4,
                minimum_teams=1,
            )

    def test_rejects_ambiguous_normalized_identity_within_same_team_and_position(self):
        snapshot = make_snapshot()
        ambiguous = replace(
            snapshot.players[1],
            normalized_name=snapshot.players[0].normalized_name,
            team_source_id=snapshot.players[0].team_source_id,
            position=snapshot.players[0].position,
        )
        with self.assertRaisesRegex(ValidationError, "ambiguous normalized identity"):
            validate_snapshot(
                replace(snapshot, players=(snapshot.players[0], ambiguous) + snapshot.players[2:]),
                minimum_players=4,
                minimum_teams=1,
            )

    def test_rejects_non_positive_market_value(self):
        snapshot = make_snapshot()
        bad_value = replace(snapshot.market_values[0], value=0)
        with self.assertRaisesRegex(ValidationError, "positive"):
            validate_snapshot(
                replace(snapshot, market_values=(bad_value,) + snapshot.market_values[1:]),
                minimum_players=4,
                minimum_teams=1,
            )

    def test_rejects_unresolved_player_reference(self):
        snapshot = make_snapshot()
        bad_value = replace(snapshot.market_values[0], player_id="futbolfantasy:missing")
        with self.assertRaisesRegex(ValidationError, "unknown player"):
            validate_snapshot(
                replace(snapshot, market_values=(bad_value,) + snapshot.market_values[1:]),
                minimum_players=4,
                minimum_teams=1,
            )

    def test_rejects_out_of_range_probability(self):
        snapshot = make_snapshot()
        bad_probability = replace(snapshot.starter_probabilities[0], value=101)
        with self.assertRaisesRegex(ValidationError, "probability"):
            validate_snapshot(
                replace(snapshot, starter_probabilities=(bad_probability,) + snapshot.starter_probabilities[1:]),
                minimum_players=4,
                minimum_teams=1,
            )

    def test_rejects_missing_required_position(self):
        snapshot = make_snapshot()
        players = tuple(replace(player, position="DEF") for player in snapshot.players)
        with self.assertRaisesRegex(ValidationError, "positions"):
            validate_snapshot(
                replace(snapshot, players=players), minimum_players=4, minimum_teams=1
            )

    def test_rejects_player_count_collapse(self):
        snapshot = make_snapshot(16)
        previous = PreviousSnapshot(player_count=21, market_values=())
        with self.assertRaisesRegex(ValidationError, "player count"):
            validate_snapshot(
                snapshot, previous=previous, minimum_players=4, minimum_teams=1
            )

    def test_rejects_unconfirmed_large_value_change(self):
        snapshot = make_snapshot()
        current = replace(snapshot.market_values[0], value=151)
        previous = PreviousSnapshot(
            player_count=16,
            market_values=(MarketValue(current.player_id, 100, 0),),
        )
        with self.assertRaisesRegex(ValidationError, "50%"):
            validate_snapshot(
                replace(snapshot, market_values=(current,) + snapshot.market_values[1:]),
                previous=previous,
                minimum_players=4,
                minimum_teams=1,
            )

    def test_allows_large_value_change_with_maintenance_override(self):
        snapshot = make_snapshot()
        current = replace(snapshot.market_values[0], value=151)
        previous = PreviousSnapshot(
            player_count=16,
            market_values=(MarketValue(current.player_id, 100, 0),),
        )
        validate_snapshot(
            replace(snapshot, market_values=(current,) + snapshot.market_values[1:]),
            previous=previous,
            minimum_players=4,
            minimum_teams=1,
            allow_large_change=True,
        )


if __name__ == "__main__":
    unittest.main()
