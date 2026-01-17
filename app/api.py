from pathlib import Path
from typing import AsyncIterator, List
from fastapi import FastAPI, HTTPException, Query, Request, logger
from fastapi.concurrency import asynccontextmanager

from app.trie import Trie
from app.loader import load_dictionary

BASE_DIR = Path(__file__).parent.parent

trie: Trie = Trie()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Load dictionary into Trie on application startup with proper error handling

    Raises:
        RuntimeError: If dictionary cannot be loaded
    """
  
    try:
        words = load_dictionary(BASE_DIR / "resources/dictionnaries/starwars_8k_2018.txt")
        
        for word in words:
            trie.insert(word)

    except FileNotFoundError as e:
        raise RuntimeError(f"Failed to load dictionary file: ") from e
    except ValueError as e:
        raise RuntimeError(f"Configuration or dictionary validation failed: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Service initialization failed: {e}") from e

    yield

app = FastAPI(
    title="Autocomplete Service",
    description="Trie-based autocomplete API",
    lifespan=lifespan,
)

@app.get("/autocomplete", response_model=List[str])
async def autocomplete(
    query: str = Query(..., description="Prefix to search for", min_length=1),
) -> List[str]:
    """
    Find words in the trie that start with the given prefix
    
    :param query: What to search for
    :type query: str
    :return: List of words that start with the given prefix, maximum of 4 words
    :rtype: List[str]
    :raises HTTPException: If there's an internal server error during search
    """

    try:
       return trie.search(query, limit=4)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error during search. Please try again later."
        )
