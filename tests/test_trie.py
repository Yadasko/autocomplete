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

    def test_unicode_characters(self):
        """Test that trie handles unicode characters correctly"""

        words = ["café", "naïve", "résumé", "coöperate"]

        trie = Trie()
        for word in words:
            trie.insert(word)

        results = trie.search("caf")
        assert "café" in results

        results = trie.search("naï")
        assert "naïve" in results

        results = trie.search("rés")
        assert "résumé" in results

    def test_unicode_cyrillic(self):
        """Test that trie handles Cyrillic script"""

        words = ["москва", "московский", "молоко"]

        trie = Trie()
        for word in words:
            trie.insert(word)

        results = trie.search("мос")
        assert "москва" in results
        assert "московский" in results
        assert "молоко" not in results

        results = trie.search("мо")
        assert len(results) == 3

    def test_unicode_cjk(self):
        """Test that trie handles CJK (Chinese/Japanese/Korean) characters"""

        words = ["日本語", "日本", "東京", "中国"]

        trie = Trie()
        for word in words:
            trie.insert(word)

        results = trie.search("日本")
        assert "日本" in results
        assert "日本語" in results
        assert len(results) == 2

        results = trie.search("東")
        assert "東京" in results

    def test_unicode_arabic(self):
        """Test that trie handles Arabic script"""

        words = ["مرحبا", "مرحباً", "مساء"]

        trie = Trie()
        for word in words:
            trie.insert(word)

        results = trie.search("مر")
        assert "مرحبا" in results
        assert "مرحباً" in results

    def test_unicode_greek(self):
        """Test that trie handles Greek script"""

        words = ["αλφα", "αλγόριθμος", "βήτα"]

        trie = Trie()
        for word in words:
            trie.insert(word)

        results = trie.search("αλ")
        assert "αλφα" in results
        assert "αλγόριθμος" in results

    def test_unicode_emoji(self):
        """Test that trie handles emoji characters as prefix and suffix"""

        words = ["🎉party", "🎉celebration", "🎊festival", "party🎉", "hello🌍world"]

        trie = Trie()
        for word in words:
            trie.insert(word)

        # Emoji as prefix
        results = trie.search("🎉")
        assert "🎉party" in results
        assert "🎉celebration" in results
        assert "🎊festival" not in results

        # Emoji as suffix
        results = trie.search("party🎉")
        assert "party🎉" in results

        # Emoji in middle
        results = trie.search("hello🌍")
        assert "hello🌍world" in results

    def test_unicode_normalization(self):
        """Test unicode normalization - composed vs decomposed forms

        'é' can be represented as:
        - Single codepoint U+00E9 (composed: é)
        - Two codepoints U+0065 + U+0301 (decomposed: e + combining acute)

        The trie treats these as different sequences.
        """

        trie = Trie()

        # Composed form (NFC): é is U+00E9
        composed = "caf\u00e9"
        # Decomposed form (NFD): e + combining acute accent
        decomposed = "cafe\u0301"

        trie.insert(composed)

        # Searching with same form works
        results = trie.search("caf\u00e9")
        assert composed in results

        # Searching with different normalization form won't match
        results = trie.search(decomposed)
        assert len(results) == 0

    def test_unicode_mixed_scripts(self):
        """Test that trie handles mixed scripts in same word"""

        words = ["café123", "tokyo東京", "hello世界", "αβγ-abc"]

        trie = Trie()
        for word in words:
            trie.insert(word)

        results = trie.search("café1")
        assert "café123" in results

        results = trie.search("tokyo東")
        assert "tokyo東京" in results

        results = trie.search("hello世")
        assert "hello世界" in results

        results = trie.search("αβγ-")
        assert "αβγ-abc" in results

    def test_special_characters(self):
        """Test that trie handles special characters like hyphens and dots"""

        words = ["hello-world", "hello.world", "self-aware", "e.g."]

        trie = Trie()
        for word in words:
            trie.insert(word)

        results = trie.search("hello-")
        assert "hello-world" in results

        results = trie.search("hello.")
        assert "hello.world" in results

        results = trie.search("self-")
        assert "self-aware" in results

        results = trie.search("e.")
        assert "e.g." in results

    def test_numbers_in_words(self):
        """Test that trie handles words containing numbers"""

        words = ["test123", "3com", "mp3", "21st"]

        trie = Trie()
        for word in words:
            trie.insert(word)

        results = trie.search("test1")
        assert "test123" in results

        results = trie.search("3")
        assert "3com" in results

        results = trie.search("mp")
        assert "mp3" in results

        results = trie.search("21")
        assert "21st" in results

    def test_spaces_in_words(self):
        """Test that trie handles words with spaces"""

        words = ["new york", "los angeles", "san francisco", "new jersey"]

        trie = Trie()
        for word in words:
            trie.insert(word)

        results = trie.search("new ")
        assert "new jersey" in results
        assert "new york" in results

        results = trie.search("los a")
        assert "los angeles" in results

    def test_apostrophes(self):
        """Test that trie handles apostrophes in words"""

        words = ["don't", "it's", "we're", "o'clock", "rock'n'roll"]

        trie = Trie()
        for word in words:
            trie.insert(word)

        results = trie.search("don")
        assert "don't" in results

        results = trie.search("it'")
        assert "it's" in results

        results = trie.search("o'c")
        assert "o'clock" in results

        results = trie.search("rock'n")
        assert "rock'n'roll" in results

    def test_underscores(self):
        """Test that trie handles underscores in words"""

        words = ["snake_case", "my_variable", "test_function_name"]

        trie = Trie()
        for word in words:
            trie.insert(word)

        results = trie.search("snake_")
        assert "snake_case" in results

        results = trie.search("test_f")
        assert "test_function_name" in results

    def test_ampersand_and_symbols(self):
        """Test that trie handles ampersands and other symbols"""

        words = ["r&d", "at&t", "h&m", "a+b", "c++"]

        trie = Trie()
        for word in words:
            trie.insert(word)

        results = trie.search("r&")
        assert "r&d" in results

        results = trie.search("at&")
        assert "at&t" in results

        results = trie.search("c+")
        assert "c++" in results

    def test_mixed_non_alphabetic(self):
        """Test that trie handles mixed non-alphabetic characters"""

        words = ["test-case_v2.0", "user@domain.com", "file/path/name", "100%"]

        trie = Trie()
        for word in words:
            trie.insert(word)

        results = trie.search("test-case_")
        assert "test-case_v2.0" in results

        results = trie.search("user@")
        assert "user@domain.com" in results

        results = trie.search("file/")
        assert "file/path/name" in results

        results = trie.search("100")
        assert "100%" in results
