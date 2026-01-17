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