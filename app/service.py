import time
import logging
from pathlib import Path
from typing import List

from app.trie import Trie
from app.loader import load_dictionary

DICTIONARY_PATH = "resources/dictionaries/starwars_8k_2018.txt"

logger = logging.getLogger(__name__)

class TrieService:
    """Encapsulates trie-based autocomplete functionality

    :param base_dir: Base directory for resolving the dictionary file path
    :raises FileNotFoundError: If the dictionary file does not exist
    :raises ValueError: If the dictionary file contains no valid words
    """

    def __init__(self, base_dir: Path) -> None:
        self._trie = Trie()
        self._load_dictionary(base_dir)

    def _load_dictionary(self, base_dir: Path) -> None:
        """Load dictionary file and populate the trie

        :param base_dir: Base directory for resolving the dictionary file path
        """
        start_time = time.time()

        dictionary_path = base_dir / DICTIONARY_PATH
        result = load_dictionary(dictionary_path)

        for word in result.words:
            self._trie.insert(word)

        load_time = time.time() - start_time
        logger.info(f"Trie built with {len(result.words)} words in {load_time:.2f}s (skipped {result.skipped_count} malformed lines)")

    def search(self, query: str) -> List[str]:
        """Search for words matching the given prefix

        :param query: The prefix to search for (will be lowercased)
        :return: List of matching words in alphabetical order
        """
        return self._trie.search(query)
