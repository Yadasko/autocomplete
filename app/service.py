import time
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any, List

from app.trie import Trie
from app.loader import load_dictionary
from app.settings import Settings

logger = logging.getLogger(__name__)

class TrieService:
    """
    Encapsulates trie-based autocomplete functionality with optional caching

    This service handles:
    - Loading dictionary and building the trie
    - Caching search results (when enabled)
    """

    def __init__(self, settings: Settings, base_dir: Path) -> None:
        self._settings = settings
        self._trie = Trie()
        self._cached_search: Any = None
        self._load_dictionary(base_dir)
        self._setup_cache()

    def _load_dictionary(self, base_dir: Path) -> None:
        """Load dictionary file and populate the trie"""
        start_time = time.time()

        dictionary_path = base_dir / self._settings.dictionary_path
        result = load_dictionary(dictionary_path)

        for word in result.words:
            self._trie.insert(word)

        load_time = time.time() - start_time
        logger.info(f"Trie built with {len(result.words)} words in {load_time:.2f}s (skipped {result.skipped_count} malformed lines)")

    def _setup_cache(self) -> None:
        """Configure the search cache based on settings"""
        if self._settings.cache_enabled:
            
            limit = self._settings.autocomplete_limit

            @lru_cache(maxsize=self._settings.cache_max_size)
            def cached_search(query: str) -> List[str]:
                return self._trie.search(query, limit)

            self._cached_search = cached_search
        else:
            # No caching - call trie directly
            self._cached_search = None

    def search(self, query: str) -> List[str]:
        """
        Search for words matching the given prefix

        :param query: The prefix to search for (will be lowercased)
        :return: List of matching words, up to the configured limit
        """
        if self._cached_search is not None:
            return self._cached_search(query)

        return self._trie.search(query, self._settings.autocomplete_limit)

    def clear_cache(self) -> None:
        """Clear the search cache. No-op if caching is disabled"""
        if self._cached_search is not None:
            self._cached_search.cache_clear()

    def cache_info(self):
        """Return cache statistics, or None if caching is disabled"""
        if self._cached_search is not None:
            return self._cached_search.cache_info()
        return None

    @property
    def settings(self) -> Settings:
        return self._settings
