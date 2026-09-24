from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    hotel_api_mode: str = "mock"

    hotel_api_url: str = ""
    hotel_api_token: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()