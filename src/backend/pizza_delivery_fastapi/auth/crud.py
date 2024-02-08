import uuid
from datetime import datetime, timedelta

from pydantic import EmailStr
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.core_config import core_logger as logger
from ..core.models import RefreshToken, User
from ..core.service import execute, execute_add, fetch_one_all
from .config import auth_config
from .exceptions import InvalidCredentials
from .schemas import UserCreate, LoginUser
from .security import check_password, hash_password
from .utils import generate_random_alphanum


async def create_user(user: UserCreate, session: AsyncSession) -> User:
    new_user = User(**user.model_dump())
    new_user.password = hash_password(new_user.password)
    new_user = await execute_add(new_user, session=session)
    logger.info(f"CRUD: <create_user for: user.email: {user.email}>")
    return new_user


async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    select_query = select(User).where(User.id == user_id)
    user = await fetch_one_all(select_query, session=session)
    if user:
        logger.info(f"CRUD: <get_user_by_id for: user_id: {user_id}>")
        return user


async def get_user_by_email(
    email: EmailStr, session: AsyncSession
) -> User | None:
    select_query = select(User).where(User.email == email)
    user = await fetch_one_all(select_query, session=session)
    if user:
        logger.info(f"CRUD: <get_user_by_email for: email: {email}>")
        return user


async def authenticate_user(
    auth_data: LoginUser,
    # email: str,
    # password: str,
    session: AsyncSession,
) -> User:
    # user = await get_user_by_email(email=email, session=session)
    user = await get_user_by_email(auth_data.email, session=session)
    if not user:
        raise InvalidCredentials()

    # if not check_password(password, user.password):
    if not check_password(auth_data.password, user.password):
        raise InvalidCredentials()

    return user


async def create_refresh_token(
    *,
    user_id: int,
    refresh_token: str | None = None,
    session: AsyncSession,
) -> str:
    if not refresh_token:
        select_query = select(RefreshToken).where(
            RefreshToken.user_id == user_id
        )
        token = await fetch_one_all(select_query, session=session)
        if not token:
            # TODO: is_valid_token
            new_refresh_token = generate_random_alphanum(
                auth_config.LEN_REFRESH_TOKEN
            )
        else:
            return token.refresh_token
    else:
        new_refresh_token = refresh_token
    token = RefreshToken(
        uuid=uuid.uuid4(),
        refresh_token=new_refresh_token,
        expires_at=datetime.utcnow()
        + timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
        user_id=user_id,
    )
    new_refresh_token = await execute_add(token, session=session)
    logger.info(
        f"CRUD: <create_refresh_token for: user_id: {user_id}, refresh_token: {refresh_token}>"
    )
    return new_refresh_token.refresh_token


async def get_refresh_token(
    refresh_token: str,
    session: AsyncSession,
) -> RefreshToken:
    select_query = select(RefreshToken).where(
        RefreshToken.refresh_token == refresh_token
    )
    token = await fetch_one_all(select_query, session=session)
    if token is not None:
        return token


async def expire_refresh_token(
    refresh_token_uuid: str,
    session: AsyncSession,
) -> None:
    update_query = (
        update(RefreshToken)
        .values(expires_at=datetime.utcnow() + timedelta(days=22))
        .where(RefreshToken.uuid == refresh_token_uuid)
    )
    await execute(update_query, session=session)


async def update_user_is_active(user: UserCreate, session: AsyncSession, is_active=False):
    if is_active:
        stmt = update(User).where(User.id == user.id).values(is_active=is_active)
    else:
        stmt = update(User).where(User.id == user.id).values(is_active=is_active)
    await execute(select_query=stmt, session=session)