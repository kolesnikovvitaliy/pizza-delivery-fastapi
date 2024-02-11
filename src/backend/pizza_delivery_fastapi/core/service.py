from typing import Any

from sqlalchemy import Insert, Result, Select, Update
from sqlalchemy.ext.asyncio import AsyncSession


async def session_close(session: AsyncSession) -> None:
    await session.commit()
    # await session.close()


async def fetch_one_all(
    select_query: Select | Insert | Update,
    session: AsyncSession,
    all: bool = False,
) -> Any | None:
    result: Result = await session.execute(select_query)
    await session_close(session=session)
    if all:
        return result.scalars().all()
    return result.scalars().first()


async def execute_add(model: Any, session: AsyncSession) -> Any:
    session.add(model)
    await session.commit()
    await session.refresh(model)
    await session.close()
    return model


async def execute_delete(
    model: Any, value: Any, session: AsyncSession
) -> None:
    await session.delete(model, value)
    await session_close(session=session)


async def execute_get(model: Any, value: Any, session: AsyncSession) -> Any:
    result: Result = await session.get(model, value)
    await session_close(session=session)
    return result


async def execute(
    select_query: Insert | Update,
    session: AsyncSession,
) -> None:
    await session.execute(select_query)
    await session_close(session=session)
