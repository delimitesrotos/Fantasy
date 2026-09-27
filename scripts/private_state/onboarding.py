"""Pure routing for the guided onboarding conversation."""

from typing import Any, Dict, Mapping


REQUIRED_STAGES = (
    (
        "league_rules",
        "Envíame una captura de las reglas de tu liga (puntuación, límites, "
        "primas, cláusulas y funcionamiento del mercado).",
    ),
    (
        "own_team",
        "Envíame una captura de tu plantilla completa donde se vean también "
        "tu saldo y, si aparece, el valor del equipo.",
    ),
    (
        "standings",
        "Envíame una captura de la clasificación actual de la liga.",
    ),
)


def _is_complete(state: Mapping[str, Any], stage: str) -> bool:
    value = state.get(stage, {})
    return isinstance(value, Mapping) and value.get("complete") is True


def _destination_flow(trigger: str) -> str:
    normalized = trigger.casefold().strip()
    if "jornada" in normalized:
        return "matchday"
    if "hoy" in normalized:
        return "daily"
    return "general"


def next_onboarding_step(
    state: Mapping[str, Any], trigger: str
) -> Dict[str, Any]:
    """Return the one next question or route a complete state to its flow."""

    for stage, question in REQUIRED_STAGES:
        if not _is_complete(state, stage):
            return {
                "stage": stage,
                "flow": "onboarding",
                "questions": [question],
                "warnings": [],
            }

    warnings = []
    if not _is_complete(state, "rival_rosters"):
        warnings.append(
            "Las plantillas de rivales aún son parciales; se incorporarán "
            "progresivamente y esa limitación se mostrará en cada análisis."
        )

    return {
        "stage": "ready",
        "flow": _destination_flow(trigger),
        "questions": [],
        "warnings": warnings,
    }

