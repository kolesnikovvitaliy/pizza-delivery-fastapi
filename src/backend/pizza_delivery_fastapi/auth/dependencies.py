from datetime import datetime

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import db_connect
from ..core.models import RefreshToken, User
from . import crud
from .config import auth_config
from .exceptions import EmailTaken, RefreshTokenNotValid
from .schemas import UserCreate


async def valid_user_create(
    user: UserCreate, session: AsyncSession = Depends(db_connect)
) -> User:
    if await crud.get_user_by_email(user.email, session):
        raise EmailTaken()

    return user


async def valid_refresh_token(
    request: Request,
    # refresh_token: str = Cookie(..., alias=auth_config.REFRESH_TOKEN_KEY),
    session: AsyncSession = Depends(db_connect),
) -> RefreshToken:
    refresh_token = request.cookies.get(auth_config.REFRESH_TOKEN_KEY)
    db_refresh_token = await crud.get_refresh_token(
        refresh_token=refresh_token,
        session=session,
    )
    if not db_refresh_token:
        raise RefreshTokenNotValid()

    if not _is_valid_refresh_token(db_refresh_token):
        await crud.expire_refresh_token(
            refresh_token_uuid=db_refresh_token.uuid,
            session=session,
        )
        # raise RefreshTokenNotValid()
    return db_refresh_token


async def valid_refresh_token_user(
    refresh_token: RefreshToken = Depends(valid_refresh_token),
    session: AsyncSession = Depends(db_connect),
) -> User:
    user = await crud.get_user_by_id(
        user_id=refresh_token.user_id, session=session
    )
    if not user or not user.is_active:
        raise RefreshTokenNotValid()

    return user


def _is_valid_refresh_token(
    db_refresh_token: RefreshToken,
    session: AsyncSession = Depends(db_connect),
) -> bool:
    return datetime.utcnow() <= db_refresh_token.expires_at
