# Hoopla

A search engine for a movie streaming platform, built from scratch in Python. The goal is to go from basic keyword matching all the way to a full RAG (Retrieval-Augmented Generation) pipeline — no black-box libraries for the core search logic.

## What this is

Most "AI search" tutorials have you glue together three API calls and call it a day. This project takes a different approach: every layer of the search stack is implemented by hand so I actually understand what's happening under the hood.

The roadmap:

1. **Keyword Search** — text preprocessing, inverted indexes, TF-IDF, BM25 scoring ✅
2. **Semantic Search** — dense vector embeddings, cosine similarity *(in progress)*
3. **Hybrid Search** — blending keyword + semantic scores
4. **RAG** — retrieve context → augment prompt → generate answers with Gemini

## Current state

Right now the keyword search pipeline is functional. You can run BM25-ranked queries against a ~26 MB movie dataset from the CLI.

What's implemented:
- Text cleaning (lowercasing, punctuation removal, tokenization, stop word removal, Porter stemming)
- Inverted index with pickle-based disk caching
- TF-IDF scoring
- Full BM25 with IDF smoothing, term frequency saturation (`k1=1.5`), and document length normalization (`b=0.75`)

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
# clone and enter the project
git clone https://github.com/Saumajitt/rag-search-engine.git
cd rag-search-engine

# create a virtual environment
uv venv
# windows
.venv\Scripts\activate
# mac/linux
source .venv/bin/activate

# install dependencies
uv sync
```

You'll need the movie dataset in `data/movies.json` — it's not checked into version control due to size. Grab it from the [boot.dev course](https://www.boot.dev/) or place your own JSON file with the structure:

```json
{
  "movies": [
    { "id": 1, "title": "...", "description": "..." },
    ...
  ]
}
```

You'll also need `data/stopwords.txt` (one word per line).

## Usage

All commands are run from the project root.

```bash
# build the inverted index (run this first)
uv run cli/keyword_search_cli.py build

# keyword search
uv run cli/keyword_search_cli.py search "space adventure"

# inspect scoring
uv run cli/keyword_search_cli.py tf 424 trapper
uv run cli/keyword_search_cli.py idf grizzly
uv run cli/keyword_search_cli.py tfidf 424 trapper
uv run cli/keyword_search_cli.py bm25_idf grizzly
uv run cli/keyword_search_cli.py bm25_tf 424 trapper
uv run cli/keyword_search_cli.py bm25_search "space adventure"
```

## Project structure

```
rag-search-engine/
├── data/
│   ├── movies.json          # movie dataset (~26 MB, gitignored)
│   └── stopwords.txt        # stop words list
├── cache/                   # auto-generated pickle files
├── cli/
│   ├── keyword_search_cli.py
│   ├── semantic_search_cli.py
│   └── lib/
│       ├── search_utils.py       # data loading, constants
│       ├── keyword_search.py     # inverted index, BM25
│       └── semantic_search.py    # embeddings (wip)
├── pyproject.toml
└── README.md
```

## How BM25 works (briefly)

BM25 scores a document against a query by combining two ideas:

- **Term frequency with saturation** — the first few mentions of a word matter a lot, but repeated mentions have diminishing returns. Controlled by `k1`.
- **Inverse document frequency** — rare terms are weighted higher than common ones. A word that appears in every movie description tells you nothing.
- **Length normalization** — a short document mentioning "salmon" 3 times is probably more about salmon than a 10-page document mentioning it 4 times. Controlled by `b`.

The final score for a document is the sum of `BM25(term)` across all query terms.

## What's next

- [ ] Semantic search with `all-MiniLM-L6-v2` embeddings
- [ ] Hybrid scoring (keyword + vector)
- [ ] Chunking strategies for better retrieval
- [ ] Re-ranking and evaluation
- [ ] RAG with Gemini API
- [ ] Agentic query refinement
- [ ] Multimodal search (text + images)

## Credits

Built while working through the [RAG course on boot.dev](https://www.boot.dev/), taught by Isaac Flath.
