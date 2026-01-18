from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class DictionaryResult:
    """
    Result of loading a dictionary file

    :param words: List of valid words loaded from the file
    :param skipped_count: Number of malformed lines that were skipped
    """
    words: List[str]
    skipped_count: int


def load_dictionary(file_path: Path) -> DictionaryResult:
    """Load dictionary from file

    Expected file format: Each line contains "XXXXX word" where XXXXX is a
    numbering scheme (ignored) and word is the actual word.

    :param file_path: Path to the dictionary file.
    :return: DictionaryResult containing words and count of skipped lines.
    :raises FileNotFoundError: If the dictionary file does not exist.
    :raises ValueError: If no valid words are found in the file.
    """

    if not file_path.exists():
        raise FileNotFoundError(f"Dictionary file not found: {file_path}")
    
    words: List[str] = []
    skipped_count = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) < 2:
                skipped_count += 1
                continue

            word = parts[-1]
            words.append(word)

    if not words:
        raise ValueError(f"No valid words found in {file_path}")

    return DictionaryResult(words=words, skipped_count=skipped_count)