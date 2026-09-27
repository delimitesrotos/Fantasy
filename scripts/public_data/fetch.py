"""Conservative HTTP boundary for the canonical public source."""

from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .parse import CANONICAL_URL


USER_AGENT = "FantasyPublicData/1.0 (+https://github.com/delimitesrotos/Fantasy)"


class FetchError(RuntimeError):
    """Raised when a public response is unavailable or unsafe to parse."""


def fetch_html(
    url: str = CANONICAL_URL,
    timeout: int = 30,
    max_bytes: int = 8_000_000,
    opener: Callable = urlopen,
) -> str:
    request = Request(
        url,
        headers={"Accept": "text/html", "User-Agent": USER_AGENT},
        method="GET",
    )
    try:
        with opener(request, timeout=timeout) as response:
            content_type = response.headers.get_content_type()
            if content_type != "text/html":
                raise FetchError("source did not return HTML")
            body = response.read(max_bytes + 1)
            if len(body) > max_bytes:
                raise FetchError("source response exceeds maximum size")
            charset = response.headers.get_content_charset() or "utf-8"
    except FetchError:
        raise
    except (HTTPError, URLError, OSError) as error:
        raise FetchError("source request failed: {}".format(error)) from error
    try:
        return body.decode(charset)
    except (LookupError, UnicodeDecodeError) as error:
        raise FetchError("source response encoding is invalid") from error
