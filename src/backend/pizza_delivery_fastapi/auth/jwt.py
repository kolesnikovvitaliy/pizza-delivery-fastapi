from datetime import datetime, timedelta
from typing import Dict

from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt

from . import utils
from .config import auth_config
from .dependencies import valid_refresh_token_user
from .exceptions import AuthorizationFailed, AuthRequired, InvalidToken
from .schemas import JWTData, UserCreate


# from ..core.core_config import core_logger as logger


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str | None = None,
        scopes: Dict[str, str] | None = None,
        description: str | None = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(
        self,
        request: Request,
        response: Response,
        user: UserCreate = Depends(valid_refresh_token_user),
    ) -> str | None:
        authorization: str = request.cookies.get(auth_config.ACCESS_TOKEN_KEY)
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            access_token = await self.update_access_token(
                user=user,
                response=response,
            )
            return access_token
        else:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        return param

    @staticmethod
    async def update_access_token(
        response: Response,
        user: UserCreate,
    ) -> str:
        access_token = create_access_token(user=user)
        response.set_cookie(**utils.get_token_settings(access_token))
        _, new_access_token = get_authorization_scheme_param(f"Bearer {access_token}")
        return new_access_token


oauth2_scheme = OAuth2PasswordBearerWithCookie(
    tokenUrl="/auth/users/login", auto_error=False
)


def create_access_token(
    *,
    user: UserCreate,
    expires_delta: timedelta = timedelta(minutes=auth_config.JWT_EXP),
) -> str:
    jwt_data = {
        "sub": str(user.id),
        "exp": datetime.utcnow() + expires_delta,
        "is_active": user.is_active,
    }

    return jwt.encode(jwt_data, auth_config.JWT_SECRET, algorithm=auth_config.JWT_ALG)


async def parse_jwt_user_data_optional(
    token: str = Depends(oauth2_scheme),
) -> JWTData | None:
    print(token, "TOKEN_OPTIONAL_1", "####################")
    if not token:
        return None
    try:
        payload = jwt.decode(
            token, auth_config.JWT_SECRET, algorithms=[auth_config.JWT_ALG]
        )
    except JWTError:
        raise InvalidToken()

    return JWTData(**payload)


async def parse_jwt_user_data(
    token: JWTData | None = Depends(parse_jwt_user_data_optional),
) -> JWTData:
    print(token, "TOKEN_USER_DATA_2", "##############################")
    if not token:
        raise AuthRequired()

    return token


async def parse_jwt_admin_data(
    token: JWTData = Depends(parse_jwt_user_data),
) -> JWTData:
    if not token.is_admin:
        raise AuthorizationFailed()

    return token


async def validate_admin_access(
    token: JWTData | None = Depends(parse_jwt_user_data_optional),
) -> None:
    if token and token.is_admin:
        return

    raise AuthorizationFailed()
