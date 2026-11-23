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


def fetch_url(url: str) -> str:
    """Download `url` and return the page text without chrome or scripts."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(_DROP_TAGS):
        tag.decompose()

    text = soup.get_text(strip=True)
    lines = [line for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def fetch_top_results(results: list[dict], n: int = 3) -> list[dict]:
    """Fetch the first `n` search results. Each page includes a `text` field."""
    pages = []
    for result in results[:n]:
        pages.append({**result, "text": fetch_url(result["url"])})
    return pages
