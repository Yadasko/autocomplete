from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.api import app
from app.routers import autocomplete as autocomplete_module

@pytest.fixture(scope="module")
def client():
     with TestClient(app) as test_client:
        yield test_client

class TestAutocompleteAPI:
    def test_basic_autocomplete(self, client):
        """Test basic autocomplete"""

        response = client.get("/autocomplete?query=app")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        assert len(data) == 4
        assert "apparently" in data
        assert "appearing" in data

    def test_query_whitespace_stripped(self, client):
        """Test that leading and trailing whitespace is stripped from query"""

        response = client.get("/autocomplete?query=  app  ")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 4
        assert "apparently" in data

    def test_query_too_long_returns_400(self, client):
        """Test that query exceeding 50 characters returns 400"""

        long_query = "a" * 51
        response = client.get(f"/autocomplete?query={long_query}")

        assert response.status_code == 400
        assert "Query too long" in response.json()["detail"]

    def test_query_at_max_length_succeeds(self, client):
        """Test that query at exactly 50 characters succeeds"""

        max_query = "a" * 50
        response = client.get(f"/autocomplete?query={max_query}")

        assert response.status_code == 200


class TestAutocompleteCache:
    @pytest.fixture(autouse=True)
    def clear_cache(self):
        """Clear cache before each test"""
        autocomplete_module._cache.clear()
        yield
        autocomplete_module._cache.clear()

    @pytest.fixture
    def client(self):
        with TestClient(app) as test_client:
            yield test_client

    def test_cache_returns_same_result(self, client):
        """Test that repeated queries return the same cached result"""

        response1 = client.get("/autocomplete?query=sky")
        response2 = client.get("/autocomplete?query=sky")

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.json() == response2.json()

    def test_cache_prevents_repeated_trie_search(self, client):
        """Test that cache prevents repeated trie searches"""

        # First request - populates cache
        client.get("/autocomplete?query=luke")

        # Patch trie.search to track if it's called again
        with patch.object(app.state.trie, "search") as mock_search:
            response = client.get("/autocomplete?query=luke")

            assert response.status_code == 200
            mock_search.assert_not_called()

    def test_cache_stores_query_after_search(self, client):
        """Test that query is stored in cache after search"""

        assert "vader" not in autocomplete_module._cache

        client.get("/autocomplete?query=vader")

        assert "vader" in autocomplete_module._cache

    def test_different_queries_cached_separately(self, client):
        """Test that different queries are cached separately"""

        client.get("/autocomplete?query=sky")
        client.get("/autocomplete?query=dark")

        assert "sky" in autocomplete_module._cache
        assert "dark" in autocomplete_module._cache
        assert autocomplete_module._cache["sky"] != autocomplete_module._cache["dark"]