import logging
from typing import List

from fastapi import APIRouter, HTTPException, Query, Request

logger = logging.getLogger(__name__)

router = APIRouter(tags=["autocomplete"])


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
    :raises HTTPException: If the query exceeds {settings.max_query_length} characters
    """
    settings = request.app.state.settings
    query = query.strip()

    if len(query) > settings.max_query_length:
        raise HTTPException(
            status_code=400,
            detail=f"Query too long. Maximum length is {settings.max_query_length} characters."
        )

    try:
        return request.app.state.cached_search(query.lower())

    except Exception as e:
        logger.exception("Search failed for query: %s", query)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during search. Please try again later."
        )
