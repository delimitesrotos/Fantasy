"""Deterministic JSON documents and atomic publication."""

from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import tempfile
from typing import Dict, Mapping, MutableMapping, Union

from .freshness import classify_freshness
from .models import ParsedSnapshot


SCHEMA_VERSION = 1
JsonDocument = MutableMapping[str, object]


def _base_document(dataset: str, generated_at: datetime) -> JsonDocument:
    return {
        "dataset": dataset,
        "generated_at": generated_at.isoformat(),
        "schema_version": SCHEMA_VERSION,
    }


def build_documents(snapshot: ParsedSnapshot, now: datetime) -> Dict[str, JsonDocument]:
    market_status = classify_freshness(
        snapshot.source_updated_at, now, timedelta(hours=30)
    )
    probability_status = classify_freshness(
        snapshot.retrieved_at, now, timedelta(hours=8)
    )
    players = [
        {
            "id": player.id,
            "name": player.name,
            "normalized_name": player.normalized_name,
            "position": player.position,
            "source_id": player.source_id,
            "team": player.team,
            "team_source_id": player.team_source_id,
        }
        for player in sorted(snapshot.players, key=lambda item: item.id)
    ]
    market_values = [
        {
            "market_value": {
                "currency": "EUR",
                "daily_change": value.daily_change,
                "freshness": market_status,
                "platform": snapshot.platform,
                "retrieved_at": snapshot.retrieved_at.isoformat(),
                "source": snapshot.source,
                "source_updated_at": snapshot.source_updated_at.isoformat(),
                "source_url": snapshot.source_url,
                "value": value.value,
            },
            "player_id": value.player_id,
        }
        for value in sorted(snapshot.market_values, key=lambda item: item.player_id)
    ]
    probabilities = [
        {
            "player_id": probability.player_id,
            "starter_probability": {
                "freshness": probability_status,
                "retrieved_at": snapshot.retrieved_at.isoformat(),
                "source": snapshot.source,
                "source_updated_at": None,
                "source_url": snapshot.source_url,
                "target_matchday": probability.target_matchday,
                "value": probability.value,
            },
        }
        for probability in sorted(
            snapshot.starter_probabilities, key=lambda item: item.player_id
        )
    ]
    player_document = _base_document("players", now)
    player_document["players"] = players
    market_document = _base_document("market_values", now)
    market_document["market_values"] = market_values
    probability_document = _base_document("starter_probabilities", now)
    probability_document["starter_probabilities"] = probabilities
    metadata_document = _base_document("metadata", now)
    metadata_document.update(
        {
            "pipeline_status": "valid",
            "platform": snapshot.platform,
            "counts": {
                "market_values": len(market_values),
                "players": len(players),
                "starter_probabilities": len(probabilities),
            },
            "sources": {
                "market_values": {
                    "error": None,
                    "freshness_max_age_hours": 30,
                    "last_success": now.isoformat(),
                    "provider": snapshot.source,
                    "retrieved_at": snapshot.retrieved_at.isoformat(),
                    "source_updated_at": snapshot.source_updated_at.isoformat(),
                    "status": market_status,
                    "url": snapshot.source_url,
                },
                "starter_probabilities": {
                    "error": None,
                    "freshness_max_age_hours": 8,
                    "last_success": now.isoformat(),
                    "provider": snapshot.source,
                    "retrieved_at": snapshot.retrieved_at.isoformat(),
                    "source_updated_at": None,
                    "status": probability_status,
                    "url": snapshot.source_url,
                },
            },
        }
    )
    return {
        "players.json": player_document,
        "market-values.json": market_document,
        "starter-probabilities.json": probability_document,
        "metadata.json": metadata_document,
    }


def publish_documents(
    documents: Mapping[str, Mapping[str, object]], output_dir: Union[Path, str]
) -> None:
    output_path = Path(output_dir)
    required = {
        "players.json",
        "market-values.json",
        "starter-probabilities.json",
        "metadata.json",
    }
    if set(documents) != required:
        raise ValueError("document set is incomplete")
    encoded = {
        name: json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        for name, document in documents.items()
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=str(output_path.parent)) as raw_tmp:
        tmp = Path(raw_tmp)
        for name, content in encoded.items():
            (tmp / name).write_text(content, encoding="utf-8")
        output_path.mkdir(parents=True, exist_ok=True)
        for name in sorted(encoded):
            os.replace(str(tmp / name), str(output_path / name))
