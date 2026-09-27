from email.message import Message
import unittest

from scripts.public_data.fetch import FetchError, USER_AGENT, fetch_html


class FakeResponse:
    def __init__(self, body, content_type="text/html; charset=UTF-8"):
        self.body = body
        self.headers = Message()
        self.headers["Content-Type"] = content_type

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self, amount):
        return self.body[:amount]


class RecordingOpener:
    def __init__(self, response):
        self.response = response
        self.requests = []

    def __call__(self, request, timeout):
        self.requests.append((request, timeout))
        return self.response


class FetchHtmlTests(unittest.TestCase):
    def test_fetches_html_with_explicit_user_agent(self):
        opener = RecordingOpener(FakeResponse(b"<html>hola</html>"))
        self.assertEqual(fetch_html(opener=opener), "<html>hola</html>")
        request, timeout = opener.requests[0]
        self.assertEqual(request.get_header("User-agent"), USER_AGENT)
        self.assertEqual(timeout, 30)

    def test_rejects_non_html_response(self):
        opener = RecordingOpener(FakeResponse(b"{}", "application/json"))
        with self.assertRaisesRegex(FetchError, "HTML"):
            fetch_html(opener=opener)

    def test_rejects_response_above_byte_ceiling(self):
        opener = RecordingOpener(FakeResponse(b"123456"))
        with self.assertRaisesRegex(FetchError, "maximum"):
            fetch_html(opener=opener, max_bytes=5)

    def test_decodes_declared_charset(self):
        opener = RecordingOpener(
            FakeResponse("Fútbol".encode("iso-8859-1"), "text/html; charset=iso-8859-1")
        )
        self.assertEqual(fetch_html(opener=opener), "Fútbol")


if __name__ == "__main__":
    unittest.main()
