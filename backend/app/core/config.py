from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    APP_NAME: str = "Scout API"
    ENV: str = "development"
    
    DATABASE_URL: str
    GEMINI_API_KEY: str = ""
    RAPIDAPI_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )


settings = Settings()