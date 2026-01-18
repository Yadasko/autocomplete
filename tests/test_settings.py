import os
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.settings import Settings


class TestSettingsLoading:
    def test_default_settings(self):
        """Test that default settings are loaded correctly"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()

        assert settings.dictionary_path == "resources/dictionaries/starwars_8k_2018.txt"
        assert settings.autocomplete_limit == 4

    def test_settings_from_environment(self):
        """Test that settings can be overridden via environment variables"""
        env_vars = {
            "DICTIONARY_PATH": "custom/path.txt",
            "AUTOCOMPLETE_LIMIT": "10",
        }
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()

        assert settings.dictionary_path == "custom/path.txt"
        assert settings.autocomplete_limit == 10


class TestAutocompleteLimit:
    def test_autocomplete_respects_limit_setting(self, env_override):
        """Test that autocomplete respects the AUTOCOMPLETE_LIMIT setting"""
        env_override(AUTOCOMPLETE_LIMIT="2")

        # Import app fresh to pick up new settings
        from app.api import app

        with TestClient(app) as client:
            response = client.get("/autocomplete?query=a")

            assert response.status_code == 200
            data = response.json()
            assert len(data) <= 2


