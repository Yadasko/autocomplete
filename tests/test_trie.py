from app.trie import Trie

class TestTrie:

    def test_insert_and_basic_search(self):
        """Test basic insert"""

        words = ["hello", "world", "apple", "application", "apply"]

        trie = Trie()

        for word in words:
            trie.insert(word)

        results = trie.search("he")
        assert "hello" in results
        assert len(results) == 1

        results = trie.search("app")
        assert results == ["apple", "application", "apply"]

    
    def test_prefix_not_found(self):
        """Test that empty list is returned for non-existent prefix"""

        words = ["apple", "banana", "grape"]

        trie = Trie()
        for word in words:
            trie.insert(word)

        results = trie.search("xyz")
        assert results == []

    def test_empty_prefix(self):
        """Test that empty prefix returns empty list"""

        trie = Trie()
        trie.insert("apple")

        results = trie.search("")
        assert results == []

    def test_limit_parameter(self):
        """Test that limit parameter restricts result count"""

        trie = Trie()
        words = ["cat", "catch", "category", "cathedral", "cattle"]
        for word in words:
            trie.insert(word)

        results = trie.search("cat", limit=3)
        assert len(results) == 3
        assert results == ["cat", "catch", "category"]

    def test_case_insensitivity(self):
        """Test that the trie is case insensitive"""

        words = ["Hello", "WORLD"]

        trie = Trie()
        for word in words:
            trie.insert(word)

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

    def test_exact_match_included(self):
        """Test that exact matches are included in results"""

        words  = ["cat", "catch"]

        trie = Trie()
        for word in words:
            trie.insert(word)

        results = trie.search("cat")
        assert "cat" in results
        assert "catch" in results

    def test_duplicate_inserts(self):
        """Test that duplicate inserts don't create duplicate results"""

        words = ["apple", "apple", "apple"]

        trie = Trie()
        for word in words:
            trie.insert(word)

        results = trie.search("app")
        assert results == ["apple"]

    def test_empty_trie(self):
        """Test search on empty trie"""

        trie = Trie()
        results = trie.search("test")
        assert results == []

    def test_single_character_prefix(self):
        """Test search with single character prefix"""

        words = ["overtakes", "midi-chlorians", "apple", "back-to-back"]

        trie = Trie()
        for word in words:
            trie.insert(word)

        results = trie.search("a")
        assert results == ["apple"]




