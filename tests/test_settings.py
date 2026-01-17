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
        assert settings.cache_enabled is True
        assert settings.cache_max_size == 128

    def test_settings_from_environment(self):
        """Test that settings can be overridden via environment variables"""
        env_vars = {
            "DICTIONARY_PATH": "custom/path.txt",
            "AUTOCOMPLETE_LIMIT": "10",
            "CACHE_ENABLED": "false",
        }
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()

        assert settings.dictionary_path == "custom/path.txt"
        assert settings.autocomplete_limit == 10
        assert settings.cache_enabled is False


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


class TestCacheToggle:
    def test_cache_disabled_returns_none_cache_info(self, env_override):
        """Test that cache_info returns None when CACHE_ENABLED=false"""
        env_override(CACHE_ENABLED="false")

        from app.api import app

        with TestClient(app) as client:
            client.get("/autocomplete?query=test")

            # cache_info() returns None when caching is disabled
            assert app.state.service.cache_info() is None

    def test_cache_disabled_always_searches_trie(self, env_override):
        """Test that trie search is always called when CACHE_ENABLED=false"""
        env_override(CACHE_ENABLED="false")

        from unittest.mock import patch
        from app.api import app

        with TestClient(app) as client:
            client.get("/autocomplete?query=force")

            # Second request - should still hit the trie, not cache
            with patch.object(app.state.service._trie, "search", wraps=app.state.service._trie.search) as mock_search:
                client.get("/autocomplete?query=force")
                mock_search.assert_called_once()
