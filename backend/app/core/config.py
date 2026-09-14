from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    ADZUNA_APP_ID: str
    ADZUNA_APP_KEY: str
    ADZUNA_COUNTRY: str = "in"

    SERPAPI_KEY: str
    GREENHOUSE_BOARDS: str = ""
    LEVER_ACCOUNTS: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()