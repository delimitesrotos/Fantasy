#!/usr/bin/env python3
"""Fetch, validate, and atomically publish the public data snapshot."""

import argparse
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import List, Optional
from zoneinfo import ZoneInfo


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from scripts.public_data.fetch import FetchError, fetch_html
from scripts.public_data.freshness import FreshnessError, classify_freshness
from scripts.public_data.models import MarketValue, PreviousSnapshot
from scripts.public_data.parse import ParseError, PLATFORM, parse_market_html
from scripts.public_data.serialize import build_documents, publish_documents
from scripts.public_data.validate import ValidationError, validate_snapshot


class PipelineError(RuntimeError):
    """Raised for local snapshot or orchestration errors."""


def _parse_now(raw: Optional[str]) -> datetime:
    if raw is None:
        return datetime.now(ZoneInfo("Europe/Madrid"))
    value = datetime.fromisoformat(raw)
    if value.tzinfo is None or value.utcoffset() is None:
        raise PipelineError("--now must include a timezone offset")
    return value


def _load_previous(output_dir: Path) -> Optional[PreviousSnapshot]:
    players_path = output_dir / "players.json"
    values_path = output_dir / "market-values.json"
    if not players_path.exists() or not values_path.exists():
        return None
    try:
        players = json.loads(players_path.read_text(encoding="utf-8"))["players"]
        raw_values = json.loads(values_path.read_text(encoding="utf-8"))["market_values"]
        values = tuple(
            MarketValue(
                player_id=entry["player_id"],
                value=entry["market_value"]["value"],
                daily_change=entry["market_value"]["daily_change"],
            )
            for entry in raw_values
        )
        return PreviousSnapshot(player_count=len(players), market_values=values)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        raise PipelineError("existing snapshot is invalid") from error


def _status_from_metadata(source, now: datetime) -> str:
    raw_observed = source.get("source_updated_at") or source.get("retrieved_at")
    if not raw_observed:
        return "unknown"
    try:
        observed = datetime.fromisoformat(raw_observed)
        return classify_freshness(
            observed, now, timedelta(hours=source["freshness_max_age_hours"])
        )
    except (FreshnessError, KeyError, TypeError, ValueError):
        return "unknown"


def _write_failure_metadata(output_dir: Path, now: datetime, error: Exception) -> None:
    metadata_path = output_dir / "metadata.json"
    if metadata_path.exists():
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            metadata = {}
    else:
        metadata = {}
    metadata.setdefault("schema_version", 1)
    metadata.setdefault("dataset", "metadata")
    metadata.setdefault("platform", PLATFORM)
    metadata.setdefault(
        "counts",
        {"players": 0, "market_values": 0, "starter_probabilities": 0},
    )
    metadata.setdefault("sources", {})
    for name, max_age in (("market_values", 30), ("starter_probabilities", 8)):
        source = metadata["sources"].setdefault(
            name,
            {
                "provider": "futbolfantasy",
                "url": "https://www.futbolfantasy.com/analytics/laliga-fantasy/mercado",
                "retrieved_at": None,
                "source_updated_at": None,
                "last_success": None,
                "freshness_max_age_hours": max_age,
            },
        )
        source["status"] = _status_from_metadata(source, now)
        source["error"] = str(error)
    metadata["generated_at"] = now.isoformat()
    metadata["pipeline_status"] = "failed"
    metadata["last_error"] = str(error)
    output_dir.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=str(output_dir), delete=False
    ) as handle:
        handle.write(encoded)
        temporary_name = handle.name
    os.replace(temporary_name, metadata_path)


def _argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="Read HTML from a local fixture")
    parser.add_argument(
        "--output", type=Path, default=Path("data/public/latest")
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--allow-large-change", action="store_true")
    parser.add_argument("--now", help=argparse.SUPPRESS)
    parser.add_argument("--minimum-players", type=int, default=400)
    parser.add_argument("--minimum-teams", type=int, default=15)
    return parser


def run(argv: Optional[List[str]] = None) -> int:
    args = _argument_parser().parse_args(argv)
    try:
        now = _parse_now(args.now)
        html = (
            args.input.read_text(encoding="utf-8")
            if args.input is not None
            else fetch_html()
        )
        snapshot = parse_market_html(html, now)
        market_status = classify_freshness(
            snapshot.source_updated_at, now, timedelta(hours=30)
        )
        if market_status != "fresh":
            raise ValidationError("canonical market cycle is stale")
        previous = _load_previous(args.output)
        validate_snapshot(
            snapshot,
            previous=previous,
            minimum_players=args.minimum_players,
            minimum_teams=args.minimum_teams,
            allow_large_change=args.allow_large_change,
        )
        documents = build_documents(snapshot, now)
        if not args.check:
            publish_documents(documents, args.output)
        print(
            "Validated {} players, {} market values, {} starter probabilities.".format(
                len(snapshot.players),
                len(snapshot.market_values),
                len(snapshot.starter_probabilities),
            )
        )
        return 0
    except (FetchError, FreshnessError, OSError, ParseError, PipelineError, ValidationError) as error:
        print("Public data update failed: {}".format(error), file=sys.stderr)
        if not args.check:
            try:
                _write_failure_metadata(args.output, _parse_now(args.now), error)
            except OSError as metadata_error:
                print(
                    "Could not write failure metadata: {}".format(metadata_error),
                    file=sys.stderr,
                )
        return 1


if __name__ == "__main__":
    raise SystemExit(run())
