import logging
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.concurrency import asynccontextmanager

from app.routers import autocomplete as autocomplete_router
from app.service import TrieService

BASE_DIR = Path(__file__).parent.parent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialize the autocomplete service on application startup"""
    try:
        service = TrieService(BASE_DIR)
    except FileNotFoundError as e:
        raise RuntimeError(f"Failed to load dictionary: {e}") from e

    app.state.service = service
    yield


app = FastAPI(
    title="Autocomplete Service",
    description="Trie-based autocomplete API",
    lifespan=lifespan,
)

app.include_router(autocomplete_router.router)


@app.get("/health")
async def health(request: Request) -> JSONResponse:
    """Health check endpoint for orchestration purposes.

    Returns 200 when the server is ready and the dictionary is loaded.
    Returns 503 if the service is not ready.
    """
    if hasattr(request.app.state, "service") and request.app.state.service is not None:
        return JSONResponse(status_code=200, content={"status": "healthy"})
    return JSONResponse(status_code=503, content={"status": "unhealthy"})
