from datetime import datetime
from pathlib import Path
import unittest

from scripts.public_data.parse import ParseError, normalize_name, parse_market_html


FIXTURES = Path(__file__).parent / "fixtures"
RETRIEVED_AT = datetime.fromisoformat("2026-09-27T12:00:00+02:00")


class ParseMarketHtmlTests(unittest.TestCase):
    def test_parses_identity_market_value_and_probability(self):
        snapshot = parse_market_html(
            (FIXTURES / "valid_market.html").read_text(), RETRIEVED_AT
        )

        self.assertEqual(snapshot.platform, "laliga_fantasy_oficial")
        self.assertEqual(snapshot.source_updated_at.isoformat(), "2026-09-27T03:00:00+02:00")
        self.assertEqual(snapshot.players[0].id, "futbolfantasy:13036")
        self.assertEqual(snapshot.players[0].name, "Yoel Lago")
        self.assertEqual(snapshot.players[0].team, "Celta")
        self.assertEqual(snapshot.players[0].position, "DEF")
        self.assertEqual(snapshot.market_values[0].value, 10_825_329)
        self.assertEqual(snapshot.market_values[0].daily_change, 522_098)
        self.assertEqual(snapshot.starter_probabilities[0].value, 95)
        self.assertEqual(snapshot.starter_probabilities[0].target_matchday, 8)

    def test_normalizes_accents_and_punctuation(self):
        self.assertEqual(normalize_name("Kylian Mbappé"), "kylian_mbappe")
        self.assertEqual(normalize_name("  João-Félix Jr. "), "joao_felix_jr")

    def test_rejects_page_without_canonical_platform_identity(self):
        with self.assertRaisesRegex(ParseError, "canonical platform"):
            parse_market_html(
                (FIXTURES / "ambiguous_platform.html").read_text(), RETRIEVED_AT
            )

    def test_rejects_malformed_required_row_field(self):
        html = (FIXTURES / "valid_market.html").read_text().replace(
            'data-valor="10825329"', 'data-valor="ten-million"', 1
        )
        with self.assertRaisesRegex(ParseError, "market value"):
            parse_market_html(html, RETRIEVED_AT)

    def test_rejects_truncated_market_table(self):
        html = (FIXTURES / "valid_market.html").read_text().split("</tbody>", 1)[0]
        with self.assertRaisesRegex(ParseError, "closed market table"):
            parse_market_html(html, RETRIEVED_AT)

    def test_rejects_out_of_range_probability(self):
        html = (FIXTURES / "valid_market.html").read_text().replace("95%", "105%", 1)
        with self.assertRaisesRegex(ParseError, "starter probability"):
            parse_market_html(html, RETRIEVED_AT)

    def test_rejects_source_timestamp_too_far_in_future(self):
        html = (FIXTURES / "valid_market.html").read_text().replace(
            "27/09/2026 03:00", "27/09/2026 12:30", 1
        )
        with self.assertRaisesRegex(ParseError, "future"):
            parse_market_html(html, RETRIEVED_AT)

    def test_finds_update_timestamp_when_later_small_elements_exist(self):
        html = (FIXTURES / "valid_market.html").read_text().replace(
            "</body>", "<footer><small>Texto legal</small></footer></body>"
        )
        snapshot = parse_market_html(html, RETRIEVED_AT)
        self.assertEqual(
            snapshot.source_updated_at.isoformat(), "2026-09-27T03:00:00+02:00"
        )


if __name__ == "__main__":
    unittest.main()
