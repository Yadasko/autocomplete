from pathlib import Path
from typing import List



def load_dictionary(file_path: Path) -> List[str]:
    """
    Load dictionary from file.
    Expected file format: Each line contains "XXXXX word"
    where XXXXX is a numbering scheme (can be ignored) and word is the actual word.
    (Format taken from eff wordlists, with the introduction removed)

    :param file_path: Path to the dictionary file
    :type file_path: Path
    :return: List of words from the dictionary
    :rtype: List[str]
    """

    if not file_path.exists():
        raise FileNotFoundError(f"Dictionary file not found: {file_path}")
    
    words: List[str] = []
    
    with open(file_path, "r", encoding="utf-8") as f:
        for _, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) < 2:
                # Skip malformed lines
                continue

            word = parts[-1]
            words.append(word)

    if not words:
        raise ValueError(f"No valid words found in {file_path}")

    return words