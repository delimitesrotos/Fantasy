"""Strict parser for FútbolFantasy's public LALIGA Fantasy market page."""

from datetime import datetime
from html.parser import HTMLParser
import re
import unicodedata
from typing import Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

from .freshness import FreshnessError, classify_freshness
from .models import MarketValue, ParsedSnapshot, Player, StarterProbability


CANONICAL_URL = "https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado"
PLATFORM = "laliga_fantasy_oficial"
SOURCE = "futbolfantasy"
POSITION_CODES = {
    "Portero": "POR",
    "Defensa": "DEF",
    "Mediocampista": "MED",
    "Delantero": "DEL",
}


class ParseError(ValueError):
    """Raised when source markup cannot be proved safe to consume."""


def normalize_name(name: str) -> str:
    decomposed = unicodedata.normalize("NFKD", name)
    ascii_name = "".join(
        character
        for character in decomposed
        if not unicodedata.combining(character)
    )
    return re.sub(r"[^a-z0-9]+", "_", ascii_name.lower()).strip("_")


def _classes(attrs: Dict[str, str]) -> Tuple[str, ...]:
    return tuple(attrs.get("class", "").split())


class _MarketParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.canonical_href: Optional[str] = None
        self.h1_parts: List[str] = []
        self.small_parts: List[str] = []
        self._in_h1 = False
        self._in_small = False
        self._in_market_table = False
        self.market_table_closed = False
        self._row: Optional[Dict[str, str]] = None
        self._in_player_name = False
        self._capture_name = False
        self._name_parts: List[str] = []
        self._in_team = False
        self._capture_team = False
        self._team_parts: List[str] = []
        self._capture_probability = False
        self._probability_parts: List[str] = []
        self.rows: List[Dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs_list: List[Tuple[str, Optional[str]]]) -> None:
        attrs = {key: value or "" for key, value in attrs_list}
        classes = _classes(attrs)
        if tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonical_href = attrs.get("href")
        if tag == "h1":
            self._in_h1 = True
        if tag == "small":
            self._in_small = True
        if tag == "table" and "analytics-table" in classes:
            self._in_market_table = True
        if self._in_market_table and tag == "tr" and "elemento_jugador" in classes:
            self._row = dict(attrs)
            self._name_parts = []
            self._team_parts = []
            self._probability_parts = []
        if self._row is None:
            return
        if tag == "a" and "player-name" in classes:
            self._in_player_name = True
        elif self._in_player_name and tag == "span" and not self._name_parts:
            self._capture_name = True
        if tag == "div" and "player-equipo" in classes:
            self._in_team = True
        elif self._in_team and tag == "span" and not self._team_parts:
            self._capture_team = True
        if "rival-probability" in classes:
            title = attrs.get("title", "")
            match = re.search(r"Jornada\s+(\d+)", title, re.IGNORECASE)
            if match:
                self._row["target_matchday"] = match.group(1)
        if any(value.startswith("prob-") for value in classes):
            self._capture_probability = True

    def handle_data(self, data: str) -> None:
        if self._in_h1:
            self.h1_parts.append(data)
        if self._in_small:
            self.small_parts.append(data)
        if self._capture_name:
            self._name_parts.append(data)
        if self._capture_team:
            self._team_parts.append(data)
        if self._capture_probability:
            self._probability_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1":
            self._in_h1 = False
        if tag == "small":
            self._in_small = False
        if tag == "span":
            if self._capture_name:
                self._capture_name = False
            if self._capture_team:
                self._capture_team = False
            if self._capture_probability:
                self._capture_probability = False
        if tag == "a" and self._in_player_name:
            self._in_player_name = False
        if tag == "div" and self._in_team:
            self._in_team = False
        if tag == "tr" and self._row is not None:
            self._row["display_name"] = " ".join(self._name_parts).strip()
            self._row["team_name"] = " ".join(self._team_parts).strip()
            self._row["probability"] = " ".join(self._probability_parts).strip()
            self.rows.append(self._row)
            self._row = None
        if tag == "table" and self._in_market_table:
            self._in_market_table = False
            self.market_table_closed = True


def _parse_source_updated_at(parts: List[str]) -> datetime:
    update_text = " ".join(" ".join(parts).split())
    match = re.search(r"Última actualización:\s*(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2})", update_text)
    if not match:
        raise ParseError("source update timestamp is missing")
    return datetime.strptime(match.group(1), "%d/%m/%Y %H:%M").replace(
        tzinfo=ZoneInfo("Europe/Madrid")
    )


def _required_int(row: Dict[str, str], key: str, label: str) -> int:
    try:
        return int(row[key])
    except (KeyError, TypeError, ValueError) as error:
        raise ParseError("invalid {} for player row".format(label)) from error


def parse_market_html(html: str, retrieved_at: datetime) -> ParsedSnapshot:
    parser = _MarketParser()
    parser.feed(html)
    parser.close()
    heading = " ".join(" ".join(parser.h1_parts).split())
    if parser.canonical_href != CANONICAL_URL or "LaLiga Fantasy Oficial" not in heading:
        raise ParseError("canonical platform identity is missing or ambiguous")
    if not parser.market_table_closed:
        raise ParseError("closed market table is missing")
    source_updated_at = _parse_source_updated_at(parser.small_parts)
    try:
        classify_freshness(source_updated_at, retrieved_at, retrieved_at - retrieved_at)
    except FreshnessError as error:
        raise ParseError(str(error)) from error

    players: List[Player] = []
    market_values: List[MarketValue] = []
    probabilities: List[StarterProbability] = []
    for row in parser.rows:
        position_name = row.get("data-posicion", "")
        if position_name == "Entrenador":
            continue
        if position_name not in POSITION_CODES:
            raise ParseError("invalid player position")
        source_id = row.get("data-id", "").strip()
        name = row.get("display_name", "").strip()
        team = row.get("team_name", "").strip()
        team_source_id = row.get("data-equipo", "").strip()
        if not source_id or not name or not team or not team_source_id:
            raise ParseError("player identity is incomplete")
        player_id = "futbolfantasy:{}".format(source_id)
        players.append(
            Player(
                id=player_id,
                source_id=source_id,
                name=name,
                normalized_name=normalize_name(name),
                team=team,
                team_source_id=team_source_id,
                position=POSITION_CODES[position_name],
            )
        )
        market_values.append(
            MarketValue(
                player_id=player_id,
                value=_required_int(row, "data-valor", "market value"),
                daily_change=_required_int(row, "data-diferencia1", "daily change"),
            )
        )
        raw_probability = row.get("probability", "").strip()
        if raw_probability:
            match = re.fullmatch(r"(\d{1,3})%", raw_probability)
            if not match:
                raise ParseError("invalid starter probability")
            probability = int(match.group(1))
            if not 0 <= probability <= 100:
                raise ParseError("invalid starter probability")
            target_matchday = _required_int(row, "target_matchday", "target matchday")
            probabilities.append(
                StarterProbability(
                    player_id=player_id,
                    value=probability,
                    target_matchday=target_matchday,
                )
            )
    if not players:
        raise ParseError("market table contains no player rows")
    return ParsedSnapshot(
        platform=PLATFORM,
        source=SOURCE,
        source_url=CANONICAL_URL,
        retrieved_at=retrieved_at,
        source_updated_at=source_updated_at,
        players=tuple(players),
        market_values=tuple(market_values),
        starter_probabilities=tuple(probabilities),
    )
