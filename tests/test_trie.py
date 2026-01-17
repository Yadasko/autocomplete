from app.trie import Trie

class TestTrie:

    def test_insert_and_basic_search(self):
        """Test basic insert"""
        trie = Trie()
        trie.insert("hello")
        trie.insert("world")
        trie.insert("HELLO")  # Test case insensitivity

        trie.insert("apple")
        trie.insert("application")
        trie.insert("apply")

        results = trie.search("he")
        assert "hello" in results
        assert len(results) == 1

        results = trie.search("app")
        assert results == ["apple", "application", "apply"]




