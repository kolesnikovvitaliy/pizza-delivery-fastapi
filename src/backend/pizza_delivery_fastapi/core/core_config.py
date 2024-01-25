from pydantic_settings import BaseSettings
from .db.db_config import DBSettings, db_settings


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db: DBSettings = db_settings


settings = Settings()
