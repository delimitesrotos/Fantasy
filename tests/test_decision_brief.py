import unittest

from scripts.private_state.decision_brief import (
    DecisionBriefError,
    event_from_confirmed_choice,
    validate_decision_brief,
)


def valid_option(name):
    return {
        "name": name,
        "upside": "Mejora el once esta jornada",
        "downside": "Reduce el colchón de caja",
        "impact": "Sustituye al defensa con menor expectativa",
        "conditions": "Solo si el precio no supera 8,2 M€",
        "reversibility": "Media: puede venderse, con riesgo de pérdida",
        "confidence": "media",
    }


class DecisionBriefTests(unittest.TestCase):
    def test_rejects_bare_buy_instruction(self):
        with self.assertRaisesRegex(DecisionBriefError, "context"):
            validate_decision_brief({"recommendation": "Compra a X"})

    def test_rejects_single_option(self):
        brief = {
            "decision": "Qué hacer con X antes de las 20:00",
            "context": [{"fact": "Precio 8 M€", "source": "app", "freshness": "hoy"}],
            "unknowns": ["Once oficial aún no publicado"],
            "options": [valid_option("Pujar")],
            "preference": "Pujar hasta 8,2 M€ por mejora marginal",
            "switch_threshold": "No pujar si supera 8,2 M€",
            "choice_question": "¿Qué opción eliges?",
        }

        with self.assertRaisesRegex(DecisionBriefError, "two options"):
            validate_decision_brief(brief)

    def test_accepts_contextualized_alternatives(self):
        brief = {
            "decision": "Qué hacer con X antes de las 20:00",
            "context": [{"fact": "Precio 8 M€", "source": "app", "freshness": "hoy"}],
            "unknowns": ["Once oficial aún no publicado"],
            "options": [valid_option("Pujar"), valid_option("No actuar")],
            "preference": "Pujar hasta 8,2 M€ por mejora marginal",
            "switch_threshold": "No pujar si supera 8,2 M€",
            "choice_question": "¿Qué opción eliges?",
        }

        self.assertIs(validate_decision_brief(brief), brief)

    def test_unconfirmed_choice_cannot_create_event(self):
        with self.assertRaisesRegex(DecisionBriefError, "confirmation"):
            event_from_confirmed_choice(
                event_type="BUY",
                player_id="laliga:123",
                amount=8_000_000,
                confirmed=False,
            )

    def test_confirmed_choice_creates_append_only_event(self):
        event = event_from_confirmed_choice(
            event_type="BUY",
            player_id="laliga:123",
            amount=8_000_000,
            confirmed=True,
        )

        self.assertEqual(event["event_type"], "BUY")
        self.assertEqual(event["player_id"], "laliga:123")
        self.assertEqual(event["amount"], 8_000_000)
        self.assertTrue(event["confirmed"])
        self.assertIn("event_id", event)
        self.assertIn("recorded_at", event)


if __name__ == "__main__":
    unittest.main()
