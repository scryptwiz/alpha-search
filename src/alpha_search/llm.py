from openai import OpenAI

from alpha_search.context import build_context

_EXTRACT_SYSTEM = (
    "You extract search keywords for a reading-list title search.\n"
    "Given a user question, return 2 to 6 important keywords or a short search phrase.\n"
    "Focus on named entities, topics, and distinctive terms.\n"
    "Remove filler (please, can you, explain, I heard that, etc.).\n"
    "Return ONLY the keywords on one line, space-separated. "
    "No punctuation, no quotes, no explanation."
)

_ANSWER_SYSTEM = (
    "You are a helpful retrieval assistant for Alpha Search.\n"
    "Your job is to answer the user's question using ONLY the source articles "
    "provided in the message. Do not use outside knowledge. Do not invent facts, "
    "quotes, or links.\n"
    "If the sources do not contain enough information, say you don't know and "
    "suggest a better search query.\n"
    "When you use information from a source, ground the answer in that source.\n"
    "At the end of every reply, add a Sources section listing each article you "
    "used in this format:\n"
    "Sources:\n"
    "- Title — URL\n"
    "Only list sources you actually used. Prefer concise, direct answers."
)


def extract_search_query(
    question: str,
    *,
    client: OpenAI | None = None,
    model: str = "gpt-4o-mini",
) -> str:
    """Turn a long question into a short keyword query for Alpha search."""
    client = client or OpenAI()

    extract = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": _EXTRACT_SYSTEM},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )

    raw = extract.choices[0].message.content or ""
    query = raw.strip().lower()

    for ch in ",.?!;:\"'`":
        query = query.replace(ch, " ")

    words = [w for w in query.split() if w][:6]
    if not words:
        return question.strip().lower()
    return " ".join(words)


def answer_from_sources(
    question: str,
    pages: list[dict],
    *,
    client: OpenAI | None = None,
    model: str = "gpt-4o-mini",
    max_chars: int = 6000,
) -> str:
    """Answer `question` using only the fetched Alpha source pages."""
    client = client or OpenAI()
    usable = [p for p in pages if (p.get("text") or "").strip()]
    if not usable:
        return (
            "I couldn't read any of the source pages, so I don't know. "
            "Try a different search query."
        )

    context = build_context(usable, max_chars=max_chars)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": _ANSWER_SYSTEM},
            {
                "role": "user",
                "content": (
                    f"Question: {question}\n\n"
                    f"Source articles:\n\n"
                    f"{context}"
                ),
            },
        ],
    )
    return response.choices[0].message.content or ""
