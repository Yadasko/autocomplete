import time
import logging
from pathlib import Path
from typing import List

from app.trie import Trie
from app.loader import load_dictionary
from app.settings import Settings

logger = logging.getLogger(__name__)

class TrieService:
    """Encapsulates trie-based autocomplete functionality"""

    def __init__(self, settings: Settings, base_dir: Path) -> None:
        self._settings = settings
        self._trie = Trie()
        self._load_dictionary(base_dir)

    def _load_dictionary(self, base_dir: Path) -> None:
        """Load dictionary file and populate the trie"""
        start_time = time.time()

        dictionary_path = base_dir / self._settings.dictionary_path
        result = load_dictionary(dictionary_path)

        for word in result.words:
            self._trie.insert(word)

        load_time = time.time() - start_time
        logger.info(f"Trie built with {len(result.words)} words in {load_time:.2f}s (skipped {result.skipped_count} malformed lines)")

    def search(self, query: str) -> List[str]:
        """
        Search for words matching the given prefix

        :param query: The prefix to search for (will be lowercased)
        :return: List of matching words, up to the configured limit
        """
        return self._trie.search(query, self._settings.autocomplete_limit)

    @property
    def settings(self) -> Settings:
        return self._settings
