import os

import pytest

# Set test environment variables before app import
os.environ.setdefault("DICTIONARY_PATH", "resources/dictionaries/starwars_8k_2018.txt")
os.environ.setdefault("AUTOCOMPLETE_LIMIT", "4")
os.environ.setdefault("CACHE_ENABLED", "true")
os.environ.setdefault("CACHE_MAX_SIZE", "128")


@pytest.fixture
def env_override(monkeypatch):
    """
    Fixture to override environment variables for a test.
    Returns a helper function to set env vars.

    Usage:
        def test_something(env_override):
            env_override(AUTOCOMPLETE_LIMIT="2", CACHE_ENABLED="false")
            # ... test code
    """
    def _override(**env_vars):
        for key, value in env_vars.items():
            monkeypatch.setenv(key, value)
    return _override
