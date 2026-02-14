from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

class Settings(BaseSettings):
    DB_URL: str
    BOT_TOKEN: str
    ADMIN_DB_URL: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR/'.env'
    )

settings = Settings()