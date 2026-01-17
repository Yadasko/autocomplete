from typing import List
from fastapi import FastAPI, HTTPException, Query, Request, logger

from app.trie import Trie

trie: Trie = Trie()
words = ["apple", "application", "appetite", "afternoon", "after-dark", "banana", "band", "bandana", "bandwidth",
         "cat", "cater", "caterpillar", "dog", "dodge", "doll", "dolphin", "elephant"]

for word in words:
    trie.insert(word)


app = FastAPI(
    title="Autocomplete Service",
    description="Trie-based autocomplete API"
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
