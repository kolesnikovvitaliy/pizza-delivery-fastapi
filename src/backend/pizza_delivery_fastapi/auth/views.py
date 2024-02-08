# from typing import Annotated
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Request,
    Response,
    status,
)

# from fastapi.security import OAuth2PasswordRequestForm
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
    LoginUser,
)

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post(
    "/signup",
    response_model=ShowUser,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    auth_data: UserCreate = Depends(valid_user_create),
    session: AsyncSession = Depends(db_connect),
) -> ShowUser:
    """
    ## Create a user
    This requires the following
    ```
            username:str
            email:str[EmailStr]
            password:str[min_len(6), example("string!1Q")]
            is_staff:bool
            is_active:bool

    ```

    """
    user = await crud.create_user(
        user=auth_data,
        session=session,
    )
    return user


@router.post("/login", response_model=AccessTokenResponse)
async def login(
    auth_data: LoginUser,
    response: Response,
    # form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(db_connect),
) -> AccessTokenResponse:
    """
    ## Login a user
    This requires
    ```
        email:str
        password:str
    ```
    and returns a token pair `access` and `refresh`
    """
    user = await crud.authenticate_user(auth_data, session)
    # user = await crud.authenticate_user(
    #     email=form_data.username,
    #     password=form_data.password,
    #     session=session,
    # )
    refresh_token_value = await crud.create_refresh_token(
        user_id=user.id, session=session
    )
    await crud.update_user_is_active(user=user, session=session, is_active=True)
    access_token = jwt.create_access_token(user=user)
    response.set_cookie(**utils.get_token_settings(refresh_token_value))
    response.set_cookie(**utils.get_token_settings(access_token))

    return AccessTokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_value,
    )


@router.get("/me", response_model=ShowUser)
async def get_my_account(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    session: AsyncSession = Depends(db_connect),
) -> ShowUser:
    """
    ## Get user profile
    This returns a current user account
    """
    logger.info(f"CRUD create_user for: jwt_data: {jwt_data}")
    user = await crud.get_user_by_id(user_id=jwt_data.user_id, session=session)
    return user


@router.delete("/logout")
async def logout(
    request: Request,
    response: Response,
    user: UserCreate = Depends(valid_refresh_token_user),
    session: AsyncSession = Depends(db_connect),
) -> None:
    """
    ## Logout a user
    This returns a message 'access logout'
    """
    refresh_token: RefreshToken = await valid_refresh_token(
        request=request,
        session=session,
    )
    await crud.update_user_is_active(user=user, session=session)
    await crud.expire_refresh_token(
        refresh_token_uuid=refresh_token.uuid,
        session=session,
    )
    response.delete_cookie(auth_config.REFRESH_TOKEN_KEY)
    response.delete_cookie(auth_config.ACCESS_TOKEN_KEY)
    return {"msg": "access logout"}


@router.put("/expire_tokens", response_model=AccessTokenResponse)
async def refresh_tokens(
    worker: BackgroundTasks,
    response: Response,
    refresh_token: CreateRefreshToken = Depends(valid_refresh_token),
    user: UserCreate = Depends(valid_refresh_token_user),
    session: AsyncSession = Depends(db_connect),
) -> AccessTokenResponse:
    """
    ## Update a fresh token
    This updates the expiration date of the refresh token
    """
    refresh_token_value = await crud.create_refresh_token(
        user_id=refresh_token.user_id, session=session
    )
    response.set_cookie(**utils.get_token_settings(refresh_token_value))

    worker.add_task(
        crud.expire_refresh_token, refresh_token.uuid, session=session
    )
    return AccessTokenResponse(
        access_token="",
        refresh_token=refresh_token_value,
    )
