# Autocomplete API

A FastAPI-based autocomplete service using a Trie data structure for prefix-based word suggestions

## Features

- Trie-based prefix search for efficient lookups
- Unicode support
- Docker-ready

## Quick Start

```bash
uv sync
uvicorn app.api:app
```

Test the API:
```bash
curl "http://localhost:8000/autocomplete?query=dar"
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/autocomplete?query=<prefix>` | GET | Returns matching words |
| `/health` | GET | Health check for orchestration |

## Docker

```bash
docker build -t autocomplete .
docker run -p 8000:8000 autocomplete
```

## Testing

```bash
uv run pytest
```

## Notes, optimizations and enhancements

### Sorting keys on Trie search
The implementation of the Trie search alphabeticaly sorts the children of a node at every new node to ensure the alphabetical ordering of the results.
While this has no performance impact in our dataset of 8000k words, we could instead sort the words at insertion, to increase our start-up time but reduce our search time.

Another solution would be to use `sorteddicts`, adding another dependency to the app.

### Caching the results for fast response time
A cache could be put in place, either directly on the fastAPI route, or in the service/Trie class. This would allow for a fast response on cache hits and add a very minimal response time overhead on cache misses, the trade-off being the memory usage. With our dataset, the performance boost achieved by adding a cache is negligeable. 
Adding a cache also raises concurrency issues when using multi-threaded web servers.

### Optimizing storage of the Trie
The use of the `__slots__` attributes on the children of the `Trie` could reduce the memory taken by specifying what type of data is getting stored.

While this could reduce the memory usage by some margin, it is overkill for this assignment. If the dictionnary were to expand by a lot, and profilling exposed a large memory consumption by the Trie structure, or if the app were to be running a constraint environnement (i.e a small pod in the cloud), this could be an easy way to reduce its memory footprint.

### Make it production ready
This app is lacking features to be production-ready:
- Unified logging
  - Easily parseable format like JSON
  - Metrics (i.e response time, cache hit/miss)
  - Request ID tracing for correlation
- Environnement configuration (.env)
- More thorough input validation on both input dictionnaries and web queries
  - Only alphanumeric enforced by regex?
- Rate limiting
- Pagination
  - Adding limit and offset/page query parameters to get more matching words