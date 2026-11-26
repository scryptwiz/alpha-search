from alpha_search.search import load_entries
from rank_bm25 import BM25Okapi

def tokenize(text: str) -> list[str]:
    """Tokenize text into words."""
    return text.lower().split()


def search_bm25(query: str, entries: list[dict] | None = None) -> list[dict]:
    """Rank Alpha titles with BM25 (sparse keyword search v2)."""

    query_words = query.lower().split()
    if entries is None:
        entries = load_entries()

    tokenized_corpus = [tokenize(entry["title"]) for entry in entries]
    bm25 = BM25Okapi(tokenized_corpus)
    scores = bm25.get_scores(query_words)

    results = [
        {**entry, "score": float(score)}
        for entry, score in zip(entries, scores)
        if score > 0
    ]
    results.sort(key=lambda item: item["score"], reverse=True)
    return results