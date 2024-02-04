import random
import string
from typing import Any, Dict

from ..core.core_config import settings
from .config import auth_config

ALPHA_NUM = string.ascii_letters + string.digits


def generate_random_alphanum(length: int = 20) -> str:
    return "".join(random.choices(ALPHA_NUM, k=length))


def get_token_settings(
    token: str,
    expired: bool = False,
) -> Dict[str, Any]:
    if len(token) > auth_config.LEN_REFRESH_TOKEN:
        key: str = auth_config.ACCESS_TOKEN_KEY
        max_age: int = int(auth_config.JWT_EXP)
        value: str = (f"Bearer {token}",)
    else:
        key: str = auth_config.REFRESH_TOKEN_KEY
        max_age: int = int(auth_config.REFRESH_TOKEN_EXP)
        value: str = (token,)

    base_cookie = {
        "key": key,
        "httponly": True,
        "samesite": "none",
        "secure": auth_config.SECURE_COOKIES,
        "domain": settings.SITE_DOMAIN,
    }
    if expired:
        return base_cookie

    return {
        **base_cookie,
        "value": value[0],
        "max_age": max_age,
    }
