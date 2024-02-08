from pizza_delivery_fastapi.auth import crud
from pizza_delivery_fastapi.auth.schemas import JWTData
from pizza_delivery_fastapi.core.service import (
    execute_add,
    fetch_one_all,
    execute,
)
from sqlalchemy import select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from pizza_delivery_fastapi.core.models import Order, User
from .schemas import CreateOrder, OrderUpdate, OrderUpdatePartial


async def create_order(
    session: AsyncSession,
    order_in: CreateOrder,
    jwt_data: JWTData,
) -> Order | None:
    current_user: Result[User] = await crud.get_user_by_id(
        user_id=jwt_data.user_id,
        session=session,
    )
    order = Order(**order_in.model_dump())
    order.user = current_user
    new_order: Result[Order] = await execute_add(model=order, session=session)
    return new_order


async def get_orders(
    session: AsyncSession,
) -> Order | None:
    stmt = select(Order).order_by(Order.id)
    orders: Result = await fetch_one_all(
        select_query=stmt, session=session, all=True
    )
    return list(orders)


async def get_order(session: AsyncSession, order_id: int) -> Order | None:
    stmt = select(Order).filter(Order.id == order_id)
    return await fetch_one_all(select_query=stmt, session=session)


async def get_user_orders(
    session: AsyncSession,
    jwt_data: JWTData,
) -> Order | None:
    stmt = (
        select(Order)
        .where(Order.user_id == jwt_data.user_id)
        .order_by(Order.id)
    )
    orders: Result = await fetch_one_all(
        select_query=stmt, session=session, all=True
    )
    return list(orders)


async def get_user_order(
    jwt_data: JWTData, session: AsyncSession, order_id: int
) -> Order | None:
    stmt = (
        select(Order)
        .where(Order.user_id == jwt_data.user_id)
        .filter(Order.id == order_id)
    )
    return await fetch_one_all(select_query=stmt, session=session)


async def update_order(
    session: AsyncSession,
    order_update: OrderUpdate | OrderUpdatePartial,
    order: Order,
    partial: bool = False,
) -> Order:
    stmt = (
        update(Order)
        .where(Order.id == order.id)
        .values(**order_update.model_dump(exclude_none=partial))
    )
    await execute(select_query=stmt, session=session)
    for name, value in order_update.model_dump(exclude_none=partial).items():
        setattr(order, name, value)

    return order


async def update_order_status(
    session: AsyncSession,
    order_update: OrderUpdate | OrderUpdatePartial,
    order: Order,
    partial: bool = False,
) -> Order:
    stmt = (
        update(Order)
        .where(Order.id == order.id)
        .values(order_status=order_update.order_status)
    )
    for name, value in order_update.model_dump(exclude_none=partial).items():
        setattr(order, name, value)
    await execute(select_query=stmt, session=session)

    return order


async def delete_order(
    session: AsyncSession,
    order: Order,
) -> None:
    await session.delete(order)
    await session.commit()
