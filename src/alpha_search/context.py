"""Format fetched pages into LLM prompt context."""


def build_context(pages: list[dict], max_chars: int = 6000) -> str:
    """Format fetched pages into a single prompt context string.

    Skips pages with no text (e.g. failed fetches).
    """
    blocks = []
    for i, page in enumerate(pages, start=1):
        text = (page.get("text") or "").strip()
        if not text:
            continue
        blocks.append(
            f"[{i}] {page['title']}\n"
            f"URL: {page['url']}\n\n"
            f"{text[:max_chars]}"
        )
    return "\n\n---\n\n".join(blocks)
