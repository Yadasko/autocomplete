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
    def test_cache_disabled_does_not_store(self, env_override):
        """Test that cache is not used when CACHE_ENABLED=false"""
        env_override(CACHE_ENABLED="false")

        from app.api import app
        from app.routers import autocomplete as autocomplete_module

        autocomplete_module._cache.clear()

        with TestClient(app) as client:
            client.get("/autocomplete?query=test")

            # Cache should remain empty when disabled
            assert "test" not in autocomplete_module._cache

        autocomplete_module._cache.clear()

    def test_cache_disabled_does_not_return_cached(self, env_override):
        """Test that cache lookup is skipped when CACHE_ENABLED=false"""
        env_override(CACHE_ENABLED="false")

        from app.api import app
        from app.routers import autocomplete as autocomplete_module

        # Pre-populate cache
        autocomplete_module._cache["force"] = ["cached_result"]

        with TestClient(app) as client:
            response = client.get("/autocomplete?query=force")

            assert response.status_code == 200
            data = response.json()
            # Should NOT return the cached value, but actual trie results
            assert data != ["cached_result"]

        autocomplete_module._cache.clear()
