import time
import logging

from pathlib import Path
from typing import AsyncIterator
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from app.trie import Trie
from app.loader import load_dictionary
from app.routers import autocomplete as autocomplete_router

BASE_DIR = Path(__file__).parent.parent

logging.basicConfig(
    level=getattr(logging, "INFO"),
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Load dictionary into Trie on application startup with proper error handling

    Raises:
        RuntimeError: If dictionary cannot be loaded or has no valid words
    """
    trie = Trie()

    try:
        start_time = time.time()
        words = load_dictionary(BASE_DIR / "resources/dictionnaries/starwars_8k_2018.txt")

        for word in words:
            trie.insert(word)

        load_time = time.time() - start_time
        logger.info(f"Trie built successfully in {load_time:.2f}s")

    except FileNotFoundError as e:
        raise RuntimeError(f"Failed to load dictionary file: ") from e
    except ValueError as e:
        raise RuntimeError(f"Configuration or dictionary validation failed: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Service initialization failed: {e}") from e

    app.state.trie = trie
    yield


app = FastAPI(
    title="Autocomplete Service",
    description="Trie-based autocomplete API",
    lifespan=lifespan,
)

app.include_router(autocomplete_router.router)
