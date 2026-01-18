import logging
from typing import List

from fastapi import APIRouter, HTTPException, Query, Request

MAX_QUERY_LENGTH = 50

logger = logging.getLogger(__name__)
router = APIRouter(tags=["autocomplete"])

@router.get("/autocomplete", response_model=List[str])
async def autocomplete(
    request: Request,
    query: str = Query(..., description="Prefix to search for", min_length=1),
) -> List[str]:
    """Find words in the trie that start with the given prefix

    :param request: FastAPI request object
    :param query: Prefix to search for
    :return: List of matching words, up to the configured limit
    :raises HTTPException: 400 if query is empty after stripping or exceeds max length
    :raises HTTPException: 500 if search fails
    """
    service = request.app.state.service
    query = query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty or contain only whitespace"
        )

    if len(query) > MAX_QUERY_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Query too long. Maximum length is {MAX_QUERY_LENGTH} characters"
        )

    try:
        return service.search(query)

    except Exception:
        logger.exception("Search failed for query: %s", query)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during search. Please try again later"
        )
