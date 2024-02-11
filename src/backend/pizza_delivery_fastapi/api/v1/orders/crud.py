from pizza_delivery_fastapi.auth import crud
from pizza_delivery_fastapi.auth.schemas import JWTData
from pizza_delivery_fastapi.core.models.order_product_association import OrderProductAssociation
from pizza_delivery_fastapi.core.models.product import Product
from pizza_delivery_fastapi.core.service import (
    execute_add,
    fetch_one_all,
    execute,
)
from sqlalchemy.orm import selectinload
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
    # Calzone, Margherita, Marinara
    current_user: Result[User] = await crud.get_user_by_id(
        user_id=jwt_data.user_id,
        session=session,
    )
    stmt_product = select(Product).where(
        Product.name == order_in.pizza_name
    )

    pizza: Result[Product] = await fetch_one_all(
        select_query=stmt_product,
        session=session,
    )
    order = Order(**order_in.model_dump())
    order.products_details.append(
        OrderProductAssociation(
            product=pizza,
            unit_price=pizza.price,
            count=11,
        )
    )
    order.user = current_user
    new_order: Result[Order] = await execute_add(
        model=order, session=session
    )
    return new_order


async def get_orders_with_products_assoc(session: AsyncSession) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAssociation.product
            ),
        )
        .order_by(Order.id)
    )
    orders: Result = await fetch_one_all(
        select_query=stmt, session=session, all=True
    )
    return list(orders)


# async def demo_get_orders_with_products_with_assoc(session: AsyncSession):
#     orders = await get_orders_with_products_assoc(session)

#     for order in orders:
#         print(order.id, order.promocode, order.created_at, "products:")
#         for (
#             order_product_details
#         ) in order.products_details:  # type: OrderProductAssociation
#             print(
#                 "-",
#                 order_product_details.product.id,
#                 order_product_details.product.name,
#                 order_product_details.product.price,
#                 "qty:",
#                 order_product_details.count,
#             )


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
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAssociation.product
            ),
        )
    )
    return await fetch_one_all(select_query=stmt, session=session)


async def update_order(
    session: AsyncSession,
    order_update: OrderUpdate | OrderUpdatePartial,
    order: Order,
    partial: bool = False,
) -> Order:
    stmt_product = select(Product).where(
        Product.name == order_update.pizza_name
    )
    pizza: Result[Product] = await fetch_one_all(
        select_query=stmt_product, session=session
    )
    await session.execute(
        update(OrderProductAssociation)
        .where(OrderProductAssociation.order_id == order.id)
        .values(product_id=pizza.id)
    )
    stmt_update = (
        update(Order)
        .where(Order.user_id == order.user_id)
        .filter(Order.id == order.id)
        .values(**order_update.model_dump())
    )
    await execute(select_query=stmt_update, session=session)
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
