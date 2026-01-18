from typing import Dict, List

class TrieNode:

    def __init__(self) -> None:
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        word = word.lower()
    
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_end_of_word = True


    def search(self, prefix: str, limit: int = 4) -> List[str]:
        """
        Find words in the trie that start with the given prefix
        
        :param prefix: What to search for
        :type prefix: str
        :param limit: How many results to return
        :type limit: int
        :return: List of words that start with the given prefix, maximum of 'limit' words
        :rtype: List[str]
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
        self.dfs_collect(node, prefix, results, limit)

        return results

    def dfs_collect(
            self,
            node: TrieNode,
            current_word: str,
            results: List[str],
            limit: int
        ) -> None:
        """
        DFS traversal 
        
        :param node: Current trie node
        :type node: TrieNode
        :param current_word: Word built so far 
        :type current_word: str
        :param results: Output list to append matching words
        :type results: List[str]
        :param limit: Maximum number of results to collect
        :type limit: int
        """

        if (len(results) >= limit):
            return
        
        if node.is_end_of_word:
            results.append(current_word)

            if len(results) >= limit:
                return
            
        # Sorting here may cause performance hit for large tries
        # See discussion in README.md
        for char in sorted(node.children.keys()):

            # Avoid unnecessary traversal if limit is reached
            if len(results) >= limit:
                break

            self.dfs_collect(
                node.children[char],
                current_word + char,
                results,
                limit
            )

        return

