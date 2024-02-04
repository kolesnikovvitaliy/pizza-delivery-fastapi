from fastapi import APIRouter, BackgroundTasks, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.core_config import core_logger as logger
from ..core.db import db_connect

# from fastapi.security import OAuth2PasswordRequestForm
from ..core.models import RefreshToken
from . import crud, jwt, utils

# from typing import Annotated, Any
from .config import auth_config
from .dependencies import (
    valid_refresh_token,
    valid_refresh_token_user,
    valid_user_create,
)
from .jwt import parse_jwt_user_data
from .schemas import (
    AccessTokenResponse,
    CreateRefreshToken,
    JWTData,
    ShowUser,
    UserCreate,
)

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post(
    "/user",
    response_model=ShowUser,
    status_code=status.HTTP_201_CREATED,
)  # CREATE USER
async def create_user(
    auth_data: UserCreate = Depends(valid_user_create),
    session: AsyncSession = Depends(db_connect),
) -> ShowUser:
    user = await crud.create_user(
        user=auth_data,
        session=session,
    )
    return user


@router.get("/users/me", response_model=ShowUser)
async def get_my_account(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    session: AsyncSession = Depends(db_connect),
) -> ShowUser:
    logger.info(f"CRUD create_user for: jwt_data: {jwt_data}")
    user = await crud.get_user_by_id(user_id=jwt_data.user_id, session=session)
    return user


@router.post("/users/login", response_model=AccessTokenResponse)
async def auth_user(
    auth_data: UserCreate,
    # form_data: Annotated[UserCreate, OAuth2PasswordRequestForm, Depends()],,
    response: Response,
    session: AsyncSession = Depends(db_connect),
) -> AccessTokenResponse:
    user = await crud.authenticate_user(auth_data, session)
    refresh_token_value = await crud.create_refresh_token(
        user_id=user.id, session=session
    )
    access_token = jwt.create_access_token(user=user)
    response.set_cookie(**utils.get_token_settings(refresh_token_value))
    response.set_cookie(**utils.get_token_settings(access_token))

    return AccessTokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_value,
    )


@router.put("/users/expire_tokens", response_model=AccessTokenResponse)
async def refresh_tokens(
    worker: BackgroundTasks,
    response: Response,
    refresh_token: CreateRefreshToken = Depends(valid_refresh_token),
    user: UserCreate = Depends(valid_refresh_token_user),
    session: AsyncSession = Depends(db_connect),
) -> AccessTokenResponse:
    refresh_token_value = await crud.create_refresh_token(
        user_id=refresh_token.user_id, session=session
    )
    response.set_cookie(**utils.get_token_settings(refresh_token_value))

    worker.add_task(crud.expire_refresh_token, refresh_token.uuid, session=session)
    return AccessTokenResponse(
        access_token="",
        refresh_token=refresh_token_value,
    )


@router.delete("/users/logout")
async def logout_user(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(db_connect),
) -> None:
    refresh_token: RefreshToken = await valid_refresh_token(
        request=request,
        session=session,
    )
    await crud.expire_refresh_token(
        refresh_token_uuid=refresh_token.uuid,
        session=session,
    )
    response.delete_cookie(auth_config.REFRESH_TOKEN_KEY)
    response.delete_cookie(auth_config.ACCESS_TOKEN_KEY)
    return {"msg": "access logout"}
