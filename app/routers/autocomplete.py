import logging
from typing import Dict, List

from fastapi import APIRouter, HTTPException, Query, Request

logger = logging.getLogger(__name__)

router = APIRouter(tags=["autocomplete"])

_cache: Dict[str, List[str]] = {}


@router.get("/autocomplete", response_model=List[str])
async def autocomplete(
    request: Request,
    query: str = Query(..., description="Prefix to search for", min_length=1),
) -> List[str]:
    """
    Find words in the trie that start with the given prefix

    :param query: What to search for
    :type query: str
    :return: List of words that start with the given prefix, maximum of 4 words
    :rtype: List[str]
    :raises HTTPException: If there's an internal server error during search
    :raises HTTPException: If the query exceeds 50 characters
    """
    settings = request.app.state.settings
    query = query.strip()

    if len(query) > settings.max_query_length:
        raise HTTPException(
            status_code=400,
            detail=f"Query too long. Maximum length is {settings.max_query_length} characters."
        )

    cache_key = query.lower()
    if settings.cache_enabled and cache_key in _cache:
        return _cache[cache_key]

    try:
        results = request.app.state.trie.search(query, limit=settings.autocomplete_limit)
        if settings.cache_enabled:
            _cache[cache_key] = results
        return results

    except Exception as e:
        logger.exception("Search failed for query: %s", query)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during search. Please try again later."
        )
