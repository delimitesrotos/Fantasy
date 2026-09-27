"""Typed records shared by parsing, validation, and serialization."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple


@dataclass(frozen=True)
class Player:
    id: str
    source_id: str
    name: str
    normalized_name: str
    team: str
    team_source_id: str
    position: str


@dataclass(frozen=True)
class MarketValue:
    player_id: str
    value: int
    daily_change: int


@dataclass(frozen=True)
class StarterProbability:
    player_id: str
    value: int
    target_matchday: int


@dataclass(frozen=True)
class ParsedSnapshot:
    platform: str
    source: str
    source_url: str
    retrieved_at: datetime
    source_updated_at: datetime
    players: Tuple[Player, ...]
    market_values: Tuple[MarketValue, ...]
    starter_probabilities: Tuple[StarterProbability, ...]


@dataclass(frozen=True)
class PreviousSnapshot:
    player_count: int
    market_values: Tuple[MarketValue, ...]
    last_success: Optional[datetime] = None
