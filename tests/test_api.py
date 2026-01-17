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