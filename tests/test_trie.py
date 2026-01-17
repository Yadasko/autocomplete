from app.trie import Trie

class TestTrie:

    def test_insert_and_basic_search(self):
        """Test basic insert"""

        trie = Trie()
        trie.insert("hello")
        trie.insert("world")

        trie.insert("apple")
        trie.insert("application")
        trie.insert("apply")

        results = trie.search("he")
        assert "hello" in results
        assert len(results) == 1

        results = trie.search("app")
        assert results == ["apple", "application", "apply"]

    def test_case_insensitivity(self):
        """Test that the trie is case insensitive"""

        trie = Trie()
        trie.insert("Hello")
        trie.insert("WORLD")

        results = trie.search("he")
        assert "hello" in results

        results = trie.search("WoR")
        assert "world" in results

    def test_alphabetical_ordering(self):
        """Test that results are returned in alphabetical order"""
        
        trie = Trie()
        words = ["cryptography", "cryptanalysis", "cryptographic algorithm", "cryptographers"]
        for word in words:
            trie.insert(word)

        results = trie.search("crypt")
        assert results == ["cryptanalysis", "cryptographers", "cryptographic algorithm", "cryptography"]



