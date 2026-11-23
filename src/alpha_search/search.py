"""Algorithm 0: score Alpha titles by query-word overlap."""

from pathlib import Path


def project_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise FileNotFoundError(f"Could not find the project root from {here}")


def entries_path() -> Path:
    return project_root() / "data" / "alpha_entries.txt"


def load_entries(path: Path | None = None) -> list[dict]:
    path = path or entries_path()
    entries = []
    for index, line in enumerate(path.read_text().splitlines()):
        line = line.strip()
        if not line:
            continue
        url, _, title = line.partition(" ")
        entries.append({"id": index, "url": url, "title": title})
    return entries


def search_alpha(query: str, entries: list[dict] | None = None) -> list[dict]:
    """Return title matches for `query`, highest score first.

    A result scores 1 for each query word that appears in the title.
    """
    if entries is None:
        entries = load_entries()

    query_words = query.lower().split()
    results = []
    for entry in entries:
        title = entry["title"].lower()
        score = sum(1 for word in query_words if word in title)
        if score > 0:
            results.append({**entry, "score": score})

    results.sort(key=lambda item: item["score"], reverse=True)
    return results
