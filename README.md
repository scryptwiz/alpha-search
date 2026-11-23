# alpha-search

Search the Alpha reading list, then fetch the matching articles.

```
alpha-search/
├── data/
│   └── alpha_entries.txt          # scraped list
├── notebooks/
│   └── 01_fetch.ipynb             # scrape, search, then fetch
├── src/
│   └── alpha_search/
│       ├── __init__.py
│       ├── search.py              # search_alpha(query)
│       └── fetch.py               # fetch_url, fetch_top_results
└── pyproject.toml
```

| Place | Role |
| --- | --- |
| `src/alpha_search/*.py` | Reusable functions |
| `notebooks/` | Experiments. Call the functions, print the output |
| `data/` | Saved lists |

From a notebook:

```python
from alpha_search.search import search_alpha
from alpha_search.fetch import fetch_url, fetch_top_results

results = search_alpha("docker compose")
pages = fetch_top_results(results, n=3)
```

The package is installed editable from this repo, so those imports resolve to `src/alpha_search`.
