from pydantic_settings import BaseSettings

from backend_config.environments import (
    JWT_ALGORITHM,
    JWT_EXPIRES,
    JWT_SECRET_CODE,
)


class AuthConfig(BaseSettings):
    JWT_ALG: str = JWT_ALGORITHM
    JWT_SECRET: str = JWT_SECRET_CODE
    JWT_EXP: int = JWT_EXPIRES  # minutes

    ACCESS_TOKEN_KEY: str = "Authorization"
    REFRESH_TOKEN_KEY: str = "refreshToken"
    LEN_REFRESH_TOKEN: int = 64
    REFRESH_TOKEN_EXP: int = 60 * 60 * 24 * 21  # 21 days

    SECURE_COOKIES: bool = True


auth_config = AuthConfig()
