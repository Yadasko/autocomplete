from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    dictionary_path: str = "resources/dictionaries/starwars_8k_2018.txt"
    autocomplete_limit: int = 4
    cache_enabled: bool = True
    cache_max_size: int = 128
    max_query_length: int = 50
