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

    :param query: Prefix to search for
    :return: List of matching words, up to the configured limit
    :raises HTTPException: 400 if query exceeds max length
    :raises HTTPException: 500 if search fails
    """
    service = request.app.state.service
    query = query.strip()

    if len(query) > service.settings.max_query_length:
        raise HTTPException(
            status_code=400,
            detail=f"Query too long. Maximum length is {service.settings.max_query_length} characters."
        )

    try:
        return service.search(query)

    except Exception:
        logger.exception("Search failed for query: %s", query)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during search. Please try again later."
        )
