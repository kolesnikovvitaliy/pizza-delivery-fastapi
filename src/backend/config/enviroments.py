import os

from dotenv import load_dotenv

from config import dotenv_path


if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


PORT: int = int(os.environ.get("DOCKER_BACKEND_PORT"))
HOST: str = os.environ.get("DOCKER_BACKEND_HOST")
