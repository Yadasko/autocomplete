from typing import Dict, List

DEFAULT_SEARCH_LIMIT = 4

class TrieNode:
    """A single node in the trie structure

    :ivar children: Mapping of characters to child nodes
    :ivar is_end_of_word: Whether this node marks the end of a valid word
    """

    def __init__(self) -> None:
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False


class Trie:
    """A trie (prefix tree) data structure for efficient prefix-based word lookup"""

    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert a word into the trie

        :param word: The word to insert (will be lowercased)
        """
        node = self.root
        word = word.lower()
    
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_end_of_word = True


    def search(self, prefix: str, limit: int = DEFAULT_SEARCH_LIMIT) -> List[str]:
        """Find words in the trie that start with the given prefix

        :param prefix: The prefix to search for (will be lowercased)
        :param limit: Maximum number of results to return
        :return: List of matching words in alphabetical order, up to ``limit`` results
        """
        if not prefix:
            return []
        
        prefix = prefix.lower()
        
        # Navigate to the prefix node
        node = self.root
        for char in prefix: 
            if char not in node.children:
                return []
            node = node.children[char]

        results: List[str] = []
        self._dfs_collect(node, prefix, results, limit)

        return results

    def _dfs_collect(
            self,
            node: TrieNode,
            current_word: str,
            results: List[str],
            limit: int
        ) -> None:
        """Collect words via depth-first traversal from the given node

        :param node: Current trie node to traverse from
        :param current_word: The word prefix built so far
        :param results: Output list to append matching words to
        :param limit: Maximum number of results to collect
        """

        if len(results) >= limit:
            return
        
        if node.is_end_of_word:
            results.append(current_word)

        # Sorting here may cause performance hit for large tries
        # See discussion in README.md
        for char in sorted(node.children.keys()):

            # Avoid unnecessary traversal if limit is reached
            if len(results) >= limit:
                break

            self._dfs_collect(
                node.children[char],
                current_word + char, # This will create a new string object for every call. Could be optimized with a list and join if needed
                results,
                limit
            )

