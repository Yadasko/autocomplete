import time
import logging
from functools import lru_cache

from pathlib import Path
from typing import AsyncIterator
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from app.trie import Trie
from app.loader import load_dictionary
from app.routers import autocomplete as autocomplete_router
from app.settings import Settings

BASE_DIR = Path(__file__).parent.parent

logging.basicConfig(
    level=getattr(logging, "INFO"),
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Load dictionary into Trie on application startup with proper error handling

    :raises RuntimeError: If dictionary cannot be loaded or has no valid words
    """
    settings = Settings()
    trie = Trie()

    try:
        start_time = time.time()
        words = load_dictionary(BASE_DIR / settings.dictionary_path)

        for word in words:
            trie.insert(word)

        load_time = time.time() - start_time
        logger.info(f"Trie built successfully in {load_time:.2f}s")

    except FileNotFoundError as e:
        raise RuntimeError(f"Failed to load dictionary file: {settings.dictionary_path}") from e
    except ValueError as e:
        raise RuntimeError(f"Configuration or dictionary validation failed: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Service initialization failed: {e}") from e

    app.state.settings = settings
    app.state.trie = trie

    @lru_cache(maxsize=settings.cache_max_size if settings.cache_enabled else 0)
    def cached_search(query: str) -> list:
        return trie.search(query, limit=settings.autocomplete_limit)

    app.state.cached_search = cached_search
    yield


app = FastAPI(
    title="Autocomplete Service",
    description="Trie-based autocomplete API",
    lifespan=lifespan,
)

app.include_router(autocomplete_router.router)
