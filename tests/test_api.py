from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.api import app

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
        app.state.service.clear_cache()
        yield
        app.state.service.clear_cache()

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
        with patch.object(app.state.service._trie, "search") as mock_search:
            response = client.get("/autocomplete?query=luke")

            assert response.status_code == 200
            mock_search.assert_not_called()

    def test_cache_stores_query_after_search(self, client):
        """Test that query is stored in cache after search"""

        initial_size = app.state.service.cache_info().currsize

        client.get("/autocomplete?query=vader")

        assert app.state.service.cache_info().currsize == initial_size + 1

    def test_different_queries_cached_separately(self, client):
        """Test that different queries are cached separately"""

        initial_size = app.state.service.cache_info().currsize

        client.get("/autocomplete?query=sky")
        client.get("/autocomplete?query=dark")

        assert app.state.service.cache_info().currsize >= initial_size + 2


class TestHealthEndpoint:
    def test_health_returns_200_when_service_ready(self, client):
        """Test that /health returns 200 when service is loaded"""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_health_returns_503_when_service_not_ready(self, client):
        """Test that /health returns 503 when service is not available"""
        with patch.object(app.state, "service", None):
            response = client.get("/health")

        assert response.status_code == 503
        assert response.json() == {"status": "unhealthy"}