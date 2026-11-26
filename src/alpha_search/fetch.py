"""Fetch an article URL and return its visible text."""

import requests
from bs4 import BeautifulSoup

_DROP_TAGS = (
    "script",
    "style",
    "noscript",
    "svg",
    "iframe",
    "form",
    "nav",
    "header",
    "footer",
    "img",
    "link",
    "meta",
    "title",
    "base",
    "head",
)

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_url(url: str) -> dict:
    """Download `url` and return clean text.

    Always returns a dict so one bad site does not crash the pipeline:
    {"ok": bool, "text": str, "error": str | None}
    """
    try:
        response = requests.get(url, timeout=30, headers=_HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(_DROP_TAGS):
            tag.decompose()

        text = soup.get_text(strip=True)
        lines = [line for line in text.splitlines() if line.strip()]
        return {"ok": True, "text": "\n".join(lines), "error": None}
    except Exception as exc:
        return {"ok": False, "text": "", "error": str(exc)}


def fetch_top_results(results: list[dict], n: int = 3) -> list[dict]:
    """Fetch the first `n` search results. Each page includes ok/text/error."""
    pages = []
    for result in results[:n]:
        fetched = fetch_url(result["url"])
        pages.append({**result, **fetched})
    return pages
