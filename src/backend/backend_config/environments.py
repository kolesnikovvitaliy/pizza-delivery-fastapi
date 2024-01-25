import os

from dotenv import load_dotenv

from backend_config import dotenv_path


if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    POSTGRES_HOST: str = os.environ.get("POSTGRES_LOCAL")
else:
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")

PORT: int = int(os.environ.get("BACKEND_PORT_OUT"))
HOST: str = os.environ.get("BACKEND_HOST_OUT")

SCHEMAS: str = os.environ.get("SCHEMAS")
POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_PORT: int = int(os.environ.get("POSTGRES_PORT"))
POSTGRES_DB: str = os.environ.get("POSTGRES_DB")

DB_URL_REAL: str = f'{SCHEMAS}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'
