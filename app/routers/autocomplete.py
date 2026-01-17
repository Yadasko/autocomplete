from typing import Dict, List

from fastapi import APIRouter, HTTPException, Query, Request

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
    query = query.strip()

    if len(query) > 50:
        raise HTTPException(
            status_code=400,
            detail="Query too long. Maximum length is 50 characters."
        )

    if query in _cache:
        return _cache[query]

    try:
        results = request.app.state.trie.search(query, limit=4)
        _cache[query] = results
        return results

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error during search. Please try again later."
        )
