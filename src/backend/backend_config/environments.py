import os
from dotenv import load_dotenv

from backend_config import dotenv_path


if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")

LOG_LEVEL: str = os.environ.get("LOG_LEVEL")
PORT: int = int(os.environ.get("BACKEND_PORT_OUT"))
HOST: str = os.environ.get("BACKEND_HOST_OUT")

SCHEMAS: str = os.environ.get("SCHEMAS")
POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_PORT: int = int(os.environ.get("POSTGRES_PORT"))
POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITM")
JWT_SECRET_CODE: str = os.environ.get("JWT_SECRET_CODE")
JWT_EXPIRES: int = int(os.environ.get("JWT_EXPIRES"))


if os.path.exists(dotenv_path):
    DB_URL_REAL: str = "sqlite+aiosqlite:///sqlite.db"  # activated if local db sqlite
    # POSTGRES_HOST: str = os.environ.get("POSTGRES_LOCAL")  # activated if local db postgres
else:
    DB_URL_REAL: str = f'{SCHEMAS}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'
